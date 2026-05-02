from django.contrib.auth import get_user_model, login
from django.utils.deprecation import MiddlewareMixin

class AutoLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            User = get_user_model()
            try:
                user = User.objects.get(username='omjadhav007')
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            except User.DoesNotExist:
                pass
