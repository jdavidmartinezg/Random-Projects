#Análisis COLFUTURO

#setwd('D:/JD DSEPP/Documentos')

colfuturo <- read.csv("Colfuturo2016.csv", sep=";")
View(colfuturo)

#install.packages('tm')
library(tm)


#Se quitan signos de puntuación
txtclean = gsub("[[:punct:]]", "", colfuturo$Perfil)

#Se quitan números
txtclean = gsub("[[:digit:]]", "", txtclean)

corpus = Corpus(VectorSource(txtclean))

corpus = tm_map(corpus, tolower)

corpus <- tm_map(corpus, PlainTextDocument)

corpus = tm_map(corpus, removeWords, c(stopwords("spanish")))

corpus = tm_map(corpus, content_transformer(stripWhitespace))

corpus <- Corpus(VectorSource(corpus))

tdm <- DocumentTermMatrix(corpus)

colfuturo <- as.matrix(tdm)

colfu <- as.data.frame(colfuturo)

most <- colSums(colfu)

head(most)





sort_most <- sort(most, decreasing=TRUE)

most <- as.data.frame(sort_most)

View(most)

write.table(most ,file = 'colfuturo_freqs.csv', sep=';')





