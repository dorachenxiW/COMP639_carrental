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
        sql='SELECT * FROM user WHERE userid = %s;'
        connection.execute(sql, (session['id'],))
        account = connection.fetchone()
        # Check what role it is and direct to its profile page
        if account[4] == 'customer':
            sql1='SELECT * FROM user LEFT JOIN customer ON user.userid = customer.userid WHERE user.userid = %s;'
            connection.execute(sql1, (session['id'],))
            account1=connection.fetchone()
            # Show the profile page with account info
            return render_template('profile.html', account=account1)
        elif account[4] == 'staff':
            sql2='SELECT * FROM user LEFT JOIN staff ON user.userid = staff.userid WHERE user.userid = %s;'
            connection.execute(sql2, (session['id'],))
            account2=connection.fetchone()
            return render_template('profile_staff.html', account=account2)
        elif account[4] =='admin':
            sql2='SELECT * FROM user LEFT JOIN staff ON user.userid = staff.userid WHERE user.userid = %s;'
            connection.execute(sql2, (session['id'],))
            account2=connection.fetchone()
            return render_template('profile_admin.html', account=account2)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/profile/edit', methods=['GET','POST'])
def editprofile():
    if 'loggedin' in session:
        connection = getCursor()
        sql='SELECT * FROM user WHERE userid = %s;'
        connection.execute(sql, (session['id'],))
        account = connection.fetchone()
        if account[4] == 'customer':
            sql1='SELECT * FROM user LEFT JOIN customer ON user.userid = customer.userid WHERE user.userid = %s;'
            connection.execute(sql1, (session['id'],))
            account1=connection.fetchone()
            return render_template('editprofile.html', account=account1)
        #Get the info from the table user join table customer
        elif account[4] == 'staff':
            sql2='SELECT * FROM user LEFT JOIN staff ON user.userid = staff.userid WHERE user.userid = %s;'
            connection.execute(sql2, (session['id'],))
            account2=connection.fetchone()
            return render_template('editprofile_staff.html', account=account2)
        elif account[4] == 'admin':
            sql2='SELECT * FROM user LEFT JOIN staff ON user.userid = staff.userid WHERE user.userid = %s;'
            connection.execute(sql2, (session['id'],))
            account2=connection.fetchone()
            return render_template('editprofile_admin.html', account=account2)
    return redirect(url_for('login'))

@app.route('/profile/edit/update', methods=['GET','POST'])
def updateprofile():
    if 'loggedin' in session:
        # Get the updated info from the form
        username=request.form.get('username')
        #print(username)
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        address=request.form.get('address')
        phone=request.form.get('phone')
        email=request.form.get('email')
        connection = getCursor()
        # Update the user table now 
        connection.execute('UPDATE user SET username=%s, email=%s WHERE userid=%s;', (username, email, session['id'],))
        # Get account information in order to check the role of the user 
        sql='SELECT * FROM user WHERE userid = %s;'
        connection.execute(sql, (session['id'],))
        account=connection.fetchone()
        if account[4]=='customer':
            # Update the customer table now 
            connection.execute('UPDATE customer SET firstname=%s, lastname=%s, address=%s, phone=%s WHERE userid=%s;', (firstname, lastname, address, phone, session['id'], ))
            return redirect(url_for('profile'))
        elif account[4]=='staff' or account[4] == 'admin':
            connection.execute('UPDATE staff SET firstname=%s, lastname=%s, address=%s, phone=%s WHERE userid=%s;', (firstname, lastname, address, phone, session['id'], ))
            # update the staff table now
            return redirect(url_for('profile'))
    return redirect(url_for('login'))

# change password for users
@app.route('/profile/changepassword', methods=['POST'])
def changepassword():
    if 'loggedin' in session:
        connection=getCursor()
        sql='SELECT * FROM user WHERE userid = %s;'
        connection.execute(sql, (session['id'],))
        account=connection.fetchone()
        if account[4]=='customer':
            return render_template('changepassword_customer.html')
        elif account[4]=='staff':
            return render_template('changepassword_staff.html')
        elif account[4] == 'admin':
            return render_template('changepassword_admin.html')
    return redirect(url_for('login'))

