import logging
import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests

logger = logging.getLogger(__name__)

def send_order_confirmation_email(order):
    """
    Sends an HTML order confirmation email to the farmer.
    Run this in a separate thread to avoid blocking the response.
    """
    try:
        subject = f"Order Confirmation – SmartAgri | Order #{order.id}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [order.farmer.email]

        context = {
            'order': order,
            'items': order.items.all(),
            'farmer': order.farmer
        }

        html_content = render_to_string('orders/email/order_confirm.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        logger.info(f"Order confirmation email sent to {order.farmer.email} for Order #{order.id}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send order email for Order #{order.id}: {str(e)}")
        return False

def send_order_confirmation_sms(order):
    """
    Sends a confirmation SMS using a standard gateway (Logic placeholder).
    Adjust API URL and Key based on specific provider (Fast2SMS/TextLocal).
    """
    try:
        # Check if user has phone number
        phone_number = getattr(order.farmer, 'phone_number', None)
        # Fallback to profile if using OneToOne
        if not phone_number and hasattr(order.farmer, 'profile'):
             phone_number = getattr(order.farmer.profile, 'phone', None)
        
        if not phone_number:
            logger.warning(f"No phone number found for user {order.farmer.username}, skipping SMS.")
            return False

        message = f"SmartAgri: Your order #{order.id} is confirmed. Total Rs {order.total_amount}. Status: {order.get_status_display()}."
        
        # Example Implementation for Fast2SMS (Common in India)
        # api_key = os.environ.get('SMS_API_KEY')
        # if not api_key: return (Safety check)
        
        # Payload for demonstration
        # payload = {
        #    "authorization": api_key,
        #    "message": message,
        #    "numbers": phone_number
        # }
        # response = requests.post("https://www.fast2sms.com/dev/bulkV2", data=payload)
        
        # Mocking success for development
        logger.info(f"SMS SENT to {phone_number}: {message}")
        return True

    except Exception as e:
        logger.error(f"Failed to send SMS for Order #{order.id}: {str(e)}")
        return False

class OrderNotificationThread(threading.Thread):
    """
    Thread to handle notifications asynchronously so the user doesn't wait.
    """
    def __init__(self, order):
        self.order = order
        threading.Thread.__init__(self)

    def run(self):
        send_order_confirmation_email(self.order)
        send_order_confirmation_sms(self.order)

def trigger_order_notifications(order):
    """
    Public interface to trigger all notifications.
    """
    OrderNotificationThread(order).start()
