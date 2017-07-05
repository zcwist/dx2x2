from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from csvreader import get_user_list
from DataBaseSetUp import User, Base, Survey,Skill_Entry,Skill_List_Manager, AxisTemplate,Canvas

import config
from sqlalchemy.pool import NullPool

def setConnection():
    Str = config.getDBStr()
    engine = create_engine(Str, poolclass=NullPool)
    # engine = create_engine('sqlite:///OurDataBase.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)

    session = DBSession()
    return session

#add user
#Input csv format:  user_id,user_name
def addUser(cvsaddress):
    session = setConnection()
    user_list = get_user_list(cvsaddress)
    
    for item in user_list:
        try:
            user = User(user_id = item[0], user_name = item[1])
            session.add(user)
            session.commit()
        except Exception as e:
            print e
            print("User Name: {}, User Id: {}: Already exist".format(item[1], item[0]))
            session.rollback()
    print("successfully added Users")
    session.close()
    
def addOneUser(uid, firstName):
    session = setConnection()
    try:
        user = User(user_id=uid, user_name=firstName)
        session.add(user)
        session.commit()
    except Exception as e:
        print e
        print("User Name: {}, User Id: {}: Already exist".format(uid, firstName))
    session.close()
#delete user
def deleteUser(user_id, user_name):
    session = setConnection()
    try:
        targetUser = session.query(User).filter(and_(User.user_id == user_id,User.user_name == user_name)).one()
        session.delete(targetUser)
        session.commit()
        print("Successully deleted")
    except Exception as e:
        print("Target User does not exsit in database")
    session.close()

        

#add skill List Manager
def addSkillList(newListName, ListDescription = ""):
    session = setConnection()
    skill_listManager = Skill_List_Manager(skill_list_name = newListName, skill_list_descrip = ListDescription)
    session.add(skill_listManager)
    session.commit()
    session.close()



#add skill in skillList
def addSkill(cvsaddress, ListManagerID):
    session = setConnection()
    skill_list = get_user_list("../Data/skill.csv")
    targetListManager = session.query(Skill_List_Manager).filter(Skill_List_Manager.id == ListManagerID).one()
    for item in skill_list:
        skill = Skill_Entry(skill_name = item[0], skill_descrip = item[1], skill_list_manager = targetListManager)
        session.add(skill)
        session.commit()
    session.close()

    
    
#add Template
def addAxisTemplate(leftText, rightText, upText, downText):
    session = setConnection()

    axis1 = AxisTemplate(left = leftText, right = rightText, 
                        up = upText, down = downText)
    session.add(axis1)
    session.commit()
    session.close()


#add Survey
### create new survey
###given a survey list ID and a template ID create a survey
def createNewSurvey(skill_listID, templateID, surveyKey):
    session = setConnection()

    skill_listManager = session.query(Skill_List_Manager).filter(Skill_List_Manager.id == skill_listID).one()
    template = session.query(AxisTemplate).filter(AxisTemplate.id == templateID).one()
    newSurvey = Survey(survey_key= surveyKey, skill_list_manager=skill_listManager, axistemplate=template)
    session.add(newSurvey)
    sessionwwwwa.commit()
    session.close()


    


if __name__ == "__main__":
    addOneUser("0103","0103")
    # deleteUser("0103","0103")
    # addUser("../Data/newUser.csv")
    # template = session.query(AxisTemplate).filter(AxisTemplate.id == 1).one()
    # template.up = "Skills I want to hone"
    # template.down = "Skills I don't want to hone"
    # template.left = "Skills I am limited in"
    # template.right = "Skills I have"
    # #
    # session.add(template)
    # session.commit()
    # Test the written functions
    # addUser("../Data/newUser.csv")
    # ##a demo created to test the database function
    # ###add user from the CVS to User table
    # user_list = get_user_list("../Data/user.csv")
    # for item in user_list:
    #     user = User(user_id = item[0], user_name = item[1])
    #     session.add(user)
    #     session.commit()
    
    # print "added user"
    
    # ###add skill_list
    # skill_listManager = Skill_List_Manager(skill_list_name = "List of Skills", skill_list_descrip = "this is the list created for instructional purpose in ME292C")
    # session.add(skill_listManager)
    # session.commit()
    
    
    # print "created a skill list"
    
    # ###add skill to skill list
    # skill_list = get_user_list("../Data/skill.csv")
    # for item in skill_list:
    #     skill = Skill_Entry(skill_name = item[0], skill_descrip = item[1], skill_list_manager = skill_listManager)
    #     session.add(skill)
    #     session.commit()
    # print "added skill to skill list!"
    
    
    # ##add AxisTemplate
    # axis1 = AxisTemplate(left = "Design Skills i don't have", right = "Design Skills i have", 
    #                     up = "Design Skills i want to hone", down = "Design Skills i don't want to hone")
    # session.add(axis1)
    # session.commit()
    
    # print "added Axis!"
    
    
    # ##add survey 
    # survey1 = Survey(survey_key = "T1", skill_list_manager = skill_listManager, axistemplate = axis1)
    # session.add(survey1)
    # session.commit()
    # print "added survey"
    
    
    
    # ###Fake add some Canvas user input
