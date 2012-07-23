
xtitle("GrippeNet.fr - 2012, Symptom survey ", Sys.time(), level=1)

weeks = sort(unique(weekly$yw))
nb.weeks = length(weeks)

###
## Timeliness
##
xbloc("Timeliness")

out(summary(weekly$delay.date), title=i18n('summary_delay'))

graph.open(my.path('weekly_delay_date_hist'), width=700, height=400)
  hist(weekly$delay.date, breaks=100, freq=F, border="white", col=colors.web$blue, xlab=i18n('delay_in_day'), main=i18n('graph_delay'))
  title.sub()
graph.close()

out( round(100*prop.table(table(weekly$delay.date)),2), title=i18n('graph_delay'))

# Vertical barplot for each week
# @param weekly weekly data frame
# @param v variable name
# @param col color
# @param k bar width (height actually, because it's vertical)
# @param h.max max size of a bar in % of the X-axis unit
barplot.byweek = function(weekly, v, col, k=.3, h.max=0.98) {
  ii = aggregate(as.formula(paste("i ~ ",v," + yw")), data=weekly, sum)
  total = aggregate(i ~ yw, data=ii, sum)
  ii = merge(ii, total, by='yw', all.x=T, suffixes=c('','.total'))
  ii$prop = ii$i / ii$i.total
  yw = unique(ii$yw)
  par(las=1)
  plot(c(1,length(yw)+1), range(ii[,v]), type="n", axes=F, xlab="Week",ylab="")
  for(i in 1:length(yw)) {
    w = yw[i]
    r = ii[ ii$yw == w,]
    x = rep(i, nrow(r))
    x2 = i + (r$prop * h.max)
    rect(x, r[,v] - k, x2, r[,v] + k, col=col, border=col)
  }
  axis(1, at=1:length(yw), yw, cex.axis=.7)
  axis(2)
}


#####
# Delay of the previous survey by week
# Does the distribution of delay change with time
###
graph.open(my.path('weekly_delay_bytime'), width=800, height=600)
  barplot.byweek(weekly,'delay.date', col=colors.web$blue)
  title(main=i18n('graph_delay_by_week'))
  title.sub()
graph.close()

ii = table(weekly$weekly.idx)
graph.open(my.path('weekly_least_number_survey'), width=600, height=400)
  barplot(ii, col=colors.web$blue, border=NA, main=i18n('graph_at_least_number_survey'), xlab=i18n('count_of_survey'),ylab=i18n('participants'))
  title.sub()
graph.close()

out(ii, title=i18n('graph_at_least_number_survey'))

tt = tapply(weekly$weekly.idx, weekly$person_id, max)

out(freq(tt), title=i18n('part_by_total_survey'))

ii = table(tt)
graph.open(my.path('weekly_number_survey_person'), width=600, height=400)
  barplot(ii, col=colors.web$blue, border=NA, main=i18n('part_by_total_survey'), xlab=i18n('count_of_survey'), ylab=i18n('participants'))
  title.sub()
graph.close()

ii = 100*prop.table(ii)
graph.open(my.path('weekly_prop_survey_person'), width=600, height=400)
  barplot(ii, col=colors.web$blue, border=NA, main=i18n('prop_part_by_total_survey'), xlab=i18n('count_of_survey'), ylab=i18n('prop_participants'))
  title.sub()
graph.close()

graph.open(my.path('weekly_idx_by_week'), width=800, height=500)
  barplot.byweek(weekly, 'weekly.idx', col=colors.web$green)
  title(main="Number of survey for each participant at each week", ylab="Number of filled survey by participant")
  title.sub()
graph.close()

ii = 100*prop.table(table(weekly$dayofweek))
graph.open(my.path('weekly_dayofweek'), width=700, height=400)
  names(ii) <- c('Sunday','Monday','Tuesday','Wednesday', 'Thursday','Friday','Saturday')
  barplot(ii, col=colors.web$blue, border=NA, main="% of symptom surveys by day of the week", xlab="day of the week", ylab="% of survey")
  title.sub()
graph.close()

out(ii, title="% of survey by day of week")

