source('conf.r')

share.lib(stats)

# note intake(id=77) supprimé car donnée de tests CT
# intake(id=951) supprimé car données de test

library(RColorBrewer)

my.colors = function(n) {
 brewer.pal(n, "Set2")
}


intake = survey_load_results("intake", c('timestamp','code_com','gender','date.birth','vacc.curseason',"main.activity","occupation","hear.radio","hear.newspaper","hear.internet","hear.poster","hear.family","hear.work",'hear.hworker','hear.project','transport'), geo=c('dep','reg'))

# We keep only the most recent response to the intake survey
u = aggregate(timestamp ~ person_id, data=intake, max)
intake = merge(u, intake, by=c('person_id','timestamp'), all.x=T)

# recode some variables
intake$age = calc.age(intake$date.birth) # @see share/lib/survey
intake$gender = factor(intake$gender, c(0,1), i18n(c('male','female')))
intake$vacc.curseason = factor(intake$vacc.curseason, 0:2, i18n(c('Yes','No','DNK')))
#intake$main.activity = factor(intake$main.activity, 0:8, )
#intake$occupation = factor(intake$occupation, 0:5, )

intake = subset(intake, select=-date.birth) # remove uneeded variables

par(font.sub=3, cex.sub=.8, cex.main=1.1)

graph.open(my.path('sexe'), width=300, height=400)
	barplot.percent(intake$gender, col = unlist(colors.web[c('green','blue')]) ) 
	title(main=i18n("sex_of_participants"), sub=sub.text, ylab=i18n('percentage'), cex.sub=.8)
graph.close()

age.categories = c(0, 18, 20, 30, 40, 50, 60, 70, 80, 200)

intake$age.cat = cut.age(intake$age, age.categories) 

graph.open(my.path('age'), width=600, height=400)
	barplot.percent(intake$age.cat, col=my.colors(nlevels(intake$age.cat)))
	title(main=i18n("age_of_participants"), sub=sub.text, ylab=i18n('percentage'), xlab=i18n('age_group'), cex.sub=.8)
graph.close()

graph.open(my.path('age_by_sex'), width=800, height=400)
	cols = brewer.pal(nlevels(intake$age.cat), "Set3")
	tt = round(100*prop.table(table(intake$age.cat, intake$gender),2),1)
	ymax = max(tt, na.rm=T)*1.05
	barplot(tt, col=cols, beside=T, ylim=c(0, ymax),ylab=i18n('percentage'),cex.sub=.8, sub=sub.text, main=i18n("age_of_participants_by_sex"))
	legend("top", levels(intake$age.cat), fill=cols, cex=0.8, bty="n", horiz=T)
graph.close()

# Hear about us

hear.about = c("hear.radio","hear.newspaper","hear.internet","hear.poster","hear.family","hear.work", 'hear.hworker', 'hear.project')
ii = apply(intake[, hear.about ], 2, sum)
ii = ii[ order(ii, decreasing=T) ]
iip = round(100*ii / nrow(intake))
names(iip) <- i18n(names(iip))
ymax = max(iip)*1.15
graph.open(my.path('hearabout'), width=680, height=500)
	r = barplot(iip, col=colors.web$blue, cex.names=.7, ylim=c(0,ymax), border=NA, las=1)
	title(sub=sub.text, cex.sub=.8, main=i18n('graph.hear.about'))
	txt = paste(iip,'% (',ii,')',sep='')
	barplot.headtext(r, iip, txt,cex=.8)
graph.close()

# Main occupation
activities = c('activity.fulltime','activity.partial','activity.self', 'activity.student','activity.home','activity.unemployed','activity.sick','activity.retired', 'activity.other')
y = factor(intake$main.activity, 0:8, i18n(activities))
mar = par(mar=c(5,3,4,0)+.1)
graph.open(my.path('main-activity'), width=650, height=650/1.618)
	barplot.percent(y, col=colors.web$blue, cex.names=.6, order=T, space=.1)
	title(main=i18n('graph_main_activity'), sub=sub.text, cex.sub=.8)
graph.close()

# Vaccination for the current season
graph.open(my.path('vaccination-curseason'), width=650, height=650/1.618)
	barplot.percent(intake$vacc.curseason, col=colors.web$blue, cex.names=.6, order=T, space=.1)
	title(main=i18n('graph_vacc_curseason'), sub=sub.text, cex.sub=.8)
graph.close()

par(mar)

# Departement
dep = load_geo_zone("dep")
pop = load_population("dep", 2012)
intake.dep = aggregate(person_id ~ code_dep, data=intake, length)
intake.dep = replace.names(intake.dep, 'count'='person_id')
intake.dep = merge(intake.dep, dep, by='code_dep', all=T)
intake.dep = merge(intake.dep, pop, by='code_dep', all.x=T)

intake.dep$pop.rate = intake.dep$count * (100000/intake.dep$population)

intake.dep = intake.dep[ order(intake.dep$pop.rate, decreasing=T),]

write.csv(intake.dep, file=my.path('intake-dep.csv'), row.names=F)

graphics.off()
graph.open(my.path('deptop20'), width=600, height=500)
	mar = mar.org = par("mar")

	split.screen( 
		matrix(c(
			0, 1, .95, 1,
			0, 1, 0.05, .95,
			0, 1,   0, .05)
			, byrow=T, nrow=3, ncol=4)
		)
	split.screen(c(1,2), screen=2)

	screen(1)
	par(mar=c(1,1,1,1)*.1)
	plot(c(0,1), c(0,1), type="n", axes=F)
	text(.5, .5, i18n('graph_top20dep'), cex=1.2)

	screen(3)
	par(mar=c(1,1,1,1)*.1)
	plot(c(0,1), c(0,1), type="n", axes=F)
	text(.5, .5, sub.text, cex=.8)

	screen(4)
	ii = head(intake.dep, n=20)
	ii = ii[nrow(ii):1,]
	mar = mar.org = par("mar")
	mar[2] = 11 ; mar[4] = .5; mar[3] = 0
	par(mar=mar)
	barplot(ii$pop.rate, horiz=T, names.arg=ii$title, las=1, cex.names=.6, space=.2, col=colors.web$green, xlab="", border=NA)
	title(xlab="Participants pour 100 000 habitants", adj=0, cex.lab=.7)

	screen(5)
	mar = mar.org
	mar[2] = 1; mar[3] = 0; mar[4] = .5
	par(mar=mar)
	barplot(ii$count, horiz=T ,axisnames=FALSE, xlab="", col=colors.web$blue, border=NA)
	title(xlab="Nombre de Participants", adj=0, cex.lab=.8)
	close.screen(all = TRUE)
graph.close()