# TNPG: Steve, Roster: Samson, Joseph, Ryan


from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = b'_MinecraftSTEVE'

validuser = 'admin'
validpass = 'admin'

@app.route('/')
def index():
    login_status = False
    if 'username' in session:
        login_status = True
        return render_template("index.html", loginstatus=login_status)
    return render_template("index.html", loginstatus=login_status) #'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['username'] == validuser and request.form['password'] == validpass:
        session['username'] = request.form['username']
        print("\nCookie stuff: " + str(session)+ "\n")
        return redirect(url_for('index'))
    if request.method == 'POST' and not request.form['username'] == validuser and not request.form['password'] == validpass:
        return render_template('login.html', failmsg='Wrong username and password!')
    return render_template("login.html", failmsg='')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and check_username(request.form['signup_username']) == 1 and check_password(request.form['signup_password']) == 1:
        return redirect(url_for('login'))
    if request.method == 'POST' and check_username(request.form['signup_username']) == 0 and check_password(request.form['signup_password']) == 1:
        return render_template("signup.html", failmsg='Username is too short!')
    if request.method == 'POST' and check_username(request.form['signup_username']) == 1 and check_password(request.form['signup_password']) == 0:
        return render_template("signup.html", failmsg='Password is too short!')
    if request.method == 'POST' and check_username(request.form['signup_username']) == 0 and check_password(request.form['signup_password']) == 0:
        return render_template("signup.html", failmsg='Please enter a valid username and password!')
    return render_template("signup.html", failmsg='')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    print("\nPopped the cookie\n")
    login_status = False
    return redirect(url_for('index'))

@app.route('/aboutus')
def aboutus():
    login_status = False
    if 'username' in session:
        login_status = True
        return render_template("about.html", loginstatus=login_status)
    return render_template("about.html", loginstatus=login_status) #'You are not logged in'

@app.route('/donate')
def donate():
    login_status = False
    if 'username' in session:
        login_status = True
        return render_template("donate.html", loginstatus=login_status)
    return render_template("donate.html", loginstatus=login_status) #'You are not logged in'

@app.route('/profile')
def profile():
    login_status = False
    if 'username' in session:
        login_status = True
        return render_template("profile.html", loginstatus=login_status)
    return render_template("profile.html", loginstatus=login_status) #'You are not logged in'

def check_password(password):
    if len(password) < 8:
        return 0
    return 1

def check_username(username):
    if len(username) < 4:
        return 0
    return 1

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
