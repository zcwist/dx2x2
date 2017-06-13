import csv

def get_user_list(f):
    with open('Data/user.csv', 'rb') as csvfile:
    with open('Data/user.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            user_list.append((row[0],row[1]))
    return user_list
            
if __name__=="__main__" :
    print get_user_list()