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
           
           #select survey
           selectInput("surveyID", "Survey no.",
                       c(1,2),multiple = TRUE,selected = 1)
    ),
    column(4,
           selectInput("skills","Skills",
                       c("ALL",skills))
    ),
    column(4,
           selectInput("names","All Students",
                       c("All students")),
           
           sliderInput(inputId = "bins",
                       label = "Number of bins:",
                       min = 1,
                       max = 50,
                       value = 30)
    )
    
  ),
  
  fluidRow(
    column(6,
           plotlyOutput("scatter")
    ),
    column(6,
           plotOutput(outputId = "distPlot2")
    )
  )
  
  
)