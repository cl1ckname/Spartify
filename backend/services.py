import traceback
from logging import getLogger
from django import http
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from .SpotifyAPI.api_errors import AuthenticationError, RegularError

api_logger = getLogger(__name__)

def _get_error_response(self, request: http.HttpRequest, e: Exception) -> http.response.HttpResponseBase:
    if isinstance(e, AuthenticationError):
        api_logger.error(e, extra={'username': request.user.username, 'endpoint': e.endpoint, 'status_code': e.status})
        return redirect('authentication_error')
    elif isinstance(e, RegularError):
        api_logger.error(e, extra={'username': request.user.username, 'endpoint': e.endpoint, 'status_code': e.status})
        return redirect('server_error')
    else:
        return http.response.JsonResponse(
            {'errorMessage': str(traceback.format_exc())}, status = 400
        )

class SafeView(TemplateView):
    ''' Process exceptions '''
    def dispatch(self, request: http.HttpRequest, *args, **kwargs) -> http.response.HttpResponseBase:
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            response = _get_error_response(request, e)
        return response
    