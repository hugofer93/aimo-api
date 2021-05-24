from json import dumps as json_dumps
from typing import Optional

from bottle import request
from marshmallow import ValidationError
from peewee import IntegrityError

from api.models import Note, User
from api.serializers import NoteSerializer, UserSerializer
from auth.serializers import JWTLoginSerializer
from utils.jwt_auth import jwt_auth_required
from utils.exceptions import JSONResponseBadRequest
from utils.request import get_user_from_request
from utils.response import JSONResponse, JSONResponseCreated


# NOTES RESOURCE

class NoteResource:
    SerializerClass = NoteSerializer

    @classmethod
    @jwt_auth_required
    def get_notes_resource(cls) -> JSONResponse:
        """Get note list for endpoint.

        Returns:
            JSONResponse: Note list.
        """
        serializer = cls.SerializerClass()
        user = get_user_from_request()
        note_list = cls.list_notes(cls, user)
        data = serializer.dumps(note_list, many=True)
        return JSONResponse(body=data)

    def list_notes(self, user: Optional[User] = None) -> list:
        """Get note list from database.

        Args:
            user (User, None): User instance. Defaults to None.

        Returns:
            list: Note list.
        """
        if user:
            note_query = Note.get_user_notes(user)
        else:
            note_query = Note.select_available()
        note_list = list()
        if len(note_query):
            note_list = list(note_query)
        return note_list

    @classmethod
    @jwt_auth_required
    def create_notes_resource(cls) -> JSONResponse:
        """Create a note for the endpoint.

        Returns:
            JSONResponse: New user note.
        """
        serializer = cls.SerializerClass()
        try:
            result = serializer.load(request.json)
            user = get_user_from_request()
            result['user'] = user
            note = Note.create(**result)
            data = serializer.dumps(note)
        except ValidationError as error:
            data = json_dumps(error.messages)
            return JSONResponseBadRequest(body=data)
        return JSONResponse(body=data)


# USERS RESOURCE

class UserResource:
    SerializerClass = UserSerializer

    @classmethod
    def create_users_resource(cls) -> JSONResponse:
        """Create a user for the endpoint.

        Returns:
            JSONResponse: Access Token.
        """
        serializer = cls.SerializerClass()
        jwt_login_serializer = JWTLoginSerializer()
        try:
            result = serializer.load(request.json)
            user = User.create(**result)

            # inject the user into the context,
            # to avoid another query to the DB
            jwt_login_serializer.context['user'] = user

            data = jwt_login_serializer.load(result)
        except ValidationError as error:
            data = json_dumps(error.messages)
            return JSONResponseBadRequest(body=data)
        except IntegrityError as error:
            data = {'detail': ['User already exists.', ]}
            data = json_dumps(data)
            return JSONResponseBadRequest(body=data)
        return JSONResponseCreated(body=data)
