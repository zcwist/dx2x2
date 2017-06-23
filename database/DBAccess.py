from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBaseSetUp import User, Base, Survey,Skill_Entry,AxisTemplate,Canvas,Skill_List_Manager

# engine = create_engine('sqlite:///OurDataBase.db')
import config
Str = config.getDBStr()
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

def setCanvasData(user, survey, coor):
    try:
        currentData = session.query(Canvas).filter(Canvas.user_id == user and Canvas.class_id == survey).one()
        #add in new Entry if it is Empty
        
        currentData.coordinates = coor
        session.add(currentData)
        session.commit()
    except Exception as e:
        newStudentEntry = Canvas(user_id = user, class_id = survey, coordinates = coor)
        session.add(newStudentEntry)
        session.commit()
        
def getCanvasCoordinates(user, survey):
        try:
            currentData = session.query(Canvas).filter(Canvas.user_id == user and Canvas.class_id == survey).one()
            return currentData.coordinates
        except Exception as e:
            return None

def getCanvasEntry(survey_id, user_id):
    return """{u'canvas_data': {u'skill_no_pos': [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'10', u'12', u'13', u'14', u'15', u'16', u'17', u'18', u'19', u'20', u'21', u'22', u'23', u'24', u'25', u'26', u'27', u'28', u'29', u'30', u'31', u'32', u'33', u'34'], u'canvas_size': {u'width': 838, u'height': 475}, u'skills_pos': {u'11': {u'top': 141, u'left': 132.5}}}, u'survey_id': u'1', u'user_id': u'001'}"""
#     # try:
#     #     cooridnates = session.query(Canvas).filter(Canvas.)

### create new survey
###given a survey list ID and a template ID create a survey
def createNewSurvey(skill_listID, templateID, surveyKey):
    skill_listManager = session.query(Skill_List_Manager).filter(Skill_List_Manager.id == skill_listID).one()
    template = session.query(AxisTemplate).filter(AxisTemplate.id == templateID).one()
    newSurvey = Survey(survey_key= surveyKey, skill_list_manager=skill_listManager, axistemplate=template)
    session.add(newSurvey)
    session.commit()





if __name__ == "__main__":
    surveyID = get_survey_id("T1")
    print(surveyID)
    #temporary hack. Not sure how far we want to go on this,
    createNewSurvey(1,1,"T1EndSemester")
    print(get_skill_list(surveyID))