## By week

# Count of survey by user+week
ii = aggregate(i ~ person_id + yw, data=weekly, sum)
tt = table(ii$i, ii$yw) 
out(tt, title="Number of participants by count of survey in a week")
out(round(100*prop.table(tt, margin=2),1), title="% of participants with this count of survey this week")

## Count of week by user
ii = aggregate(yw ~ person_id, data=ii, length)
out( freq(ii$yw), title="Number of participants by number of week of participation (at least 1 survey)")

tt = table(ii$yw)
graph.open(my.path('weekly_number_week_person'), width=600, height=400)
  barplot(tt, col=colors.web$blue, border=NA, main="Number of participants by count of weeks of participation (overall)")
  title.sub()
graph.close()

graph.open(my.path('weekly_prop_week_person'), width=600, height=400)
  barplot(100*prop.table(tt), col=colors.web$blue, border=NA, main="% of participants by count of weeks of participation (overall)")
  title.sub()
graph.close()

ii = aggregate(i ~ weekly.idx + yw, data=weekly, max)

xbloc(end=T) # end of Timeliness Analysis

xbloc("Symptoms")
###
# Symptomes
###

# Delay from symptome start and reporting
weekly$reporting.delay = as.numeric( weekly$date - weekly$sympt.start)
weekly$reporting.delay[ weekly$reporting.delay < 0] <- NA
weekly$reporting.delay[weekly$reporting.delay > weekly$delay.date ] <- NA
weekly$reporting.delay[ weekly$reporting.delay > nb.weeks*7] <- NA

graph.open(my.path('weekly_reportingdelay_byweek'), width=600, height=400)
  barplot.byweek(weekly, 'reporting.delay', col="blue")
  title(main="Distribution of Reporting delay (cleaned) by week", ylab="Reporting delay (day)")
  title.sub()
graph.close()

# overall symptoms
ss = sympt.aliases[ sympt.aliases != "no.sympt"]
ii = apply(weekly[, ss], 2, sum)
n = sum( weekly$no.sympt == F)
ii = 100*ii / n
names(ii) <- i18n(names(ii))

graph.open(my.path('weekly_reported_sympt_overall'), width=750, height=500)
  mar = par("mar")
  mar[2] = 8
  par(mar=mar, las=1)
  barplot(ii, col=colors.web$blue, horiz=T, cex.names=0.8, xlab="Percentage", main=paste("Reported symptoms by survey (N=",n, round(100*n/nrow(weekly)),"%)"))
  title.sub()
graph.close()
graphics.off()

# Number of reported symptoms overall
graph.open(my.path('weekly_number_sympt_overall'), width=750, height=500)
  ii = apply(weekly[, ss], 1, sum)
  barplot.percent(ii, col="blue", cex.head=0.7)
  title(main="Number of reported symptoms (overall)", xlab="Number of reported symptoms", ylab="Percent")
  title.sub()
graph.close()

# symptome at-least once per person
ii = aggregate(as.list(weekly[, c(sympt.aliases)]), list(person_id=weekly$person_id), sum) # number of symptom by user
ii = ii[, sympt.aliases] > 0 # each symptom as bool (0 or at least once)
n = nrow(ii)
ii = apply(ii, 2, sum)
ii = ii / n

graph.open(my.path('weekly_sympt_perc_once_peruser'), width=750, height=500)
  mar = par("mar")
  mar[2] = 8
  par(mar=mar, las=1)
  names(ii) <- i18n(names(ii))
  barplot(ii, col=colors.web$blue, horiz=T, cex.names=0.8, xlab="Percentage of participant", main=paste("% of user having reported a symptom at least once (N=",n, round(100*n/nrow(weekly)),"%)"))
  title.sub()
graph.close()
graphics.off()

graph.open(my.path('weekly_status_overall'), width=750, height=400)
  barplot.percent(weekly$status, col=colors.web$green, main=paste("Health syndrom overall surveys N=",nrow(weekly)), cex.names=0.8)
  title(ylab="Percentage")
  title.sub()
graph.close()

