# 
source('conf.r')

# estimate count of syndrom for a given week
# active user is counted on the 21 previous days of the week

# date of the end of calculation period
# used
week.point = ISOYearWeek(Sys.Date() - 7) # previous week 
date.max = WeekStart(week.point) + 6 # last day we should include participant having a onset (dont count as active after that date)
date.point = date.max # delay from this date for active participant
exclude.same = F  # should exclude when reported as "it is the same episod" (counted as active but not the syndrom report)

weekly = survey_load_results("weekly", c('timestamp', 'same.episode','sympt.start','fever.start') )

weekly$date = as.Date(weekly$timestamp) # date

#participants = aggregate(id ~ person_id, data=weekly, length)
#p = aggregate(date ~ person_id, data=weekly, min)
#names(p)[2] <- 'first.survey'
#participants = merge(participants, p, by='person_id')
#p = aggregate(date ~ person_id, data=weekly, max)
#names(p)[2] <- 'last.survey'
#participants = merge(participants, p, by='person_id')

health.status = dbQuery('SELECT pollster_results_weekly_id as id, status FROM pollster_health_status')
weekly = merge(weekly, health.status, by='id')

weekly = weekly[ weekly$date >= date.point - 21,] # keep only 21 days of surveys

weekly$sympt.start = as.Date(as.character(weekly$sympt.start))
weekly$fever.start = as.Date(as.character(weekly$fever.start))

# first argument wich is not NA
coalesce <-function(x) {
  x[ min(which(!is.na(x))) ]
}

# onset = first available date from symptom start, fever.start and survey date
weekly$onset = as.Date(apply(weekly[, c('sympt.start', 'fever.start', 'date') ], 1, coalesce))

# take account of the onset date for the week
weekly$yw = ISOYearWeek(weekly$onset)

# get intake, only keep the last available intake
intake = survey_load_results("intake", c('timestamp','code_com'))
u = aggregate(timestamp ~ person_id, data=intake, max)
intake = merge(u, intake, by=c('person_id','timestamp'), all.x=T)
intake = subset(intake, select=-c(timestamp)) # dont need timestamp of intake any more

# count of number of people having at least one time the symptom in the week
syndrom = c("COMMON-COLD"="cold","GASTROINTESTINAL"="gastro", "ILI"="ili","NO-SYMPTOMS"="no.sympt", "NON-INFLUENZA"="other")

# make indicators variables (with pretty names)
for(i in 1:length(syndrom)) {
  n = names(syndrom)[i]
  weekly[, syndrom[i] ] = ifelse( weekly$status == n, 1, 0)
}

# exclude when onset date is after our maximum date (end of the week we want to estimate)
weekly = weekly[ weekly$onset <= date.max,]

weekly$active = 1 # at least one activity by survey

# active participant = having at least one survey on 3 weeks
active = aggregate(active ~ person_id, data=weekly, sum)
active$active = as.integer(active$active > 0) # only active once in the period
active = merge(active, intake, by='person_id', all.x=T) # get the geo code

# active participant for the last week (within 3 previous weeks)
active.week = aggregate(active ~ code_com, data=active, sum)

if(exclude.same) {
  # remove weekly where user said it was the same episode from the last visit
  weekly = weekly[ is.na(weekly$same.episode) | weekly$same.episode > 0,]
}

# now we only take account of the week of interest

weekly = weekly[ weekly$yw == week.point,] # only keep our week of interest

# Count number of syndrom by user and by week
count = aggregate(as.list(weekly[, syndrom]), list(person_id=weekly$person_id), sum)

count = merge(count, intake, by='person_id', all.x=T) # get the geo code for each user

# make syndrom exclusive in a week ?
# nop now

count[,syndrom] = as.integer(count[,syndrom] > 0) # syndrom counted only once for each user

# aggregate by geo code
count.week = aggregate( as.list(count[,syndrom]), list(code_com=count$code_com), sum)

ii = merge(active.week, count.week, by='code_com', all.x=T)

ok = grepl("([0-9]{2}|2[AB])[0-9]{3}", ii$code_com)

if( !all(ok) ) {
  cat("Non attribué a une commune\n")
  print(ii[!ok,])
}

ii = ii[ok,]

na <-function(x) {  
  x[is.na(x)] <- 0 
  x
}

# Update incidence for this week
dbQuery("DELETE FROM incidence_com where yw=",week.point)

query = "INSERT INTO incidence_com (count_ili, count_cold, count_gastro, count_nosympt, active, yw, code_com) VALUES"
qq = paste("(",na(ii$ili),",",na(ii$cold),",",na(ii$gastro),",",na(ii$no.sympt),",",ii$active,",",week.point,",'",ii$code_com,"')",sep='')

query = paste(query, paste(qq, collapse=','))

dbQuery(query)

# Update week index table
w = dbQuery("SELECT yw from incidence_yw where yw=",week.point)
if(nrow(w) == 0) {
  dbQuery("INSERT INTO incidence_yw VALUES (",week.point,")")
}