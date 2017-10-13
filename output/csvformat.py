import csv

def mergeCSV(file1,file2,file):
	studentList = []
	with open(file1) as csvfile, open(file2) as csvfile2:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		spamreader2 = csv.reader(csvfile2, delimiter=',', quotechar='|')
		isFirst = True
		skilllist = list()
		for row1,row2 in zip(spamreader,spamreader2):
			if isFirst:
				skilllist = row1[1:]
				isFirst = False
				continue

			for i,(xscore,yscore) in enumerate(zip(row1[1:],row2[1:])):
				student = dict()
				student["uid"] = row1[0]
				student["skill"] = skilllist[i]
				student["x"] = xscore
				student["y"] = yscore
				studentList.append(student)

	with open(file,'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(["uid","skill","x","y"])
		for item in studentList:
			spamwriter.writerow([item["uid"],item["skill"],item["x"],item["y"]])


if __name__ == '__main__':
	mergeCSV("x_summary_1013.csv","y_summary_1013.csv","292C2.csv")


