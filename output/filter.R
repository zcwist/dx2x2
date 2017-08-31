
datafilter <- function(surveyID, skillname, studentuid){
  csv = read.csv(file=paste("s_",surveyID,".csv",sep=""),header=TRUE)
  filteredcsv = csv
  if (skillname != "ALL"){
    filteredcsv = subset(filteredcsv, skill==skillname)
  }
  if (studentuid != "All Students"){
    filteredcsv = subset(filteredcsv, uid==studentuid)
  }
  return(filteredcsv)
  
  # print(filteredcsv)
  # plot_ly(x=filteredcsv$x,y=filteredcsv$y,color=filteredcsv$skill)
}

