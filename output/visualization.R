import <- function(){
  setwd("~/Code/python/dx/dx2x2/output")
  library(readr)
  x_summary1 <<- read_csv("x_summary1.csv")
  x_summary2 <<- read_csv("x_summary2.csv")
  y_summary1 <<- read_csv("y_summary1.csv")
  y_summary2 <<- read_csv("y_summary2.csv")
  
  df <<- data.frame(index = 1:34, 
                   meanx = apply(x_summary1[2:35],2,mean,na.rm=TRUE),
                   sdx = apply(x_summary1[2:35],2,sd,na.rm=TRUE),
                   meany = apply(y_summary1[2:35],2,mean,na.rm=TRUE),
                   sdy = apply(y_summary1[2:35],2,sd,na.rm=TRUE),
                   row.names = colnames(x_summary1)[2:35])
  df2 <<- data.frame(index = 1:34, 
                    meanx = apply(x_summary2[2:35],2,mean,na.rm=TRUE),
                    sdx = apply(x_summary2[2:35],2,sd,na.rm=TRUE),
                    meany = apply(y_summary2[2:35],2,mean,na.rm=TRUE),
                    sdy = apply(y_summary2[2:35],2,sd,na.rm=TRUE),
                    row.names = colnames(x_summary2)[2:35])
}
rawdata <- function(){
  plot(x_summary1[[2]],y_summary1[[2]],xlim=c(-10, 10),ylim=c(-10,10),xlab="Proficiency", ylab="Interest")
  for (skill in 3:35){
    points(x_summary1[[skill]],y_summary1[[skill]])
  }
  
  for (skill in 2:35){
    points(x_summary2[[skill]],y_summary2[[skill]],col="red")
  }
  legend("bottomleft", legend=c("1st Survey", "2nd Survey"),
         col=c("black", "red"), pch=21)
}

errorbar <- function(){
  # skill = colnames(y_summary1)[2:35]
  # mean = apply(y_summary1[2:35],2,mean)
  # sd = apply(y_summary1[2:35],2,sd)
  x <- 1:34
  #plot(x, mean,ylim=range(c(mean-sd,mean+sd)),pch=19)
  #arrows(x, mean-sd, x, mean+sd, length = 0.05, angle = 90, code=3)
  
  
  
  df <- df[with(df,order(meany)),]
  
  plot(x,df$meanx, ylim=range(c(-10,10)),col="red")
  arrows(x, df$meanx-df$sdx, x, df$meanx+df$sdx, length = 0.05, angle = 90, code=3,col="red")
  
  par(new=TRUE)
  
  plot(x,df$meany, ylim=range(c(-10,10)),col="blue")
  arrows(x, df$meany-df$sdy, x, df$meany+df$sdy, length = 0.05, angle = 90, code=3,col="blue")
  
  # sortdf = df[with(df,order(meanx)),]
  # sortdf = df
  # plot(x, sortdf$mean, ylim=range(c(-10,10)),col="red")
  # arrows(x, sortdf$mean-sortdf$sd, x, sortdf$mean+sortdf$sd, length = 0.05, angle = 90, code=3,col="red")
  
  # par(new=TRUE)
  # 
  # df <- data.frame(index = 1:34, mean = apply(y_summary1[2:35],2,mean),sd = apply(y_summary1[2:35],2,sd),row.names = colnames(x_summary1)[2:35])
  # sortdf = df[with(df,order(mean)),]
  # sortdf = df
  # plot(x, sortdf$mean, ylim=range(c(-10,10)),col="blue")
  # arrows(x, sortdf$mean-sortdf$sd, x, sortdf$mean+sortdf$sd, length = 0.05, angle = 90, code=3,col="blue")
  
  
}

twoderror <- function(){
  plot(df$meanx,df$meany,xlim=range(c(-10,10)),ylim=range(c(-10,10)))
  arrows(df$meanx, df$meany-df$sdy, df$meanx, df$meany+df$sdy, length = 0.05, angle = 90, code=3,col="blue")
  arrows(df$meanx-df$sdx,df$meany,df$meanx+df$sdx,df$meany,length = 0.05, angle = 90, code=3,col="blue")
}

vector <- function(){
  xrange = range(c(0,5))
  yrange = range(c(1,6))
  plot(df$meanx,df$meany,xlim=xrange,ylim=yrange,type="p",col="red",xlab="Proficiency",ylab="Interest")
  par(new=TRUE)
  plot(df2$meanx,df2$meany,xlim=xrange,ylim=yrange,col="blue",xlab="Proficiency",ylab="Interest")
  arrows(df$meanx,df$meany,df2$meanx,df2$meany,length = 0.05, code=2,col="black")
}

histplot <- function(){
  distance = sqrt((df2$meanx-df$meanx)^2+(df2$meany-df$meany)^2)
  hist(distance,breaks=10)
}

histall <- function(){
  
}

