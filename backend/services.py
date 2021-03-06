import traceback
import functools
from logging import getLogger
from django import http
from django.views.generic.base import TemplateView
from django.shortcuts import redirect, render
from .SpotifyAPI.api_errors import AuthenticationError, RegularError
from django.conf import settings

api_logger = getLogger(__name__)

def _get_error_response(request: http.HttpRequest, e: Exception) -> http.response.HttpResponseBase:
    if isinstance(e, AuthenticationError):
        api_logger.error(e, extra={'username': request.user.username, 'endpoint': e.endpoint, 'status_code': e.status})
        return redirect('authentication_error')
    else:
        api_logger.error(e, extra={'username': request.user.username, 'endpoint': e.endpoint, 'status_code': e.status})
        return render(request,'backend/500.html',status=500)

class SafeView(TemplateView):
    ''' Process exceptions '''
    def dispatch(self, request: http.HttpRequest, *args, **kwargs) -> http.response.HttpResponseBase:
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            response = _get_error_response(request, e)
        return response
    
def safe_view(view):
    ''' '''
    @functools.wraps(view)
    def inner(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except Exception as e:
            return _get_error_response(request, e)
    return inner