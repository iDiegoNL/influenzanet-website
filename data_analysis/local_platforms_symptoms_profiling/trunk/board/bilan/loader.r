###
# Loading Data (and recoding)
###

age.breaks = c(0, 18, 30, 40, 50, 60,70, 200)

# intake data
intake = survey_load_results("intake", unique(c('code_com','timestamp', names(epiwork.tables$intake$aliases))), geo=c('reg','dep'))

intake$age = calc.age(intake$date.birth) # @see share/lib/survey
intake$gender = factor(intake$gender, c(0,1), i18n(c('male','female')))
intake$vacc.curseason  = factor(intake$vacc.curseason, 0:2, i18n(c('Yes','No','DNK')))
intake$vacc.lastseason = factor(intake$vacc.lastseason, 0:2, i18n(c('Yes','No','DNK')))
intake$vacc.date = as.Date(intake$vacc.date)
intake$vacc.delay = difftime(intake$timestamp, as.POSIXct(intake$vacc.date), units="days")

# Intake change detection
# source('bilan/changes.r')

# keep only last survey
u = aggregate(timestamp ~ person_id, data=intake, max)
intake = merge(u, intake, by=c('person_id','timestamp'), all.x=T)

rm(u)

gc()

intake$age.cat = cut.age(intake$age, age.breaks) 

pop = read.csv2(share.data.path('pop_reg_age5.csv'),header=T)

year = 2012
age.min = 20
pop = pop[ pop$age.min >= age.min,]
pop = pop[ pop$year == year,]
pop$age.max[is.na(pop$age.max)] = pop$age.min[is.na(pop$age.max)]
pop$cat.min = cut.age(pop$age.min, age.breaks)
pop$cat.max = cut.age(pop$age.max, age.breaks)
stopifnot( all(pop$cat.min == pop$cat.max))

pop = replace.names(pop, "age.cat"="cat.min")

pop.totale = aggregate(cbind(all,male,female) ~ age.cat, data=pop, sum)
pop.reg = aggregate(cbind(all,male,female) ~ age.cat + code_reg, data=pop,sum)

weekly = survey_load_results("weekly", c('timestamp', names(epiwork.tables$weekly$aliases)))

# recode symptomes and get health status
weekly = recode.weekly(weekly)

# recoding
weekly$website = factor(weekly$website, 0:1, i18n(c('No','Yes')))
weekly$hopitalization = factor(weekly$hopitalization, 0:1, i18n(c('No','Yes')))
weekly$sympt.start = as.Date(weekly$sympt.start)
weekly$sympt.end = as.Date(weekly$sympt.end)
weekly$fever.start = as.Date(weekly$sympt.end)

gc() # clean memory


# get delay from the previous survey and a survey index for each user 
ww = weekly[, c('id','person_id','timestamp','date')]

ww = ww[ order(ww$person_id, ww$timestamp),]

ww$delay = NA
ww$delay.date = NA
ww$delay.first = NA
ww$idx = NA
idx = 0
for(p in unique(ww$person_id)) {
 cat(sprintf(round(100* idx/nrow(ww)),fmt="%-2d"),"\r")
 i = ww$person_id == p
 ww$idx[i] = 1:sum(i)
 # delai en jour fractionnaire
 d = ww$timestamp[i]
 d = c(NA, as.numeric(diff(d))/(3600*24))
 ww$delay[i] = d
 # delai en jour julien
 d = as.numeric(ww$date[i])
 first = d[1]
 d = c(NA, diff(d))
 ww$delay.date[i] = d
 d = ww$date[i] - first
 ww$delay.first[i] = d
 idx = idx + 1
}
cat("\n")

ww = replace.names(ww, "weekly.idx"="idx")

#
# delay.date = delay in julian days
# delay = delays in 24h-period 
# delay.first = delay from the first survey (in julian day)
weekly = merge(weekly, ww[,c('id','delay','delay.date','weekly.idx', 'delay.first')], by='id',all.x=T)

# index for counting rows
weekly$i = 1 # always 1

weekly$dayofweek = as.numeric(format(weekly$date,"%w"))

age.categories = data.frame(age.cat=levels(intake$age.cat), order=1:nlevels(intake$age.cat))

fn = paste('data/grippenet-',Sys.Date(),'-',paste(sample(c(letters,LETTERS), 8, replace=T), collapse=''),'.RData',sep='')
save(list=c('intake','weekly','age.breaks','pop.totale','pop.reg','age.categories'), file=fn)