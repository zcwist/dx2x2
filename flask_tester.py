import os
import flask
from database.DBAccess import *

app = flask.Flask(__name__)
app.secret_key ="design exchange"

@app.route('/', methods=['GET'])
def index():
    # print get_user_name("001")
    
    return get_user_name("001")+str(get_skill_list("1"))

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))