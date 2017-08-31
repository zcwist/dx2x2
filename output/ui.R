# Define UI for app that draws a histogram ----
ui <- fluidPage(
  
  # App title ----
  titlePanel("Skill matrix analysis"),
  
  fluidRow(
    column(4,
           #select analysis type
           selectInput("analysisType", "Analysis Type",
                       c("Survey analysis",
                         "Difference analysis")),
           radioButtons("colorby","Show colors in", choices=c("Skill","Student"),selected="Skill")
           
           
    ),
    column(4,
           #select survey
           selectInput("surveyID", "Survey no.",
                       c(1,2),multiple = F,selected = 1),
           
           conditionalPanel(
             condition = "input.analysisType == 'Difference analysis'",
             #select survey
             selectInput("surveyID2", "Survey2 no.",
                         c(1,2),multiple = F,selected = 2)
           )
           
    ),
    column(4,
           selectInput("skills","Skills",
                       c("ALL",skills)),
           selectInput("names","All Students",
                       c("All students"))
           
    )
    
  ),
  
  fluidRow(
    column(8,
           plotlyOutput("scatter")
    ),
    column(4,
           plotlyOutput("distPlot")
    )
  )
  
  
)