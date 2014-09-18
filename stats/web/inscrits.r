source('conf.r')

# note intake(id=77) supprimé car donnée de tests CT
# intake(id=951) supprimé car données de test

library(RColorBrewer)

my.colors = function(n) {
 brewer.pal(n, "Set2")
}

# Text just above barplot
# @param r return of barplot
# @param y values of barplot
# @param text text to place 
# @param cex cex factor
barplot.headtext <- function(r, y,  txt, cex) {
 h = strheight("1", cex=cex) * 1.05
 text(x=r[,1], y=y + h, txt, cex=cex)
}

# Percentage barplot 
# @param values vector of values
# @param col vector of colors (one for each kind of value)
# @param  cex.names cex for labels
# @param order should order values by decreasing frequency ?
barplot.percent <- function(values, col, cex.names=par('cex.axis'), order=F, ...) {
  tt = table(values) # frequency table
  if(order) {
	tt = tt[ order(tt, decreasing=T) ]
  }
  tt.prop = prop.table(tt)
  names(tt) <- paste( names(tt), round(tt.prop * 100, 1), "%") 
  max.scale = ceiling(max(tt.prop * 100) / 10) / 10 # maximum value for the scale (greater percentage)
  r = barplot(tt.prop, col=col, border=col, axes=F, ylim=c(0, max(tt.prop) * 1.2), cex.names=cex.names, ... )
  txt = paste(round(tt.prop * 100),"% (",tt,")",sep='')
  barplot.headtext(r, tt.prop, txt, cex=.8)
  i = c(0, seq(.1, max.scale, by=.1))
  axis(2, at=i, labels=round(i*100), las=1)
}

intake = survey_load_results("intake", c('timestamp','gender','date.birth','vacc.curseason',"main.activity","occupation","hear.radio","hear.newspaper","hear.internet","hear.poster","hear.family","hear.work"))

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

graph.open(my.path('sex'), width=300, height=400)
	barplot.percent(intake$gender, col = unlist(colors.web[c('grey','red')]) ) 
	title(main=i18n("sex_of_participants"), ylab=i18n('percentage'), cex.sub=.8)
graph.close()

age.categories = c(0, 6, 13, 20, 40, 60, 200)
intake$age.cat = cut( intake$age, breaks=age.categories, include.lowest=T, right=F)

# pretty levels for age ranges
n = length(age.categories)
lev = rep(NA, n-1)
for(i in 1:(n-1)) {
   if( (i+1) < n ) {
     lev[i] = paste( age.categories[i], (age.categories[i+1]-1), sep='-') 
   } else {
     lev[i] = paste(">=",age.categories[i])
   }
}
levels(intake$age.cat) <- lev

graph.open(my.path('age'), width=755, height=400)
	barplot.percent(intake$age.cat, col=my.colors(nlevels(intake$age.cat)))
	title(main=i18n("age_of_participants"), ylab=i18n('percentage'), xlab=i18n('age_group'), cex.sub=.8)
graph.close()

# Hear about us

hear.about = c("hear.radio","hear.newspaper","hear.internet","hear.poster","hear.family","hear.work")
ii = apply(intake[, hear.about ], 2, sum)
ii = ii[ order(ii, decreasing=T) ]
iip = round(100*ii / nrow(intake))
names(iip) <- i18n(names(iip))
ymax = max(iip)*1.15
graph.open(my.path('hearabout'), width=680, height=500)
	r = barplot(iip, col=colors.web$red, cex.names=.7, ylim=c(0,ymax), border=NA, las=1)
	title(cex.sub=.8, main=i18n('graph.hear.about'))
	txt = paste(iip,'% (',ii,')',sep='')
	barplot.headtext(r, iip, txt,cex=.8)
graph.close()

# Main occupation
#activities = c('activity.fulltime','activity.partial','activity.self', 'activity.student','activity.home','activity.unemployed','activity.sick','activity.retired', 'activity.other')
#y = factor(intake$main.activity, 0:8, i18n(activities))
#mar = par(mar=c(5,3,4,0)+.1)
#graph.open(my.path('main-activity'), width=650, height=650/1.618)
#	barplot.percent(y, col=colors.web$red, cex.names=.6, order=T, space=.1)
#	title(main=i18n('graph_main_activity'), cex.sub=.8)
#graph.close()
#
#par(mar)

# Departement
#dep = load_geo_zone("dep")
#pop = load_population("dep", 2012)
#intake.dep = aggregate(person_id ~ code_dep, data=intake, length)
#intake.dep = replace.names(intake.dep, 'count'='person_id')
#intake.dep = merge(intake.dep, dep, by='code_dep', all=T)
#intake.dep = merge(intake.dep, pop, by='code_dep', all.x=T)
#
#intake.dep$pop.rate = intake.dep$count * (100000/intake.dep$population)
#
#intake.dep = intake.dep[ order(intake.dep$pop.rate, decreasing=T),]
#
#write.csv(intake.dep, file=my.path('intake-dep.csv'), row.names=F)

graphics.off()
#graph.open(my.path('deptop20'), width=600, height=500)
#	mar = mar.org = par("mar")
#
#	split.screen( 
#		matrix(c(
#			0, 1, .95, 1,
#			0, 1, 0.05, .95,
#			0, 1,   0, .05)
#			, byrow=T, nrow=3, ncol=4)
#		)
#	split.screen(c(1,2), screen=2)
#
#	screen(1)
#	par(mar=c(1,1,1,1)*.1)
#	plot(c(0,1), c(0,1), type="n", axes=F)
#	text(.5, .5, i18n('graph_top20dep'), cex=1.2)
#
#	screen(3)
#	par(mar=c(1,1,1,1)*.1)
#	plot(c(0,1), c(0,1), type="n", axes=F)
#	text(.5, .5, sub.text, cex=.8)
#
#	screen(4)
#	ii = head(intake.dep, n=20)
#	ii = ii[nrow(ii):1,]
#	mar = mar.org = par("mar")
#	mar[2] = 11 ; mar[4] = .5; mar[3] = 0
#	par(mar=mar)
#	barplot(ii$pop.rate, horiz=T, names.arg=ii$title, las=1, cex.names=.6, space=.2, col=colors.web$green, xlab="", border=NA)
#	title(xlab="Participants pour 100 000 habitants", adj=0, cex.lab=.7)
#
#	screen(5)
#	mar = mar.org
#	mar[2] = 1; mar[3] = 0; mar[4] = .5
#	par(mar=mar)
#	barplot(ii$count, horiz=T ,axisnames=FALSE, xlab="", col=colors.web$blue, border=NA)
#	title(xlab="Nombre de Participants", adj=0, cex.lab=.8)
#	close.screen(all = TRUE)
#graph.close()
