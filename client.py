# Run with "python client.py"

# If it's static html it's better to use Nginx,
# instead of this app

from bottle import Bottle, static_file

from utils.settings import load_module_as_dict


settings = load_module_as_dict('settings')

app = Bottle()
app.config.update(settings)


@app.route('/', method=('GET', ), name='root')
def root():
    return static_file('index.html', root='templates')


# Only development
if app.config.get('DEBUG'):
    import bottle
    bottle.debug(mode=app.config.get('DEBUG'))

    @app.route('/static/<filename:path>',
               method=('GET', ),
               name='static')
    def serve_static_files(filename):
        return static_file(filename, root='staticfiles')

    app.run(host=app.config.get('HOST'),
            port=5000,
            reloader=app.config.get('DEBUG'))
