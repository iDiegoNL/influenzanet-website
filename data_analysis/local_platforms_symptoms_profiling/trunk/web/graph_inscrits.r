source('conf.r')

# get users 
users = dbQuery("SELECT id, last_login, date_joined from safe_users where is_active=true")

# get intake questionnaires
intake = survey_load_results("intake", c('timestamp','code_com'))

intake$day = as.Date(intake$timestamp)
                                                
# user by day
users$day = as.Date(users$date_joined)
user_date = aggregate(id ~ day, data=users, length)
user_date = replace.names(user_date, "user"="id")

# participant
ii = aggregate(day ~ person_id, data=intake, min) # first questionnaire filled up by a user
ii = aggregate(person_id ~ day, data=ii, length) # count by day
ii = replace.names(ii, intake="person_id")
user_date = merge(user_date, ii, by='day', all.x=T)

# count of first intake survey by day
user_date = user_date[ order(user_date$day),]

dates = data.frame(day=seq.Date(from=min(user_date$day), to=max(user_date$day), by=1))

user_date = merge(dates, user_date, all.x=T)
user_date$user[ is.na(user_date$user) ] <- 0
user_date$intake[ is.na(user_date$intake) ] <- 0

# cumulative count
user_date$cum[!is.na(user_date$user)] = cumsum(user_date$user[!is.na(user_date$user)])
user_date$intake[!is.na(user_date$intake)] = cumsum(user_date$intake[!is.na(user_date$intake)]) # number of cumulated participants

user_date = user_date[ user_date$day > ( Sys.Date() - 30 ),]


graph.open(my.path('inscrits'), width=600, height=400)
  axis.col = "darkgrey" 
  u = user_date
  par(las=1, cex=.8, mar=c(5,4,.5,.5))
  max.cum = max(u$cum, u$intake, na.rm=T)
  ymax = max.cum * 1.15
  plot(range(u$day), c(0, ymax), type="n", xlab="Date", ylab=i18n("number_of_person"), axes=F, sub=sub.text, font.sub=3, cex.sub=.8) 
  #points(u$day, u$cum, type="o", col=colors.web$green, lwd=2, pch=19, cex=1.3)
  points(u$day, u$intake, type="o", col=colors.web$blue, lwd=2, pch=19, cex=1.3)

  ticks = axTicks(2)
  ticks = ticks[ floor(ticks) == ticks ]
  axis(2, at=ticks, col=axis.col)
  axis(1, at=seq(min(u$day), max(u$day), by=1), labels=F, , col=axis.col) # premier quadrillage
  
  monday = u$day[ as.numeric(format(u$day, format="%w")) == 1 ]
  ticks = axTicks(1)
  axis(1, at=ticks, labels=format(as.Date(ticks, origin="1970-01-01"), format="%d/%m"), col=axis.col)
  box(bty="l", col=axis.col)
  legend("topleft", i18n('graph.participants'), col=c(colors.web$blue), lwd=2, cex=.9, bty="n") 
  
  h = max.cum * 0.1
	
  start.test = as.Date('2012-01-09')
  txt = "Tests internes"
  if(min(u$day) <= (start.test - 1) ) {
	y = min(u$cum)
	text(start.test, y + h*1.1 , txt, pos=4, offset=-.2, col=axis.col)
	arrows( start.test, y + h - 1, start.test, y+1, length=.1, col=axis.col, lwd=2)
  }
  start.invs = as.Date('2012-01-18')
  txt = "Tests \U00E9largis"
  if(min(u$day) < (start.invs - strwidth(txt) - 1)) {
	y = 59
	text(start.invs, y + h*1.1, txt, pos=2, offset=-.2, col=axis.col)
	arrows( start.invs, y + h - 1, start.invs, y + 1, length=.1, col=axis.col, lwd=2)
  }
  if(Sys.Date() > as.Date('2012-01-24')) {
	  start.gpn = as.Date('2012-01-25')
	  txt = "Lancement de Grippenet"
	  if(min(u$day) < (start.gpn - strwidth(txt) - 1)) {
		ym = u$cum[ u$day == start.gpn]
		y = ym + h
		text(start.gpn, y + h*0.1, txt, pos=2, offset=-.2, col=axis.col)
		arrows( start.gpn, y - 1, start.gpn, ym + .5, length=.1, col=axis.col, lwd=2)
	  }
   }
graph.close()
