# TNPG: Steve, Roster: Samson, Joseph, Ryan

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from datetime import datetime

DB_FILE="mcstory.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#c.execute("DROP TABLE IF EXISTS users;")
#c.execute("DROP TABLE IF EXISTS stories;")

#users table stores the username and password
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT);")

#stories table stores the story title, content, id, and time
c.execute("CREATE TABLE IF NOT EXISTS stories(username TEXT, title TEXT, content TEXT, ID INTEGER, time TEXT);")

db.commit()
db.close()

app = Flask(__name__)
app.secret_key = b'_MinecraftSTEVE'

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
    data = (username, password)
    db_cursor.execute("INSERT INTO users VALUES(?,?)", data)

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
        now = datetime.now()
        dt_string = now.strftime("%B %d, %Y %H:%M:%S")
        data = (username, title, content, ID, dt_string)
        db_cursor.execute("INSERT INTO stories VALUES(?, ?, ?, ?, ?)", data)
    else:
        print(username + " USER DOES NOT EXIST")
        
def story_exist(title, db_cursor):
    db_cursor.execute("SELECT * FROM stories WHERE title=?", (title,))
    
    rows = db_cursor.fetchall()#returns a list with the story

    
    if rows == []:#if empty list then no story
        return False
    return True

def recent_story(db_cursor):
    db_cursor.execute("SELECT * FROM stories")
    
    rows = db_cursor.fetchall()
    
    if rows == []:#if empty list then no story
        print("There are no stories in the database")
        return None

    for row in rows:
        story = row
    return story

def print_users(db_cursor):
    print("Username, Password")
    db_cursor.execute("SELECT * FROM users")
    
    rows = db_cursor.fetchall()
    
    for row in rows:
        print(row)
    
def print_stories(db_cursor):
    print("Username, Title, Content, ID")
    db_cursor.execute("SELECT * FROM stories")
    
    rows = db_cursor.fetchall()
    
    for row in rows:
        print(row)

def get_total_number_stories(db_cursor):
    counter = 0
    db_cursor.execute("SELECT * FROM stories")
    
    rows = db_cursor.fetchall()
        
    if rows == []:#if empty list then no story
        print("There are no stories in the database")
        return 0

    for row in rows:
        counter+=1
    
    return counter

def get_user_stories(username, db_cursor):
    db_cursor.execute("SELECT * FROM stories WHERE username=?", (username,))
    
    rows = db_cursor.fetchall()#returns a list with the story

    return rows

def get_user_total_stories(username, db_cursor):
    db_cursor.execute("SELECT * FROM stories WHERE username=?", (username,))
    counter = 0
    
    rows = db_cursor.fetchall()#returns a list with the story

    if rows == []:#if empty list then no story
        print("There are no stories for "+ username)
        return 0
    
    for row in rows:
        counter+=1
    
    return counter

def get_story_by_id(id, db_cursor):
    db_cursor.execute("SELECT * FROM stories WHERE ID=?", (str(id),))
    
    rows = db_cursor.fetchall()#returns a list with the story

    return rows[0]

def edit_story(title, content, db_cursor):#goes to the story with the title and replaces its content with the input content
    db_cursor.execute("SELECT * FROM stories WHERE title=?", (title,))
    
    rows = db_cursor.fetchall()
    
    if rows == []:#if empty list then no story
        print("There is no story with this title name")
    else:
        for row in rows:
            username = row[0]
            ID = row[3]
        
        db_cursor.execute("DELETE FROM stories WHERE title=?", (title,))
    
        add_story(username, title, content, ID, db_cursor)# the edited story will have the date of the most recent edit

#Start of Flask stuff

