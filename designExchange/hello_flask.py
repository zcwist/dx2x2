import os
import flask
from database.DBAccess import get_user_name

app = flask.Flask(__name__)
app.secret_key ="design exchange"

import flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# users_tuple = [('001', 'demo1'), ('002', 'demo2')]
# def tuple2dict(users_tuple):
#     dic = {}
#     for user in users_tuple:
#         dic[user[0]] = user[1]
#     return dic
        
# users = tuple2dict(users_tuple)
    
class User(flask_login.UserMixin):
    pass
    # def __init__(self):
    #     super(User, self).__init__()
    #     self.class_id = "id"

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='student_id' id='student_id' placeholder='student_id'></input>
                <input type='password' name='last_name' id='last_name' placeholder='Last name'></input>
                <input type='text' name='class_id' id='class_id' placeholder='class_id'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    student_id = str(flask.request.form['student_id'])
    print student_id
    print get_user_name("001")
    if not get_user_name(student_id):
        return "User doesn't exist"
    if flask.request.form['last_name'] == get_user_name(student_id):
        user = User()
        user.id = student_id
        return flask.redirect(flask.url_for('protected',class_id=flask.request.form['class_id']))

    return 'Bad login'

@app.route('/protected/<class_id>')
# @flask_login.login_required
def protected(class_id):
    return 'Logged in as: ' + flask_login.current_user.id + " at class:" + class_id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
