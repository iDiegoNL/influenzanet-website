source('conf.r')

r = dbQuery('SELECT s.id as person_id, p.* from pollster_results_satisfaction p left join survey_surveyuser s on p.global_id=s.global_id')

r = subset(r, select=-c(global_id, channel, id))
gc()

r$i = 1:nrow(r)

tt = table(r$person_id)
tt = tt[ tt > 1]
tt = names(tt) # garde les person_id en doublon

d = c()
for(id in tt) {
  i = r$i[ r$person_id == id]
  i = i[-length(i)] # 
  d = c(d, i)
}

r = r[ !r$i %in% d,]

tt = table(r$person_id)
if( all(tt == 1) ) {
 cat("OK reponses uniques")
} else {
  stop("Reponse en doublon")
}

write.csv2(r, "satisfaction.csv", row.names=F)