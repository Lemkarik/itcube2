from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

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


@app.route("/")
def index():
    # db_sess = db_session.create_session()
    return render_template("index.html")