@app.route('/profile/changepassword/update', methods=['GET','POST'])
def updatepassword():
    if 'loggedin' in session:
        # Get the new password from the form
        newpassword=request.form.get('newpassword')
        # Bcrypt the password
        hashed_newpassword = bcrypt.hashpw(newpassword.encode('utf-8'), bcrypt.gensalt())
        # Connect to db and update the user table
        connection = getCursor()
        connection.execute('UPDATE user SET password=%s WHERE userid=%s;', (hashed_newpassword, session['id'],))
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
        return render_template('staffhome.html', username=session['username'])
    return redirect(url_for('login'))

# view customers from the staff page 
@app.route('/staff/viewcustomers')
def viewcustomers():
    if 'loggedin' in session:
        # connect to db to get customer info
        connection=getCursor()
        sql='SELECT * FROM user LEFT JOIN customer on user.userid = customer.userid WHERE role = "customer";'
        connection.execute(sql)
        customerList=connection.fetchall()
        return render_template('viewcustomers.html', username=session['username'], customerlist=customerList)
    return redirect(url_for('login'))

# view and manage cars from the staff page
@app.route('/staff/managecars')
def managecars():
    if 'loggedin' in session:
        #connect to db to get car info
        connection = getCursor()
        sql_car='SELECT * FROM car;'
        connection.execute(sql_car)
        carList=connection.fetchall()
        # Get account info to direct different user to different template
        sql_user='SELECT * FROM user WHERE userid = %s;'
        connection.execute(sql_user, (session['id'],))
        account=connection.fetchone()
        if account[4]=='staff':
            return render_template('managecars.html', username=session['username'], carlist=carList)
        elif account[4]=='admin':
            return render_template('managecars_admin.html', username=session['username'], carlist=carList)
    return redirect(url_for('login'))

# Add car from the staff car management page or admin page
@app.route('/staff/managecars/add', methods=['POST'])
def addcar():
    if 'loggedin' in session:
        connection = getCursor()
        sql_user='SELECT * FROM user WHERE userid = %s;'
        connection.execute(sql_user, (session['id'],))
        account=connection.fetchone()
        if account[4]=='staff':
            return render_template('addcar.html')
        elif account[4]=='admin':
            return render_template('addcar_admin.html')
    return redirect(url_for('login'))

@app.route('/staff/managecars/add/update', methods=['GET','POST'])
def update_addcar():
    if 'loggedin' in session:
        # Get the car details from the form
        numberplate=request.form.get('numberplate')
        model=request.form.get('model')
        seatingcapacity=request.form.get('seatingcapacity')
        year=request.form.get('year')
        status=request.form.get('status')
        rentalperday=request.form.get('rentalperday')
        # Connect to db and update the info above into the db
        connection=getCursor()
        sql='INSERT INTO car (numberplate, model, seatingcapacity, year, status,rentalperday) VALUES (%s, %s, %s, %s, %s, %s);'
        connection.execute(sql, (numberplate, model, seatingcapacity, year, status, rentalperday,))
        return redirect(url_for('managecars'))
    return redirect(url_for('login'))

# Update car info from the staff car management page 
@app.route('/staff/managecars/edit', methods=['GET','POST'])
def editcar():
    if 'loggedin' in session:
        # Get carid from the hidden input within the form to decide which car is edited 
        carid=request.form.get('carid')
        # Connect to db to get the car info with the carid above
        connection=getCursor()
        sql='SELECT * FROM car WHERE carid=%s;'
        connection.execute(sql, (carid,))
        car=connection.fetchone()
        sql_user='SELECT * FROM user WHERE userid = %s;'
        connection.execute(sql_user, (session['id'],))
        account=connection.fetchone()
        if account[4]=='staff':
            return render_template('editcar.html', car = car)
        elif account[4]=='admin':
            return render_template('editcar_admin.html', car = car)
    return redirect(url_for('login'))

