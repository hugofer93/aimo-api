from marshmallow import EXCLUDE, Schema, post_load, ValidationError
from marshmallow.fields import Str

from api.models import User
from utils.jwt_auth import generate_jwtoken


class JWTLoginSerializer(Schema):
    username = Str(required=True)
    password = Str(required=True)

    @post_load
    def authenticate(self, data: dict, **kwargs) -> dict:
        """User Authentication.

        Args:
            data (dict): From request.

        Raises:
            ValidationError: If user doesn't exist or incorrect credentials.

        Returns:
            dict: Access Token.
        """
        username = data.get('username')
        password = data.get('password')

        # check first in context, else in DB
        user = self.context.get('user', None)
        if not user:
            user = User.get_user(username)

        # may be that the user doesn't exist in DB
        if not user or not user.check_password(password):
            message = "No active account found with the given credentials"
            raise ValidationError(message, field_name='detail')
        jwtoken = generate_jwtoken(user)
        data = {'access_token': jwtoken}
        return data

    class Meta:
        unknown = EXCLUDE
