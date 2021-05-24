from datetime import datetime, timedelta
from re import compile as re_compile
from typing import Callable

from bottle import request
from jwt import (DecodeError, decode as jwt_decode, InvalidTokenError,
                 encode as jwt_encode)

from api.models import User
from settings import JSON_WEB_TOKEN as JWT_SETTINGS, SECRET_KEY
from utils.exceptions import JSONResponseBadRequest, JSONResponseJWTError
from utils.response import JSONResponse


def jwt_auth_required(
        func: Callable[[], JSONResponse],
        inject_user: bool = True) -> Callable[[], JSONResponse]:
    """Decorator to require JWT Authentication.

    Args:
        func (Callable[[], JSONResponse]): Resource function.
        inject_user (bool): Inject the authenticated user into the request.
                            Defaults to True

    Returns:
        Callable[[], JSONResponse]: Resource function wrapped.
    """
    def wrapper(*args, **kwargs):
        http_auth_header = get_http_auth_header()
        check_http_auth_header(http_auth_header)
        jwtoken = get_jwtoken_from_http_auth(http_auth_header)
        jwtoken_claims = decode_jwtoken(jwtoken)
        check_jwt_claims(jwtoken_claims, inject_user=inject_user)
        return func(*args, **kwargs)
    return wrapper


def get_http_auth_header() -> str:
    """Get HTTP AUTHORIZATION from HTTP headers.

    Raises:
        JSONResponseJWTError:
            If HTTP AUTHORIZATION header doesn't exist.

    Returns:
        str: Header HTTP AUTHORIZATION value.
    """
    AUTH_HEADER_NAME = JWT_SETTINGS.get('AUTH_HEADER_NAME')
    http_auth_header = request.get_header(AUTH_HEADER_NAME, None)
    if not http_auth_header:
        raise JSONResponseJWTError()
    return http_auth_header


def check_http_auth_header(http_auth_hearder: str) -> None:
    """Check the HTTP AUTHORIZATION header.

    Args:
        http_auth_hearder (str): Header HTTP AUTHORIZATION value.

    Raises:
        JSONResponseJWTError: If HTTP AUTHORIZATION header is malformed.
    """
    AUTH_HEADER_TYPES = JWT_SETTINGS.get('AUTH_HEADER_TYPES')
    regex_pattern = ('[a-zA-Z0-9]+.[a-zA-Z0-9]+.[a-zA-Z0-9]+'
                     + '.[a-zA-Z0-9]+.?[a-zA-Z0-9\-_=]+')
    header_pattern = rf'^{AUTH_HEADER_TYPES} {regex_pattern}$'
    header_regex = re_compile(header_pattern)
    if not header_regex.match(http_auth_hearder):
        raise JSONResponseJWTError


def get_jwtoken_from_http_auth(http_auth_hearder: str) -> str:
    """Get JWToken of the HTTP AUTHORIZATION header value.

    Args:
        http_auth_hearder (str): HTTP AUTHORIZATION header value.

    Returns:
        str: JSON Web Token value.
    """
    AUTH_HEADER_TYPES = JWT_SETTINGS.get('AUTH_HEADER_TYPES')
    jwtoken = http_auth_hearder[len(AUTH_HEADER_TYPES)+1:]
    return jwtoken


def decode_jwtoken(jwtoken: str) -> dict:
    """Verify the jwtoken signature and return the token claims.

    Args:
        jwtoken (str): JSON Web Token.

    Raises:
        JSONResponseJWTError: If jwtoken is badly formed.

    Returns:
        dict: JWToken claims (payload).
    """
    ALGORITHM = JWT_SETTINGS.get('ALGORITHM')
    try:
        payload = jwt_decode(jwtoken, SECRET_KEY, algorithms=[ALGORITHM, ])
    except (DecodeError, InvalidTokenError):
        raise JSONResponseJWTError
    return payload


def generate_jwtoken(user: User) -> str:
    """Encode the payload as JSON Web Token.

    Args:
        user (User): User instance.

    Returns:
        str: JSON Web Token value.
    """
    ALGORITHM = JWT_SETTINGS.get('ALGORITHM')
    payload = create_user_jwt_claim(user)
    encoded_jwtoken = jwt_encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwtoken


def create_user_jwt_claim(user: User) -> dict:
    """Create JWT claim based on user field defined in settings.

    Args:
        user (User): User instance.

    Raises:
        JSONResponseBadRequest: If user field doesn't exist.

    Returns:
        dict: JWT claim (payload).
    """
    USER_FIELD_CLAIM = JWT_SETTINGS.get('USER_FIELD_CLAIM')
    TOKEN_LIFETIME = JWT_SETTINGS.get('TOKEN_LIFETIME')
    user_field = getattr(user, USER_FIELD_CLAIM, None)
    if not user_field:
        raise JSONResponseBadRequest
    payload = {
        USER_FIELD_CLAIM: user_field,
        'exp': datetime.utcnow() + TOKEN_LIFETIME,
    }
    return payload


def check_jwt_claims(jwtoken_claims: dict, inject_user: bool = True) -> None:
    """Check JWToken claims: jwoken expiration date and time
    and if the user is available.

    Args:
        jwtoken_claims (dict): JWToken claims (payload).
        inject_user (bool): Inject the authenticated user into the request.

    Raises:
        JSONResponseJWTError: Expired JWToken
        JSONResponseJWTError: User not available.
    """
    payload = jwtoken_claims
    exp_unix_timestamp = int(payload.get('exp'))
    jwtoken_exp_datetime = datetime.utcfromtimestamp(exp_unix_timestamp)
    now_datetime = datetime.utcnow()
    if jwtoken_exp_datetime < now_datetime:
        raise JSONResponseJWTError()
    user = User.get_user(payload.get('username'))
    if not user.available:
        raise JSONResponseJWTError()

    # add user to request
    if inject_user:
        inject_user_on_request(user)


def inject_user_on_request(user: User) -> None:
    """Inject authenticated user into HTTP request.

    Args:
        user (User): Authenticated user.
    """
    request.user = user
