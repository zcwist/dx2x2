library(shiny)
library(plotly)

source("filter.R")

# x1 <- read.csv("x_1.csv")
# x2 <- read.csv("x_2.csv")
# y1 <- read.csv("y_1.csv")
# y2 <- read.csv("y_2.csv")

template <- read.csv("template.csv",head=T,check.names=FALSE)

skills <- colnames(template)[2:length(colnames(template))]

