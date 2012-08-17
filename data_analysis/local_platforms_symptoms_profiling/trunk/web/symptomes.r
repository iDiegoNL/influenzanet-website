source('conf.r')

weekly = survey_load_results("weekly", c('timestamp', sympt.aliases,'sympt.sudden','same.episode','fever.sudden','highest.temp','sympt.start') )

weekly = recode.weekly(weekly)

# human readable titles
sympt.titles = i18n(names(sympt.aliases))
names(sympt.titles) <- names(sympt.aliases)

# color for symptoms category
color.general = colors.web$green
color.respi = colors.web$blue
color.gastro = "darkorange"
color.other = "black"

sympt.colors = list(
  'no.sympt'='grey',
# general symptoms
  'fever'=color.general, 
  'asthenia'=color.general, 
  'anorexia'=color.general, 
  'chills'=color.general,
  'headache'=color.general, 
  'pain'=color.general, 
  'chestpain'=color.general, 
  'wateryeye'=color.general, 
# respiratory & upper tract symptoms
  'rhino'=color.respi, 
  'sneeze'=color.respi, 
  'sorethroat'=color.respi, 
  'cough'=color.respi, 
  'dyspnea'=color.respi, 
  'sputum'=color.respi, 
# Digestive system symptoms
  'nausea'=color.gastro, 
  'vomiting'=color.gastro, 
  'diarrhea'=color.gastro, 
  'abdopain'=color.gastro, 
# other
  'sympt.other'=color.other
)

# get an attribute for a symptom varname
# @param what kind of attribute to get
# @param n list of symptoms (symptoms aliases = names of sympt.aliases)
sympt.get = function(what, n) {
 assoc = switch(what, 'title'=sympt.titles, 'color'=sympt.colors)
 f = match(n, names(assoc))
 i = !is.na(f)
 n[i] = unlist(assoc[ f[i] ])
 n
}

# Syndromic calculation function
share.lib('syndrom')

# Create syndrom columns 
weekly$influweb = symptomes.influweb(weekly)
weekly$influweb = factor(weekly$influweb, 1:5, i18n(c('no.sympt','ili','cold','gastroenteritis','sympt.other')))

weekly$ili.rs = symptomes.ili.rs(weekly)
weekly$gastro.rs = symptomes.gastro.rs(weekly)
weekly$gastro = symptomes.gastro(weekly)

# sympt = frequency table for each symptom
sympt = aggregate( as.list(weekly[, names(sympt.aliases)]), list(yw=weekly$yw), sum)
users = aggregate(id ~ yw, data=weekly, length) # user by week (for instance it's not user but survey result)
sympt = merge(sympt, users, by='yw', all=T)
weeks = as.numeric(as.character(sympt$yw)) # list of weeks
users = sympt$id
sympt = subset(sympt, select=-c(yw,id))
sympt = sympt[,rev(names(sympt.colors))] # color in order of type
sympt = t(sympt)
n.sympt = nrow(sympt) # count of symptoms
n.week = ncol(sympt) # count of weeks

sympt.prop = t(apply(sympt,1,function(r) r/users)) # proportion by week

graph.open(my.path('symptomes'), height=800, width=500)
	par(mar=c(5,10,2,0))
	plot( c(0, n.week + 1), c(1, n.sympt + 1), type="n", axes=F, ylab="", xlab=i18n('week_by_monday'), sub=sub.text, cex.sub=0.7)

	abline(h=1:n.sympt, col="#F0F0F0", lty=2, lwd=1)

	cex.max = 4
	cex.min = .8
	for( i in 1:ncol(sympt) ) {
		eff = sympt[,i]
		nb = users[i]
		prop = eff / nb
		r = prop * (cex.max / max(prop)) + cex.min
		x = rep(i, n.sympt)
		points(x, 1:n.sympt, type="p", pch=20, cex=r, col=sympt.get('color',names(r)))
		text(x + .3, 1:n.sympt, round(100*prop), cex=.6)
	}
  
	axis(2, at=1:n.sympt, sympt.get('title', rownames(sympt)), las=1)
	axis(1, at=1:n.week, format(WeekStart(weeks),format="%d/%m"), cex=.6, line=NA)
	legend("topleft", i18n(c('sympt.general','respiratory','digestive','sympt.other')), fill=c(color.general, color.respi, color.gastro, color.other), cex=.8, horiz=T, bty="n", x.intersp=.2)
	title(main=i18n('symptoms_by_week'))
