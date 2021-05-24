# Run with "python server.py"

from bottle import Bottle

from api import app as api_app
from database import close_db
from utils.settings import load_module_as_dict

settings = load_module_as_dict('settings')

app = Bottle()
app.config.update(settings)


# Mount child app
app.mount('/api/v1/', api_app)


# DB Configuration
app.add_hook('after_request', close_db)


# Only development
if app.config.get('DEBUG'):
    import bottle
    bottle.debug(mode=app.config.get('DEBUG'))

    app.run(host=app.config.get('HOST'),
            port=8000,
            reloader=app.config.get('DEBUG'))