@app.route('/')
def index():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() 
    print_stories(c)
    recentstoryuser = 'No user'
    recentstorytitle = 'No title'
    recentstorycontent = 'No stories'
    recentstorydate = 'No date'
    current_story_id = None
    if not recent_story(c) == None: 
        recentstoryuser = recent_story(c)[0]
        recentstorytitle = recent_story(c)[1]
        recentstorycontent = recent_story(c)[2]
        recentstorydate = recent_story(c)[4]
        current_story_id = recent_story(c)[3]
    login_status = False
    if 'username' in session:
        login_status = True
        db.close()
        return render_template("index.html", loginstatus=login_status, username = session['username'], current_story_link="/stories?id=" + str(current_story_id), recent_story_title=recentstorytitle, recent_story_content=recentstorycontent, recent_story_date=recentstorydate, recent_story_user=recentstoryuser)
    db.close()
    return render_template("index.html", loginstatus=login_status, current_story_link="/stories?id=" + str(current_story_id), recent_story_title=recentstorytitle, recent_story_content=recentstorycontent, recent_story_date=recentstorydate, recent_story_user=recentstoryuser) #'You are not logged in'

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
        return render_template("signup.html", failmsg='Username already exists. Please login.')
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
        return render_template("about.html", username = session['username'], loginstatus=login_status)
    return render_template("about.html",  loginstatus=login_status) #'You are not logged in'

@app.route('/donate')
def donate():
    login_status = False
    if 'username' in session:
        login_status = True
        return render_template("donate.html", username = session['username'], loginstatus=login_status)
    return render_template("donate.html", loginstatus=login_status) #'You are not logged in'

@app.route('/profile')
def profile():
    login_status = False
    if 'username' in session:
        login_status = True
        db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
        c = db.cursor()
        stories = get_user_total_stories(session['username'], c)
        userstorieslist = get_user_stories(session['username'], c)
        db.close()
        return render_template("profile.html", loginstatus=login_status, username=session['username'], number_stories=stories, flask_list_stories=userstorieslist)
    return render_template("profile.html", loginstatus=login_status) #'You are not logged in'

@app.route('/newstory', methods=['GET', 'POST'])
def newstory():
    login_status = False
    if 'username' in session:
        login_status = True
        if request.method == 'POST':
            db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
            c = db.cursor() 
            title = request.form['title']
            content = request.form['newstory']
            username = session['username']
            if not story_exist(title, c):
                add_story(username, title, content, get_total_number_stories(c)+1, c)
                print_stories(c)
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
    try:
        if 'username' in session:
            login_status = True
            db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
            c = db.cursor()
            userstorieslist = get_user_stories(session['username'], c)
            currentid = request.args['id']
            currentstory = get_story_by_id(currentid, c)
            if(currentstory[0] == session['username']):
                print("matching id and user")
                currentstorycontent = currentstory[2]
            else:
                print("not matching user and id")
                db.close()
                return redirect(url_for(edit_story))
            if request.method == 'POST':
                print("editing story")
                newcontent = request.form['addition']
                currenttitle = currentstory[1]
                edit_story(currenttitle, newcontent, c)
                db.commit()
                print(currentstory[2]) 
                db.close()
                return redirect(url_for('index'))
            return render_template("editstory.html", loginstatus=login_status, flask_list_stories=userstorieslist, current_story_stuff=currentstorycontent, selected_story=currentstory[1])
        return render_template("editstory.html", loginstatus=login_status)
    except:
        if 'username' in session:
            login_status = True
            db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
            c = db.cursor()
            userstorieslist = get_user_stories(session['username'], c)
            if request.method == 'POST':
                db.close()
                return redirect(url_for('editstory'))
            db.close()
            return render_template("editstory.html", loginstatus=login_status, flask_list_stories=userstorieslist, selected_story='No story selected')
        return render_template("editstory.html", loginstatus=login_status) #'You are not logged in'

@app.route('/stories')
def stories():
    #print(request.args['id'])
    login_status = False
    isvalidstory = not request.args['id'] == None
    if 'username' in session:
        login_status = True
    if request.args['id'] == None:
        return render_template("stories.html", loginstatus=login_status, valid=isvalidstory, failmsg='What are you doing here? Go back.')
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() 
    currentstory = get_story_by_id(request.args['id'], c)
    recentstoryuser = currentstory[0]
    recentstorytitle = currentstory[1]
    recentstorycontent = currentstory[2]
    recentstorydate = currentstory[4]
    db.close()
    return render_template("stories.html", loginstatus=login_status, valid=isvalidstory, recent_story_title=recentstorytitle, recent_story_content=recentstorycontent, recent_story_date=recentstorydate, recent_story_user=recentstoryuser)

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run(host='0.0.0.0',port=5000)