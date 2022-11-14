import sqlite3
from datetime import datetime

DB_FILE="mcstorytest.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#users table stores the username and password
c.execute("CREATE TABLE users(username TEXT, password TEXT);")

#stories table stores the story title, content, id, and time
c.execute("CREATE TABLE stories(username TEXT, title TEXT, content TEXT, ID INTEGER, time TEXT);")

#adds user to user database
def add_user(username, password):
    data = (username, password)
    c.execute("INSERT INTO users VALUES(?,?)", data)

#checks if a user exists
def user_exist(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    
    rows = c.fetchall()#returns a list with the username
    
    if rows == []:#if empty list then no username
        return False
    return True

#returns the password of specfied username
def get_user_pass(username):
    if user_exist(username):
        c.execute("SELECT * FROM users WHERE username=?", (username,))
            
        rows = c.fetchone()#rows is a tuple with the username in zero index and password in first
        
        return rows[1]
    else:
        print(username + " USER DOES NOT EXIST")

#adds story to stories database
def add_story(username, title, content, ID):
    if user_exist(username):
        now = datetime.now()
        dt_string = now.strftime("%B %d, %Y %H:%M:%S")
        data = (username, title, content, ID, dt_string)
        c.execute("INSERT INTO stories VALUES(?, ?, ?, ?, ?)", data)
    else:
        print(username + " USER DOES NOT EXIST")
        
def story_exist(title):
    c.execute("SELECT * FROM stories WHERE title=?", (title,))
    
    rows = c.fetchall()#returns a list with the story

    
    if rows == []:#if empty list then no story
        return False
    return True

def recent_story():
    c.execute("SELECT * FROM stories")
    
    rows = c.fetchall()
    
    if rows == []:#if empty list then no story
        print("There are no stories in the database")
    
    for row in rows:
        story = row
    print(story)

def print_users():
    print("Username, Password")
    c.execute("SELECT * FROM users")
    
    rows = c.fetchall()
    
    for row in rows:
        print(row)
    
def print_stories():
    print("Username, Title, Content, ID")
    c.execute("SELECT * FROM stories")
    
    rows = c.fetchall()
    
    for row in rows:
        print(row)
        
def edit_story(title, content):#goes to the story with the title and replaces its content with the input content
    c.execute("SELECT * FROM stories WHERE title=?", (title,))
    
    rows = c.fetchall()
    
    if rows == []:#if empty list then no story
        print("There is no story with this title name")
    else:
        for row in rows:
            username = row[0]
            ID = row[3]
        
        c.execute("DELETE FROM stories WHERE title=?", (title,))
    
        add_story(username, title, content, ID)# the edited story will have the date of the most recent edit
        


#testing code
#add_user("r1","pass1")
#add_user("r2","pass2")
#add_user("r3","pass3")
#print(user_exist("r1"))
#print(get_user_pass("r1"))
#add_story("r1", "harry potter", "once upon a time", "101")
#add_story("r1", "harry potter part 2", "once upon a time there was", "102")
#print(story_exist("harry potter part 2"))
#print(story_exist("harry potter"))
#print_users()
#print_stories()
#recent_story()
#edit_story("harry potter", "story content")

db.commit() #save changes
db.close() #close database