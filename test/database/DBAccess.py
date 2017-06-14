def get_user_name(id):
    """return list of user tuple. e.g. ('001,', 'demo1'), ('002,', 'demo2')]"""
    names = {"001":"demo1","002":"demo2"}
    return names["001"]
    
def get_survey_id(key):
    return 1


def get_skill_list(surveyID):
    return [{'id': 1, 'skill_name': u'Abductive reasoning', 'skill_descrip': u' The ability to draw the best possible explanation from a set of observations'}, {'id': 2, 'skill_name': u'Active listening', 'skill_descrip': u' The ability to listen by fully engaging and using all senses to listen and respond in a conversation'}, {'id': 3, 'skill_name': u'Clarifying', 'skill_descrip': u'The ability and habit of asking pointed questions and re-stating what has been already heard in order to confirm understanding'}]


def get_survey_template(surveyId):
    return {'top': u'Design Skills i want to hone', 'left': u"Design Skills i don't have", 'right': u'Design Skills i have', 'bottom': u"Design Skills i don't want to hone"}

def checkSurveyIdExsist(survey_id):
    return True;

if __name__ == "__main__":
    print get_user_name("001")
    
