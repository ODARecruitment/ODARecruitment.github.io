from flask import Flask, request, render_template, flash, session, url_for
import pickle
import os
import process

application = Flask(__name__)
application.secret_key = 'dont tell'


@application.route('/', methods = ['POST', 'GET'])
def hello(): 
    return render_template("home.html")     

# @app.route('/bootstrap')
# def boot():
#     return render_template("learning.html")

@application.route('/logout', methods = ['POST', 'GET'])
def logout():
    session.pop('userN')
    return render_template("logout.html")

@application.route('/upload', methods = ['GET', 'POST'])
def upload():
    ab = "upload.html"
    UPLOAD_FOLDER = "C:\\Users\\prasa\\projects\\recruitment_project\\resumes"
    application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.path.join(application.config['UPLOAD_FOLDER'], file.filename))
        path = UPLOAD_FOLDER+"\\"+file.filename
        print(file.filename)
        process.read_doc(path)
        #flash('File Uploaded Successfully')
        return render_template(ab, message = "Uploaded Successfully")
    return render_template(ab)

@application.route('/login', methods = ['POST', 'GET'])
def login():
    return render_template("login.html")

@application.route('/admin')
def admin():
    if 'userN' in session:
        return render_template("admin.html")
    else:
        return render_template("login.html", alert = "Please Login to Access Admin Page")

@application.route('/admin', methods = ['POST', 'GET'])
def adminpage():
    # return render_template("admin.html")
    a = "admin.html"
    database = {'OdaAdmin':'ODA1234'}
    name1 = request.form['username']
    pwd = request.form['password']
    if name1 not in database or database[name1]!=pwd:
        return render_template('login.html', info = "Invalid Username or Password")
    else:
        session['userN'] = name1
        print(session)
        return render_template(a)
            


if __name__ == '__main__':
    application.run()





# 1. rename the main file to 'appplication.py'
#  and write 
# 	application = Flask(__name__)
	
# 2. create the requirements.txt
#   use command :  pip freeze > requirements.txt
  
# 3. create '.ebextensions' folder and create python.config file in it
# 	put below command in python .config file
	
# 	option_settings:
# 	"aws:elasticbeanstalk:container:python":
#     WSGIPath: application:application
	
# 4. create the zip file of including all and upload 

# AWSElasticBeanstalkWebTier
# AWSElasticBeanstalkMulticontainerDocker
# AWSElasticBeanstalkWorkerTier

# AutoScalingFullAccess
# ElasticLoadBalancingFullAccess
# AdministratorAccess-AWSElasticBeanstalk





#wsgi_app = app.wsgi_app

# database = {'prasad':'1234', 'parth':'5678'}

# @app.route('/form_login', methods = ['POST', 'GET'])
# def login():
#     a = "home.html"
#     name1 = request.form['username']
#     pwd = request.form['password']
#     if name1 not in database:
#         return render_template('login.html', info = "Invalid Username")
#     else:
#         if database[name1]!=pwd:
#             return render_template("login.html", info = "Invalid Password")
#         else:
#             return render_template(a, name = name1)

    # else:
    #     return render_template("login.html")

# if __name__ == '__main__':
#     import os
#     HOST = os.environ.get('SERVER_HOST', 'localhost')
#     try:
#         PORT = int(os.environ,get('SERVER_PORT', '5555'))
#     except ValueError:
#         PORT = 5555
#     app.run(HOST, PORT)