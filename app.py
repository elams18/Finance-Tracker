from flask import Flask, redirect, url_for
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import db

# from flask import Manager
import os

app = Flask(__name__)
app.config["SESSION_TYPE"] = os.environ.get("SESSION_TYPE", "memcached")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["WTF_CSRF_SECRET_KEY"] = os.environ.get("WTF_CSRF_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
)


@app.cli.command("list-routes")
def list_routes():
    import urllib

    output = []
    for rule in app.url_map.iter_rules():
        methods = ",".join(rule.methods)
        # line = urllib.urllib("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(rule.endpoint)

    for line in sorted(output):
        print(line)


from blueprints.auth import login_manager, auth_bp

login_manager.init_app(app)
app.register_blueprint(auth_bp, url_prefix="/auth")
from blueprints.expense import expense

app.register_blueprint(expense, url_prefix="/expense")


with app.app_context():
    db.init_app(app)
    migrate = Migrate(app, db)


css = Bundle("main.css", output="main.css", filters="postcss")


assets = Environment(app)

assets.register("main_css", css)
css.build()

if __name__ == "__main__":
    app.run(port=8080, debug=True)
