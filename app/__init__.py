from flask import Flask, render_template, redirect, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from config import Develop

app = Flask(__name__)
app.config.from_object(Develop)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

from data.users import User
from data.adverts import Adverts
from data.basket import Basket
from forms.user import RegisterForm, LoginForm
from forms.advert import EditAdvertForm
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
@app.route("/<string:search>")
def index(search=''):
    adverts = db.session.query(Adverts).filter((Adverts.title.like(f'%{search}%'))
                                               | (Adverts.description.like(f'%{search}%')))
    return render_template("index.html", adverts=adverts)


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
            role={'Продавец': True, 'Покупатель': False}[form.role.data]
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_advert', methods=['GET', 'POST'])
@app.route('/edit_advert/<int:id>', methods=['GET', 'POST'])
@login_required
def add_advert(id=0):
    form = EditAdvertForm()
    if not id:
        if form.validate_on_submit():
            db_sess = db.session
            advert = Adverts(
                title=form.title.data,
                description=form.description.data,
                position=current_user.position,
                seller=current_user.id,
                price=form.price.data
            )
            db_sess.add(advert)
            db_sess.commit()
            return redirect("/")
        return render_template('edit_advert.html', title='Создание объявления', form=form)
    else:
        if form.validate_on_submit():
            db_sess = db.session
            advert = db_sess.query(Adverts).filter(Adverts.user == current_user).first()
            if advert:
                advert.title = form.title.data
                advert.description = form.description.data
                db_sess.commit()
                return redirect('/')
        return render_template('edit_advert.html', title='Редактирование объявления', form=form)


@app.route('/delete_advert/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_advert(id):
    db_sess = db.session
    news = db_sess.query(Adverts).filter(Adverts.id == id,
                                         Adverts.user == current_user
                                         ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/basket', methods=['GET', 'POST'])
@login_required
def basket():
    db_sess = db.session
    adverts = db_sess.query(Basket).filter(Basket.user == current_user).first()
    if adverts:
        adverts = adverts.adverts_ids
        print(adverts)
    print(adverts)
    return render_template('basket.html')


@app.route('/add_to_basket/<int:id>', methods=['GET', 'POST'])
@login_required
def basket(id):
    db_sess = db.session
    for i in current_user.basket:
        print(i)