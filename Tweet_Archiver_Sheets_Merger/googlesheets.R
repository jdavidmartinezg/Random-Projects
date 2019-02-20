# El siguiente script busca unificar la base de datos de tweets del proceso de paz en R directamente desde google sheets

#install.packages("googlesheets")


library(googlesheets)
library(dplyr)


#me pedira que ingrese un link al navegador y luego ese link me retornará un código
x = gs_ls()

x %>% glimpse()

#install.packages("sqldf")
library(sqldf)

#x = sqldf('SELECT DISTINCT sheet_title FROM x')


ws <- function(x){
  data_id <- gs_title(x)
  ws = data_id[3]
  return(ws)
}


x$n_ws = sapply(x$sheet_title, ws)



retrieve_data <- function(database, sheet){
  data_id <- gs_title(database)
  
  dataframe <- gs_read(data_id, ws= sheet, col_names = TRUE)
  
  my.names <- dataframe[1,]
  
  colnames(dataframe) <- my.names
  
  dataframe <- dataframe[-1,]
  
  return(dataframe)
}

df1 <- retrieve_data("PAZ(Maraguin1212)*", 2)

#files <- as.list(x$sheet_title)



for (i in 1:length(x$sheet_title)) {
  num_s = x$n_ws[i]
  print(num_s)
  if (num_s  == 1) {
    try(assign(paste("df", paste(i, "1", sep = "_sheet_") ,sep="_"), retrieve_data(x$sheet_title[i], 1)))
  }
  else{
    for (n in 1:as.numeric(num_s)){
      try(assign(paste("df", paste(i, n, sep = "_sheet_") ,sep="_"), retrieve_data(x$sheet_title[i], n)))
    }
  }
}

#AQUI PROCEDEMOS A UNIR TODAS LAS BASES QUE CUMPLAN CON LOS REQUISITOS


dfs = sapply(.GlobalEnv, is.data.frame) 

#dfs

dfs <- as.data.frame(dfs)

dfs$name <- rownames(dfs)



cols = colnames(df_1_sheet_1)

dfs$tweets = NA


#IDENTIFICAR LOS DATA FRAMES QUE CORRESPONDEN A TWEETS

for (i in 1:length(dfs$name)){
  c = colnames(get(dfs$name[i]))
  if (identical(as.vector(c), as.vector(cols)) == TRUE) {
    dfs$tweets[i] = 1
  }
  else{
    dfs$tweets[i] = 0
  }
}


general_dataset <- do.call(rbind, mget(as.vector(dfs$name[dfs$tweets == 1])))

save(general_dataset,file="tweets_peace.Rda")










