from flask import Flask, redirect, url_for
from flask_assets import Bundle, Environment

from flask_migrate import Migrate

# from flask import Manager
from blueprints import Base, db
from blueprints.auth import routes, login_manager
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('WTF_CSRF_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
app.register_blueprint(routes.auth, url_prefix='/auth')
from blueprints.expense import routes
app.register_blueprint(routes.expense, url_prefix='/expense')

with app.app_context():
    db.init_app(app=app)
    db.create_all()
    app.migrate = Migrate(app)


login_manager.init_app(app)


css = Bundle('main.css', output='main.css', filters='postcss')
assets = Environment(app)
assets.register('main_css', css)
css.build()

if __name__ == '__main__':
    app.run(port=8080, debug=True)
