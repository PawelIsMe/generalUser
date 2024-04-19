from flask import Flask, render_template, session, request, redirect, url_for, send_file
from account import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'k7ljr1eg5jr#eh8!gh'


@app.route('/')
def load_index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index():
    ipaddr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    username = request.form.get('user')
    # Creating an account when the user doesn't have another one
    if doesExist(username):
        return render_template('index.html', blad2="This nick is already taken. Please log in.")
    elif haveAnAccount(ipaddr):
        return render_template('index.html', blad2="You already have an account with this IP address.")
    else:
        print(f"{ipaddr} : {doesExist(username)}")
        session['user'] = request.form.get('user')
        session['password'] = request.form.get('password')
        session['ipaddr'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

        # Creating an account
        createAccount(request.form.get('fname'), request.form.get('lname'), session['user'], session['password'],
                      session['ipaddr'])
        return redirect(url_for('dashboard'))



@app.route('/login')
def load_login():
    ipaddr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # Auto login
    if checkIpAddr(ipaddr):
        session['user'] = checkIpAddr(ipaddr)[0]
        session['password'] = checkIpAddr(ipaddr)[1]
        return redirect(url_for('dashboard'))
    session.clear()
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    ipaddr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    session['user'] = request.form.get('user')
    session['password'] = request.form.get('password')

    # Checking user and password
    if checkLogin(session['user'], session['password']):
        if readData(session['user'], 'ipaddr') != ipaddr:
            changeData(session['user'], 'ipaddr', ipaddr)
        activateLogin(session['user'])
        return redirect(url_for('dashboard'))
    else:
        session.clear()
        return render_template("login.html", blad1="Username or password is invalid.")


@app.route('/signup')
def load_register():
    ipaddr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # Auto login
    if checkIpAddr(ipaddr):
        session['user'] = checkIpAddr(ipaddr)[0]
        session['password'] = checkIpAddr(ipaddr)[1]
        return redirect(url_for('dashboard'))
    session.clear()
    return render_template("register.html")


@app.route('/signup', methods=['POST'])
def register():
    ipaddr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    username = request.form.get('user')
    # Creating an account when the user doesn't have another one
    if doesExist(username):
        return render_template('register.html', blad2="This nick is already taken. Please log in.")
    elif haveAnAccount(ipaddr):
        return render_template('register.html', blad2="You already have an account with this IP address.")
    else:
        print(f"{ipaddr} : {doesExist(username)}")
        session['user'] = request.form.get('user')
        session['password'] = request.form.get('password')
        session['ipaddr'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

        # Creating an account
        createAccount(request.form.get('fname'), request.form.get('lname'), session['user'], session['password'],
                      session['ipaddr'])
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    ipaddr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    # The server will redirect the user when he is not logged in
    if session:
        if isLogged(session['user']):
            return render_template("dashboard.html")
    return redirect(url_for('login'))

@app.route('/logout')
def logout_from_acc():
    if session:
        user = session['user']
        logout(user)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)