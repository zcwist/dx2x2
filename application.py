import os
import flask
from database.DBAccess import *

application = flask.Flask(__name__)
application.secret_key = "design exchange"

import flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(application)

class DXUser(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(student_id):
    if not get_user_name(student_id):
        return None
    user = DXUser()
    user.id = student_id
    return user
    
@login_manager.request_loader
def request_loader(request):
    student_id = request.form.get('student_id')
    if not get_user_name(student_id):
        return
    user = DXUser()
    user.id = student_id

    user.is_authenticated = request.form['last_name'].strip().lower() == get_user_name(student_id).strip().lower()
    return user
    
@application.route('/', methods=['GET'])
def index():
    return flask.redirect(flask.url_for('login'))

@application.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('sign_in.html')
    
    student_id = str(flask.request.form['student_id'])
    # print get_user_name(student_id)
    if not get_user_name(student_id):
        return "User doesn't exist"
    if flask.request.form['last_name'].strip().lower() == get_user_name(student_id).strip().lower():
        user = DXUser()
        user.id = student_id
        
        survey_key = flask.request.form['survey_key']
        survey_id = get_survey_id(survey_key)
        if not survey_id:
            flask.flash("Survey error")
            return flask.redirect(flask.url_for('login')) 
        
        flask_login.login_user(user);
        if survey_id == 1:
            return flask.redirect(flask.url_for('protected',survey_id=survey_id))
        if survey_id > 1:
            return flask.redirect(flask.url_for('compare', survey_id=survey_id, pre_survey_id=survey_id-1));

    flask.flash('Bad login')
    return flask.redirect(flask.url_for('login')) 

@application.route('/compare/<survey_id>/<pre_survey_id>')
@flask_login.login_required
def compare(survey_id,pre_survey_id):
    return flask.render_template('compare2x2.html', survey_id=survey_id, pre_survey_id=pre_survey_id);

@application.route('/protected/<survey_id>')
@flask_login.login_required
def protected(survey_id):
    #Judge the class status before everything
    status = checkSurveyStatus(survey_id)
    if status == False:
        flask.flash("Closed survey")
        return flask.redirect(flask.url_for('login')) 
    
    if status == None:
        flask.flash("Survey error")
        return flask.redirect(flask.url_for('login')) 
   
    # skills = get_skill_list(survey_id)


    return flask.render_template('2x2.html',survey_id=survey_id)
    
@application.route('/skills/<survey_id>')
def getskills(survey_id):
    skills = get_skill_list(survey_id)
    return flask.jsonify(skills)
@application.route('/template/<survey_id>')
def gettemplate(survey_id):
    template = get_survey_template(survey_id)
    return flask.jsonify(template)
@application.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('login'))

@application.route('/userinfo')
@flask_login.login_required
def get_user_info():
    return flask.jsonify(flask_login.current_user.id);

@login_manager.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect(flask.url_for('login'))

@application.route('/kaiyue/test', methods=['GET', 'POST'])
def getDataFromSubmit():
    if flask.request.method == 'GET':
        return flask.render_template('test.html')
    dic = flask.request.json['total']
    user = dic['user_id']
    survey = dic['survey_id']
    # print ("uploading survey"+survey);
    canvas = dic['canvas_data']
    # print(canvas)
    setCanvasData(user, survey, canvas)
    # print("successfully set canvasData")
    
    # print(getCanvasCoordinates(user,survey))

    #write to db here
    
    return flask.json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    
@application.route('/loadcanvas', methods=['POST'])
def loadcanvas():
    survey_info = flask.request.json['survey_info']
    user_id = survey_info["user_id"]
    survey_id = survey_info["survey_id"]
    
    canvas_data = getCanvasCoordinates(user_id, survey_id)
    
    #check if this user is surveyed before
    if not canvas_data:
        return flask.jsonify(surveyed=False)
    else:
        return flask.jsonify(surveyed=True, canvas_data=canvas_data)
        

@application.route('/demo')
def showdemo():
    user = DXUser()
    user.id = "002"
    flask_login.login_user(user)
    # print("here")
    return flask.render_template('2x2.html', survey_id="1")

@application.route('/loaderio-03c01977e0b6a3cc4027801efa2d7407.txt')
def showFiles():
    return "loaderio-03c01977e0b6a3cc4027801efa2d7407"
if __name__ == "__main__":
    application.debug = True
    application.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8001)))
