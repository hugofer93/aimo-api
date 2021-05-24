from json import dumps as json_dumps

from bottle import HTTPError

from settings import DEBUG
from utils.response import JSONResponse


class JSONResponseError(JSONResponse):
    default_status = 500

    def __init__(self, status=None, body='', exception=None, traceback=None,
                 **options):
        status = status or self.default_status
        self.exception = exception
        self.traceback = traceback
        options['Content-Type'] = 'application/json'
        super().__init__(body, status, **options)


class JSONResponseNotAllowed(JSONResponseError):
    default_status = 405


class JSONResponseNotFound(JSONResponseError):
    default_status = 404


class JSONResponseNotAuthenticated(JSONResponseError):
    default_status = 401


class JSONResponseBadRequest(JSONResponseError):
    default_status = 400


class JSONResponseJWTError(JSONResponseNotAuthenticated):
    default_status = 401

    def __init__(self, exception=None, traceback=None, **options):
        status = 401
        message = "Authentication credentials were not provided."
        data = {'detail': message}
        data = json_dumps(data)
        super().__init__(status=status, body=data, exception=exception,
                         traceback=traceback, **options)


def handle_http_errors(error: HTTPError) -> JSONResponse:
    """Handle http errors for Bottle App.

    Args:
        error (HTTPError): Exception.

    Returns:
        JSONResponse: HTTP Response
    """
    data = {'detail': error.body or error.status}
    if DEBUG:
        if error.exception:
            data['exception'] = error.exception
        if error.traceback:
            data['traceback'] = error.traceback
    data = json_dumps(data)
    status_code = error.status_code
    return JSONResponse(body=data, status=status_code)