graph.close()

graphics.off()

# export sympt percentage by week
colnames(sympt.prop) <- weeks
write.csv( round(sympt.prop*100, 1), file=my.path('sympt-percentage.csv'))

# number of expressed symptomes
local({
	n = names(sympt.aliases)
	n = n[ n != 'no.sympt']
	sympt.nb = apply( weekly[, n], 1, sum)
	sympt.cut = cut(sympt.nb, breaks=c(0,1,5,10,15,20), include.lowest=F, right=F, labels=F)
	sympt.cut = factor(sympt.cut, 1:5, c('Aucun','1 - 4','5 - 9','10 - 15','15 +'))
	sympt.nb.tb = data.frame(yw = weekly$yw, nb=sympt.nb, class=sympt.cut)
	sympt.nb.tb$i = 1
	sympt.nb = xtabs(i ~ nb + yw, data=sympt.nb.tb) # table count by number of sympt + yw
	sympt.nb.prop = t(apply(sympt.nb, 1, function(r) r/users)) # proportion by week

	write.csv( sympt.nb, file=my.path('sympt-bycount.csv'))
	write.csv( round(sympt.nb.prop*100,1), file=my.path('sympt-bycount-percentage.csv'))

	sympt.class = xtabs(i ~ class + yw, data=sympt.nb.tb) # table count by number of sympt + yw
	sympt.class.prop = t(apply(sympt.class, 1, function(r) r/users)) # proportion by week

	n = WeekStart(as.numeric(colnames(sympt.class.prop)))
	colnames(sympt.class.prop) <- format(n, format="%d/%m") # date of monday for weeks id*
	sympt.class.prop = round(sympt.class.prop*100,1)
	library(RColorBrewer)
	cols = brewer.pal(5, "Set2")
	graph.open('sympt-bycount')
		barplot(sympt.class.prop, beside=T, col=cols, ylim=c(0, max(sympt.class.prop)*1.15), las=1	)
		legend("top", rownames(sympt.class.prop), fill=cols, horiz=T, bty="n")
		title(sub=sub.text, cex.sub=.8, xlab=i18n('week_by_monday'), ylab=i18n('percentage'))
	graph.close()
})


# wordcloud
library(wordcloud)

n = names(sympt.aliases)
n = n[ n != 'no.sympt'] # Exclude no symptoms
w = apply(weekly[ ,names(sympt.aliases)], 2, sum)
n = names(w)
names(w) <- sympt.get('title', names(w)) # get symptomes titles

graph.open(my.path('wordcloud'), width=400, height=400)
	wordcloud(names(w), w, colors=sympt.get('color',n), ordered.colors=T, scale=c(3.5,1), min.freq=0, rot.per=.15, random.color=F)
	title(sub=sub.text, cex.sub=.63)
graph.close()

## Syndromic

weekly$i = 1

w = aggregate(i ~ influweb + yw, data=weekly, sum)
total = aggregate(i ~ yw, data=weekly, sum)
w = merge(w, total, by='yw', all.x=T, suffixes=c('','.total'))
w$prop = w$i / w$i.total
cols = 	cols = brewer.pal(nlevels(w$influweb), "Set2")

#graph.open(my.path('syndrom-influweb-survey-week'), width=800, height=600)
#	plot(range(w$yw), c(0,1), type="n", xlab="Semaine", ylab="Proportion de questionnaires", las=1)
#	for(i in 1:nlevels(w$influweb)) {
#	 rr = w[ as.numeric(w$influweb) == 	i,]
#	 points(rr$yw, rr$prop, col=cols[i], pch=19, type="o", cex=1.2, lwd=2)
#	}
#	legend("top", levels(w$influweb), col=cols, pch=19, lty=1, lwd=2, horiz=T, cex=.8)
#	title(sub=sub.text, cex.sub=.8)
#graph.close()



