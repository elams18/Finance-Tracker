from flask import Flask
from flask_assets import Bundle, Environment

from db_config import engine
from blueprints import Base
from blueprints.auth import routes, login_manager
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('WTF_CSRF_SECRET_KEY')

app.register_blueprint(routes.auth, url_prefix='/auth')
from blueprints.expense import routes
app.register_blueprint(routes.expense, url_prefix='/expense')



Base.metadata.create_all(engine)
login_manager.init_app(app)


@app.route('/')
def initialize():  # put application's code here
    return 'done'


css = Bundle('main.css', output='main.css', filters='postcss')
assets = Environment(app)
assets.register('main_css', css)
css.build()


if __name__ == '__main__':
    app.run(port=8080, debug=True)
