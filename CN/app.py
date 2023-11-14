from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import random
from datetime import datetime
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
#configure mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'tm4628948@gmail.com'
app.config['MAIL_PASSWORD'] = 'qlrr njzt fezv wfiy'


# Configure db
db = yaml.safe_load(open('/Users/harendra/github/CN/db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

mail = Mail(app)


def sendMail(subject, email, recipient, body):
    msg = Message(subject, sender = email, recipients=[recipient])
    msg.body = body
    mail.send(msg)

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
        userDetails = sorted(userDetails, key=lambda x: x[0], reverse=True)
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
        userDetails = sorted(userDetails, key=lambda x: x[0], reverse=True)
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
        userDetails = sorted(userDetails, key=lambda x: x[0], reverse=True)
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
        userDetails = sorted(userDetails, key=lambda x: x[0], reverse=True)
    return render_template('rrequests.html',  userDetails = userDetails)

@app.route('/rreqmanagement', methods = ['GET', 'POST'])
def showuserAuthR():
    if request.method == 'GET':
        st = "Rejected"
        cur  = mysql.connection.cursor()
        query = "SELECT * from requestsAuth WHERE status = %s"
        resultvalue = cur.execute(query, (st))
        if(resultvalue > 0):
            userDetails =  cur.fetchall()
        else:
            userDetails = {"------------"}
        userDetails = sorted(userDetails, key=lambda x: x[0], reverse=True)
    return render_template('rreqmanagement.html',  userDetails = userDetails)

@app.route('/areqmanagement', methods = ['GET', 'POST'])
def showuserAuthA():
    if request.method == 'GET':
        st = "Approved"
        cur  = mysql.connection.cursor()
        query = "SELECT * from requestsAuth WHERE status = %s"
        resultvalue = cur.execute(query, (st))
        if(resultvalue > 0):
            userDetails =  cur.fetchall()
        else:
            userDetails = {"------------"}
        userDetails = sorted(userDetails, key=lambda x: x[0], reverse=True)
    return render_template('areqmanagement.html',  userDetails = userDetails)

@app.route('/preqmanagement', methods = ['GET', 'POST'])
def showuserAuthP():
    if request.method == 'GET':
        st = "Pending"
        cur  = mysql.connection.cursor()
        query = "SELECT * from requestsAuth WHERE status = %s"
        resultvalue = cur.execute(query, (st))
        if(resultvalue > 0):
            userDetails =  cur.fetchall()
        else:
            userDetails = {"------------"}
        userDetails = sorted(userDetails, key=lambda x: x[0], reverse=True)
    return render_template('preqmanagement.html',  userDetails = userDetails)

@app.route('/generateRequest', methods = ['GET', 'POST'])
def addrequest():
    if request.method == 'POST':
        number = request.form.get("number")
        nameOfPersonTravelling = request.form.get("nameOfPersonTravelling") 
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
        query = "INSERT INTO requests (username, usertype, guestName, contactNum, departureFrom, departureTo, departureTiming, departureDate, Capacity, Reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (username, usertype, nameOfPersonTravelling, number, departureFrom, departureTo, departureTiming, departureDate, Capacity, Reason))
        print("Success !")
        flash("Requested!!")
        mysql.connection.commit() 
        cur.close()
    return render_template('request.html')

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect('/')

@app.route('/sr', methods = ['GET'])
def sr():
    return render_template('sr.html')

@app.route('/otp', methods = ['GET', 'POST'])
def otp():
    if request.method == 'POST':
        otp = int(request.form.get("otp"))
        cur = mysql.connection.cursor()
        que = "SELECT * FROM tempUsers WHERE username = %s;"
        un = session.get('usname')
        print("otp username ", un)
        cur.execute(que, un)
        lst = cur.fetchone()
        if cur.rowcount == 0:
            return redirect('signIN')
        q = "DELETE FROM tempUsers WHERE username = %s;"
        cur.execute(q, (un))
        mysql.connection.commit() 
        print("list ", lst)
        print("in otp", otp, lst[6])
        if(otp == int(lst[6])):
            query = "INSERT INTO newUsers (fullName, userType, Contact, EmailID, username, pwd) VALUES (%s, %s, %s, %s, %s, %s);"
            cur.execute(query, (lst[0], lst[1], lst[2], lst[3], lst[4], lst[5]))
            if cur.rowcount == 0:
                return redirect('/')
            query1 = "INSERT INTO login (userID, pwd) VALUES (%s, %s)"
            cur.execute(query1, (lst[4], lst[5]))
            if cur.rowcount > 0:
                print("Success !")
                flash("Successfully Registered.")
                mysql.connection.commit() 
                cur.close()
                return redirect('/sr')
            else:
                return redirect('/signIN')
        else:
            flash("Incorrect OTP.")
            redirect('/otp')
    return render_template('otp.html')

@app.route('/signIN', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        fullName = request.form.get("name") 
        userType = request.form.get("usertype")
        number = request.form.get("number") 
        email = request.form.get("email")  
        username = request.form.get("username")
        password = request.form.get("password").encode('utf-8')
        cur = mysql.connection.cursor()
        checkQuery = "SELECT * FROM login WHERE userID = %s"
        cur.execute(checkQuery, (username))
        existingUser = cur.fetchone()
        if existingUser != None:
            flash("User name already exists in IITGN database.")
            return redirect('/signIN')
        o_otp = random.randint(100000, 999999)
        query = "INSERT INTO tempUsers (fullName, userType, Contact, EmailID, username, pwd, otp) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cur.execute(query, (fullName, userType, number, email, username, password, str(o_otp)))
        mysql.connection.commit() 
        if cur.rowcount == 0:
            print("Failure")
        if cur.rowcount > 0:
            print("Success in storege of tempUser")
        subject = 'OTP for IITGN Transport Management'
        recipient = email
        head = "Dear Sir/Ma'am,\n\n"
        body = 'Your one-time password is: ' + str(o_otp)
        signature = "\n\nBest regards,\nIITGN Transport Management Team\nContact No. 9456723723"
        bodY = f"{head}{body}{signature}"
        sendMail(subject, 'tm4628948@gmail.com', recipient, bodY)
        session['usname'] = username
        cur.close()
        return redirect('/otp')
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

@app.route('/authlogin', methods = ['GET', 'POST'])
def loginauth():
    if request.method == 'POST':
        username = request.form.get("username") 
        password = request.form.get("password").encode('utf-8')
        print(username, password)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM authlogin WHERE userID = %s", (username))
        user = cur.fetchone()
        cur.close()
        print(user)

        if user:
            passcode = user[1].encode('utf-8')

            if password == passcode:
                print("YES")
                session['user_name'] = user[0]
                return redirect('/authHome')
            else:
                return redirect('/authlogin')
        else:
            return redirect('/authlogin')

    return render_template('authlogin.html')

@app.route('/authHome', methods = ['GET', 'POST'])
def show_auth():
    if request.method == 'GET':
        cur  = mysql.connection.cursor()
        resultvalue = cur.execute("SELECT * from requestsAuth")
        if(resultvalue > 0):
            userDetails =  cur.fetchall()
        else:
            userDetails= {"----------"}
        # print(userDetails)
        userDetails = sorted(userDetails, key=lambda x: x[0], reverse=True)
    return render_template('authHome.html',  userDetails = userDetails)


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
        userDetails = sorted(userDetails, key=lambda x: x[0], reverse=True)
        return render_template('adminhome.html',  userDetails = userDetails)

@app.route('/get_remarks/<int:request_id>')
def get_remarks(request_id):
    cur  = mysql.connection.cursor()
    query = "SELECT * from requests WHERE requestID = %s;"
    quer = "SELECT * from requestsAuth WHERE requestID = %s;"
    cur.execute(query, (request_id))
    details = cur.fetchall()
    lis = []
    print(details)
    for row in details:
        new_ls = []
        qnew = "SELECT * FROM requestAprAdminDT WHERE requestID = %s;"
        cur.execute(qnew, (request_id))
        q = cur.fetchone()
        new_ls.append(row[-2])
        new_ls.append(row[-3])
        new_ls.append(row[-1])
        if q:
            new_ls.append(q[-1])
        else:
            new_ls.append(' ')
        lis.append(new_ls)
        print(new_ls)

    print(lis)
    cur.execute(quer, (request_id))
    details = cur.fetchall()
    print(details)
    for row in details:
        new_ls = []
        qnew = "SELECT * FROM requestAprAuthDT WHERE requestID = %s;"
        cur.execute(qnew, (request_id))
        q = cur.fetchone()
        new_ls.append(row[-2])
        new_ls.append(row[-3])
        new_ls.append(row[-1])
        if q:
            new_ls.append(q[-1])
        else:
            new_ls.append(' ')
        lis.append(new_ls)
        print(new_ls)
    cur.close()
    print(lis)
    return jsonify(lis)

@app.route('/get_profile/<string:username>', methods = ['GET'])
def get_profile(username):
    cur  = mysql.connection.cursor()
    query = "SELECT * from newUsers WHERE username = %s;"
    cur.execute(query, (username))
    details = cur.fetchone()

    return jsonify(details[:4])


@app.route('/updaterequest', methods = ['GET', 'POST'])
def updataRequestAdmin():
    if request.method == 'POST':
        cur  = mysql.connection.cursor()
        # data = request.form
        st = request.form.get('status')
        remarks = request.form.get('remarks')
        rid = request.form.get('requestID')
        apby = request.form.get('apby')
        q = "SELECT * FROM requestAprAdminDT where requestID = %s"
        cur.execute(q, (rid))
        qt = cur.fetchone()
        print(qt)
        current_datetime = datetime.now()
        dateNtime = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
        if qt:
            qnew = "UPDATE requestAprAdminDT SET approvedBy = %s, dateNtime = %s WHERE requestID = %s;"
            cur.execute(qnew, (apby, dateNtime, rid))
            mysql.connection.commit()
        else:
            qnew = "INSERT INTO requestAprAdminDT (requestID, approvedBy, dateNtime) VALUES (%s, %s, %s);"
            cur.execute(qnew, (rid, apby, dateNtime))
            mysql.connection.commit()
        query = "UPDATE requests SET status = %s, reasonToCancel = %s, approvedBy = %s WHERE requestID = %s;"
        cur.execute(query, (st, remarks, apby, rid))
        mysql.connection.commit() 
        ert = "SELECT * FROM requests WHERE requestID = %s;"
        cur.execute(ert, (rid))
        res = cur.fetchone()
        print(res)
        username = res[1]
        query = "SELECT * from newUsers WHERE username = %s"
        cur.execute(query, (username))
        resultvalue = cur.fetchone()
        print("rval ", resultvalue)
        rmail = resultvalue[3]
        subject = 'IITGN Transport Management'
        recipient = rmail
        head = "Dear Sir/Ma'am,\n\n"
        status = "Status: "
        by = "By: "

        body = f"{status}{st}\n{by}{apby}\n{remarks}"  
        signature = "\n\nBest regards,\nIITGN Transport Management Team\nContact No. 9456723723"
        bodY = f"{head}{body}{signature}"

        sendMail(subject, 'tm4628948@gmail.com', recipient, bodY)

        if st == 'Approved':
            f_query = "SELECT * FROM requests WHERE requestID = %s"
            cur.execute(f_query, (rid))
            ro = cur.fetchall()
            row = ro[0]
            print("row data  ", row)
            quer = "INSERT INTO requestsAuth (requestID, username, usertype, guestName, contactNum, departureFrom, departureTo, departureTiming, departureDate, Capacity, Reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(quer, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
            mysql.connection.commit()
        cur.close()
        print(st, remarks, rid, apby)
    return redirect('/adminHome')


@app.route('/updaterequestauth', methods = ['GET', 'POST'])
def updateRequestAuth():
    if request.method == 'POST':
        cur  = mysql.connection.cursor()
        # data = request.form
        st = request.form.get('status')
        remarks = request.form.get('remarks')
        rid = request.form.get('requestID')
        apby = request.form.get('apby')
        q = "SELECT * FROM requestAprAuthDT where requestID = %s"
        cur.execute(q, (rid))
        qt = cur.fetchone()
        print(qt)
        current_datetime = datetime.now()
        dateNtime = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
        if qt:
            qnew = "UPDATE requestAprAuthDT SET approvedBy = %s, dateNtime = %s WHERE requestID = %s;"
            cur.execute(qnew, (apby, dateNtime, rid))
            mysql.connection.commit()
        else:
            qnew = "INSERT INTO requestAprAuthDT (requestID, approvedBy, dateNtime) VALUES (%s, %s, %s);"
            cur.execute(qnew, (rid, apby, dateNtime))
            mysql.connection.commit()
        query = "UPDATE requestsAuth SET status = %s, remarks = %s, approvedBy = %s WHERE requestID = %s;"
        cur.execute(query, (st, remarks, apby, rid))
        mysql.connection.commit() 
        print(st, remarks, rid, apby)
        ert = "SELECT * FROM requestsAuth WHERE requestID = %s;"
        cur.execute(ert, (rid))
        res = cur.fetchone()
        print(res)
        username = res[1]
        query = "SELECT * from newUsers WHERE username = %s"
        cur.execute(query, (username))
        resultvalue = cur.fetchone()
        print("rval ", resultvalue)
        rmail = resultvalue[3]
        cur.close()
        subject = 'IITGN Transport Management'
        recipient = rmail
        head = "Dear Sir/Ma'am,\n\n"
        status = "Status: "

        body = f"{status}{st}\n{remarks}"  
        signature = "\n\nBest regards,\nIITGN Transport Management Team\nContact No. 9456723723"
        bodY = f"{head}{body}{signature}"

        sendMail(subject, 'tm4628948@gmail.com', recipient, bodY)
    return redirect('/authHome')


if __name__ == '__main__':
    app.run(debug=True, use_reloader = True)
