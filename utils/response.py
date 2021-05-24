from bottle import HTTPResponse


class JSONResponse(HTTPResponse):
    default_status = 200

    def __init__(self, body='', status=None, headers=None, **more_headers):
        more_headers['Content-Type'] = 'application/json'
        super().__init__(body, status, headers, **more_headers)


class JSONResponseCreated(JSONResponse):
    default_status = 201