@app.route('/staff/managecars/edit/update', methods=['GET','POST'])
def update_editcar():
    if 'loggedin' in session:
        carid=request.form.get('carid')
        numberplate=request.form.get('numberplate')
        model=request.form.get('model')
        seatingcapacity=request.form.get('seatingcapacity')
        year=request.form.get('year')
        status=request.form.get('status')
        rentalperday=request.form.get('rentalperday')
        connection=getCursor()
        sql='UPDATE car SET numberplate=%s, model=%s, seatingcapacity=%s, year=%s, status=%s,rentalperday=%s WHERE carid=%s;'
        connection.execute(sql, (numberplate, model, seatingcapacity, year, status, rentalperday, carid,))
        return redirect(url_for('managecars'))
    return redirect(url_for('login'))

# Delete car from the staff car management page 
@app.route('/staff/managecars/delete', methods=['GET','POST'])
def deletecar():
    if 'loggedin' in session:
        #msg=''
        carid=request.form.get('carid')
        connection=getCursor()
        sql='DELETE FROM car WHERE carid=%s;'
        connection.execute(sql,(carid,))
        #msg='You have sucessfully deleted the car!'
        return redirect(url_for('managecars'))
    return redirect(url_for('login'))

#http://locoalhost:5000/admin/ -- this is the admin page.
@app.route('/admin')
def admin():
    if 'loggedin' in session:
        return render_template('adminhome.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/admin/managecustomers')
def managecustomers():
    if 'loggedin' in session:
        connection=getCursor()
        sql_customer='SELECT * FROM user LEFT JOIN customer ON user.userid = customer.userid WHERE role="customer";'
        connection.execute(sql_customer)
        customerList=connection.fetchall()
        return render_template('managecustomers.html',customerlist=customerList)
    return redirect(url_for('login'))

@app.route('/admin/managecustomers/add', methods=['POST'])
def addcustomer():
    if 'loggedin' in session:
        return render_template('addcustomer.html')
    return redirect(url_for('login'))

@app.route('/admin/managecustomers/add/update', methods=['GET','POST'])
def updatecustomer():
    if 'loggedin' in session:
        username=request.form.get('username')
        password=request.form.get('password')
        hashedpd= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        email=request.form.get('email')
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        phone=request.form.get('phone')
        address=request.form.get('address')

        connection=getCursor()
        sql1='INSERT INTO user (username, password, email, role) VALUES (%s, %s, %s, %s);'
        connection.execute(sql1,(username, hashedpd, email,'customer',))
        connection.execute('SELECT * FROM user WHERE username = %s', (username,))
        newuser=connection.fetchall()
        newuserid=newuser[0][0]
        sql2='INSERT INTO customer (userid, firstname, lastname, phone, address) VALUES (%s, %s, %s, %s, %s);'
        connection.execute(sql2,(newuserid, firstname, lastname, phone, address,))
        return redirect(url_for('managecustomers'))
    return redirect(url_for('login'))

@app.route('/admin/managecustomers/edit', methods=['GET','POST'])
def editcustomer():
    if 'loggedin' in session:
        # Get userid from the hidden input within the form to decide which customer is edited 
        userid=request.form.get('userid')
        # Connect to db to get the customer info with the userid above
        connection=getCursor()
        sql_customer='SELECT * FROM user LEFT JOIN customer ON user.userid = customer.userid WHERE user.userid=%s;'
        connection.execute(sql_customer, (userid,))
        customer=connection.fetchone()
        return render_template('editcustomer.html', customer=customer)
    return redirect(url_for('login'))

@app.route('/staff/managecustomers/edit/update', methods=['GET','POST'])
def update_editcustomer():
    if 'loggedin' in session:
        userid=request.form.get('userid')
        username=request.form.get('username')
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        email=request.form.get('email')
        phone=request.form.get('phone')
        address=request.form.get('address')
        connection=getCursor()
        sql_user='UPDATE user SET username=%s, email=%s WHERE userid=%s;'
        sql_customer='UPDATE customer SET firstname=%s, lastname=%s,phone=%s, address=%s WHERE userid=%s;'
        connection.execute(sql_user, (username,email, userid,))
        connection.execute(sql_customer, (firstname, lastname, phone, address, userid,))
        return redirect(url_for('managecustomers'))
    return redirect(url_for('login'))

