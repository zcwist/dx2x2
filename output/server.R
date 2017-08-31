# Define server logic required to draw a histogram ----
server <- function(input, output,session) {
  
  observe({
    surveyID = input$surveyID
    studentList = c("All Students")
    for (id in surveyID){
      file = read.csv(paste("x_",toString(id),".csv",sep=""))
      studentList = c(studentList,file$Name)
    }
    
    studentList = unique(studentList)
    print(studentList)
    updateSelectInput(session,"names","Student",c(studentList))
  })
  
  
  
  # Histogram of the Old Faithful Geyser Data ----
  # with requested number of bins
  # This expression that generates a histogram is wrapped in a call
  # to renderPlot to indicate that:
  #
  # 1. It is "reactive" and therefore should be automatically
  #    re-executed when inputs (input$bins) change
  # 2. Its output type is a plot
  output$scatter <- renderPlotly({
    
    filteredData = datafilter(input$surveyID,input$skills,input$names)
    print(filteredData)
    
    plot_ly(x=filteredData$x,y=filteredData$y, type = "scatter", mode="markers")
  })
  
  output$distPlot2 <- renderPlot({
    
    x    <- faithful$waiting
    bins <- seq(min(x), max(x), length.out = input$bins + 1)
    
    hist(x, breaks = bins, col = "#75AADB", border = "white",
         xlab = "Waiting time to next eruption (in mins)",
         main = "Histogram of waiting times")
    
  })
  
}