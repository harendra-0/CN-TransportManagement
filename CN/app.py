from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
# Configure db
db = yaml.safe_load(open('/Users/harendra/github/CN/db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username") 
        password = request.form.get("password").encode('utf-8')
        print(username, password)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login WHERE userID = %s", (username))
        user = cur.fetchone()
        cur.close()
        print(user)

        if user:
            passcode = user[1].encode('utf-8')

            if password == passcode:
                print("YES")
                session['user_name'] = user[0]
                return redirect('/user')
            else:
                flash('Invalid username or password.')
                return redirect('/')
        else:
            flash('User not regiserterd with IITGN.')
            return redirect('/')

    return render_template('index.html')

@app.route('/adminLogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form.get("username") 
        password = request.form.get("password").encode('utf-8')
        print(username, password)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM adminlogin WHERE userID = %s", (username))
        user = cur.fetchone()
        cur.close()
        print(user)

        if user:
            passcode = user[1].encode('utf-8')

            if password == passcode:
                print("YES")
                session['user_name'] = user[0]
                return redirect('/adminHome')
            else:
                flash('Invalid username or password.')
                return redirect('/')
        else:
            flash('User not regiserterd with IITGN.')
            return redirect('/')

    return render_template('adminLogin.html')

@app.route('/user', methods = ['GET', 'POST'])
def showuser():
    if request.method == 'GET':
        username = session.get('user_name')
        cur  = mysql.connection.cursor()
        query = "SELECT * from requests WHERE username = %s"
        resultvalue = cur.execute(query, (username))
        if(resultvalue > 0):
            userDetails =  cur.fetchall()
        else:
            userDetails = {"------------"}
    return render_template('user.html',  userDetails = userDetails)

@app.route('/arequests', methods = ['GET', 'POST'])
def showuserA():
    if request.method == 'GET':
        st = "Approved"
        cur  = mysql.connection.cursor()
        query = "SELECT * from requests WHERE status = %s"
        resultvalue = cur.execute(query, (st))
        if(resultvalue > 0):
            userDetails =  cur.fetchall()
        else:
            userDetails = {"------------"}
    return render_template('arequests.html',  userDetails = userDetails)

@app.route('/prequests', methods = ['GET', 'POST'])
def showuserP():
    if request.method == 'GET':
        st = "Pending"
        cur  = mysql.connection.cursor()
        query = "SELECT * from requests WHERE status = %s"
        resultvalue = cur.execute(query, (st))
        if(resultvalue > 0):
            userDetails =  cur.fetchall()
        else:
            userDetails = {"------------"}
    return render_template('prequests.html',  userDetails = userDetails)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    cur  = mysql.connection.cursor()
    username = session.get('user_name')
    query = "SELECT * from newUsers WHERE username = %s"
    resultvalue = cur.execute(query, (username))
    if(resultvalue > 0):
        userDetails =  cur.fetchall()
    else:
        userDetails = {"------------"}
    return render_template('profile.html',  userDetails = userDetails)

@app.route('/rrequests', methods = ['GET', 'POST'])
def showuserR():
    if request.method == 'GET':
        st = "Rejected"
        cur  = mysql.connection.cursor()
        query = "SELECT * from requests WHERE status = %s"
        resultvalue = cur.execute(query, (st))
        if(resultvalue > 0):
            userDetails =  cur.fetchall()
        else:
            userDetails = {"------------"}
    return render_template('rrequests.html',  userDetails = userDetails)

@app.route('/generateRequest', methods = ['GET', 'POST'])
def addrequest():
    if request.method == 'POST':
        departureFrom = request.form.get("departureFrom")
        departureTo = request.form.get("departureTo") 
        departureTiming = request.form.get("timing")  
        Capacity = request.form.get("capacity")
        departureDate = request.form.get("date")
        Reason = request.form.get("reason")
        username = session.get('user_name')
        cur = mysql.connection.cursor()
        query = "SELECT * from newUsers WHERE username = %s"
        resultvalue = cur.execute(query, (username))
        userDetails =  cur.fetchall()
        print(userDetails)
        usertype = userDetails[0][1]
        print(departureFrom, Reason)
        # INSERT INTO requests (username, usertype, departureFrom, departureTo, departureTiming, departureDate, Capacity, Reason)
        # VALUES ('manpreet.singh', 'Visitor', 'Motera', 'IIT Gandhinagar', '11:00PM', '2023-11-10', 1, 'Urgent');
        query = "INSERT INTO requests (username, usertype, departureFrom, departureTo, departureTiming, departureDate, Capacity, Reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (username, usertype, departureFrom, departureTo, departureTiming, departureDate, Capacity, Reason))
        print("Success !")
        flash("Requested!!")
        mysql.connection.commit() 
        cur.close()
    return render_template('request.html')

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect('/')

@app.route('/signIN', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        fullName = request.form.get("name") 
        userType = request.form.get("usertype")
        number = request.form.get("number") 
        email = request.form.get("email")  
        username = request.form.get("username")
        password = request.form.get("password").encode('utf-8')
        print(username, password)
        cur = mysql.connection.cursor()
        query = "INSERT INTO newUsers (fullName, userType, Contact, EmailID, username, pwd) VALUES (%s, %s, %s, %s, %s, %s)"
        checkQuery = "SELECT * FROM login WHERE userID = %s"
        cur.execute(checkQuery, (username))
        existingUser = cur.fetchone()
        if existingUser != None:
            flash("User name already exists in IITGN database.")
            return redirect('/signIN')
        cur.execute(query, (fullName, userType, number, email, username, password))
        if cur.rowcount == 0:
            return redirect('/')
        query1 = "INSERT INTO login (userID, pwd) VALUES (%s, %s)"
        cur.execute(query1, (username, password))
        if cur.rowcount > 0:
            print("Success !")
            flash("Successfully resgistered.")
            mysql.connection.commit() 
            cur.close()
        else:
            return redirect('/')
        # print(user)
    return render_template('signIn.html')

@app.route('/adminLogin', methods = ['GET', 'POST'])
def loginAdmin():
    if request.method == 'POST':
        username = request.form.get("username") 
        password = request.form.get("password").encode('utf-8')
        print(username, password)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM adminlogin WHERE userID = %s", (username))
        user = cur.fetchone()
        cur.close()
        print(user)

        if user:
            passcode = user[1].encode('utf-8')

            if password == passcode:
                print("YES")
                session['user_name'] = user[0]
                return redirect('/results')
            else:
                return redirect('/adminLogin')
        else:
            return redirect('/adminLogin')

    return render_template('adminlogin.html')

@app.route('/adminHome', methods = ['GET', 'POST'])
def show_requests():
    if request.method == 'GET':
        cur  = mysql.connection.cursor()
        resultvalue = cur.execute("SELECT * from requests")
        if(resultvalue > 0):
            userDetails =  cur.fetchall()
        else:
            userDetails= {"----------"}
        # print(userDetails)
        return render_template('adminhome.html',  userDetails = userDetails)

@app.route('/updaterequest', methods = ['GET', 'POST'])
def vnivne():
    if request.method == 'POST':
        cur  = mysql.connection.cursor()
        # data = request.form
        st = request.form.get('status')
        remarks = request.form.get('remarks')
        rid = request.form.get('requestID')
        apby = request.form.get('apby')
        query = "UPDATE requests SET status = %s, reasonToCancel = %s, approvedBy = %s WHERE requestID = %s;"
        cur.execute(query, (st, remarks, apby, rid))
        mysql.connection.commit() 
        cur.close()
        print(st, remarks, rid, apby)
    return redirect('/adminHome')

if __name__ == '__main__':
    app.run(debug=True, use_reloader = True)





