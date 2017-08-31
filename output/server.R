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

    updateSelectInput(session,"names","Student",c(studentList))
  })
  
  

  output$scatter <- renderPlotly({
    
    if (input$analysisType == "Survey analysis"){
      filteredData = datafilter(input$surveyID,input$skills,input$names)
      
      if (input$colorby == "Student"){
        colorby = paste(filteredData$uid)
      }
      else if (input$colorby == "Skill"){
        colorby = filteredData$skill
      }
      
      plot <- plot_ly(filteredData, x=~x,y=~y,color=colorby,
                      type = "scatter", 
                      mode="markers", 
                      text=~paste("Student:",uid, "<br>SKill:",skill)) %>%
        layout(
          xaxis = list(range=c(-10,10)),
          yaxis = list(range=c(-10,10))
        )
    }
    
    else if (input$analysisType == "Difference analysis"){
      filteredData = compare(input$surveyID,input$surveyID2,input$skills,input$names)
      
      if (input$colorby == "Student"){
        colorby = paste(filteredData$uid)
      }
      else if (input$colorby == "Skill"){
        colorby = filteredData$skill
      }
      
      f = c(1,2)
      p <- plot_ly(filteredData, x=~x,y=~y,color=colorby,
                   frame=~survey_id,
                   type="scatter",
                   mode="markers")
      # %>% 
      #   animation_opts(
      #     2000, easing = "elastic", redraw = FALSE
      #   )
      
    }
    
    
  })
  
  output$distPlot <- renderPlotly({
    if (input$analysisType == "Survey analysis"){
      filteredData = datafilter(input$surveyID,input$skills,input$names)
      
      plot_ly(filteredData,type="histogram2dcontour",x=~x,y=~y,colors = "Blues") 
      
      
    }
    
    else if (input$analysisType == "Difference analysis"){
      filteredData = mergedata(input$surveyID,input$surveyID2,input$skills,input$names)
      plot_ly(alpha=0.6) %>%
      add_histogram(x=filteredData$x.y-filteredData$x.x,name="Proficiency") %>% 
      add_histogram(x=filteredData$y.y-filteredData$y.x,name="Interest") %>%
      layout(barmode="overlay")
      
    }
    
    
    
  })
  
}