from flask import Flask

from db_config import engine
from blueprints import Base
from blueprints.auth import routes, login_manager
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['WTF_CSRF_SECRET_KEY']= os.environ.get('WTF_CSRF_SECRET_KEY')

Base.metadata.create_all(engine)
login_manager.init_app(app)



@app.route('/')
def initialize():  # put application's code here
    return 'done'


app.register_blueprint(routes.auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run(port=8080, debug=True)