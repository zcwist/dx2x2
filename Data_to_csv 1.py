from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.DataBaseSetUp import User, Base, Survey, Skill_Entry, AxisTemplate, Canvas, Skill_List_Manager
from database.DBAccess import get_user_name

import csv

import database.config as config







def Summary(survey, name):
    Str = config.getDBStr()
    engine = create_engine(Str)

    DBSession = sessionmaker(bind=engine)

    session = DBSession()

    xrowList = []
    yrowList = []
    ColumnNameList = ["Name"] # First column in the output csv is "Name"
    user_list = [] #list of user
    # xdict = {}  # x direction values stored in here
    # ydict = {}  # y direction values stored in here

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
        xcurRow = {"Name":data.user_id} #add to x eachRow
        ycurRow = {"Name":data.user_id} #add to x eachRow
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
                Skillheight = curCoordinate["height"]
                Skillwidth = curCoordinate["width"]

                top += Skillheight / 2;
                left += Skillwidth / 2;

                # Measure criteria: -10 to 10
                y_score = float(height - top) / height * 20 - 10
                x_score = float(left) / width * 20 - 10

                if skillName not in xcurRow.keys():
                    xcurRow[skillName] = x_score


                if skillName not in ycurRow.keys():
                    ycurRow[skillName] = y_score

            except Exception as e:
                if skillName not in xcurRow.keys():
                    xcurRow[skillName] = "NA"

                if skillName not in ycurRow.keys():
                    ycurRow[skillName] = "NA"
        xrowList.append(xcurRow)
        yrowList.append(ycurRow)

    with open('x_summary_' + name + '.csv', 'w') as csvfile:
        fieldnames = ColumnNameList
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in xrowList:
            writer.writerow(row)

    with open('y_summary_' + name + '.csv', 'w') as csvfile:
        fieldnames = ColumnNameList
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in yrowList:
            writer.writerow(row)

##Test run For the demo,  the survey ID we used is 1.
Summary(1, "firstTime")
Summary(2, "secondTime")