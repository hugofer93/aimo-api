from bottle import Bottle

from api.endpoints import NoteResource, UserResource
from auth.endpoints import JWTAuthenticationResource
from utils.exceptions import handle_http_errors


app = Bottle()

# NOTES
app.route('/notes', 'GET', NoteResource.get_notes_resource)
app.route('/notes', 'POST', NoteResource.create_notes_resource)

# USERS
app.route('/users', 'POST', UserResource.create_users_resource)

# AUTH
app.route('/auth/token', 'POST', JWTAuthenticationResource.jwt_auth_resource)


# Add handle errors

app.error_handler = {
    400: handle_http_errors,
    401: handle_http_errors,
    404: handle_http_errors,
    405: handle_http_errors,
    500: handle_http_errors,
}
