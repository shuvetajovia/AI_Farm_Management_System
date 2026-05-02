from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from .models import Order, OrderItem
from inventory.models import Product
from django import forms

class OrderForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField(min_value=1)

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(farmer=self.request.user)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'

    def get_queryset(self):
        return Order.objects.filter(farmer=self.request.user)

class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('orders:list')

    def get(self, request, *args, **kwargs):
        form = OrderForm()
        products = Product.objects.all()
        return render(request, self.template_name, {'form': form, 'products': products})

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')

        if product_id and quantity:
            try:
                product = Product.objects.get(id=product_id)
                quantity = int(quantity)

                if quantity > product.stock_quantity:
                    messages.error(request, f'Insufficient stock. Only {product.stock_quantity} {product.unit} available.')
                    return redirect('orders:create')

                if quantity <= 0:
                    messages.error(request, 'Quantity must be greater than 0.')
                    return redirect('orders:create')

                with transaction.atomic():
                    order = Order.objects.create(farmer=request.user, total_amount=product.price * quantity)
                    OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)

                    # Update stock
                    product.stock_quantity -= quantity
                    product.save()

                # Trigger Notifications (Async)
                from .utils import trigger_order_notifications
                trigger_order_notifications(order)

                messages.success(request, f'Order placed successfully for {quantity} {product.unit} of {product.name}!')
                return redirect(self.success_url)

            except Product.DoesNotExist:
                messages.error(request, 'Product not found.')
            except ValueError:
                messages.error(request, 'Invalid quantity.')
        else:
            messages.error(request, 'Please select a product and quantity.')

        return redirect('orders:create')


def resend_order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk, farmer=request.user)
    from .utils import trigger_order_notifications
    trigger_order_notifications(order)
    messages.success(request, f'Confirmation notifications sent for Order #{order.id}')
    return redirect('orders:detail', pk=pk)
