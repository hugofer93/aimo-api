from typing import Optional

from bottle import request

from api.models import User


def get_user_from_request() -> Optional[User]:
    """Get user from request, if this is.

    Returns:
        Optional[User]: User instance or None.
    """
    user = None
    if hasattr(request, 'user'):
        user = request.user
    return user
