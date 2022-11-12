# TNPG: Steve, Roster: Samson, Joseph, Ryan

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

DB_FILE="mcstory.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

c.execute("DROP TABLE IF EXISTS users;")
c.execute("DROP TABLE IF EXISTS stories;")

#users table stores the username and password
c.execute("CREATE TABLE users(username TEXT, password TEXT);")

#stories table stores the story title, content, and id
c.execute("CREATE TABLE stories(username TEXT, title TEXT, content TEXT, ID INTEGER);")

db.commit()
db.close()

app = Flask(__name__)
app.secret_key = b'_MinecraftSTEVE'

validuser = 'admin'
validpass = 'admin'

#Helper Functions:
def check_password(password):
    if len(password) < 8:
        return 0
    return 1

def check_username(username):
    if len(username) < 4:
        return 0
    return 1

#adds user to user database
def add_user(username, password, db_cursor):
    db_cursor.execute("INSERT INTO users VALUES(\"" + username + "\", \"" + password + "\");")

#checks if a user exists
def user_exist(username, db_cursor):
    db_cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    
    rows = db_cursor.fetchall()#returns a list with the username
    
    if rows == []:#if empty list then no username
        return False
    return True

#returns the password of specfied username
def get_user_pass(username, db_cursor):
    if user_exist(username, db_cursor):
        db_cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            
        rows = db_cursor.fetchone()#rows is a tuple with the username in zero index and password in first
        
        return rows[1]
    else:
        print(username + " USER DOES NOT EXIST")

#adds story to stories database
def add_story(username, title, content, ID, db_cursor):
    if user_exist(username, db_cursor):
        db_cursor.execute("INSERT INTO stories VALUES(\"" + username + "\", \"" + title + "\", \"" + content + "\", " + ID + ");")
    else:
        print(username + " USER DOES NOT EXIST")
        
def story_exist(title, db_cursor):
    db_cursor.execute("SELECT * FROM stories WHERE title=?", (title,))
    
    rows = db_cursor.fetchall()#returns a list with the story

    
    if rows == []:#if empty list then no story
        return False
    return True

#Start of Flask stuff

@app.route('/')
def index():
    login_status = False
    if 'username' in session:
        login_status = True
        return render_template("index.html", loginstatus=login_status)
    return render_template("index.html", loginstatus=login_status) #'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
        c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
        username = request.form['username']
        password = request.form['password']
        if user_exist(username, c) and get_user_pass(username, c) == password:
            db.close()
            session['username'] = request.form['username']
            print("\nCookie stuff: " + str(session)+ "\n")
            return redirect(url_for('index'))
        else:
            db.close()
            return render_template('login.html', failmsg='Wrong username and password!')
    return render_template("login.html", failmsg='')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and check_username(request.form['signup_username']) == 1 and check_password(request.form['signup_password']) == 1:
        db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
        c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
        signup_username = request.form['signup_username']
        signup_password = request.form['signup_password']
        if not user_exist(signup_username, c):
            add_user(signup_username, signup_password, c)
            db.commit()
            print("Added "+ signup_username + " with password: " + signup_password)
            db.close()
            return redirect(url_for('login'))
        db.close()
        return render_template("signup.html", failmsg='Username already exists!')
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

@app.route('/newstory', methods=['GET', 'POST'])
def newstory():
    if 'username' in session:
        login_status = True
        if request.method == 'POST':
            db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
            c = db.cursor() 
            title = request.form['title']
            content = request.form['newstory']
            username = session['username']
            if not story_exist(title, c):
                add_story(username, title, content, 1, c)
                db.commit()
                db.close()
                return redirect(url_for('index'))
            db.close()
            return render_template("newstory.html", loginstatus=login_status, failmsg='Story title already exists!')
        return render_template("newstory.html", loginstatus=login_status)
    return render_template("newstory.html", loginstatus=login_status) #'You are not logged in'

@app.route('/editstory', methods=['GET', 'POST'])
def editstory():
    login_status = False
    if 'username' in session:
        login_status = True
        if request.method == 'POST':
            db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
            c = db.cursor() 
            db.commit()
            db.close()
            return redirect(url_for('index'))
        return render_template("editstory.html", loginstatus=login_status)
    return render_template("editstory.html", loginstatus=login_status) #'You are not logged in'

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()