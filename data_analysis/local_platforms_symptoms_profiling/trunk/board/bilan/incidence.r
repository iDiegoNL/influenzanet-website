
coalesce <-function(x) {
  x[ min(which(!is.na(x))) ]
}

# weekly (person_id,status, date, onset, same.episode)
# intake = data.frame(person_id, code.geo)
# week.point yw
# code.geo column of the geographic code used to aggregate data
calc.incidence = function(weekly, intake, week.point, code.geo='code_com', exclude.same=F, delay.active=21) {

  date.max = as.Date(WeekStart(week.point) + 6) # last day we should include participant having a onset (dont count as active after that date)
  date.point = date.max # delay from this date for active participant

  cat("date.max", date.max, "\n")

  weekly = weekly[ weekly$date >= (date.point - delay.active),] # keep only days within active periods
  
  cat("weekly in period",nrow(weekly),"\n")
  
  syndrom = c(
    "COMMON-COLD"="cold",
    "GASTROINTESTINAL"="gastro", 
    "ILI"="ili",
    "NO-SYMPTOMS"="no.sympt",
     "NON-INFLUENZA"="other"
  )

  # make indicators variables (with pretty names)
  for(i in 1:length(syndrom)) {
    n = names(syndrom)[i]
    weekly[, syndrom[i] ] = ifelse( weekly$status == n, 1, 0)
  }

  # exclude when onset date is after our maximum date (end of the week we want to estimate)
  weekly = weekly[ weekly$onset <= date.max,]
  
  cat(nrow(weekly)," weekly onset <= date.max\n")

  weekly$active = 1 # at least one activity by survey
  
  # active participant = having at least one survey on 3 weeks
  active = aggregate(active ~ person_id, data=weekly, sum)
  active$active = as.integer(active$active > 0) # only active once in the period
  active = merge(active, intake, by='person_id', all.x=T) # get the geo code

  # active participant for the last week (within 3 previous weeks)
  active.week = aggregate(as.formula(paste("active ~ ",code.geo)), data=active, sum)
  
  if(exclude.same) {
    cat("exclude.same activated\n")
    # remove weekly where user said it was the same episode from the last visit
    weekly = weekly[ is.na(weekly$same.episode) | weekly$same.episode > 0,]
  }

  # now we only take account of the week of interest
  
  cat("nrow=",  nrow(weekly),"\n")
  str(weekly)
  print(table(weekly$yw))
  
  weekly = weekly[ weekly$yw == week.point, ] # only keep our week of interest

  cat(nrow(weekly)," weekly for week ",yw,"\n")

  # Count number of syndrom by user and by week
  count = aggregate(as.list(weekly[, syndrom]), list(person_id=weekly$person_id), sum)
  
  count = merge(count, intake, by='person_id', all.x=T) # get the geo code for each user

  # make syndrom exclusive in a week ?
  # nop now
  
  count[,syndrom] = as.integer(count[,syndrom] > 0) # syndrom counted only once for each user

  # aggregate by geo code
  agg = list(count[, code.geo])
  names(agg) <- code.geo
  count.week = aggregate( as.list(count[,syndrom]), agg, sum)

  ii = merge(active.week, count.week, by=code.geo, all.x=T)
  ii
}

min.date = min(weekly$date) - 21

ww = weekly[, c('person_id','status', 'date', 'onset', 'same.episode', 'yw', 'sympt.start', 'fever.start', 'weekly.idx')] 

# delete date in future
ww$sympt.start[ ww$sympt.start > ww$timestamp] <- NA
ww$fever.start[ ww$fever.start > ww$timestamp] <- NA
# delete toooooo old dates

ww$sympt.start[ ww$sympt.start < min.date ] <- NA
ww$fever.start[ ww$fever.start < min.date ] <- NA

ww$onset = as.Date(apply(ww[, c('sympt.start', 'fever.start', 'date') ], 1, coalesce))

weekly_incidence = function(ww, intake) {
  weeks = unique(ww$yw)
  inc = data.frame()
  for(yw in weeks) {
    ii = calc.incidence(
        ww,
        intake[,c('person_id','code_reg')], 
        week.point=yw, 
        code.geo='code_reg')
    ii$yw = yw
    inc = rbind(inc, ii)
  }

  inc = aggregate(cbind(active,cold,gastro,ili,no.sympt,other) ~ yw, data=inc, sum, na.rm=T)
  
  vv = c('cold','gastro','ili','no.sympt','other')
  for(v in vv) {
    inc[,paste('prop.',v,sep='')] = 100*inc[,v] / inc$active
  }

  inc
}

inc = weekly_incidence(ww, intake)
inc.1 = weekly_incidence(ww[ ww$weekly.idx > 1,], intake)

weekly_graph = function(fn, inc, main) {
  graph.open(my.path(fn), width=900, height=800)
    par(mfrow=c(2,1),las=1)
    par(mar=c(.1,4,3,1))
    pp = paste("prop.",vv,sep="")
    colors = my.colors(length(vv))
    names(colors) <- pp
    ylim = max(inc[,pp])*1.15
    plot(range(inc$yw), c(0,ylim), type="n", ylab="% Syndrom /active participants", xlab="", bty="l",axes=F)
    for(v in pp) {
      points(inc$yw, inc[,v], type="o", col=colors[v], lwd=2, pch=19)
    }
    legend("top", legend=vv, col=colors, lwd=2, pch=19, horiz=T, bty="n")
    axis(2, cex.axis=.9)
    axis(1,at=unique(inc$yw), labels=F)
    title(main=main, cex=1)
    par(mar=c(4,4,1,1))
    plot(range(inc$yw), range(inc$active), type="n", bty="l",axes=F,xlab="Weeks", ylab="Number of active particpants")
    abline(h=seq(1000,3000,by=1000), col="grey")
    points(inc$yw, inc$active, type="h", lwd=5)
    axis(2, cex.axis=.9)
    axis(1,at=unique(inc$yw), inc$yw %% 100)
  graph.close()
}

weekly_graph('incidence_weekly', inc,"Incidence / All surveys")
weekly_graph('incidence_weekly_withoutfirst', inc.1, "Incidence / Without first survey")

graph.open(my.path('incidence_ili_compare_method'), width=800, height=600)
  plot(range(inc$yw), range(inc.1$prop.ili, inc$prop.ili), type="n", xlab="weeks", ylab="% ILI / Active participants", las=1)
  points(inc$yw, inc$prop.ili, type="o", col="blue", lwd=2, pch=19, cex=.8)
  points(inc.1$yw, inc.1$prop.ili, type="o", col="green", lwd=2, pch=19, cex=.8)
  legend("top", c('All surveys','Without first survey'), col=c('blue','green'),lwd=2, pch=19, cex=.8, horiz=T)
graph.close()
