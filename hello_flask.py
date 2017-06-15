import os
import flask
from database.DBAccess import *

app = flask.Flask(__name__)
app.secret_key ="design exchange"

import flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(student_id):
    if not get_user_name(student_id):
        return 
    user = User()
    user.id = student_id
    return user
    
@login_manager.request_loader
def request_loader(request):
    student_id = request.form.get('student_id')
    if not get_user_name(student_id):
        return
    user = User()
    user.id = student_id

    user.is_authenticated = request.form['last_name'] == get_user_name(student_id)
    
@app.route('/', methods=['GET'])
def index():
    return flask.redirect(flask.url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('sign_in.html')
    
    print flask.request.form

    student_id = str(flask.request.form['student_id'])
    print get_user_name(student_id)
    if not get_user_name(student_id):
        return "User doesn't exist"
    if flask.request.form['last_name'] == get_user_name(student_id):
        user = User()
        user.id = student_id
        survey_key = flask.request.form['survey_key']
        survey_id = get_survey_id(survey_key)
        print survey_id
        return flask.redirect(flask.url_for('protected',survey_id=survey_id))

    return 'Bad login'

@app.route('/protected/<survey_id>')
# @flask_login.login_required
def protected(survey_id):
    #Judge the class status before everything
    if not checkSurveyIdExsist(survey_id):
        return "Bad survey"
   
    skills = get_skill_list(survey_id)
    # return flask.render_template('2x2.html',skills=skills)
    return flask.render_template('2x2.html')
    
    # return 'Logged in as: ' + flask_login.current_user.id + " at class:" + survey_id
@app.route('/skills/<survey_id>')
def getskills(survey_id):
    skills = get_skill_list(survey_id)
    return flask.jsonify(skills);

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/kaiyue/test',methods=['GET','POST'])
def getDataFromSubmit():
    if flask.request.method == 'GET':
        return flask.render_template('test.html')
    dic = flask.request.json['total']
    print(str(dic))
    return flask.json.dumps({'success':True}), 200, {'ContentType':'application/json'}
        
  
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