# Symptom by week
ii = aggregate(as.list(weekly[, c('i', sympt.aliases)]), list(yw=weekly$yw), sum) # number of symptom by week
n = sqrt(length(sympt.aliases))

graph.open(my.path('weekly_sympt_byweek_overall'), width=800, height=900)
par(mfrow=c(ceiling(n), floor(n)), mar=c(2.1,2.1,1,1), las=1)
for(sympt in sympt.aliases) {
  plot(range(ii$yw), c(0,1), type="n", bty="l")
  p = ii[,sympt] / ii$i
  points(ii$yw, p, type="o", lwd=2, pch=19, cex=0.8, col=colors.web$blue)
  title(main=i18n(sympt), line=-1.5, col.main=colors.web$blue)
}
graph.close()
graphics.off() #reset par()

# Aggregate weekly rows by a group for each modality of a variable and
# calculate proportion of each value by group
weekly.prop = function(weekly, var, group) {
  ii = aggregate(as.formula(paste("i ~ ",var,"+", group)), data=weekly, sum)
  total = aggregate(as.formula(paste("i ~ ",group)), data=weekly, sum)
  ii = merge(ii, total, by=group, suffixes=c('','.total'))
  ii$prop = ii$i / ii$i.total
  ii
}

# Graph by Health status (Influweb)
graph.health.status = function(weekly, group, xlab="") {
  ii = weekly.prop(weekly, 'status', group)
  status = sort(unique(ii$status))
  col = my.colors(length(status))
  plot(range(ii[,group]), c(0,1.2), type="n", axes=F, xlab=xlab, ylab="Percent of survey")
  for(i in status) {
    r = ii[ ii$status == i,]
    points(r[,group], r$prop, col=col[ match(i, status) ], type="o", lwd=2, pch=19, cex=0.8)
  }
  w = sort(unique(ii[,group])) 
  axis(1, at=w, w, cex.axis=0.8)
  axis(2, las=1)
  legend("top", legend=status, col=col, lwd=2, lty=1, pch=19, pt.cex=0.8, horiz=T, bty="n", cex=0.7)
  title.sub()
}

graph.open(my.path('weekly_status_byweek_overall'), width=800, height=600)
 graph.health.status(weekly, 'yw', 'Weeks')
 title(main="Health status (Influweb) by week (on total survey by week)")
graph.close()


graph.open(my.path('weekly_status_byindex_overall'), width=800, height=600)
 graph.health.status(weekly, 'weekly.idx', 'Number of filled survey by participant')
 title(main="Health status (Influweb) by number of filled survey")
graph.close()

xbloc(end=T)

xbloc("Context")

graph.open(my.path('weekly_same_episode'), width=400, height=400)
  barplot.percent(weekly$same.episode, col=colors.web$green, main=paste("Same episode N=",nrow(weekly)), cex.names=0.8)
  title(ylab="Percentage")
  title.sub()
graph.close()

graph.open(my.path('weekly_sympt_sudden'), width=400, height=400)
  n = sum(!is.na(weekly$sympt.sudden))
  barplot.percent(weekly$sympt.sudden, col=colors.web$green, main=paste("Symptoms came suddenly N=",n), cex.names=0.8)
  title(ylab="Percentage")
  title.sub()
graph.close()

graph.open(my.path('weekly_take_temp'), width=500, height=400)
  n = sum(!is.na(weekly$take.temp))
  y = factor(weekly$take.temp, 0:2, c('Yes','No','Dont know'))
  barplot.percent(y, col=colors.web$green, main=paste("Did you take your temperature? N=",n), cex.names=0.8)
  title(ylab="Percentage")
  title.sub()
graph.close()

graph.open(my.path('weekly_location'), width=500, height=400)
  n = sum(!is.na(weekly$location))
  y = factor(weekly$location, 0:2, i18n(survey_labels('weekly','location')))
  barplot.percent(y, col=colors.web$green, main=paste("Location  N=",n), cex.names=0.8)
  title(ylab="Percentage")
  title.sub()
graph.close()


N.with.sympt = sum(!weekly$no.sympt) 

