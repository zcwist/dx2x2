from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.DBAccess import get_user_name
from database.DataBaseSetUp import User, Base, Survey, Skill_Entry, AxisTemplate, Canvas, Skill_List_Manager
import pandas as pd

# engine = create_engine('sqlite:///OurDataBase.db')

Str = 'mysql://kaiyuewang:wangkaiyue94@testdb.c7rdqxze62rp.us-east-1.rds.amazonaws.com:3306/testdb'
engine = create_engine(Str)

DBSession = sessionmaker(bind=engine)

session = DBSession()





def Summary(survey):
    ColumnNameList = ["Name"] # First column in the output csv is "Name"
    user_list = [] #list of user
    xdict = {}  # x direction values stored in here
    ydict = {}  # y direction values stored in here
    targetSurvey = session.query(Survey).filter(Survey.id == survey).one()  # retrieve the survey by survey_id
    list_id = targetSurvey.skill_list_id
    skillList = session.query(Skill_Entry).filter(
        Skill_Entry.skill_list_id == list_id).all()  # Get the skill information of this list

    ColumnNameList.extend([iter.skill_name for iter in skillList]) #Form the column

    CanvasData = session.query(Canvas).filter(Canvas.class_id == survey).all()  # get all the canvas data

    for data in CanvasData:
        print("You are currently using data from user:" + data.user_id)
        cur_user_name = get_user_name(data.user_id)
        user_list.append(cur_user_name)

        coor = data.coordinates
        # Get the height and width of the frame
        width = coor["canvas_size"]["width"]
        height = coor["canvas_size"]["height"]

        user_input_coor = coor["skills_pos"]
        #Iterate each skills that belongs to this survey and add in each user's response
        for skill in skillList:
            skillID = skill.id              #Get the id of the selected skill
            skillName = skill.skill_name    #Get the name of the selected skill

            try:
                curCoordinate = user_input_coor[str(skillID)] #Get the coordinate of current skill
                top = curCoordinate["top"]
                left = curCoordinate["left"]

                # Measure criteria: -10 to 10
                y_score = float(height - top) / height * 20 - 10
                x_score = float(left) / width * 20 - 10

                if skillName not in xdict.keys():
                    xdict[skillName] = [x_score]
                else:
                    xdict[skillName].append(x_score)

                if skillName not in ydict.keys():
                    ydict[skillName] = [y_score]
                else:
                    ydict[skillName].append(y_score)

            except Exception as e:
                if skillName not in xdict.keys():
                    xdict[skillName] = ["NA"]
                else:
                    xdict[skillName].append("NA")

                if skillName not in ydict.keys():
                    ydict[skillName] = ["NA"]
                else:
                    ydict[skillName].append("NA")

    xdict["Name"] = user_list
    ydict["Name"] = user_list
    
    ## write our to csv file
    df = pd.DataFrame(xdict, columns=ColumnNameList)
    df.to_csv('x_direction_summary.csv')
    tf = pd.DataFrame(ydict, columns=ColumnNameList)
    tf.to_csv('y_direction_summary.csv')


if __name__ == "__main__":
    Summary(1)