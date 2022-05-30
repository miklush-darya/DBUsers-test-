from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash,  check_password_hash
from flask import Flask, redirect, request, render_template, url_for, make_response, session, abort
from flask_login import LoginManager, login_user, login_required, current_user
from model_db import Users, Profiles
from userlogin import UserLogin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test13.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine('sqlite:///test13.db')

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)

# db.create_all()

menu_m2 = [{'name':'Главная', 'url': '/'},
            {'name':'Вход', 'url': 'login'},
            {'name':'Регистрация', 'url': 'registr'},
            {'name':'База', 'url': 'db'},
            {'name':'Выход', 'url': 'logout'}]

@app.route("/")
def index():
    return render_template('base.html', title='Главная', menu=menu_m2)

@app.route("/registr", methods=['POST', 'GET'])
def registr():

    if request.method == 'POST':
        if len(request.form['name'])>2 and len(request.form['email']) >4 and len(request.form['password'])>4 and request.form['password2']==request.form['password']:

            hash = generate_password_hash(request.form['password'])
            Usr = Users(email=request.form['email'], password = hash)
            db.session.add(Usr)
            db.session.flush()

            prof = Profiles(name=request.form['name'], old=request.form['old'], 
                        city = request.form['city'], user_id = Usr.id)
            db.session.add(prof)
            db.session.commit()
        
    return render_template('registr.html', title='Регистрация', menu=menu_m2)



@app.route("/login", methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if not user:
            return redirect(url_for('login'))

        if not check_password_hash(user['password'], request.form['password']):
            return redirect(url_for('login'))

    return render_template('login.html', title = "Авторизация", menu=menu_m2)


#     log = ""
#     if request.cookies.get('logged'):
#         log = request.cookies.get('logged')
#     res = make_response(f'<h1>форма авторизации</h1><p>logged: {log}')
#     res.set_cookie('logged', 'yes', 30*24*3600)
#     return res


@app.route('/db')
def for_db():
    info = []
    info = Users.query.all()
    return render_template('for_db.html', title = 'База пользователей', list = info, menu=menu_m2)


@app.route("/logout")
def logout():
    res = make_response(f'<h1>вы вышли</h1>')
    res.set_cookie('logged', "", 0)
    return res


@app.route("/profile/<username>")
@login_required
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'User: {username}'


# if __name__== "__main__":
#     app.run(debug=True)