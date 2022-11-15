import sqlite3
from datetime import datetime
DB_FILE="mcstory.db"
def reset_database():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    c.execute("DROP TABLE IF EXISTS users;")
    c.execute("DROP TABLE IF EXISTS stories;")

    #users table stores the username and password
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT);")

    #stories table stores the story title, content, id, and time
    c.execute("CREATE TABLE IF NOT EXISTS stories(username TEXT, title TEXT, content TEXT, ID INTEGER, time TEXT);")
    db.commit()
    db.close()

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

def get_all_stories(db_cursor):
    db_cursor.execute("SELECT * FROM stories")
    
    rows = db_cursor.fetchall()

    return rows

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

def get_stories_by_title(title, db_cursor):
    db_cursor.execute("SELECT * FROM stories")
    list = []
    rows = db_cursor.fetchall()#returns a list with the story

    for row in rows:
        if title.replace('+', ' ').lower() in row[1].lower():
            list.append(row)
    return list

def get_stories_by_user(user, db_cursor):
    db_cursor.execute("SELECT * FROM stories")
    list = []
    rows = db_cursor.fetchall()#returns a list with the story

    for row in rows:
        if user.replace('+', ' ').lower() in row[0].lower():
            list.append(row)
    return list

def get_users_by_name(username, db_cursor):
    db_cursor.execute("SELECT * FROM users")
    list = []
    rows = db_cursor.fetchall()#returns a list with the story

    for row in rows:
        if username.replace('+', ' ').lower() in row[0].lower():
            list.append(row)
    return list

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

#Preset database
def generate_preset_db():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() 
    add_user('samson', 'samson123', c)
    add_user('joseph', 'qwertyuiop', c)
    add_user('ryan', "asdfghjkl", c)

    add_story('samson', 'The Bogey Beast', '''A woman finds a pot of treasure on the road while she is returning from work.

    Delighted (very happy) with her luck, she decides to keep it. As she is taking it home, it keeps changing.

    However, her enthusiasm refuses to fade away (disappear or faint slowly).

    What Is Great About It: The old lady in this story is one of the most cheerful characters anyone can encounter in English fiction.

    Her positive disposition (personality) tries to make every negative situation seem like a gift, and she helps us look at luck as a matter of our view rather than events.''', 0, c)

    add_story('joseph', 'The Turtle and the Hare', '''This classic fable (story) tells the story of a very slow tortoise (turtle) and a speedy hare (rabbit).

    The tortoise challenges the hare to a race. The hare laughs at the idea that a tortoise could run faster than he, but the race leads to surprising results.

    What Is Great About It: Have you ever heard the English expression, “Slow and steady wins the race”? This story is the basis for that common phrase.

    This timeless (classic) short story teaches a lesson that we all know but can sometimes forget: Natural talent is no substitute for hard work, and overconfidence often leads to failure.''', 1, c)

    add_story('ryan', 'The Tale of Johnny Town Mouse', '''Timmie Willie is a country mouse who is accidentally taken to a city in a vegetable basket. When he wakes up, he finds himself at a party and makes a friend.

    When he is unable to bear (tolerate or experience) the city life, he returns to his home but invites his friend to the village.

    When his friend visits him, something similar happens.''', 2, c)

    db.commit()
    db.close()