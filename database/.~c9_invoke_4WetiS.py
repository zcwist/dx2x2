from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBaseSetUp import User, Base, Survey,Skill_list,AxisTemplate,Canvas


Str = 'mysql://kaiyuewang:wangkaiyue94@testdb.c7rdqxze62rp.us-east-1.rds.amazonaws.com:3306/testdb'
engine = create_engine(Str)

DBSession = sessionmaker(bind = engine)

session = DBSession()

def get_user_name(id):
    ##"""return user name by id, return None if id doesn’t exist"""
        user = session.query(User).filter(User.user_id == id).one()
    except Exception as e:
        return None
    if user:
        return user.user_name


def get_skill_list(surveyID):
    #"""return a skill json by surveyID [{skill_name:"",skill_descrip:""}]
    #return None if surveyID doesn't exist"""
    try:
        survey = session.query(Survey).filter(Survey.survey_key == surveyID).one()
        p
        lists = session.query(Skill_list).filter(Skill_list.survey == survey).all()
    except Exception as e:
        return None
    if lists:
        for entry in lists:
            print(entry.skill_name)
            print(entry.skill_descrip)

def get_surveys_name_list():
    """return a list of survey names"""
    try:
        survey = session.query(Survey.survey_key).all()
        print(survey)
        return survey
    except Exception as e:
        return None

def get_survey_template(surveyId):
    """return template by surveyId {top:"",bottom:"",left:"",right:""}
    return None if surveyID doesn't exist"""
    pass


if __name__ == "__main__":
    get_surveys_name_list()