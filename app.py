# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import Flask, render_template, request, jsonify, flash, redirect
import psycopg2  # pip install psycopg2
import psycopg2.extras

app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'
 #postgres://uquscjwofvxyvx:519f6613a42f0ce996e85edb85575458a6e4634fd9272701dd6057844610cb87@ec2-54-147-36-107.compute-1.amazonaws.com:5432/dda7fqt9mrnr8n
mysql = MySQL(app)

# @app.route('/',methods =['GET', 'POST'])


@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'role' in request.form:
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s AND role= %s', (username, password,role ))
        user = cursor.fetchone()
        if user:            
            if user['role'] == 'admin':
                    session['loggedin'] =True
                    #session['id'] = user['id']
                    session['username'] = user['username']
                    session['password'] = user['password']
                    mesage = 'Logged in successfully !'
                    return redirect(url_for('admin'))
                
                
            elif user['role'] == 'andwemedia':
                session['loggedin'] = True
                #session['id'] = user['id']
                session['username'] = user['username']
                session['password'] = user['password']
                mesage = 'Logged in successfully !'
                return redirect(url_for('today',mesage=mesage))
            
            elif user['role'] == 'viw3d':
                session['loggedin'] = True
                #session['id'] = user['id']
                session['username'] = user['username']
                session['password'] = user['password']
                mesage = 'Logged in successfully !'
                return redirect(url_for('Indexv',mesage=mesage))
            elif user['role'] == 'micrografix':
                session['loggedin'] = True
                # session['id'] = user['id']
                session['username'] = user['username']
                session['password'] = user['password']
                mesage = 'Logged in successfully !'
                return redirect(url_for('Indexm',mesage=mesage))
            else:
               mesage = 'Only admin can login' 
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
#@app.route('/')
#def logout1():
 #   return render_template('login.html')

@app.route('/')
@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'role' in request.form :
		username = request.form['username']
		password = request.form['password']
		role = request.form['role']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', role):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not role:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username, password,role, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)
# =================================^^^^^^^^^^^^^^^^^^^^^^^^^^^^^================================
#===========================================================================================
#=======================================FOR SUPER ADMIN========================================================
@app.route('/admin')
def admin():
    if 'loggedin'  in session:
        curr=mysql.connection.cursor()
        curr.execute('SELECT * from data where d=curdate()')
        f=curr.fetchall()
        curr.execute('SELECT * from micrografix where md=curdate()')
        m=curr.fetchall()
        curr.execute('SELECT * from viw3d where vd=curdate()')
        v=curr.fetchall()
        curr.close()
        return render_template("admin.html",data=f,micrografix=m,viw3d=v,)
    return redirect(url_for('login'))

#=========================================================================================================
@app.route('/showtask')
def Index():
    if 'loggedin'  in session: 
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM data')
        d=cur.fetchall()
        cur.close()
        return render_template("index.html",data=d)
    else:
        return render_template('login.html')
# ================================================= VIW3D =============================
@app.route('/showtaskviw')
def Indexv():
    if 'loggedin'  in session: 
        curr=mysql.connection.cursor()
        curr.execute('SELECT * from viw3d')
        f=curr.fetchall()
        curr.close()
        return render_template("viwindex.html",viw3d=f)
    else:
        return render_template('login.html')

# ================================================= micrografix =============================
@app.route('/showtaskmicro')
def Indexm():
    if 'loggedin'  in session: 
        mcur=mysql.connection.cursor()
        mcur.execute('SELECT * from micrografix')
        m=mcur.fetchall()
        mcur.close()
        return render_template("microindex.html",micrografix=m)
    else:
        return render_template('login.html')

# ======================this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
        if request.method=='POST':
            if 'loggedin'  in session: 
                name=request.form['name']
                email=request.form['email']
                phone=request.form['phone']
                assign=request.form['assign']
                status=request.form['status']
                d=request.form['d']
                cur=mysql.connection.cursor()
                cur.execute("INSERT INTO data(name,email,phone,assign,status,d) values(%s,%s,%s,%s,%s,%s) ",(name,email,phone,assign,status,d))
                flash('TASK ADDED SUCCESFULLY!')
                mysql.connection.commit()
            return redirect(url_for('Index',data=d))
        else:
            return render_template('login.html')
    #====================================================
    #===========================================================for admin ===============================
