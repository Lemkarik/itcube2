from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Develop

app = Flask(__name__)
app.config.from_object(Develop)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

from data.users import User
from data.adverts import Adverts
from forms.user import RegisterForm, LoginForm
from data.__all_models import *


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
    db_sess = db.session
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    # db_sess = db_session.create_session()
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db.session
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            position=form.position.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)
