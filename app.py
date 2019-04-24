from flask import Flask , render_template ,request ,flash , redirect , url_for , session
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from wtforms import Form , StringField , TextAreaField, PasswordField , validators
from functools import wraps

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'portfolio'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)



@app.route('/')
def home():
    return render_template('home.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=2, max=30)])
    username = StringField('Username', [validators.length(min=2, max=50)])
    email = StringField('Password', [validators.length(min=4, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Password Do Not Match')
    ])

    confirm = PasswordField('Confirm Password')




@app.route('/register', methods=['POST', 'GET'])
def registration():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        mysql.connection.commit()
        cur.close()

        flash("You are now registered, Goto login page", 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candid = request.form['password']

        # Create Cursor
        cur = mysql.connection.cursor()
        
        # GET USER BY USERMAME
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_candid, password):
                #PASSED
                session['logged_in'] = True
                session['username'] = username

                flash("YOU ARE NOW LOGGED IN", 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Login'
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = 'Username Not Found'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("YOU ARE NOW LOGGED OUT", "danger")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/skills/web_development')
def web_development():
    return render_template('web_development.html')

@app.route('/skills/artificial_intelligence')
def artificial_intelligence():
    return render_template('ai.html')

@app.route('/skills/web_designing')
def web_designing():
    return render_template('web_designing.html')

@app.route('/skills/graphics_designing')
def GD():
    return render_template('graphics_designing.html')

if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True, port=9000)