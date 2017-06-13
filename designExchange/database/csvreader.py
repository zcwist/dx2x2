import csv

def get_user_list(filename='../Data/user.csv'):
    user_list = []
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            user_list.append((row[0],row[1]))
    return user_list
            
if __name__=="__main__" :
    print get_user_list()