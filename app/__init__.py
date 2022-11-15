# TNPG: Steve, Roster: Samson, Joseph, Ryan

from flask import Flask, render_template, request, session, redirect, url_for
from db import *

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

def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list

reset_database()
generate_preset_db()

#Start of Flask stuff

@app.route('/')
def index():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() 
    print_stories(c)
    storieslist = get_all_stories(c)
    storieslist = storieslist[::-1]
    if(len(storieslist) == 0):
        storieslist = [('No user', 'No title', 'No story', None, 'No date')]
    login_status = False
    if 'username' in session:
        login_status = True
        db.close()
        return render_template("index.html", loginstatus=login_status, username = session['username'], flask_list_stories=storieslist)
    db.close()
    return render_template("index.html", loginstatus=login_status, flask_list_stories=storieslist) #'You are not logged in'

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
        if not request.form['signup_password'] == request.form['signup_password_check']:
            return render_template("signup.html", failmsg='Passwords dont match!')
        db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
        c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
        signup_username = request.form['signup_username']
        signup_password = request.form['signup_password']
        signup_password_check = request.form['signup_password_check']
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
    if not login_status:
        return render_template("profile.html", loginstatus=login_status)
    try:
        currentuser=request.args['id']
        db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
        c = db.cursor()
        stories = get_user_total_stories(currentuser, c)
        userstorieslist = get_user_stories(currentuser, c)[::-1]
        db.close()
        return render_template("profile.html", loginstatus=login_status, username=currentuser, number_stories=stories, flask_list_stories=userstorieslist)
    except:
        db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
        c = db.cursor()
        stories = get_user_total_stories(session['username'], c)
        userstorieslist = get_user_stories(session['username'], c)[::-1]
        db.close()
        return render_template("profile.html", loginstatus=login_status, username=session['username'], number_stories=stories, flask_list_stories=userstorieslist)

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
            return render_template("editstory.html", loginstatus=login_status, flask_list_stories=userstorieslist, current_story_stuff=currentstorycontent, selected_story=currentstory[1], story_is_selected=True)
        return render_template("editstory.html", loginstatus=login_status)
    except:
        if 'username' in session:
            fail_msg = ''
            login_status = True
            db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
            c = db.cursor()
            userstorieslist = get_user_stories(session['username'], c)
            if len(userstorieslist) == 0:
                fail_msg = 'No stories'
            if request.method == 'POST':
                db.close()
                return redirect(url_for('editstory'))
            db.close()
            return render_template("editstory.html", loginstatus=login_status, flask_list_stories=userstorieslist, selected_story='No story selected', story_is_selected=False, failmsg = fail_msg)
        return render_template("editstory.html", loginstatus=login_status) #'You are not logged in'

@app.route('/stories')
def stories():
    #print(request.args['id'])
    login_status = False
    isvalidstory = not request.args['id'] == 'None'
    if 'username' in session:
        login_status = True
    if request.args['id'] == 'None':
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

@app.route('/search')
def search():
    login_status = False
    if 'username' in session:
        login_status = True
    try:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        searchcontent = request.args['search']
        storieslist = Union(get_stories_by_title(searchcontent, c), get_stories_by_user(searchcontent, c))
        userslist = get_users_by_name(searchcontent, c)
        db.close()
        return render_template("search.html", loginstatus=login_status, flask_stories_results=storieslist, flask_users_results=userslist)
    except:
        return render_template("search.html", loginstatus=login_status)


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run(host='0.0.0.0',port=5000)