@app.route('/adminandwemedia', methods = ['POST'])
def adminandwemedia():
        if request.method=='POST':
            if 'loggedin'  in session:
                name=request.form['name']
                email=request.form['email']
                phone=request.form['phone']
                assign=request.form['assign']
                status=request.form['status']
                d=request.form['d']
                cur=mysql.connection.cursor()
                cur.execute("INSERT INTO data(name,email,phone,assign,status,d) values(%s,%s,%s,%s,%s,%s) ",(name,email,phone,assign,status,d))
                #flash('TASK ADDED SUCCESFULLY!')
                mysql.connection.commit()
            return redirect(url_for('admin',data=d))
        else:
            return render_template('login.html')
    
# ================================================= VIW3D =============================
@app.route('/vinsert', methods = ['POST'])
def vinsert():
        if request.method=='POST':
            if 'loggedin'  in session:
                vname=request.form['vname']
                vemail=request.form['vemail']
                vphone=request.form['vphone']
                vassign=request.form['vassign']
                vstatus=request.form['vstatus']
                vd=request.form['vd']
                cur=mysql.connection.cursor()
                cur.execute("INSERT INTO viw3d(vname,vemail,vphone,vassign,vstatus,vd) values(%s,%s,%s,%s,%s,%s) ",(vname,vemail,vphone,vassign,vstatus,vd))
                flash('TASK ADDED SUCCESFULLY!')
                mysql.connection.commit()
            return redirect(url_for('Indexv',viw3d=vd))
        else:
            return render_template('login.html')  

#=======================================================================
#======================================================= for admin ============================================
@app.route('/adminviw', methods = ['POST'])
def adminviw():
        if request.method=='POST':
            if 'loggedin'  in session:
                vname=request.form['vname']
                vemail=request.form['vemail']
                vphone=request.form['vphone']
                vassign=request.form['vassign']
                vstatus=request.form['vstatus']
                vd=request.form['vd']
                cur=mysql.connection.cursor()
                cur.execute("INSERT INTO viw3d(vname,vemail,vphone,vassign,vstatus,vd) values(%s,%s,%s,%s,%s,%s) ",(vname,vemail,vphone,vassign,vstatus,vd))
           # flash('TASK ADDED SUCCESFULLY!')
                mysql.connection.commit()
            return redirect(url_for('admin',viw3d=vd)) 
        else:
            return render_template('login.html') 
#===================================================MIRCROGRAFIX=============================================================================

@app.route('/minsert', methods = ['POST'])
def minsert():
        if request.method=='POST':
            if 'loggedin'  in session:
                mname=request.form['mname']
                memail=request.form['memail']
                mphone=request.form['mphone']
                massign=request.form['massign']
                mstatus=request.form['mstatus']
                md=request.form['md']
                mcur=mysql.connection.cursor()
                mcur.execute("INSERT INTO micrografix(mname,memail,mphone,massign,mstatus,md) values(%s,%s,%s,%s,%s,%s) ",(mname,memail,mphone,massign,mstatus,md))
                flash('TASK ADDED SUCCESFULLY!')
                mysql.connection.commit()
            return redirect(url_for('Indexm',micrografix=md))
        else:
            return render_template('login.html')  
    
    #=======================================================================
#======================================================= for admin ============================================
@app.route('/adminmicro', methods = ['POST'])
def adminmicro():
        if request.method=='POST':
            if 'loggedin'  in session:
                mname=request.form['mname']
                memail=request.form['memail']
                mphone=request.form['mphone']
                massign=request.form['massign']
                mstatus=request.form['mstatus']
                md=request.form['md']
                mcur=mysql.connection.cursor()
                mcur.execute("INSERT INTO micrografix(mname,memail,mphone,massign,mstatus,md) values(%s,%s,%s,%s,%s,%s) ",(mname,memail,mphone,massign,mstatus,md))
            #flash('TASK ADDED SUCCESFULLY!')
                mysql.connection.commit()
            return redirect(url_for('admin',micrografix=md)) 
        else:
            return render_template('login.html') 
