
from flask import Flask, render_template, request, flash,redirect,url_for,session
import sqlite3
app = Flask(__name__)
app.secret_key="7510"
with sqlite3.connect("database.db") as con:
    con.execute("create table if not exists admins(aid integer primary key, aname text, ausername text, email text, phone text, designation text, password text)")
    con.execute("create table if not exists teacher(Tid integer primary key, tname text, tusername text, college text, department text, email text, phone text, password text )")
    con.execute("create table if not exists Students(sid integer primary key, sname text, susername text, Course text, Semaster text, email text, phone text,  designation text, password text)")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():

    return render_template('login.html')
@app.route('/loginapp',methods=['GET','POST'])
def loginapp():
    if request.method=='POST':
        username=request.form['uname']
        password=request.form['pwd']
        with sqlite3.connect("database.db") as con:
            con.row_factory=sqlite3.Row
            cur=con.cursor()
            cur.execute("select * from teacher where tusername=? and password=?",(username,password))
            data=cur.fetchone()
        if data:
            session['loggedin']=True
            session['username']=data[1]
            return redirect(url_for("user"))
        else:
            flash("Incorrect username/password.try again!")
    return redirect(url_for("login"))
@app.route('/register',methods=['GET','POST'])
def register():
    msg = "msg"
    if request.method=='POST':
        try:
            name= request.form['name']
            username = request.form['uname']
            college = request.form['college']
            department = request.form['dname']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['passwd']
            with sqlite3.connect("employee.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("insert into teacher (tname,tusername,college,department,email,phone,password) values(?,?,?,?,?,?,?)",(name,username,college,department,email,phone,password))
                con.commit()
                msg = "Employee successfully Added"
        except:
            con.rollback()
            msg = "We can not add the employee to the list"

        finally:
            return render_template("sucess.html",msg=msg)
            con.close()
@app.route('/studentreg',methods=['GET','POST'])

@app.route('/user')
def user():
    return render_template('user.html',uname=session["username"])
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.clear()
    return redirect(url_for("index"))
@app.route('/admin',methods=['GET','POST'])
def admin():
    return render_template('admin.html')

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method=='POST':
        username=request.form['aname']
        password=request.form['apwd']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from admins where ausername=? and password=?",(username,password))
        data=cur.fetchone()
        if data:
            session['alogedin'] = True
            session['ausername'] = data[1]
            return redirect("admindash")
        else:
            flash("Incorrect username/password.try again!")
    return redirect(url_for("admin"))
@app.route('/select')
def select():
    return render_template('select.html')
@app.route('/treg')
def treg():
    return render_template('register.html')
@app.route('/sreg')
def sreg():
    return render_template('studentreg.html')
@app.route('/admindash')
def admindash():
    return render_template('admindash.html',uname=session["ausername"])

@app.route("/tview")
def tview():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    #total=con.cursor()
    #total.execute("SELECT COUNT(Tid) FROM teacher")
    cur.execute("select * from teacher")
    rows = cur.fetchall()
    #num = total.fetchone()
    #num = [v for v in total.fetchone().values()][0]
    #print(num)
    print(rows)
    return render_template("view.html",rows = rows)
if __name__ == '__main__':
    app.run(debug=True)