graph.open(my.path('weekly_contactmed'), width=750, height=400)
  vv = survey_labels('weekly','contactmed')
  ii = apply(weekly[!weekly$no.sympt, vv], 2, sum)
  ii = ii / N.with.sympt
  names(ii) <- i18n(names(ii))
  barplot(ii, col=colors.web$green, main=paste("Contact with telephone/web medical service ? N=",N.with.sympt), cex.names=0.8)
  title.sub()
graph.close()

graph.open(my.path('weekly_visit'), width=750, height=400)
  vv = survey_labels('weekly','visit')
  ii = apply(weekly[!weekly$no.sympt, vv], 2, sum)
  ii = ii / N.with.sympt
  names(ii) <- i18n(names(ii))
  barplot(ii, col=colors.web$green, main=paste("Visit to medical service ? N=",N.with.sympt), cex.names=0.8)
  title.sub()
graph.close()

graph.open(my.path('weekly_visit_gp_status'), width=750, height=400)
  barplot(tt, beside=T, legend.text=c('No','Yes'),main=i18n("visit_to_GP"), col=unlist(colors.web), border=NA, args.legend=list(x="top",horiz=T))
graph.close()

graph.open(my.path('weekly_hospitalization'), width=400, height=400)
  n = sum(!is.na(weekly$hospitalization[!weekly$no.sympt]))
  miss = round(100*(N.with.sympt - n)/ N.with.sympt)
  y = factor(weekly$hospitalization[!weekly$no.sympt], 0:1, i18n(c('No','Yes'))) 
  barplot.percent(y, col=colors.web$green, main=paste(i18n("Hospitalization")," N=",N.with.sympt,", ",i18n("missing"),"=",miss,"%"), cex.names=0.8)
  title.sub()
graph.close()

graph.open(my.path('weekly_medication'), width=750, height=400)
  vv = survey_labels('weekly','medic')
  ii = apply(weekly[!weekly$no.sympt, vv], 2, sum)
  ii = 100*ii / N.with.sympt
  names(ii) <- i18n(names(ii))
  barplot(ii, col=colors.web$green, main=paste("Visit to medical service ? N=",N.with.sympt), cex.names=0.8, las=1)
  title.sub()
graph.close()

graph.open(my.path('weekly_antiviro'), width=400, height=400)
  i = weekly$medic.antiviral > 0
  vv = survey_labels('weekly','antiviro')
  ii = apply(weekly[!i, vv], 2, sum)
  ii = 100*ii / sum(i)
  names(ii) <- i18n(names(ii))
  y = barplot(ii, col=colors.web$green, cex.names=0.8)
  barplot.headtext(y, ii, paste(round(ii),"%"), .7)
  title(main=i18n('antiviro'))
  title.sub()
graph.close()

graph.open(my.path('weekly_antibio'), width=400, height=400)
  i = weekly$medic.antibio > 0
  vv = survey_labels('weekly','antibio')
  ii = apply(weekly[!i, vv], 2, sum)
  ii = 100*ii / sum(i)
  names(ii) <- i18n(names(ii))
  y = barplot(ii, col=colors.web$green, cex.names=0.8)
  barplot.headtext(y, ii, paste(round(ii),"%"), .7)
  title(main=i18n('antibio'))
  title.sub()
graph.close()


graph.open(my.path('weekly_website'), width=400, height=400)
  n = sum(!is.na(weekly$website[!weekly$no.sympt]))
  miss = round(100*(N.with.sympt - n)/ N.with.sympt)
  barplot.percent(weekly$website[!weekly$no.sympt], col=colors.web$green, main=paste("visit to a medical website  N=",n, "missing=",miss,"%"), cex.names=0.8)
  title.sub()
graph.close()

graph.open(my.path('weekly_sympt_cause'), width=750, height=400)
  n = sum(!is.na(weekly$sympt.cause[!weekly$no.sympt]))
  miss = round(100*(N.with.sympt - n)/ N.with.sympt)
  y = factor(weekly$sympt.cause[!weekly$no.sympt], 0:5, i18n(survey_labels('weekly','sympt.cause')))
  barplot.percent(y, col=colors.web$green, main=paste("Perceived cause of symptoms  N=",n, "missing=",miss,"%"), cex.names=0.8)
  title.sub()
