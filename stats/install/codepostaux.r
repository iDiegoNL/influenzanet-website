source('conf.r')
r = read.csv2('code-postaux_v3.csv')

lev = levels(r$article)

i = (lev != '') & (lev != "L'")
lev[i] = paste(lev[i]," ")

levels(r$article) <- lev

r$article[ is.na(r$article)] = ""

r$titre = paste(r$article, r$title, sep='')

r = r[,c('insee','code_post','titre')]
r = replace.names(r, "zip"="code_post","code"="insee","title"="titre")
if( is.integer(r$zip) ) {
  r$zip = sprintf("%05d", r$zip)
}

r$title = gsub("'","''", r$title, fixed=T)

qq = paste("('",r$zip,"','",r$code,"','",r$title,"')",sep='')
query = paste('BEGIN TRANSACTION;\nTRUNCATE TABLE municipal_codes;\nINSERT INTO municipal_codes (zip,code,title) VALUES ',paste(qq,collapse=','),";\n")
write(query, file="municpal_codes.sql")