# ================================================================================================================
# this is our update route where we are going to update our task
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method=='POST':
       if 'loggedin'  in session:
        # id=request.form['id']
            id_data=request.form['id']
            name=request.form['name']
            email=request.form['email']
            phone=request.form['phone']
            assign=request.form['assign']
            status=request.form['status']
            d=request.form['d']
            cur=mysql.connection.cursor()
            cur.execute("""
                    UPDATE data set name=%s,email=%s,phone=%s,assign=%s,status=%s,d=%s
                    where id=%s 
                    """,(name,email,phone,assign,status,d,id_data))
            flash('TASK UPDATED SUCCESFULLY!')
            mysql.connection.commit()
            return redirect(url_for('Index'))
    else:
        return render_template('login.html') 
# ================================================= VIW3D =============================
# this is our update route where we are going to update our task
@app.route('/vupdate', methods = ['GET', 'POST'])
def vupdate():
  if request.method=='POST':
       if 'loggedin'  in session:
        # id=request.form['id']
        id_viw=request.form['id']
        vname=request.form['vname']
        vemail=request.form['vemail']
        vphone=request.form['vphone']
        vassign=request.form['vassign']
        vstatus=request.form['vstatus']
        vd=request.form['vd']
        curr=mysql.connection.cursor()
        curr.execute("""
                    UPDATE viw3d set vname=%s,vemail=%s,vphone=%s,vassign=%s,vstatus=%s,vd=%s
                    where id=%s 
                    """,(vname,vemail,vphone,vassign,vstatus,vd,id_viw))
        flash('TASK UPDATED SUCCESFULLY!')
        mysql.connection.commit()
        return redirect(url_for('Indexv',viw3d=vd))
       else:
           return render_template('login.html')

# ================================================= MICROGRAFIX =============================
@app.route('/mupdate', methods = ['GET', 'POST'])
def mupdate():
  if request.method=='POST':
      if 'loggedin'  in session:
        # id=request.form['id']
        id_viw=request.form['id']
        mname=request.form['mname']
        memail=request.form['memail']
        mphone=request.form['mphone']
        massign=request.form['massign']
        mstatus=request.form['mstatus']
        md=request.form['md']
        mcur=mysql.connection.cursor()
        mcur.execute("""
                    UPDATE micrografix set mname=%s,memail=%s,mphone=%s,massign=%s,mstatus=%s,md=%s
                    where id=%s 
                    """,(mname,memail,mphone,massign,mstatus,md,id_viw))
        flash('TASK UPDATED SUCCESFULLY!')
        mysql.connection.commit()
        return redirect(url_for('Indexm',micrografix=md))
      else:
          return render_template('login.html')
# ===========================FOR DONE BUTTON=========================    
@app.route('/done/<string:id_data>/', methods = ['POST','GET'])
def done(id_data):
    if 'loggedin'  in session:
        cur=mysql.connection.cursor()
        cur.execute("UPDATE data set status='COMPLETED'  where id=%s ",(id_data,))
        mysql.connection.commit()
        return redirect(url_for('today'))
# ============================================ FOR VIW 3D=================================================
@app.route('/vdone/<string:id_data>/', methods = ['POST','GET'])
def vdone(id_data):
    if 'loggedin' in session:
        curr=mysql.connection.cursor()
        curr.execute("UPDATE viw3d set vstatus='COMPLETED'  where id=%s ",(id_data,))
        mysql.connection.commit()
        return redirect(url_for('vtoday'))
    else:
          return render_template('login.html')

# ================================================= MICROGRAFIX =============================
@app.route('/mdone/<string:id_data>/', methods = ['POST','GET'])
def vmdone(id_data):
    if 'loggedin' in session:
        mcur=mysql.connection.cursor()
        mcur.execute("UPDATE micrografix set mstatus='COMPLETED'  where id=%s ",(id_data,))
        mysql.connection.commit()
        return redirect(url_for('mtoday'))
    else:
        return render_template('login.html')
  # =============================================================================================
# This route is for deleting our task
@app.route('/delete/<string:id_data>/', methods = ['POST','GET'])
def delete(id_data):
    if 'loggedin' in session:
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM data where id=%s ",(id_data,))
        mysql.connection.commit()
        return redirect(url_for('Index'))
    else:
        return render_template('login.html')
