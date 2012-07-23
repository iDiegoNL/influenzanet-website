
source('conf.r')

target.year = 2012
source.year = 2009
fn = 'insee_pop_legale_2009.csv'

r = read.csv2('insee_pop_legale_2009.csv', header=T)

n = names(r)
n[ n == "Code.région" ] <- 'code_reg'
n[ n == "Code.département"] <- 'code_dep'
n[ n == 'Code.commune' ] <- 'code_com'
n[ n == "Population.municipale"] <- "pop.municipale"
n[ n==  "Population.totale"] <- 'pop.totale'
names(r) <- n

r$pop.municipale = as.numeric(gsub(" ", "", as.character(r$pop.municipale)))
r$pop.totale = as.numeric(gsub(" ", "", as.character(r$pop.totale)))

r$code_reg = factor(sprintf("%02d", r$code_reg))

# recode departement avec un zero initial
lev = levels(r$code_dep)
i = lev %in% c("2A","2B")
lev[!i] = ifelse(nchar(lev[!i]) < 2, sprintf("%02d",as.numeric(lev[!i])) , lev[!i])
levels(r$code_dep) <- lev

r$outremer = !r$code_dep %in% c( sprintf("%02d", c(01:19, 21:96)),"2A","2B") 

r$metropole = !r$outremer

## check() -> a verfier avec la page de la population légale INSEE http://www.insee.fr/fr/ppp/bases-de-donnees/recensement/populations-legales/france-departements.asp
sum(r$pop.municipale)

sum(r$pop.municipale[r$metropole])

r$insee = paste( ifelse( r$outremer, substr(as.character(r$code_dep),1,2), as.character(r$code_dep)), sprintf("%03d", r$code_com), sep='')

dbQuery("INSERT INTO pop_update_log (year, source_year, comment, date) values (",target.year,",",source.year,",'",fn,"',now())")

dbQuery('DELETE FROM pop_com where year=',target.year)

query = paste("('",r$insee,"',",target.year,",",r$pop.municipale,")",sep='')
query = paste(query, collapse=',')
query = paste("INSERT INTO pop_com (code_com,year,population) VALUES ", query)
dbQuery(query)

dbQuery('DELETE FROM pop_dep where year=',target.year)
pop_dep = aggregate(pop.municipale ~ code_dep, data=r, sum)
query = paste("('",pop_dep$code_dep,"',",target.year,",",pop_dep$pop.municipale,")",sep='')
query = paste(query, collapse=',')
query = paste("INSERT INTO pop_dep (code_dep,year,population) VALUES ", query)
dbQuery(query)

dbQuery('DELETE FROM pop_reg where year=',target.year)
pop_reg = aggregate(pop.municipale ~ code_reg, data=r, sum)
query = paste("('",pop_reg$code_reg,"',",target.year,",",pop_reg$pop.municipale,")",sep='')
query = paste(query, collapse=',')
query = paste("INSERT INTO pop_reg (code_reg,year,population) VALUES ", query)
dbQuery(query)

