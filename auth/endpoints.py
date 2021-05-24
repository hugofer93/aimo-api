from json import dumps as json_dumps

from bottle import request
from marshmallow import ValidationError

from auth.serializers import JWTLoginSerializer
from utils.exceptions import JSONResponseBadRequest
from utils.response import JSONResponse


class JWTAuthenticationResource:
    SerializerClass = JWTLoginSerializer

    @classmethod
    def jwt_auth_resource(cls) -> JSONResponse:
        """User Authentication with JSON Web Token.

        Returns:
            JSONResponse: Access JWToken.
        """
        serializer = cls.SerializerClass()
        try:
            result = serializer.load(request.json)
            data = json_dumps(result)
        except ValidationError as error:
            data = json_dumps(error.messages)
            return JSONResponseBadRequest(body=data)
        return JSONResponse(body=result)
