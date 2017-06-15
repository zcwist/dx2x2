# class Canvas(Base):
#     __tablename__ = 'canvas'
#     id = Column(Integer, primary_key = True)
#     user_id = Column(String(80), ForeignKey('userdata.user_id'))
#     class_id = Column(Integer, ForeignKey('survey.id') )
#     version = Column(Integer, default=1)
#     date = Column(DateTime)
#     coordinates = Column(JSON)
    
    
#     userdata = relationship(User)
#     survy = relationship(Survey)
canvasEntry = Canvas(user_id = "001", class_id = "T1")


def setCanvasData(user, survey, coor):
    try:
        currentData = session.query(Canvas).filter(Canvas.user_id == user_id and Canvas.class_id == survey_id).one()
        #add in new Entry if it is Empty
        currentData.coordinates = coor
        session.add(currentData)
        session.commit()
    except Exception as e:
        newStudentEntry = Canvas(user_id = user, survey_id = survey, coordinates = coor)
        session.add(newStudentEntry)
        session.commit()
        
def getCanvasCoordinates(user, survey):
        try:
            currentData = session.query(Canvas).filter(Canvas.user_id == user_id and Canvas.class_id == survey_id).one()
            return currentData.coordinates
        except Exception as e:
            return None
    