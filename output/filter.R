
datafilter <- function(surveyID, skillname, studentuid){
  csv = read.csv(file=paste("292C",surveyID,".csv",sep=""),header=TRUE)
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

compare <- function(surveyID,survey2ID, skillname, studentuid){
  csv = read.csv(file=paste("292C",surveyID,".csv",sep=""),header=TRUE)
  csv = cbind(csv,survey_id=surveyID)
  csv2 = read.csv(file=paste("292C",survey2ID,".csv",sep=""),header=TRUE)
  csv2 = cbind(csv2,survey_id=survey2ID)
  
  # filteredcsv = merge(csv,csv2,by=c("uid","skill"))
  filteredcsv = rbind(csv,csv2)
  
  if (skillname != "ALL"){
    filteredcsv = subset(filteredcsv, skill==skillname)
  }
  if (studentuid != "All Students"){
    filteredcsv = subset(filteredcsv, uid==studentuid)
  }
  
  return(filteredcsv)
}

mergedata <-  function(surveyID,survey2ID, skillname, studentuid){
  
  csv = read.csv(file=paste("292C",surveyID,".csv",sep=""),header=TRUE)
  csv2 = read.csv(file=paste("292C",survey2ID,".csv",sep=""),header=TRUE)
  
  filteredcsv = merge(csv,csv2,by=c("uid","skill"))
  
  if (skillname != "ALL"){
    filteredcsv = subset(filteredcsv, skill==skillname)
  }
  if (studentuid != "All Students"){
    filteredcsv = subset(filteredcsv, uid==studentuid)
  }
  
  return(filteredcsv)
  
}

