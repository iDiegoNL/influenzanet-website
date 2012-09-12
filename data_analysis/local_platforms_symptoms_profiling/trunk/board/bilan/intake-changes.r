##
# Change detection in intake survey

intake.user = aggregate(id ~ person_id, data=intake, length)

out(freq(intake.user$id), main="Questionnaire intake par participants")

# check person_id = 3453 (N=15) => no change
# check person_id = 2785 (N=6) => no change
# check person_id = 1162 (N=4) => no change

# Changes for each person 
intake.changes = data.frame()
nn = names(intake)
nn = nn[ !nn %in% c("timestamp","id","person_id","age")]
for(person in intake.user$person_id[intake.user$id > 1]) {
   cat("Parsing person",person,"\n")
   ii = intake[ intake$person_id == person,]
   x = sapply(nn, function(v) { length(unique(ii[,v]))-1 })
   x$person_id = person
   x$N = nrow(ii)
   intake.changes = rbind( intake.changes, x)
}

# Changes by question
changes = sapply(nn, function(v) { sum(intake.changes[,v]) })
changes = data.frame(changes)
changes$prop = round(100*changes$changes / nrow(intake.changes),1)
out(changes, main=paste("Changement d'une variable intake par utilisateur N=",nrow(intake.changes)))

