from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
import bcrypt

app = Flask(__name__)

app.secret_key = '1234'

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

#http://localhost:5000/ - this is the default page. From this page, user can choose to log in or register. Admin button will be directed to the login page as well.  
@app.route("/")
def default():
    return render_template('default.html')

#http://locoalhost:5000/admin/ -- this is the admin page.
@app.route("/admin/")
def admin():
    if 'loggedin' in session:
        return render_template('admin.html')
    return redirect(url_for('login'))

# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        # Check if account exists using MySQL
        connection = getCursor()
        connection.execute('SELECT * FROM user WHERE username = %s', (username,))
        # Fetch one record and return result
        account = connection.fetchone()
        if account is not None:
            password = account[2]
            if bcrypt.checkpw(user_password.encode('utf-8'),password.encode('utf-8')):
            # If account exists in accounts table in out database
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                # redirect to admin page if role == "admin"
                if account[4] == 'admin':
                    return redirect(url_for('admin'))
                # redirect to staff page if role == "staff"
                elif account[4] == 'staff':
                    return redirect(url_for('staff'))
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


 # http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/home', methods=['GET'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        #connect to db
        connection = getCursor()
        # Get car information from db
        sql_car = 'select * from car;'
        connection.execute(sql_car)
        car = connection.fetchall()

        return render_template('home.html', username=session['username'], car = car)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#http://localhost:5000/home/cardetails
@app.route('/home/cardetails', methods=['GET','POST'])
def cardetails():
    if 'loggedin' in session:
        numberplate = request.form.get('numberplate')
        print(numberplate)
        connection=getCursor()
        sql_indivcar='select * from car where numberplate = %s;'
        connection.execute(sql_indivcar, (numberplate,))
        indivcar=connection.fetchone()
        print(indivcar)
        return render_template('cardetails.html', username=session['username'], item=indivcar)

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        connection = getCursor()
        connection.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = connection.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            #print(hashed)
            connection.execute('INSERT INTO user (username, password, email, role) VALUES (%s, %s, %s, %s);', (username, hashed, email, 'customer'),)
            # connect to db to get userid out from the user table after the new user has been added
            connection.execute('Select userid from user WHERE username=%s;', (username,))
            userid = connection.fetchone()
            #print(userid)
            # insert the new user information into the customer table as well, only userid will be recorded in this table when a customer registers
            connection.execute('INSERT INTO customer (userid) VALUES (%s);', (userid[0],))
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        connection = getCursor()
        #Get the info from the table user join table customer
        sql='SELECT * FROM user LEFT JOIN customer ON user.userid = customer.userid WHERE user.userid = %s;'
        connection.execute(sql, (session['id'],))
        account = connection.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/profile/update', methods=['GET','POST'])
def updateinfo():
    if 'loggedin' in session:
        connection = getCursor()
        #Get the info from the table user join table customer
        sql='SELECT * FROM user LEFT JOIN customer ON user.userid = customer.userid WHERE user.userid = %s;'
        connection.execute(sql, (session['id'],))
        account = connection.fetchone()
        return render_template('profile_update.html', account=account)
    return redirect(url_for('login'))

@app.route('/profile/edit', methods=['GET','POST'])
def editinfo():
    if 'loggedin' in session:
        # Get the updated info from the form
        username=request.form.get('username')
        #print(username)
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        address=request.form.get('address')
        phone=request.form.get('phone')
        password=request.form.get('password')
        email=request.form.get('email')
        #Hash the password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        connection = getCursor()
        #Update the db (user table and customer table) with the new information that be filled through the form 
        connection.execute('UPDATE user SET username=%s, password=%s, email=%s WHERE userid=%s;', (username, hashed, email, session['id'],))
        connection.execute('UPDATE customer SET firstname=%s, lastname=%s, address=%s, phone=%s WHERE userid=%s;', (firstname, lastname, address, phone, session['id'], ))
        return redirect(url_for('profile'))
    return redirect(url_for('login'))
    
# staff page 
@app.route('/staff')
def staff():
    if 'loggedin' in session:
        # connect to db to get back the account info
        connection=getCursor()
        sql='SELECT * FROM user LEFT JOIN staff ON user.userid = staff.userid WHERE user.userid = %s;'
        connection.execute(sql, (session['id'],))
        account=connection.fetchone()
        return render_template('staff.html', username=session['username'], account = account)
    return redirect(url_for('login'))