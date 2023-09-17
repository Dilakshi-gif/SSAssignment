from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
import re
import hashlib
import createKey
import encrypt
import decrypt

app = Flask(__name__)

conn= mysql.connector.connect(host="localhost",user="root",password="",database="user")
cursor=conn.cursor()

@app.route('/')
def login():
    render_template('login.html')


@app.route('login_validation',methods=['POST'])
def login_validation():
    if not re.match(r'[^@] + [^@] + \.[^@] +', 'email'):
        message = "Invalid Email"
    else:
                cursor.execute("INSERT INTO user(email,password,type) VALUES(%s,%s,%s)".format ('email','hashpw','role'))
                mysql.connector.commit()
                cursor.close()
                message = "Successfully Register"
    return render_template("message.html")


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST' and 'txtuname' in request.form and 'txtpw' in request.form and 'txtcpw' in request.method:
        h= hashlib.new("sha512")
        email = request.form['txtuname']
        pw = request.form['txtpw']
        cpw= request.form['txtcpw']
        role = request.form['role']
        h.update(pw.encode())

        hashpw = h.hexdigest()
        cursor = mysql.connector.cursor()

        cursor.execute("SELECT email From user where email= %s",(email,))
        account = cursor.fetchone()
        if pw == cpw:
            if account:
                message= 'Account alredy exists !'

            elif not re.match(r'[^@] + [^@] + \.[^@] +', email):
                message = "Invalid Email"

            else:
                cursor.execute("INSERT INTO user(email,password,type) VALUES(%s,%s,%s)", (email,hashpw,role))
                mysql.connector.commit()
                cursor.close()
                message = "Successfully Register"
                return render_template("message.html")
        else:
            message= 'Password and confirm password not equal'
        return render_template('register.html', message='')
    else:
        return render_template('register.html', message='')
@app.route('/Message', methods =['GET', 'POST'])
def Message():
    if request.method == 'POST' and 'msg' in request.form and 'role' in request.form:
        msg = request.form['msg']
        role = request.form['role']

        createKey.KeyGeneration()

        encrypt.Encryption(msg,role)
        return render_template('Message.html',message = 'Message Successfully Encrypt')
    else:
        return render_template('Message.html',message= '')
@app.route('/read',methods= ['GET','POST'])
def read():
    if request.method== 'POST' and 'txtuname' in request.form and 'txtpw' in request.form:
        h=hashlib.new("sha512")
        email = request.form['txtuname']
        pw = request.form['txtpw']
        h.update(pw.encode())

        hashpw= h.hexdigest()
        cursor2 = mysql.connector.cursor()
        cursor2.execute("SELECT email,password,type FROM user where email= %s and password= %s ", (email,hashpw))
        account= cursor2.fetchone()
        if account:
            user_type = account[2]
            data = decrypt.Decryption(user_type)

            message ='Account alredy exists !'
            return render_template('read.html',Data= data,message= "")
        else:
            return render_template('read.html', Data = '', message='Invalid login !')
    else:
        return render_template('read.html', Data='', message='')
    

if __name__ == "__main__":
    app.run()
    
