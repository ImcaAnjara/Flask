# ! -*- coding:utf-8 -*-

from flask import Flask, redirect, url_for 
from flask import request, render_template
from flask import make_response, session, escape
from flask import flash
from werkzeug import secure_filename
from flask_mail import Mail, Message

app=Flask(__name__)
#Secret_Key for session
app.secret_key = 'fhdfqsffoqfn'


#Route
@app.route('/')
def index():
    return "Gestion étudiant"

#Variable
@app.route('/stagiaire/<name>')
def set_name(name):
    return "Stagiaire: %s" % name

#>Redirection Url
@app.route('/admin')
def hello_admin():
    return 'Hello admin !!!'

@app.route('/user/<username>')
def hello_user(username):
    return 'Hello user: %s' % username

@app.route('/enseigne/<name>')
def redirect_enseigne(name):
    if name =='admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_user', username = name))
    
#HTTP Methods
@app.route('/success/<name>')
def success(name):
    return 'Welcome %s' % name

@app.route('/login', methods =['POST', 'GET'])
def login():
    if request.method =='POST':
        user = request.form['nm']
        return redirect(url_for('success', name = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name = user))
    

#Templates
@app.route('/templates/<user>/<int:score>')
def render(user, score):
    return render_template('hello.html', nametotemplate = user, markstotemplate = score)

@app.route('/templates/result/')
def result():
    dict = {'phy':50,'che':60,'maths':70}
    return render_template('result.html', result = dict)

@app.route('/staticjs/')
def staticjs():
    return render_template('static.html')


#Sending Form Data to Templates
@app.route('/dataform')
def student():
    return render_template('student.html')

@app.route('/dataform/result', methods =['POST', 'GET'])
def result_student():
    if request.method == 'POST':
        result = request.form
        return render_template('result.html', result = result)
    

#Cookies
@app.route('/cookies')
def indexcookies():
    return render_template('index_cookies.html')

@app.route('/setcookies', methods =['POST', 'GET'])
def setcookies():
    if request.method == 'POST':
        user = request.form['nm']
   
        resp = make_response(render_template('readcookie.html'))
        resp.set_cookie('userID', user)
        return resp
    
@app.route('/getcookies')
def getcookies():
    name = request.cookies.get('userID')
    return '<h1>welcome '+name+'</h1>'
    

#Sessions
#To set session
# session['username'] = 'admin'
#To remove session
# session.pop('username', None)

@app.route('/session')
def indexsession():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
         "<b><a href = '/logoutsession'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/sessionlogin'></b>" + \
      "click here to log in</b></a>"
      
@app.route('/sessionlogin', methods = ['GET', 'POST'])
def loginsession():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('indexsession'))
    return render_template('loginsession.html')
#     return '''
#     <form action = "" method = "post">
#          <p><input type = "text" name = "username" /></p>
#          <p><input type = "submit" value = "login" /></p>
#     </form>
#     
#    '''
   
@app.route('/logoutsession')
def logout():
# remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('indexsession'))


#Message Falshing
@app.route('/messageflashing')
def indexmessage():
    return render_template('indexmessage.html')

@app.route('/loginmessage', methods = ['GET', 'POST'])
def loginmessage():
    error = None
    
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
           request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('indexmessage'))
     
    return render_template('loginmessage.html', error = error)

#File Uploading
@app.route('/upload')
def uploadfile():
    return render_template("upload.html") 
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
    return 'file uploaded successfully'


#Flask mail
mail = Mail(app)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'antsiresy2@gmail.com'
app.config['MAIL_PASSWORD'] = 'claudericka'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/mail')
def indexmail():
    msg = Message('Hello', sender = 'antsiresy2@gmail.com', recipients = ['antsiresy@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"


if __name__ =='__main__':
    app.run('localhost',5001, True)
#     app.run(debug = True)