graph.close()

graph.open(my.path('weekly_sympt_cause_bystatus'), width=650, height=950)
  ii = weekly.prop(weekly[ !weekly$no.sympt,], 'sympt.cause', 'status')
  status = sort(unique(ii$status))
  par(mfrow=c(length(status), 1), las=1)
  for(i in status) {
    r = ii[ ii$status == i,]
    if(nrow(r) == 0) {
      plot(c(0,1),c(0,1), type="n")
    }
    y = barplot(r$prop, col=colors.web$green, names.arg=i18n(survey_labels('weekly','sympt.cause')), ylim=c(0,1.05))
    barplot.headtext(y, r$prop, paste(round(100*r$prop),"%"), .7)
    title(main=paste("Perceived cause for Health status", i18n(i)))
  }
graph.close()

graph.open(my.path('weekly_change_routine'), width=600, height=400)
  n = sum(!is.na(weekly$change.routine[!weekly$no.sympt]))
  miss = round(100*(N.with.sympt - n)/ N.with.sympt)
  y = factor(weekly$change.routine[!weekly$no.sympt], 0:2, i18n(survey_labels('weekly','change.routine')))
  barplot.percent(y, col=colors.web$green, main=paste("Change routine  N=",n, "missing=",miss,"%"), cex.names=0.8)
  title.sub()
graph.close()

graph.open(my.path('weekly_off_work'), width=600, height=400)
  i = !weekly$no.sympt & weekly$change.routine == 2 # routine off
  i[is.na(i)] <- FALSE
  n = sum(!is.na(weekly$off.work[i]))
  N = sum(i)
  miss = round(100*(N - n)/ N)
  y = factor(weekly$off.work[i], 0:3, i18n(c('Yes','No','','Other')) )
  barplot.percent(y, col=colors.web$green, main=paste("Still off work  N=",n, "missing=",miss,"%"), cex.names=0.8)
  title.sub()
graph.close()

graph.open(my.path('weekly_off_work_delay'), width=750, height=400)
  y = factor(weekly$off.workdelay[i], 0:7, c('1','2','3','4','5','6-10','11-15','>15'))
  n = sum(!is.na(weekly$off.work[i]))
  miss = round(100*(N - n)/ N)
  barplot.percent(y, col=colors.web$green, main=paste("off work delay (day)  N=",n, "missing=",miss,"%"), cex.names=0.8, ylab="Percent")
  title.sub()
graph.close()

graph.open(my.path('weekly_household_flu'), width=600, height=500)
  y = factor(weekly$household.flu, 0:8, c('0','1','2','3','4','5','>6','dkn','empty'))
  n = sum(!is.na(y))
  N = nrow(weekly)
  miss = round(100*(N - n)/ N)
  barplot.percent(y, col=colors.web$green, main=paste("Other member in househould with flu-like N=",n, "missing=",miss,"%"), cex.names=0.8, cex.head=0.7, ylab="Percent")
  title.sub()
graph.close()


graph.open(my.path('weekly_contact_fu'), width=600, height=500)
  y = factor(weekly$household.meet, 0:8, c('0','1','2','3','4','5','>6','dkn','empty'))
  n = sum(!is.na(y))
  N = nrow(weekly)
  miss = round(100*(N - n)/ N)
  barplot.percent(y, col=colors.web$green, main=paste("Contacts with people having flu-like (except househould)\nN=",n, "missing=",miss,"%"), cex.names=0.8, cex.head=0.7, ylab="Percent")
  title.sub()
graph.close()


xbloc(end=T)

#ww = weekly[ order(weekly$person_id, weekly$timestamp), c('person_id','timestamp','no.sympt','status','same.episode')]
#episodes = data.frame()
#pp = unique(ww$person_id)
#for(person in pp) {
# d = ww[ ww$person_id == person,]
# n = nrow(d)
# i = 1
# while(i <= n) {
#   if( d[i, no.sympt])
#   i = i + 1
# }
#}
#