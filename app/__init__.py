from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from data import db_session
from data.users import User

from configs import Develop

app = Flask(__name__)
app.config.from_object(Develop)

login_manager = LoginManager(app)
login_manager.init_app(app)

db = SQLAlchemy(app)


def get_session():
    return db.session


migrate = Migrate()
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    # db_sess = db_session.create_session()
    return render_template("index.html")