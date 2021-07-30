from django.shortcuts import redirect
from backend.SpotifyAPI.api_errors import AuthenticationError, RegularError, SpotifyError
# from backend.logger import api_logger
from logging import getLogger

api_logger = getLogger(__name__)


class ApiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        return response
    def process_exception(self, request, exception: SpotifyError):
        if isinstance(exception, AuthenticationError):
            api_logger.error(exception, extra={'username': request.user.username, 'endpoint': exception.endpoint, 'status_code': exception.status})
            return redirect('authentication_error')
        elif isinstance(exception, RegularError):
            print('------------')
            print(api_logger.handlers, api_logger.level, api_logger.name)
            api_logger.error(exception, extra={'username': request.user.username, 'endpoint': exception.endpoint, 'status_code': exception.status})
            return redirect('server_error')
        else:
            print(' no spotify exceptions')
            return self.get_response(request)