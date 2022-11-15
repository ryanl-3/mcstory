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

    add_story('joseph', 'Lorem Ipsum', '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Arcu vitae elementum curabitur vitae nunc sed velit dignissim. Dictum fusce ut placerat orci nulla pellentesque dignissim enim sit. Sit amet consectetur adipiscing elit duis tristique sollicitudin nibh. Lorem sed risus ultricies tristique nulla aliquet. Amet risus nullam eget felis eget nunc lobortis mattis aliquam. At risus viverra adipiscing at in tellus integer feugiat scelerisque. Feugiat nibh sed pulvinar proin gravida hendrerit lectus a. Tortor at auctor urna nunc. Cursus risus at ultrices mi. Mi proin sed libero enim sed faucibus turpis in eu. Ultrices tincidunt arcu non sodales neque sodales. Tellus integer feugiat scelerisque varius morbi enim nunc. Eu consequat ac felis donec et odio pellentesque diam. Amet mauris commodo quis imperdiet massa.

Enim nec dui nunc mattis enim ut. Amet venenatis urna cursus eget. Dolor sed viverra ipsum nunc aliquet bibendum enim. Risus sed vulputate odio ut. Vestibulum morbi blandit cursus risus. Lacus sed viverra tellus in hac habitasse. Vulputate enim nulla aliquet porttitor lacus luctus accumsan. Pharetra vel turpis nunc eget lorem dolor. Ornare quam viverra orci sagittis eu volutpat odio facilisis mauris. Elit eget gravida cum sociis natoque penatibus et magnis. Ultrices gravida dictum fusce ut placerat orci nulla. At urna condimentum mattis pellentesque id nibh tortor id aliquet. Netus et malesuada fames ac turpis. Enim sit amet venenatis urna. Pellentesque dignissim enim sit amet venenatis urna cursus eget nunc. At risus viverra adipiscing at in tellus integer. Fringilla est ullamcorper eget nulla facilisi etiam dignissim diam quis. Turpis egestas integer eget aliquet nibh.

Semper quis lectus nulla at volutpat diam ut venenatis tellus. Consectetur a erat nam at. In eu mi bibendum neque egestas. Augue lacus viverra vitae congue. Aenean et tortor at risus viverra adipiscing at in tellus. Egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Diam maecenas sed enim ut sem viverra aliquet. Eget magna fermentum iaculis eu non diam phasellus. Auctor urna nunc id cursus metus aliquam. Massa enim nec dui nunc mattis enim ut tellus. Ac turpis egestas sed tempus urna et. Quis auctor elit sed vulputate. Dui faucibus in ornare quam viverra orci sagittis eu volutpat. Etiam erat velit scelerisque in dictum. Et tortor at risus viverra. Amet risus nullam eget felis eget nunc lobortis mattis. Bibendum ut tristique et egestas quis ipsum suspendisse ultrices. At in tellus integer feugiat scelerisque varius morbi enim nunc. Ipsum suspendisse ultrices gravida dictum.

Posuere urna nec tincidunt praesent. Duis ut diam quam nulla porttitor. Urna et pharetra pharetra massa massa ultricies mi quis hendrerit. Sodales ut etiam sit amet. Ut aliquam purus sit amet luctus venenatis lectus magna. Id ornare arcu odio ut sem nulla. Viverra aliquet eget sit amet tellus. Turpis nunc eget lorem dolor. Donec massa sapien faucibus et molestie ac feugiat sed lectus. Id eu nisl nunc mi ipsum faucibus vitae aliquet. Eu augue ut lectus arcu bibendum. Auctor urna nunc id cursus. Ac odio tempor orci dapibus ultrices in. Lacus sed viverra tellus in hac habitasse platea dictumst. Sit amet consectetur adipiscing elit ut aliquam purus.

Semper eget duis at tellus at. Duis ut diam quam nulla porttitor massa id. Amet mauris commodo quis imperdiet massa tincidunt nunc. Morbi blandit cursus risus at ultrices mi. Id diam maecenas ultricies mi eget mauris. In nulla posuere sollicitudin aliquam. Et magnis dis parturient montes nascetur ridiculus mus. Pretium fusce id velit ut. Elementum pulvinar etiam non quam. Posuere lorem ipsum dolor sit amet consectetur. Commodo ullamcorper a lacus vestibulum sed arcu non. Adipiscing vitae proin sagittis nisl rhoncus. Arcu cursus euismod quis viverra nibh cras pulvinar mattis. Magna sit amet purus gravida quis blandit turpis cursus. In massa tempor nec feugiat nisl pretium. Phasellus faucibus scelerisque eleifend donec pretium vulputate sapien nec. Netus et malesuada fames ac turpis egestas. Cras semper auctor neque vitae tempus.

Consectetur purus ut faucibus pulvinar elementum integer enim neque volutpat. Nunc scelerisque viverra mauris in aliquam sem. Nulla aliquet enim tortor at auctor urna. Neque egestas congue quisque egestas diam in arcu cursus. Porta non pulvinar neque laoreet suspendisse. Sit amet purus gravida quis blandit turpis cursus. Mattis nunc sed blandit libero volutpat sed cras. Netus et malesuada fames ac turpis egestas maecenas pharetra. Tincidunt tortor aliquam nulla facilisi cras fermentum. Nec ullamcorper sit amet risus nullam eget felis eget nunc. Aliquam faucibus purus in massa tempor nec feugiat. Nisi scelerisque eu ultrices vitae auctor eu augue ut lectus. Donec massa sapien faucibus et molestie ac. Euismod elementum nisi quis eleifend quam adipiscing vitae proin sagittis. Lobortis scelerisque fermentum dui faucibus in ornare quam. Pellentesque eu tincidunt tortor aliquam nulla. Elit scelerisque mauris pellentesque pulvinar pellentesque. Pellentesque adipiscing commodo elit at imperdiet dui. Mi eget mauris pharetra et ultrices neque.

Enim sed faucibus turpis in eu mi. Donec pretium vulputate sapien nec sagittis aliquam. Eu feugiat pretium nibh ipsum consequat nisl vel. Sit amet cursus sit amet dictum sit amet. Elementum nisi quis eleifend quam adipiscing vitae proin. Enim diam vulputate ut pharetra. Semper quis lectus nulla at volutpat. Nunc sed velit dignissim sodales ut eu sem. Et netus et malesuada fames ac. Quam lacus suspendisse faucibus interdum. Ullamcorper velit sed ullamcorper morbi tincidunt. At tempor commodo ullamcorper a lacus vestibulum sed arcu. Et leo duis ut diam. Et malesuada fames ac turpis egestas. Pellentesque elit eget gravida cum. Ultrices gravida dictum fusce ut placerat orci nulla. Eu facilisis sed odio morbi. Integer feugiat scelerisque varius morbi enim nunc. Felis eget nunc lobortis mattis aliquam faucibus. Sagittis eu volutpat odio facilisis.

Aliquet lectus proin nibh nisl. Morbi leo urna molestie at elementum. Sed euismod nisi porta lorem mollis aliquam. Eget nunc lobortis mattis aliquam faucibus purus. Nulla malesuada pellentesque elit eget gravida cum sociis natoque. Phasellus faucibus scelerisque eleifend donec pretium vulputate sapien nec. Elit ullamcorper dignissim cras tincidunt lobortis feugiat vivamus at. In nibh mauris cursus mattis. Dui sapien eget mi proin sed libero enim sed faucibus. Cursus turpis massa tincidunt dui ut ornare lectus. Diam in arcu cursus euismod quis viverra nibh cras.

Amet luctus venenatis lectus magna fringilla urna porttitor rhoncus dolor. Quam elementum pulvinar etiam non quam lacus. A cras semper auctor neque. Tempor orci eu lobortis elementum nibh. Cursus sit amet dictum sit amet justo donec enim. Netus et malesuada fames ac turpis. Et ligula ullamcorper malesuada proin libero nunc consequat interdum. Sit amet massa vitae tortor condimentum. Varius quam quisque id diam vel quam elementum pulvinar. Nibh cras pulvinar mattis nunc sed blandit libero volutpat. Est placerat in egestas erat imperdiet sed euismod nisi porta. Pellentesque id nibh tortor id aliquet lectus proin. In ornare quam viverra orci sagittis eu volutpat odio facilisis. Ut diam quam nulla porttitor. Cras sed felis eget velit.

Ac feugiat sed lectus vestibulum. Faucibus ornare suspendisse sed nisi lacus sed viverra tellus. Enim neque volutpat ac tincidunt. Sed felis eget velit aliquet sagittis id consectetur purus ut. Semper viverra nam libero justo laoreet sit amet cursus. Vulputate ut pharetra sit amet. Sed elementum tempus egestas sed sed. Lorem ipsum dolor sit amet consectetur adipiscing. Urna id volutpat lacus laoreet non curabitur gravida arcu. Integer eget aliquet nibh praesent tristique magna sit amet. Leo vel orci porta non pulvinar neque laoreet. Risus sed vulputate odio ut. Et ultrices neque ornare aenean.

Blandit aliquam etiam erat velit scelerisque in. Orci a scelerisque purus semper. Nisl condimentum id venenatis a condimentum vitae sapien pellentesque habitant. Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt. Nunc faucibus a pellentesque sit. Vitae nunc sed velit dignissim sodales ut eu sem. Tellus integer feugiat scelerisque varius morbi enim. Integer eget aliquet nibh praesent tristique. Aliquam id diam maecenas ultricies. Viverra justo nec ultrices dui sapien eget mi proin. Consequat semper viverra nam libero justo.

Viverra ipsum nunc aliquet bibendum enim facilisis. Pellentesque habitant morbi tristique senectus et netus et. Molestie a iaculis at erat pellentesque adipiscing commodo elit at. Massa tincidunt dui ut ornare lectus sit amet est placerat. Ipsum suspendisse ultrices gravida dictum. Felis eget nunc lobortis mattis. Amet tellus cras adipiscing enim eu turpis egestas pretium. Tortor posuere ac ut consequat. Nunc sed blandit libero volutpat sed cras ornare arcu. In eu mi bibendum neque egestas. Venenatis urna cursus eget nunc scelerisque viverra mauris in aliquam. Facilisi morbi tempus iaculis urna id. Ac felis donec et odio pellentesque diam volutpat commodo sed. Quam pellentesque nec nam aliquam. Nunc congue nisi vitae suscipit tellus. Elit pellentesque habitant morbi tristique senectus et netus et. Facilisi cras fermentum odio eu feugiat.

Pharetra convallis posuere morbi leo urna molestie. Mauris in aliquam sem fringilla ut morbi tincidunt augue interdum. Nunc mattis enim ut tellus elementum sagittis. Cursus in hac habitasse platea. Auctor neque vitae tempus quam pellentesque. Hendrerit gravida rutrum quisque non tellus orci ac auctor. Commodo sed egestas egestas fringilla phasellus faucibus scelerisque eleifend. Lacus vestibulum sed arcu non odio euismod lacinia at quis. Euismod elementum nisi quis eleifend quam adipiscing vitae proin. Eget velit aliquet sagittis id consectetur. Neque egestas congue quisque egestas diam in arcu cursus. Eu lobortis elementum nibh tellus molestie nunc. Enim eu turpis egestas pretium aenean pharetra magna ac. Sed turpis tincidunt id aliquet risus. At lectus urna duis convallis convallis tellus id interdum velit. Amet consectetur adipiscing elit ut aliquam purus. Adipiscing commodo elit at imperdiet dui accumsan. Faucibus purus in massa tempor. In hac habitasse platea dictumst quisque sagittis purus. Quis viverra nibh cras pulvinar mattis nunc sed blandit.

Pellentesque diam volutpat commodo sed egestas egestas fringilla phasellus faucibus. Eu feugiat pretium nibh ipsum consequat. Hac habitasse platea dictumst vestibulum rhoncus est pellentesque. Nec nam aliquam sem et tortor consequat id. Venenatis urna cursus eget nunc scelerisque. Et magnis dis parturient montes nascetur ridiculus mus mauris. Cursus sit amet dictum sit. Amet cursus sit amet dictum sit. Dictum sit amet justo donec enim diam vulputate. Est ultricies integer quis auctor elit sed vulputate mi. Consequat mauris nunc congue nisi vitae. Pellentesque elit ullamcorper dignissim cras tincidunt lobortis feugiat vivamus. Urna duis convallis convallis tellus id. Nibh cras pulvinar mattis nunc sed blandit. Neque ornare aenean euismod elementum nisi quis eleifend quam. Nisl suscipit adipiscing bibendum est ultricies integer quis auctor.

Dolor sit amet consectetur adipiscing elit duis tristique sollicitudin nibh. Nunc eget lorem dolor sed viverra ipsum nunc. Varius duis at consectetur lorem donec massa sapien faucibus. Amet est placerat in egestas erat imperdiet sed euismod. Dolor sit amet consectetur adipiscing elit ut aliquam purus sit. Lobortis feugiat vivamus at augue eget arcu dictum. Consequat semper viverra nam libero. Nunc lobortis mattis aliquam faucibus. Lobortis feugiat vivamus at augue eget arcu dictum. Sit amet commodo nulla facilisi nullam vehicula. Est placerat in egestas erat imperdiet sed. At varius vel pharetra vel turpis nunc eget lorem dolor. Non quam lacus suspendisse faucibus interdum posuere. Elementum integer enim neque volutpat ac tincidunt vitae semper. Cursus eget nunc scelerisque viverra mauris in aliquam sem. Magnis dis parturient montes nascetur. Nunc congue nisi vitae suscipit tellus mauris a. Amet cursus sit amet dictum sit. Lacus suspendisse faucibus interdum posuere lorem ipsum.

Et malesuada fames ac turpis egestas integer eget aliquet nibh. Non odio euismod lacinia at quis risus sed. Velit ut tortor pretium viverra suspendisse potenti nullam ac tortor. Interdum posuere lorem ipsum dolor sit amet consectetur adipiscing. Molestie at elementum eu facilisis sed odio morbi quis commodo. Pellentesque elit eget gravida cum. Arcu dictum varius duis at consectetur. Mauris pellentesque pulvinar pellentesque habitant morbi tristique. Risus ultricies tristique nulla aliquet enim. Scelerisque viverra mauris in aliquam sem fringilla ut. Cras sed felis eget velit. Magnis dis parturient montes nascetur ridiculus. Mattis pellentesque id nibh tortor id aliquet lectus proin nibh. Quam id leo in vitae turpis massa sed elementum. Pretium nibh ipsum consequat nisl vel pretium lectus quam id. Enim ut tellus elementum sagittis vitae et leo duis ut.

Lorem ipsum dolor sit amet consectetur. Phasellus egestas tellus rutrum tellus pellentesque. Risus in hendrerit gravida rutrum. Varius duis at consectetur lorem donec. Orci phasellus egestas tellus rutrum tellus pellentesque eu tincidunt. Amet massa vitae tortor condimentum lacinia quis. Pretium lectus quam id leo in vitae turpis massa. Sed vulputate odio ut enim blandit volutpat. Nec dui nunc mattis enim. Cursus vitae congue mauris rhoncus. Pharetra pharetra massa massa ultricies mi. Ac felis donec et odio pellentesque diam volutpat. Sit amet cursus sit amet dictum sit. Sed risus ultricies tristique nulla aliquet.

Tortor consequat id porta nibh. Rhoncus aenean vel elit scelerisque mauris. Cursus risus at ultrices mi tempus imperdiet nulla malesuada pellentesque. Tellus mauris a diam maecenas. In cursus turpis massa tincidunt dui ut. Ac orci phasellus egestas tellus rutrum tellus pellentesque eu. Adipiscing bibendum est ultricies integer. Eleifend donec pretium vulputate sapien nec sagittis aliquam malesuada. Nulla aliquet porttitor lacus luctus. Vitae aliquet nec ullamcorper sit.

Purus sit amet volutpat consequat mauris nunc. Vel pretium lectus quam id leo in. Vitae et leo duis ut. Sed risus ultricies tristique nulla aliquet enim tortor at auctor. Ut lectus arcu bibendum at varius vel pharetra vel. In ante metus dictum at tempor commodo ullamcorper a lacus. Vulputate sapien nec sagittis aliquam malesuada bibendum. Pharetra et ultrices neque ornare aenean. Orci sagittis eu volutpat odio facilisis mauris sit. Quis auctor elit sed vulputate mi sit amet mauris. Est ultricies integer quis auctor elit sed vulputate mi sit. Orci a scelerisque purus semper eget duis at tellus at. Eget mi proin sed libero. Fringilla est ullamcorper eget nulla facilisi etiam dignissim diam. Adipiscing elit ut aliquam purus sit amet luctus. Habitant morbi tristique senectus et netus et.

Auctor augue mauris augue neque. Iaculis eu non diam phasellus vestibulum lorem sed risus. Malesuada pellentesque elit eget gravida cum sociis. Tempus imperdiet nulla malesuada pellentesque elit eget gravida cum. Non arcu risus quis varius. Lobortis scelerisque fermentum dui faucibus. Sit amet commodo nulla facilisi nullam vehicula ipsum a. Ut aliquam purus sit amet. Eget duis at tellus at. Odio eu feugiat pretium nibh.

Non sodales neque sodales ut etiam. Pellentesque diam volutpat commodo sed. A cras semper auctor neque vitae tempus quam pellentesque nec. Sem fringilla ut morbi tincidunt augue interdum velit euismod. Faucibus in ornare quam viverra. Nunc lobortis mattis aliquam faucibus purus in massa tempor nec. Odio eu feugiat pretium nibh ipsum consequat. Placerat duis ultricies lacus sed. Aliquam malesuada bibendum arcu vitae elementum curabitur vitae. Nisl purus in mollis nunc sed. Orci dapibus ultrices in iaculis. Viverra nam libero justo laoreet sit amet cursus sit amet. Montes nascetur ridiculus mus mauris vitae ultricies leo integer. Odio euismod lacinia at quis. Id venenatis a condimentum vitae sapien pellentesque. Mattis pellentesque id nibh tortor id aliquet lectus. Ipsum nunc aliquet bibendum enim facilisis gravida neque convallis. Aenean vel elit scelerisque mauris pellentesque pulvinar pellentesque habitant.

Imperdiet massa tincidunt nunc pulvinar sapien. Lacus laoreet non curabitur gravida arcu. Mi tempus imperdiet nulla malesuada pellentesque elit eget gravida cum. Diam maecenas sed enim ut. Nibh ipsum consequat nisl vel pretium. Orci phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Nunc aliquet bibendum enim facilisis gravida neque convallis. Lobortis elementum nibh tellus molestie nunc. Feugiat scelerisque varius morbi enim nunc faucibus a pellentesque sit. Vestibulum lorem sed risus ultricies tristique nulla aliquet enim tortor. Adipiscing elit ut aliquam purus sit amet luctus venenatis lectus. Viverra suspendisse potenti nullam ac tortor. Aliquam eleifend mi in nulla posuere sollicitudin aliquam. Non blandit massa enim nec dui nunc. Eget nunc scelerisque viverra mauris in aliquam sem fringilla ut. Hac habitasse platea dictumst quisque sagittis purus sit. Viverra adipiscing at in tellus integer feugiat scelerisque.

Tellus elementum sagittis vitae et leo duis ut diam quam. Volutpat lacus laoreet non curabitur gravida. Interdum consectetur libero id faucibus nisl tincidunt eget nullam non. Sem nulla pharetra diam sit. Tellus integer feugiat scelerisque varius. Magna fermentum iaculis eu non. Sed turpis tincidunt id aliquet risus feugiat in. Venenatis urna cursus eget nunc scelerisque viverra. Facilisi etiam dignissim diam quis enim lobortis scelerisque fermentum. Magna etiam tempor orci eu lobortis elementum nibh tellus molestie. Venenatis urna cursus eget nunc scelerisque viverra mauris in aliquam. Velit sed ullamcorper morbi tincidunt ornare massa eget.

In fermentum et sollicitudin ac orci phasellus egestas tellus. Feugiat nisl pretium fusce id. Augue ut lectus arcu bibendum at varius. Dolor magna eget est lorem. Ac feugiat sed lectus vestibulum mattis ullamcorper velit sed ullamcorper. Mi eget mauris pharetra et ultrices neque ornare aenean euismod. Eget nullam non nisi est sit amet. Rutrum tellus pellentesque eu tincidunt tortor. Et pharetra pharetra massa massa ultricies. Arcu dictum varius duis at consectetur lorem donec massa. Ornare quam viverra orci sagittis. Cras sed felis eget velit aliquet sagittis id. Vitae elementum curabitur vitae nunc sed velit dignissim. Massa vitae tortor condimentum lacinia quis vel. Tellus integer feugiat scelerisque varius morbi enim nunc faucibus a. Vel turpis nunc eget lorem dolor sed viverra. Tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada proin libero. Urna duis convallis convallis tellus id interdum velit laoreet. Laoreet non curabitur gravida arcu ac tortor dignissim convallis.

Tincidunt tortor aliquam nulla facilisi cras fermentum odio eu feugiat. Suspendisse faucibus interdum posuere lorem ipsum dolor sit amet. Feugiat in ante metus dictum at tempor commodo ullamcorper. Eget sit amet tellus cras adipiscing. Risus nec feugiat in fermentum posuere urna. Adipiscing at in tellus integer. Ante metus dictum at tempor commodo ullamcorper a. Sit amet justo donec enim diam vulputate ut pharetra sit. Pulvinar mattis nunc sed blandit. In ante metus dictum at tempor commodo ullamcorper. Suscipit adipiscing bibendum est ultricies integer quis auctor elit. Vitae sapien pellentesque habitant morbi tristique senectus et netus et. Eleifend donec pretium vulputate sapien nec sagittis. Orci ac auctor augue mauris augue. Nunc mi ipsum faucibus vitae aliquet nec ullamcorper. Sagittis vitae et leo duis ut. Eleifend mi in nulla posuere sollicitudin aliquam. Eu consequat ac felis donec et odio pellentesque diam. Justo nec ultrices dui sapien. A erat nam at lectus urna duis.

Pulvinar etiam non quam lacus suspendisse. Platea dictumst vestibulum rhoncus est pellentesque elit ullamcorper. Commodo sed egestas egestas fringilla phasellus. Congue mauris rhoncus aenean vel elit scelerisque mauris pellentesque. Et malesuada fames ac turpis. Vitae turpis massa sed elementum tempus egestas sed. Semper risus in hendrerit gravida. Nibh tellus molestie nunc non blandit massa enim nec. Egestas congue quisque egestas diam in arcu cursus euismod quis. Enim lobortis scelerisque fermentum dui faucibus in ornare quam viverra. Condimentum vitae sapien pellentesque habitant. Enim diam vulputate ut pharetra sit amet. Posuere urna nec tincidunt praesent semper feugiat nibh sed.

Nibh venenatis cras sed felis eget velit aliquet sagittis. Semper viverra nam libero justo. Facilisis sed odio morbi quis commodo odio aenean sed. Lacus suspendisse faucibus interdum posuere lorem ipsum. Leo a diam sollicitudin tempor. Et pharetra pharetra massa massa ultricies mi. Sed lectus vestibulum mattis ullamcorper. Ut tortor pretium viverra suspendisse. Aliquam id diam maecenas ultricies mi eget mauris pharetra. Bibendum neque egestas congue quisque egestas diam in arcu cursus. Ultricies leo integer malesuada nunc vel risus commodo viverra maecenas. Metus dictum at tempor commodo ullamcorper. Morbi tristique senectus et netus et malesuada. Tellus elementum sagittis vitae et leo duis ut.

Elementum integer enim neque volutpat ac tincidunt vitae semper quis. Mattis aliquam faucibus purus in. Lobortis scelerisque fermentum dui faucibus in ornare quam viverra orci. Egestas purus viverra accumsan in nisl nisi. In tellus integer feugiat scelerisque varius. Tempor nec feugiat nisl pretium fusce id velit ut tortor. Sapien faucibus et molestie ac. Vitae suscipit tellus mauris a diam maecenas sed enim. Metus aliquam eleifend mi in. Tincidunt eget nullam non nisi est sit amet facilisis. Velit dignissim sodales ut eu sem integer vitae justo eget. Purus in mollis nunc sed.

Neque sodales ut etiam sit amet nisl. Sit amet consectetur adipiscing elit. Faucibus nisl tincidunt eget nullam non nisi. Erat velit scelerisque in dictum non. Viverra justo nec ultrices dui. Massa sed elementum tempus egestas sed sed risus pretium. Duis at tellus at urna condimentum mattis pellentesque id nibh. Egestas diam in arcu cursus. Odio euismod lacinia at quis risus sed vulputate odio ut. Mauris a diam maecenas sed enim. Lectus nulla at volutpat diam ut. Rhoncus aenean vel elit scelerisque mauris. Eget egestas purus viverra accumsan in nisl nisi scelerisque eu. Felis eget nunc lobortis mattis aliquam. Porttitor massa id neque aliquam vestibulum morbi. Morbi tristique senectus et netus et malesuada fames. In mollis nunc sed id semper. Aliquet eget sit amet tellus cras adipiscing enim eu.

Vulputate eu scelerisque felis imperdiet proin fermentum leo. Faucibus interdum posuere lorem ipsum dolor sit amet consectetur adipiscing. Iaculis eu non diam phasellus vestibulum. Nibh venenatis cras sed felis eget. Viverra justo nec ultrices dui sapien eget mi. Dictumst vestibulum rhoncus est pellentesque elit ullamcorper. Sed sed risus pretium quam vulputate dignissim suspendisse in. Nullam ac tortor vitae purus faucibus ornare. Interdum velit laoreet id donec ultrices tincidunt arcu non. Sed risus ultricies tristique nulla aliquet. Tellus mauris a diam maecenas sed enim ut sem viverra. Velit scelerisque in dictum non consectetur a. Ac auctor augue mauris augue.

Diam ut venenatis tellus in metus vulputate eu scelerisque. Egestas dui id ornare arcu. Ut tortor pretium viverra suspendisse. Varius vel pharetra vel turpis nunc eget lorem. Adipiscing tristique risus nec feugiat in. Imperdiet dui accumsan sit amet nulla. Euismod elementum nisi quis eleifend quam adipiscing vitae. Consectetur a erat nam at lectus urna duis convallis. Amet porttitor eget dolor morbi non arcu risus quis varius. Varius duis at consectetur lorem donec massa sapien faucibus. Congue quisque egestas diam in. Vulputate sapien nec sagittis aliquam. Id diam vel quam elementum pulvinar etiam non quam lacus. Blandit turpis cursus in hac habitasse platea. Fames ac turpis egestas maecenas pharetra convallis. Orci porta non pulvinar neque laoreet suspendisse interdum consectetur libero.

Lobortis scelerisque fermentum dui faucibus in ornare quam viverra orci. Integer enim neque volutpat ac tincidunt vitae semper quis lectus. Non sodales neque sodales ut etiam sit amet nisl. Viverra ipsum nunc aliquet bibendum enim. Euismod in pellentesque massa placerat duis ultricies lacus sed turpis. Dui vivamus arcu felis bibendum ut tristique et. Condimentum vitae sapien pellentesque habitant. Eu mi bibendum neque egestas congue quisque egestas diam. Suspendisse ultrices gravida dictum fusce ut placerat orci. Purus sit amet volutpat consequat mauris. Libero volutpat sed cras ornare arcu dui vivamus arcu. Ornare massa eget egestas purus viverra accumsan in nisl. Vel orci porta non pulvinar neque laoreet suspendisse interdum. Magna fermentum iaculis eu non diam. Porttitor lacus luctus accumsan tortor posuere. Nullam non nisi est sit amet.

Odio tempor orci dapibus ultrices in iaculis nunc. Sed turpis tincidunt id aliquet risus feugiat in ante. Malesuada bibendum arcu vitae elementum curabitur vitae. Dolor sed viverra ipsum nunc. Quam pellentesque nec nam aliquam sem et tortor consequat id. Integer feugiat scelerisque varius morbi enim nunc faucibus a. Rhoncus aenean vel elit scelerisque. Posuere morbi leo urna molestie at elementum eu facilisis. Fringilla est ullamcorper eget nulla facilisi etiam. Consectetur lorem donec massa sapien faucibus. Pharetra pharetra massa massa ultricies mi quis hendrerit dolor magna. Nisi est sit amet facilisis. Id volutpat lacus laoreet non curabitur gravida arcu ac tortor. Aliquet eget sit amet tellus cras adipiscing enim. Id leo in vitae turpis massa sed elementum tempus egestas. Rhoncus urna neque viverra justo nec. Nunc scelerisque viverra mauris in aliquam sem fringilla. Etiam non quam lacus suspendisse faucibus interdum posuere lorem ipsum.

Tellus elementum sagittis vitae et leo duis. Aliquet risus feugiat in ante. Tortor at auctor urna nunc id. Nisl vel pretium lectus quam id leo. Velit dignissim sodales ut eu sem. Neque egestas congue quisque egestas diam. Mauris ultrices eros in cursus turpis massa tincidunt dui ut. Ullamcorper dignissim cras tincidunt lobortis feugiat vivamus at augue eget. Egestas sed tempus urna et pharetra. Lectus sit amet est placerat in egestas erat imperdiet sed. Pharetra massa massa ultricies mi quis hendrerit dolor. Facilisi nullam vehicula ipsum a arcu cursus vitae congue. Viverra maecenas accumsan lacus vel facilisis volutpat est.

Lorem mollis aliquam ut porttitor leo a diam. Cras tincidunt lobortis feugiat vivamus. Ut tortor pretium viverra suspendisse potenti nullam ac tortor vitae. Augue eget arcu dictum varius duis at. Eget dolor morbi non arcu. Sit amet risus nullam eget felis. Consequat id porta nibh venenatis cras sed felis. Elementum pulvinar etiam non quam lacus. Ac felis donec et odio. Amet massa vitae tortor condimentum lacinia quis. Laoreet suspendisse interdum consectetur libero id faucibus. Orci nulla pellentesque dignissim enim sit amet venenatis. In cursus turpis massa tincidunt dui ut ornare. Condimentum lacinia quis vel eros donec. Duis convallis convallis tellus id interdum velit. At erat pellentesque adipiscing commodo elit. Velit scelerisque in dictum non. Metus vulputate eu scelerisque felis imperdiet. Consectetur adipiscing elit duis tristique sollicitudin nibh sit amet. Mollis nunc sed id semper risus.

A condimentum vitae sapien pellentesque habitant. Aliquet bibendum enim facilisis gravida neque convallis a. Magna ac placerat vestibulum lectus mauris ultrices eros. Egestas fringilla phasellus faucibus scelerisque. At varius vel pharetra vel turpis nunc eget lorem. Velit aliquet sagittis id consectetur purus ut faucibus. Venenatis tellus in metus vulputate eu scelerisque felis imperdiet proin. Erat nam at lectus urna duis convallis convallis. Donec enim diam vulputate ut pharetra sit. Purus ut faucibus pulvinar elementum integer enim neque. Id venenatis a condimentum vitae sapien pellentesque habitant. Viverra suspendisse potenti nullam ac tortor. Ac tortor vitae purus faucibus ornare suspendisse sed nisi lacus. Tempor orci dapibus ultrices in iaculis nunc. Volutpat maecenas volutpat blandit aliquam. Dui sapien eget mi proin sed libero enim. Turpis in eu mi bibendum. Lacus luctus accumsan tortor posuere ac ut consequat semper. Ac tortor dignissim convallis aenean et tortor at risus.

Pellentesque id nibh tortor id aliquet. Proin libero nunc consequat interdum varius sit amet mattis vulputate. Ultrices tincidunt arcu non sodales neque. Nibh sed pulvinar proin gravida hendrerit. Dui vivamus arcu felis bibendum ut tristique. Vulputate odio ut enim blandit volutpat maecenas volutpat. Auctor urna nunc id cursus metus aliquam eleifend mi. Ac tortor vitae purus faucibus ornare. Aenean pharetra magna ac placerat vestibulum lectus. Et malesuada fames ac turpis egestas integer eget aliquet nibh. Praesent elementum facilisis leo vel fringilla est ullamcorper.

Et leo duis ut diam quam nulla porttitor massa id. Dignissim sodales ut eu sem integer vitae. Aliquam sem fringilla ut morbi tincidunt. Varius quam quisque id diam vel quam elementum pulvinar. Lorem dolor sed viverra ipsum. In ornare quam viverra orci sagittis eu volutpat odio. Hendrerit gravida rutrum quisque non tellus. Sagittis nisl rhoncus mattis rhoncus urna neque viverra justo nec. Urna molestie at elementum eu facilisis sed odio. Egestas dui id ornare arcu. Ut consequat semper viverra nam. Pharetra massa massa ultricies mi quis hendrerit dolor magna.

Nunc mattis enim ut tellus elementum sagittis vitae. Fringilla phasellus faucibus scelerisque eleifend. Interdum velit euismod in pellentesque massa placerat duis. In iaculis nunc sed augue lacus. In hendrerit gravida rutrum quisque non. Purus gravida quis blandit turpis cursus in. Ut tristique et egestas quis ipsum suspendisse. Suscipit tellus mauris a diam maecenas. Justo laoreet sit amet cursus sit amet dictum sit amet. Pharetra pharetra massa massa ultricies. Facilisis volutpat est velit egestas dui. Nunc lobortis mattis aliquam faucibus. Blandit aliquam etiam erat velit scelerisque in dictum. Orci a scelerisque purus semper eget duis. Ut tortor pretium viverra suspendisse. Aliquam eleifend mi in nulla posuere sollicitudin aliquam.

Est lorem ipsum dolor sit amet consectetur adipiscing elit. Sapien faucibus et molestie ac feugiat. Nunc mi ipsum faucibus vitae aliquet nec. Sollicitudin tempor id eu nisl nunc. Sit amet consectetur adipiscing elit ut aliquam purus sit. Ultrices tincidunt arcu non sodales neque sodales ut etiam sit. Placerat in egestas erat imperdiet sed euismod nisi porta. Diam maecenas ultricies mi eget mauris pharetra et ultrices. A arcu cursus vitae congue. Libero nunc consequat interdum varius. Urna nunc id cursus metus aliquam eleifend mi in nulla. Pretium vulputate sapien nec sagittis aliquam malesuada bibendum. Lacinia quis vel eros donec ac. Pulvinar neque laoreet suspendisse interdum consectetur libero id faucibus. Diam quam nulla porttitor massa id neque aliquam vestibulum. Amet dictum sit amet justo donec enim diam vulputate.

Nisi est sit amet facilisis magna etiam tempor orci eu. Tortor condimentum lacinia quis vel eros donec ac odio. Molestie nunc non blandit massa. Nibh praesent tristique magna sit amet purus gravida quis. Ac tortor vitae purus faucibus ornare suspendisse sed nisi. Tortor vitae purus faucibus ornare suspendisse sed. Nibh tellus molestie nunc non blandit massa enim nec. Sagittis purus sit amet volutpat consequat mauris nunc. Donec ac odio tempor orci dapibus ultrices in. Semper risus in hendrerit gravida rutrum.

Sed elementum tempus egestas sed sed risus. Metus vulputate eu scelerisque felis imperdiet. Volutpat odio facilisis mauris sit amet massa vitae tortor condimentum. Ac turpis egestas sed tempus urna et. At risus viverra adipiscing at in tellus integer feugiat scelerisque. Egestas tellus rutrum tellus pellentesque eu tincidunt. Orci ac auctor augue mauris. Id ornare arcu odio ut sem nulla pharetra diam. Ultrices eros in cursus turpis massa tincidunt dui ut ornare. Sed tempus urna et pharetra pharetra massa. Urna cursus eget nunc scelerisque viverra mauris. Morbi tristique senectus et netus. Enim ut tellus elementum sagittis vitae et leo duis ut. Viverra accumsan in nisl nisi scelerisque. Aenean et tortor at risus viverra adipiscing at in tellus. Amet consectetur adipiscing elit ut aliquam. Sollicitudin ac orci phasellus egestas tellus rutrum tellus pellentesque. Faucibus purus in massa tempor nec feugiat nisl. Sociis natoque penatibus et magnis dis. Quis imperdiet massa tincidunt nunc pulvinar sapien.

Pulvinar mattis nunc sed blandit libero volutpat sed. Dui accumsan sit amet nulla facilisi. Aliquam ut porttitor leo a diam sollicitudin tempor. Habitant morbi tristique senectus et netus. Nec dui nunc mattis enim ut tellus elementum. Sagittis orci a scelerisque purus semper eget duis at. Auctor augue mauris augue neque gravida in. Neque volutpat ac tincidunt vitae semper quis lectus nulla. Posuere sollicitudin aliquam ultrices sagittis orci a scelerisque. Dolor sed viverra ipsum nunc aliquet bibendum. Suspendisse sed nisi lacus sed viverra tellus in. Pellentesque pulvinar pellentesque habitant morbi tristique. Vulputate sapien nec sagittis aliquam malesuada bibendum arcu vitae. Elementum tempus egestas sed sed risus pretium quam vulputate dignissim. Quam quisque id diam vel quam elementum. Vel facilisis volutpat est velit egestas dui id.

Aliquet risus feugiat in ante. Sit amet cursus sit amet dictum sit. Magna ac placerat vestibulum lectus mauris ultrices eros in cursus. Nunc vel risus commodo viverra maecenas accumsan lacus vel. Ultrices sagittis orci a scelerisque. Pulvinar elementum integer enim neque volutpat. Amet nulla facilisi morbi tempus iaculis urna id. Mauris augue neque gravida in fermentum et sollicitudin ac. Porta nibh venenatis cras sed felis eget. Mattis molestie a iaculis at erat pellentesque adipiscing commodo.

Sollicitudin aliquam ultrices sagittis orci a scelerisque. Nunc non blandit massa enim nec dui nunc. Odio aenean sed adipiscing diam donec. Sit amet volutpat consequat mauris. Ipsum consequat nisl vel pretium lectus quam id leo in. Sociis natoque penatibus et magnis dis parturient montes nascetur. Tortor consequat id porta nibh venenatis cras sed felis eget. Quam nulla porttitor massa id neque aliquam. Sapien faucibus et molestie ac feugiat. At imperdiet dui accumsan sit amet nulla facilisi. Sed libero enim sed faucibus turpis in eu. Sit amet nisl suscipit adipiscing bibendum. Cras pulvinar mattis nunc sed blandit libero volutpat.

Sed felis eget velit aliquet sagittis. Eget magna fermentum iaculis eu. Ipsum a arcu cursus vitae congue mauris rhoncus. Curabitur vitae nunc sed velit dignissim sodales ut. Sed faucibus turpis in eu mi bibendum. Turpis egestas maecenas pharetra convallis posuere morbi leo urna molestie. Sed risus ultricies tristique nulla aliquet enim. Libero id faucibus nisl tincidunt eget nullam non nisi est. Mauris nunc congue nisi vitae suscipit tellus mauris. Amet nisl suscipit adipiscing bibendum est. Vulputate odio ut enim blandit volutpat maecenas volutpat. Augue lacus viverra vitae congue. Vitae et leo duis ut diam quam.

Quam lacus suspendisse faucibus interdum posuere. Pulvinar mattis nunc sed blandit libero volutpat sed. Fermentum odio eu feugiat pretium nibh ipsum consequat nisl. Massa enim nec dui nunc mattis enim ut tellus elementum. Maecenas pharetra convallis posuere morbi. Tempus imperdiet nulla malesuada pellentesque elit eget gravida cum. Fusce id velit ut tortor pretium viverra suspendisse. Congue nisi vitae suscipit tellus mauris a diam maecenas sed. Leo a diam sollicitudin tempor id. Tristique senectus et netus et malesuada fames ac. Pulvinar etiam non quam lacus suspendisse faucibus interdum. Ornare lectus sit amet est placerat. Velit dignissim sodales ut eu sem. Diam maecenas sed enim ut. Ultricies mi eget mauris pharetra et ultrices. Id nibh tortor id aliquet lectus proin. Sapien pellentesque habitant morbi tristique senectus. Ultricies lacus sed turpis tincidunt id aliquet risus feugiat in. Sed risus pretium quam vulputate dignissim.

Risus at ultrices mi tempus imperdiet nulla malesuada. Consectetur adipiscing elit duis tristique sollicitudin nibh sit amet. Scelerisque fermentum dui faucibus in ornare. Neque gravida in fermentum et sollicitudin ac. Montes nascetur ridiculus mus mauris vitae ultricies leo. Ipsum dolor sit amet consectetur adipiscing elit ut aliquam. Tellus mauris a diam maecenas. Purus viverra accumsan in nisl nisi scelerisque. Elementum integer enim neque volutpat. Adipiscing elit pellentesque habitant morbi tristique senectus.

Felis bibendum ut tristique et egestas quis ipsum suspendisse. Duis at consectetur lorem donec massa sapien. Morbi enim nunc faucibus a pellentesque sit amet porttitor eget. Bibendum at varius vel pharetra. Sed elementum tempus egestas sed. Eget arcu dictum varius duis at consectetur lorem donec massa. Nibh nisl condimentum id venenatis a condimentum vitae sapien pellentesque. Viverra maecenas accumsan lacus vel facilisis. Fames ac turpis egestas integer eget aliquet nibh. Posuere lorem ipsum dolor sit amet consectetur adipiscing elit. Viverra adipiscing at in tellus integer. Turpis egestas sed tempus urna et pharetra pharetra massa. Erat velit scelerisque in dictum. Justo eget magna fermentum iaculis eu. Proin fermentum leo vel orci porta non pulvinar neque laoreet.

Nunc eget lorem dolor sed viverra ipsum. Magna fringilla urna porttitor rhoncus dolor. Imperdiet dui accumsan sit amet nulla facilisi. A diam sollicitudin tempor id eu nisl. Aliquam nulla facilisi cras fermentum odio eu feugiat pretium nibh. Molestie nunc non blandit massa enim nec. Et pharetra pharetra massa massa ultricies mi quis. Facilisis sed odio morbi quis commodo. Luctus venenatis lectus magna fringilla urna. Lobortis elementum nibh tellus molestie nunc non blandit massa enim. Eget egestas purus viverra accumsan in. Aliquam malesuada bibendum arcu vitae. Rhoncus dolor purus non enim praesent elementum. Eget mauris pharetra et ultrices neque ornare aenean euismod elementum. Ipsum faucibus vitae aliquet nec ullamcorper sit. Libero justo laoreet sit amet cursus sit amet dictum sit.''', 1, c)

    add_story('ryan', 'The Tale of Johnny Town Mouse', '''Timmie Willie is a country mouse who is accidentally taken to a city in a vegetable basket. When he wakes up, he finds himself at a party and makes a friend.

    When he is unable to bear (tolerate or experience) the city life, he returns to his home but invites his friend to the village.

    When his friend visits him, something similar happens.''', 2, c)

    db.commit()
    db.close()