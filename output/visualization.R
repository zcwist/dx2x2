plot(x_summary1[[2]],y_summary1[[2]],xlim=c(-10, 10),ylim=c(-10,10))
for (skill in 3:35){
  points(x_summary1[[skill]],y_summary1[[skill]])
}

for (skill in 2:35){
  points(x_summary2[[skill]],y_summary2[[skill]],col="red")
}
legend("bottomleft", legend=c("1st Survey", "2nd Survey"),
       col=c("black", "red"), pch=21)