#=====================================================================================
#============================FOR ADMIN===================================================
@app.route('/admindelete/<string:id_data>/', methods = ['POST','GET'])
def admindelete(id_data):
    if 'loggedin' in session:
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM data where id=%s ",(id_data,))
        mysql.connection.commit()
        return redirect(url_for('admin'))
    else:
        return render_template('login.html')
# ============================================ FOR VIW 3D=================================================
@app.route('/vdelete/<string:id_data>/', methods = ['POST','GET'])
def vdelete(id_data):
    if 'loggedin' in session:
        curr=mysql.connection.cursor()
        curr.execute("DELETE FROM viw3d where id=%s ",(id_data,))
        mysql.connection.commit()
        return redirect(url_for('Indexv'))
    else:
        return render_template('login.html')

# ================================================= MICROGRAFIX =============================
@app.route('/mdelete/<string:id_data>/', methods = ['POST','GET'])
def mdelete(id_data):
    if 'loggedin' in session:
        mcur=mysql.connection.cursor()
        mcur.execute("DELETE FROM micrografix where id=%s ",(id_data,))
        mysql.connection.commit()
        return redirect(url_for('Indexm'))
    else:
        return render_template('login.html')
# ==========================FOR DATE SEARCH===================================================================
@app.route('/today', methods=['GET','POST'])
def today():
    if 'loggedin' in session:
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM data where  d=curdate() AND (status='IN QUE' OR status='TODAYS TASK' OR status='completed') ")
        d=cur.fetchall()
        v=cur.execute("select count(*) from data where  d=curdate() ")
        v=cur.fetchone()[0]
        cur.execute("UPDATE data set status='TODAYS TASK'  where status='IN QUE' AND d=curdate() ")
        mysql.connection.commit()
        cur.close()
        return render_template("index.html",data=d,tod=v,)
    else:
        return render_template('login.html')
    #======================================= for auto update ================================================================

# ============================================ FOR VIW 3D=================================================
@app.route('/vtoday', methods=['GET','POST'])
def vtoday():
    if 'loggedin' in session:
        curr=mysql.connection.cursor()
        curr.execute("SELECT * FROM viw3d where vstatus='TODAYS TASK' AND vd=curdate()")
        vd=curr.fetchall()
        v=curr.execute("select count(*) from viw3d where vstatus='TODAYS TASK' ")
        v=curr.fetchone()[0]
        curr.execute("UPDATE viw3d set vstatus='TODAYS TASK'  where vstatus='IN QUE' AND vd=curdate() ")
        mysql.connection.commit()
        curr.close()
        return render_template("viwindex.html",viw3d=vd,tod=v)
    else:
        return render_template('login.html')
# ================================================= MICROGRAFIX =============================
@app.route('/mtoday', methods=['GET','POST'])
def mtoday():
    if 'loggedin' in session:
        mcur=mysql.connection.cursor()
        mcur.execute("SELECT * FROM micrografix where mstatus='TODAYS TASK' AND md=curdate()")
        md=mcur.fetchall()
        v=mcur.execute("select count(*) from micrografix where mstatus='TODAYS TASK' ")
        v=mcur.fetchone()[0]
        mcur.execute("UPDATE micrografix set mstatus='TODAYS TASK'  where mstatus='IN QUE' AND md=curdate() ")
        mysql.connection.commit()
        mcur.close()
        return render_template("microindex.html",micrografix=md,tod=v)
    else:
        return render_template('login.html')
# ========================================================

@app.route('/option', methods = ['GET', 'POST'])
def option():
 d=""
 if request.method=='POST':
    if 'loggedin' in session:
        dt=request.form['d']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM data where d LIKE %s",(dt,))
        d=cur.fetchall()
        cur.close()
    return render_template("index.html",data=d)
 else:
    return render_template('login.html')
# ============================================ FOR VIW 3D=================================================

@app.route('/voption', methods = ['GET', 'POST'])
def voption():
 d=""
 if request.method=='POST':
    dt=request.form['vd']
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM viw3d where vd LIKE %s",(dt,))
    vd=cur.fetchall()
    cur.close()
 return render_template("viwindex.html",viw3d=vd)
