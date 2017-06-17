from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.DataBaseSetUp import User, Base, Survey,Skill_Entry,AxisTemplate,Canvas,Skill_List_Manager

# engine = create_engine('sqlite:///OurDataBase.db')

Str = 'mysql://kaiyuewang:wangkaiyue94@testdb.c7rdqxze62rp.us-east-1.rds.amazonaws.com:3306/testdb'
engine = create_engine(Str)

DBSession = sessionmaker(bind = engine)

session = DBSession()


def Summary(survey):
    xdict = {} #x direction values
    ydict = {} #y direction values
    targetSurvey = session.query(Survey).filter(Survey.id == survey).one()
    list_id = targetSurvey.skill_list_id
    skillList = session.query(Skill_Entry).filter(Skill_Entry.skill_list_id == list_id).all() #Get the skill information of this list
    
    CanvasData = session.query(Canvas).filter(Canvas.class_id == survey).all() #get all the canvas data
    for data in CanvasData:
        coor = data.coordinates
        # print(coor)
        
        width = coor["canvas_size"]["width"]
        height = coor["canvas_size"]["height"]
        # print(height,width)
        for skill in skillList:
            skillID = skill.id
            try:
                curCoordinate = coor["skills_pos"][str(skillID)]
                top = curCoordinate["top"]
                left = curCoordinate["left"]
                # print(top,left)
                y_score = float(height - top) / height* 20 - 10
                x_score = float(left) / width * 20 - 10
                
                print(skillID)
                if skillID in xdict.keys():
                    xdict[skillID] = [x_score]
                else:
                    xdict[skillID].append(x_score)
                print(xdict)
                    
                    
                if skillID in ydict.keys():
                    ydict[skillID] = [y_score]
                else:
                    ydict[skillID].append(y_score)
                    
            except Exception as e:
                continue
        print(xdict)
                
            

            


Summary(1)