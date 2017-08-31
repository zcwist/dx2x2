library(shiny)

# Define UI for app that draws a histogram ----
ui <- fluidPage(
  
  # App title ----
  titlePanel("Skill matrix analysis"),
  
  fluidRow(
    column(4,
           #select analysis type
           selectInput("analysisType", "Analysis Type",
                       c("Survey analysis",
                         "Difference analysis"))
    ),
    column(4,
           selectInput("skills","Skills",
                       skills)
    ),
    column(4,
           selectInput("names","student",
                       c("student1","student2")),
           
           sliderInput(inputId = "bins",
                       label = "Number of bins:",
                       min = 1,
                       max = 50,
                       value = 30)
    )
    
  ),
  
  fluidRow(
    column(6,
           plotOutput(outputId = "distPlot")
    ),
    column(6,
           plotOutput(outputId = "distPlot2")
    )
  )
  
  
)

# Define server logic required to draw a histogram ----
server <- function(input, output) {
  
  # Histogram of the Old Faithful Geyser Data ----
  # with requested number of bins
  # This expression that generates a histogram is wrapped in a call
  # to renderPlot to indicate that:
  #
  # 1. It is "reactive" and therefore should be automatically
  #    re-executed when inputs (input$bins) change
  # 2. Its output type is a plot
  output$distPlot <- renderPlot({
    
    x    <- faithful$waiting
    bins <- seq(min(x), max(x), length.out = input$bins + 1)
    
    hist(x, breaks = bins, col = "#75AADB", border = "white",
         xlab = "Waiting time to next eruption (in mins)",
         main = "Histogram of waiting times")
    
  })
  
  output$distPlot2 <- renderPlot({
    
    x    <- faithful$waiting
    bins <- seq(min(x), max(x), length.out = input$bins + 1)
    
    hist(x, breaks = bins, col = "#75AADB", border = "white",
         xlab = "Waiting time to next eruption (in mins)",
         main = "Histogram of waiting times")
    
  })
  
}

# Create Shiny app ----
shinyApp(ui = ui, server = server)