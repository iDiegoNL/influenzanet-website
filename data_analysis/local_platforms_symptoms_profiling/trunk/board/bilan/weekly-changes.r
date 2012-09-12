
w = aggregate(i ~ yw + person_id, data=weekly, sum)

w = w[ w$i > 1,]

weekly.changes = data.frame()
nn = names(weekly)
nn = nn[ !nn %in% c("timestamp","id","person_id","yw","date","delay.date","delay","delay.first","dayofweek")]

for(row in 1:nrow(w)) {
   person_id = w$person_id[row]
   yw = w$yw[row]
   cat("Parsing row",row,"\n")
   ii = weekly[ weekly$person_id == person_id & weekly$yw == yw,]
   x = sapply(nn, function(v) { length(unique(ii[,v]))-1 })
   x$person_id = person_id
   x$yw = yw
   x$N = nrow(ii)
   weekly.changes = rbind( weekly.changes, x)
}