#====================================================== MICROGRAFIX =========================================
@app.route('/moption', methods = ['GET', 'POST'])
def moption():
 d=""
 if request.method=='POST':
    mt=request.form['md']
    mcur=mysql.connection.cursor()
    mcur.execute("SELECT * FROM micrografix where md LIKE %s",(mt,))
    md=mcur.fetchall()
    mcur.close()
 return render_template("microindex.html",micrografix=md)
# ============================== onchange date  ========================================
@app.route('/t', methods = ['GET', 'POST'])
def t():
 d=""
 if request.method=='POST':
    dt=request.form['d']
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM data where d LIKE %s",(dt,))
    d=cur.fetchall()
    cur.close()
 return render_template("index.html",data=d)
# ============================================ FOR VIW 3D=================================================
@app.route('/vt', methods = ['GET', 'POST'])
def vt():
 vd=""
 if request.method=='POST':
    vt=request.form['vd']
    curr=mysql.connection.cursor()
    curr.execute("SELECT * FROM viw3d where vd LIKE %s",(vt,))
    vd=curr.fetchall()
    curr.close()
 return render_template("viwindex.html",viw3d=vd)
#====================================================== MICROGRAFIX =========================================
@app.route('/mt', methods = ['GET', 'POST'])
def mt():
 md=""
 if request.method=='POST':
    mt=request.form['md']
    mcur=mysql.connection.cursor()
    mcur.execute("SELECT * FROM micrografix where md LIKE %s",(mt,))
    md=mcur.fetchall()
    mcur.close()
 return render_template("microindex.html",micrografix=md)
#=================================================For Admin=====================================================
@app.route('/admint', methods = ['GET', 'POST'])
def admint():
 vd=""
 md=''
 if request.method=='POST':
    admindate=request.form['admindate']
    curr=mysql.connection.cursor()
    curr.execute("SELECT * FROM data where d LIKE %s",(admindate,))
    d=curr.fetchall()
    curr.execute("SELECT * FROM micrografix where md LIKE %s",(admindate,))
    md=curr.fetchall()
    curr.execute("SELECT * FROM viw3d where vd LIKE %s",(admindate,))
    vd=curr.fetchall()
    curr.close()
 return render_template("admin.html",data=d,viw3d=vd,micrografix=md)
# ================TASK STATUS========================================================================

@app.route('/complated',methods=['GET','POST'])
def complated():
    cur=mysql.connection.cursor()
    cur.execute("select * FROM data where status='COMPLETED'")
    d=cur.fetchall()
    v=cur.execute("select count(*) from data where status='COMPLETED' ")
    v=cur.fetchone()[0]
    cur.close()
    return render_template("index.html",data=d,cou=v)
# ============================================ FOR VIW 3D=================================================
@app.route('/vcomplated',methods=['GET','POST'])
def vcomplated():
    cur=mysql.connection.cursor()
    cur.execute("select * FROM viw3d where vstatus='COMPLETED'")
    d=cur.fetchall()
    v=cur.execute("select count(*) from viw3d where vstatus='COMPLETED' ")
    v=cur.fetchone()[0]
    cur.close()
    return render_template("viwindex.html",viw3d=d,cou=v)
#====================================================== MICROGRAFIX =========================================
@app.route('/mcomplated',methods=['GET','POST'])
def mcomplated():
    mcur=mysql.connection.cursor()
    mcur.execute("select * FROM micrografix where mstatus='COMPLETED'")
    d=mcur.fetchall()
    v=mcur.execute("select count(*) from micrografix where mstatus='COMPLETED' ")
    v=mcur.fetchone()[0]
    mcur.close()
    return render_template("microindex.html",micrografix=d,cou=v)
# =======================================================================================================

@app.route('/pending',methods=['GET','POST'])
def pending():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM data where status='PENDING' ")
    d=cur.fetchall()
    cur.close()
    return render_template("index.html",data=d)

@app.route('/inque',methods=['GET','POST'])
def inque():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM data where status='IN QUE' ")
    d=cur.fetchall()
    v=cur.execute("select count(*) from data where status='IN QUE' ")
    v=cur.fetchone()[0]
    u=cur.execute(" update data set status='TODAYS TASK' where d=curdate();")
    u=cur.fetchall()
    cur.close()
    return render_template("index.html", inq=v,data=d,)
