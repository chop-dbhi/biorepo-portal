from django.conf import settings
from accounts.views import eula
from django.utils.deprecation import MiddlewareMixin


class CheckEulaMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and not request.user.profile.eula:
            # ignore static and media files since, the EULA page has to render
            # properly
            if (
                request.path.startswith(settings.STATIC_URL) or
                request.path.startswith(settings.MEDIA_URL)
            ):
                return

            return eula(request, readonly=False, redirect_to=request.path)
