from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBaseSetUp import User, Base, Survey,Skill_Entry,AxisTemplate,Canvas,Skill_List_Manager

# engine = create_engine('sqlite:///OurDataBase.db')

Str = 'mysql://kaiyuewang:wangkaiyue94@testdb.c7rdqxze62rp.us-east-1.rds.amazonaws.com:3306/testdb'
engine = create_engine(Str)

DBSession = sessionmaker(bind = engine)

session = DBSession()

def get_user_name(id):
    try:
        user = session.query(User).filter(User.user_id == id).one()
    except Exception as e:
        return None
    if user:
        return user.user_name


def get_skill_list(surveyID):
    #"""return a list of dictionary [{skill_name:"",skill_descrip:"", skill_id:""}]
    #return None if surveyID doesn't exist"""
    try:
        survey = session.query(Survey).filter(Survey.id == surveyID).one()
        listManager = session.query(Skill_List_Manager).filter(Skill_List_Manager.id == survey.skill_list_id).one()
        lists = session.query(Skill_Entry).filter(Skill_Entry.skill_list_id == listManager.id).all()
    except Exception as e:
        return None
    if lists:
        print("success")
        list1 = []
        for entry in lists:
            list1.append({ "skill_name":entry.skill_name, "skill_descrip": entry.skill_descrip, "id": entry.id})
        return list1

def get_survey_id(key):
    """return a list of survey names.[{survey_key:"",survey_id:""}]"""
    try:
        survey = session.query(Survey).filter(Survey.survey_key == key).one()
        return survey.id
    except Exception as e:
        return None

def get_survey_template(surveyId):
    """return template by surveyId {top:"",bottom:"",left:"",right:""}
    return None if surveyID doesn't exist"""
    try:
        survey = session.query(Survey).filter(Survey.id == surveyId).one()
        
        templateID = survey.template_id
        selectedtemplate = session.query(AxisTemplate).filter(AxisTemplate.id == templateID).one()
        return {"top": selectedtemplate.up, "bottom": selectedtemplate.down, "left": selectedtemplate.left, "right": selectedtemplate.right}
    except Exception as e:
        print("Can't access template")
        return None

def checkSurveyIdExsist(survey_id):
    try:
        survey = session.query(Survey).filter(Survey.id == survey_id).one()
        return True;
    except Exception as e:
        return False;
        
def checkSurveyStatus(survey_id):
    try:
        survey = session.query(Survey).filter(Survey.id == survey_id).one()
        return survey.isOpen
    except Exception as e:
        return None;
# def getCanvasEntry(survey_id, user_id):
#     try:
#         cooridnates = session.query(Canvas).filter(Canvas.)
if __name__ == "__main__":
    surveyID = get_survey_id("T1")
    print(surveyID)
    
    
    print(get_skill_list(surveyID));