# ============================================ FOR VIW 3D=================================================
@app.route('/vinque',methods=['GET','POST'])
def vinque():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM viw3d where vstatus='IN QUE' ")
    d=cur.fetchall()
    v=cur.execute("select count(*) from viw3d where vstatus='IN QUE' ")
    v=cur.fetchone()[0]
    cur.close()
    return render_template("viwindex.html", inq=v,viw3d=d)
#====================================================== MICROGRAFIX =========================================
@app.route('/minque',methods=['GET','POST'])
def minque():
    mcur=mysql.connection.cursor()
    mcur.execute("SELECT * FROM micrografix where mstatus='IN QUE' ")
    md=mcur.fetchall()
    v=mcur.execute("select count(*) from micrografix where mstatus='IN QUE' ")
    v=mcur.fetchone()[0]
    mcur.close()
    return render_template("microindex.html", inq=v,micrografix=md)
# =======================================================================================================

@app.route('/workinprogress',methods=['GET','POST'])
def workinprogress():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM data where status='WORK IN PROGRESS' ")
    d=cur.fetchall()
    cur.close()
    return render_template("index.html",data=d)


@app.route('/dbc',methods=['GET','POST'])
def dbc():
    cur=mysql.connection.cursor()
    cur.execute("select count(*) FROM data where status='COMPLETED'")
    d=cur.fetchall()[0]
    # cur.execute("select count(*) from data where status='COMPLETED'")
    # count_variable=cur.fetchone()
    cur.close()
    return render_template("index.html",data=(d))

@app.route('/dbp',methods=['GET','POST'])
def dbp():
    cur=mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM data where status='PENDING' ")
    d=cur.fetchall()
    cur.close()
    return render_template("dbp.html",data=d)

@app.route('/dbq',methods=['GET','POST'])
def dbq():
    cur=mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM data where status='IN QUE' ")
    d=cur.fetchall()
    cur.close()
    return render_template("dbq.html",data=d)

@app.route('/dbw',methods=['GET','POST'])
def dbw():
    cur=mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM data where status='WORK IN PROGRESS' ")
    d=cur.fetchall()
    cur.close()
    return render_template("dbw.html",data=d)
# ================================For Count today's task================================================================
@app.route('/countcompleted',methods=['GET','POST'])
def count():
    cur=mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM data where d=curdate() ")
    d=cur.fetchall()
    cur.close()
    return render_template("countcompleted.html",data=d)

@app.route('/totaltask',methods=['GET','POST'])
def count1():
    cur=mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM data where d=curdate() ")
    d=cur.fetchall()
    cur.close()
    return render_template("dashboardexample.html",data=d)


# ====================client routing ==================







# This is the index route where we are going to
# query on all our employee data
@app.route('/add',methods=['GET','POST'])
def i():
    if 'loggedin' in session:
        if request.method=='POST':
        
            name=request.form['name']
            email=request.form['email']
            phone=request.form['phone']
            project=request.form['project']
   
            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO data1(name,email,phone,project) values(%s,%s,%s,%s)",(name,email,phone,project))
            mysql.connection.commit()
            return redirect(url_for('allclient',data1=project))
    else:
        return render_template('login.html')
 # ============================================ FOR VIW 3D=================================================  
@app.route('/vadd',methods=['GET','POST'])
def vi():
    if request.method=='POST':
        cname=request.form['cname']
        cemail=request.form['cemail']
        cphone=request.form['cphone']
        cproject=request.form['cproject']
   
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO viwclient(cname,cemail,cphone,cproject) values(%s,%s,%s,%s)",(cname,cemail,cphone,cproject))
        mysql.connection.commit()
        return redirect(url_for('vallclient',viwclient=cproject))
    
    return render_template("vi.html")
# ================================================FOR MICROGRAFIX ===============================================
@app.route('/madd',methods=['GET','POST'])
def mi():
    if request.method=='POST':
        miname=request.form['miname']
        miemail=request.form['miemail']
        miphone=request.form['miphone']
        miproject=request.form['miproject']
   
        mcur=mysql.connection.cursor()
        mcur.execute("INSERT INTO micrografixclient(miname,miemail,miphone,miproject) values(%s,%s,%s,%s)",(miname,miemail,miphone,miproject))
        mysql.connection.commit()
        return redirect(url_for('mallclient',micrografixclient=miproject))
    
    return render_template("microclientindex.html")


