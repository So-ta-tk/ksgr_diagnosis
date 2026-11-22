setwd("C:/Users/gyoum/Desktop/プログラミング練習/others/16typeDiagnosis/score")
library(tidyverse)
library(corrplot)
df<-read.csv("ksgr_scores.csv")
cor(df[,3:10])
corrplot(cor(df[,3:10]))
df <-df |> 
  mutate(Q =質問番号,
         option =選択肢) |> 
  select(,-c("質問番号","選択肢"))
grid_Q = c(1:10)
grid_option = c("A","B","C")

