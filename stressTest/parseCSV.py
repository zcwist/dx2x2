import csv

def get_user_list(filename='./userList.csv'):
    """return list of user tuple. e.g. ('001,', 'demo1'), ('002,', 'demo2')]"""
    user_list = []
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            user_list.append((row[0],row[1]))
    return user_list