# this route is for inserting data to mysql database via html forms
@app.route('/allclient')
def allclient():
    if 'loggedin' in session:
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM data1')
        d=cur.fetchall()
        cur.close()
        return render_template("i.html",data1=d)
    else:
        return render_template('login.html')
 # ===============================================================*********************** FOR VIW3D ============  
@app.route('/vallclient')
def vallclient():
    curr=mysql.connection.cursor()
    curr.execute('SELECT * FROM viwclient')
    cd=curr.fetchall()
    curr.close()
    return render_template("vi.html",viwclient=cd)
# =============================================================== MICROGRAFIX ============  
@app.route('/mallclient')
def mallclient():
    mcur=mysql.connection.cursor()
    mcur.execute('SELECT * FROM micrografixclient')
    cd=mcur.fetchall()
    mcur.close()
    return render_template("microclientindex.html",micrografixclient=cd)


# this is our update route where we are going to update our client
@app.route('/edit', methods = ['GET', 'POST'])
def edit():
  if request.method=='POST':
        # id=request.form['id']
        id_data=request.form['id']
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        project=request.form['project']
        cur=mysql.connection.cursor()
        cur.execute("""
                    UPDATE data1 set name=%s,email=%s,phone=%s,project=%s
                    where id=%s 
                    """,(name,email,phone,project,id_data))
        flash('DATA UPDATED SUCCESFULLY!')
        mysql.connection.commit()
        return redirect(url_for('i'))
  return render_template("i.html",data1=id_data)
# ==============================================================viewclient
@app.route('/clientedit', methods = ['GET', 'POST'])
def clientedit():
  if request.method=='POST':
        # id=request.form['id']
        id_data=request.form['id']
        cname=request.form['cname']
        cemail=request.form['cemail']
        cphone=request.form['cphone']
        cproject=request.form['cproject']
        cur=mysql.connection.cursor()
        cur.execute("""
                    UPDATE viwclient set cname=%s,cemail=%s,cphone=%s,cproject=%s
                    where id=%s 
                    """,(cname,cemail,cphone,cproject,id_data))
        flash('CLIENT UPDATED SUCCESFULLY!')
        mysql.connection.commit()
        return redirect(url_for('vallclient'))
  return render_template("vi.html",viwclient=id_data)
# =============================================================== MICROGRAFIX ============  
@app.route('/miclientedit', methods = ['GET', 'POST'])
def miclientedit():
  if request.method=='POST':
        # id=request.form['id']
        id_data=request.form['id']
        miname=request.form['miname']
        miemail=request.form['miemail']
        miphone=request.form['miphone']
        miproject=request.form['miproject']
        mcur=mysql.connection.cursor()
        mcur.execute("""
                    UPDATE micrografixclient set miname=%s,miemail=%s,miphone=%s,miproject=%s
                    where id=%s 
                    """,(miname,miemail,miphone,miproject,id_data))
        flash('CLIENT UPDATED SUCCESFULLY!')
        mysql.connection.commit()
        return redirect(url_for('mallclient'))
  return render_template("microclientindex.html",micrografixclient=id_data)


# ===========================================================================
@app.route('/dele/<string:id_data>/', methods = ['POST','GET'])
def dele(id_data):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM data1 where id=%s ",(id_data,))
    mysql.connection.commit()
    return redirect(url_for('allclient'))

# ==================================================viw3dclient Delete =========================
@app.route('/clientdele/<string:id_data>/', methods = ['POST','GET'])
def clientdele(id_data):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM viwclient where id=%s ",(id_data,))
    mysql.connection.commit()
    return redirect(url_for('vallclient'))

# =============================================================== MICROGRAFIX ============  
@app.route('/miclientdele/<string:id_data>/', methods = ['POST','GET'])
def miclientdele(id_data):
    mcur=mysql.connection.cursor()
    mcur.execute("DELETE FROM micrografixclient where id=%s ",(id_data,))
    mysql.connection.commit()
    return redirect(url_for('mallclient'))
# ===========================================================================
# ===============================================================*********************** FOR VIW3D ============


# ===========================================================================
if __name__ == "__main__":
    app.run(debug=True)