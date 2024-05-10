from flask import Flask, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import sqlite3


app = Flask(__name__)
app.secret_key = 'secretik'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
conn.commit()


class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = c.fetchone()
    if user_data:
        user = User()
        user.id = user_data[0]
        user.username = user_data[1]
        return user
    return None


@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = c.fetchone()
        if user_data and check_password_hash(user_data[2], password):
            user = User()
            user.id = user_data[0]
            user.username = user_data[1]
            login_user(user, remember=True)
            return redirect(url_for('index'))
        else:
            error = 'Пользователь с таким логином / паролем не найден'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            user_data = c.fetchone()
            user = User()
            user.id = user_data[0]
            user.username = user_data[1]
            login_user(user, remember=True)
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            error = 'Пользователь с таким логином уже существует'
    return render_template('register.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)