@app.route('/admin/managecustomers/delete', methods=['GET','POST'])
def deletecustomer():
    if 'loggedin' in session:
        userid=request.form.get('userid')
        connection=getCursor()
        sql_user='DELETE FROM user WHERE userid=%s'
        sql_customer='DELETE FROM customer WHERE userid=%s;'
        connection.execute(sql_customer,(userid,))
        connection.execute(sql_user,(userid,))
        return redirect(url_for('managecustomers'))
    return redirect(url_for('login'))


@app.route('/admin/managestaff', methods=['GET','POST'])
def managestaff():
    if 'loggedin' in session:
        connection=getCursor()
        sql_staff='SELECT * FROM user LEFT JOIN staff ON user.userid = staff.userid WHERE role="staff" or role="admin";'
        connection.execute(sql_staff)
        staffList=connection.fetchall()
        return render_template('managestaff.html', stafflist=staffList)
    return redirect(url_for('login'))


# Add staff from admin page 
@app.route('/admin/managestaff/add', methods=['POST'])
def addstaff():
    if 'loggedin' in session:
        return render_template('addstaff.html')
    return redirect(url_for('login'))

@app.route('/admin/managestaff/add/update', methods=['GET','POST'])
def updatestaff():
    if 'loggedin' in session:
        username=request.form.get('username')
        email=request.form.get('email')
        role=request.form.get('role')
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        phone=request.form.get('phone')
        address=request.form.get('address')
        password=request.form.get('password')
        hashedpd= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        connection=getCursor()
        sql1='INSERT INTO user (username, password, email, role) VALUES (%s, %s, %s, %s);'
        connection.execute(sql1,(username, hashedpd, email, role,))
        connection.execute('SELECT * FROM user WHERE username = %s', (username,))
        newuser=connection.fetchall()
        newuserid=newuser[0][0]
        sql2='INSERT INTO staff (userid, firstname, lastname, phone, address) VALUES (%s, %s, %s, %s, %s);'
        connection.execute(sql2,(newuserid, firstname, lastname, phone, address,))
        return redirect(url_for('managestaff'))
    return redirect(url_for('login'))

@app.route('/admin/managestaff/edit', methods=['GET','POST'])
def editstaff():
    if 'loggedin' in session:
        # Get userid from the hidden input within the form to decide which car is edited 
        userid=request.form.get('userid')
        # Connect to db to get the car info with the userid above
        connection=getCursor()
        sql_staff='SELECT * FROM user LEFT JOIN staff ON user.userid = staff.userid WHERE user.userid=%s;'
        connection.execute(sql_staff, (userid,))
        staff=connection.fetchone()
        return render_template('editstaff.html', staff=staff)
    return redirect(url_for('login'))

@app.route('/staff/managestaff/edit/update', methods=['GET','POST'])
def update_editstaff():
    if 'loggedin' in session:
        userid=request.form.get('userid')
        username=request.form.get('username')
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        email=request.form.get('email')
        phone=request.form.get('phone')
        address=request.form.get('address')
        connection=getCursor()
        sql_user='UPDATE user SET username=%s, email=%s WHERE userid=%s;'
        sql_staff='UPDATE staff SET firstname=%s, lastname=%s,phone=%s, address=%s WHERE userid=%s;'
        connection.execute(sql_user, (username,email, userid,))
        connection.execute(sql_staff, (firstname, lastname, phone, address, userid,))
        return redirect(url_for('managestaff'))
    return redirect(url_for('login'))

# Delete staff from the admin managestaff page 
@app.route('/admin/managestaff/delete', methods=['GET','POST'])
def deletestaff():
    if 'loggedin' in session:
        userid=request.form.get('userid')
        connection=getCursor()
        sql_user='DELETE FROM user WHERE userid=%s'
        sql_staff='DELETE FROM staff WHERE userid=%s;'
        connection.execute(sql_staff,(userid,))
        connection.execute(sql_user,(userid,))
        return redirect(url_for('managestaff'))
    return redirect(url_for('login'))
    
