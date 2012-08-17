
par(las=1)
xtitle("GrippeNet.fr - Bilan 2009, ", Sys.time(), level=1)

out(paste("Dernier intake par utilisateur N=", nrow(intake)))

r = aggregate(id ~ age.cat, data=intake, length)
r = merge(r, pop.totale[,c('age.cat','all')], by='age.cat', all=T)
r = merge(r, age.categories)
r = r[order(r$order), ] # reorder age cat
r$prop = 100*r$id / sum(r$id)
r$prop.pop = 100*r$all / sum(r$all)
r$rr = r$prop / r$prop.pop

graph.open(my.path('age_proportion'), width=600, height=400)
  ylim = max(r[,c('prop','prop.pop')])*1.1
  barplot(t(r[,c('prop','prop.pop')]), beside=T, names.arg=r$age.cat, col=unlist(colors.web[c('blue','green')]), border=NA, legend.text = c('GrippeNet','French Population'), args.legend=list(x="top",horiz=T, bty="n"), ylim=c(0,ylim), las=1)
	title(main=i18n("age_of_participants"), ylab=i18n('percentage'), xlab=i18n('age_group'))
  title.sub()
graph.close()

out(r, main="Age des participants", name="age")

p = rbind( data.frame(age.cat=pop.totale$age.cat,gender=i18n('male'), pop=pop.totale$male), data.frame(age.cat=pop.totale$age.cat,gender=i18n('female'), pop=pop.totale$female) )
r = aggregate(list(total.pop=p$pop), list(gender=p$gender), sum)
p = merge(r, p, by='gender', all=T)
r = aggregate(id ~ age.cat + gender, data=intake, length)
r = merge(r, p, by=c('age.cat','gender'), all=T)
p = aggregate(list(total.gender=r$id), list(gender=r$gender), sum)
r = merge(r, p, by='gender') # total participant by gender
r = merge(r, age.categories)
r = r[order(r$order), ] # reorder age cat

r$prop.pop = 100*r$pop/r$total.pop # Proportion of population for each gender & age
r$prop = 100*r$id/r$total.gender # propotion of GrippeNet participant by gender & age
r$rr = r$prop / r$prop.pop

graph.open(my.path('age_by_sex_relativeratio'), width=800, height=500)
  x = xtabs(rr ~ gender + age.cat, data=r)
  ylim = max(x) * 1.1
  barplot(x, beside=T, col=unlist(colors.web[c('blue','green')]), border=NA, legend.text=rownames(x), args.legend=list(x="top",horiz=T, bty="n"), ylim=c(0,ylim))
  title.sub()
  title(main=i18n('graph_agesexe_relative_ratio'), ylab=i18n('relative_ratio'), xlab=i18n("age_group"), cex.main=1)
graph.close()


library(lattice)

graph.open(my.path('age_by_sex_percentage'), width=900, height=500)
  cols = unlist(colors.web[c('blue','green')]) 
  print(
    barchart(prop + prop.pop ~ age.cat | gender, data=r, col=cols, border=NA, ylab=i18n('percentage'),
    key=simpleKey(c('GrippeNet','French Population'), col=cols, points=F, rectangles=F, columns=2, font=2),
    par.settings=list(strip.background=list(col="white")),
    main="GrippeNet participants by age-group & gender compared to French population"
    )    
  )
graph.close()

graph.open(my.path('age_by_sex'), width=800, height=400)
	cols = brewer.pal(nlevels(intake$age.cat), "Set3")
	tt = round(100*prop.table(table(intake$age.cat, intake$gender),2),1)
	ymax = max(tt, na.rm=T)*1.15
	barplot(tt, col=cols, beside=T, ylim=c(0, ymax),ylab=i18n('percentage'),main=i18n("age_of_participants_by_sex"))
	legend("top", levels(intake$age.cat), fill=cols, cex=0.8, bty="n", horiz=T)
  title.sub()
graph.close()

out(tt, name="age-sexe", main="Age by sex")

# Hear about us
vv = survey_labels('intake','hear.about') 
ii = multiple.freq(intake[, vv ])
colnames(ii) <- i18n(vv)
graph.open(my.path('hearabout'), width=750, height=500)
	barplot.percent(ii, col=colors.web$blue, cex.names=.8,  las=1)
  title.sub()
graph.close()

out(ii, name="hear-about", main="Hear About us")

# Main Activity
y = factor(intake$main.activity, 0:8, i18n(survey_labels('intake','activities') ))
mar = par(mar=c(5,3,4,0)+.1)
graph.open(my.path('main-activity'), width=730, height=450)
	barplot.percent(y, col=colors.web$blue, cex.names=.8, order=T, space=.1)
	title(main=i18n('graph_main_activity'))
  title.sub()
graph.close()

out(freq(y), name="main-activity", main="Main Activity")

# Occupation
y = factor(intake$occupation, 0:5, i18n(survey_labels('intake','occupation')))
mar = par(mar=c(5,3,4,0)+.1)
graph.open(my.path('main-occupation'), width=750, height=450)
	barplot.percent(y, col=colors.web$blue, cex.names=.7, order=T, space=.1)
	title(main=i18n('graph_main_occupation'))
 title.sub()
graph.close()

out(freq(y), name="main-occupation", main="Main Occupation")

# Transport
y = factor(intake$transport, 0:5, i18n(survey_labels('intake','transport')))
mar = par(mar=c(5,3,4,0)+.1)
graph.open(my.path('transport'), width=700, height=450)
	barplot.percent(y, col=colors.web$blue, cex.names=.8, order=T, space=.1)
	title(main=i18n('graph_transport'))
  title.sub()
graph.close()

out(freq(y), name="transport", main="Transport method")

# Transport time
y = factor(intake$time.transport, 0:4, i18n(survey_labels('intake','time.transport')))
mar = par(mar=c(5,3,4,0)+.1)
graph.open(my.path('time.transport'), width=650, height=650/1.618)
	barplot.percent(y, col=colors.web$blue, cex.names=.9, order=T, space=.1)
	title(main=i18n('graph_time_transport'))
 title.sub()
graph.close()

out(freq(y), name="time-transport", main="Transport Time")


y = factor(intake$often.ili, 0:5, i18n(survey_labels('intake','often.ili')))
mar = par(mar=c(5,3,4,0)+.1)
graph.open(my.path('often-ili'), width=700, height=450)
	barplot.percent(y, col=colors.web$blue, cex.names=.8, order=T, space=.1)
	title(main=i18n('graph_often_ili'))
  title.sub()
graph.close()

out(freq(y), name="often-ili", main=i18n('graph_often_ili'))

vv = survey_labels('intake','education') 
ii = multiple.freq(intake[, vv ])
colnames(ii)<- i18n(vv)
graph.open(my.path('education'), width=750, height=500)
	barplot.percent(ii, col=colors.web$blue, cex.names=.8,  las=1)
  title(main=i18n('graph_education_level'))
  title.sub()
graph.close()

out(ii, name="education", main="Education level")


vv = survey_labels('intake','contact') 
ii = multiple.freq(intake[, vv ])
colnames(ii)<- i18n(vv)
graph.open(my.path('contact'), width=750, height=500)
	barplot.percent(ii, col=colors.web$blue, cex.names=.8,  las=1)
  title.sub()
graph.close()

out(ii, name="contact", main=i18n('graph_contacts'))

vv = survey_labels('intake','daycare') 
ii = multiple.freq(intake[, vv ])
colnames(ii)<- i18n(vv)
graph.open(my.path('daycare'), width=750, height=500)
	barplot.percent(ii, col=colors.web$blue, cex.names=.8,  las=1)
	title(main="Daycare")
  title.sub()
graph.close()

out(ii, name="daycare", main="Mode de garde")

y = intake$vacc.lastseason
mar = par(mar=c(5,3,4,0)+.1)
graph.open(my.path('vacc-lastseason'), width=750, height=650/1.618)
	barplot.percent(y, col=colors.web$blue, cex.names=.8, order=T, space=.1)
	title(main=i18n('graph_vacc_lastseason'))
  title.sub()
graph.close()

out(freq(y), name="vacc-lastseason", main=i18n('graph_vacc_lastseason'))

# Vaccination for the current season
graph.open(my.path('vaccination-curseason'), width=750, height=650/1.618)
	barplot.percent(intake$vacc.curseason, col=colors.web$blue, cex.names=.6, order=T, space=.1)
	title(main=i18n('graph_vacc_curseason'))
  title.sub()
graph.close()

out( table(intake$vacc.curseason), main=i18n('graph_vacc_curseason'))

## Vaccinated population
i =  intake$vacc.curseason %in% i18n(c('Yes','No'))
tt = table(intake$vacc.curseason[i, drop=T], intake$age.cat[i])
tt = 100*prop.table(tt, margin=2)

graph.open(my.path('vaccination-curseason-byage'), width=750, height=650/1.618)
  barplot(tt, beside=T, names.arg=colnames(tt), col=unlist(colors.web[c('blue','green')]), border=NA, legend.text=rownames(tt), xlab=i18n('age_group'))
  title(main=i18n('graph_vacc_curseason_byage'))
  title.sub()
graph.close()

y = factor(intake$voucher, 0:2, i18n(c('No','Yes','DNK')))
tt = table(intake$vacc.curseason[i, drop=T], y[i])
tt = 100*prop.table(tt, margin=2)
ylim = max(tt)*1.1
graph.open(my.path('vaccination-curseason-voucher'), width=750, height=650/1.618)
  barplot(tt, beside=T, names.arg=colnames(tt), col=c(unlist(colors.web[c('blue','green')])), border=NA, legend.text=rownames(tt),
       xlab=i18n('graph_voucher'), args.legend=c(horiz=T,bty="n",x="top"), ylim=c(0,ylim))
  title(main=i18n('graph_vacc_cur_byvoucher'))
  title.sub()
graph.close()


vv = survey_labels('intake','condition') 

r = multiple.xfreq(intake[i,], vv, 'vacc.curseason') 
tt = r$prop
rownames(tt) <- tt[,'vacc.curseason']
tt = tt[,vv]
ylim = max(tt)*1.1
colnames(tt) <- i18n(colnames(tt))
graph.open(my.path('vaccination-curseason-voucher'), width=750, height=650/1.618)
  barplot(as.matrix(tt), beside=T, names.arg=colnames(tt), col=c(unlist(colors.web[c('blue','green')])), border=NA, legend.text=rownames(tt),
       xlab=i18n('condition'), args.legend=c(horiz=T,bty="n",x="top"), ylim=c(0,ylim))
  title(main=i18n('graph_vacc_curseason_condition'))
  title.sub()
graph.close()

out(round(tt,2), name="vacc-curseaon-byage", main=i18n('graph_vacc_curseason_byage'))

out( table(intake$vacc.curseason , intake$vacc.lastseason, dnn=c('Current Season','Last Season')), main="Vaccination selon les saisons")

vacc = intake$vacc.curseason == i18n('Yes')
N.vacc.curseason = sum(vacc)
vacc = intake$vacc.curseason == i18n('No')
N.novac.curseason = sum(vacc)
rm(vacc)

# Vaccination reasons
vv = survey_labels('intake','vacc.reason') 
ii = multiple.freq(intake[, vv ])
colnames(ii)<- i18n(vv)
graph.open(my.path('vacc-reason'), width=950, height=500)
	barplot.percent(ii, col=colors.web$blue, cex.names=.6,  las=1)
	title(main=i18n('graph_vacc_reason'))
  title.sub()
graph.close()

out(ii, main=i18n('graph_vacc_reason'))

r = apply(intake[, vv ], 1, sum) > 0
out(paste("N=",sum(r), round(100*sum(r)/N.vacc.curseason,2),"% des vaccinés"),main="Au moins une réponse à la raison de la vaccination")

# Non vaccination reasons
vv = survey_labels('intake','notvac.reason') 
ii = multiple.freq(intake[, vv ])
colnames(ii)<- i18n(vv)
graph.open(my.path('notvacc-reason'), width=950, height=500)
	barplot.percent(ii, col=colors.web$blue, cex.names=.6,  las=1)
  title(main=i18n('graph_notvacc_reason'))
  title.sub()
graph.close()

out(ii, main=i18n('graph_notvacc_reason'))
r = apply(intake[, vv ], 1, sum) > 0
out(paste("N=",sum(r), round(100*sum(r)/N.novac.curseason, 2),"% des non-vaccinés (N=",N.novac.curseason,")"),main="Au moins une réponse à la raison de la vaccination")

# Vaccination Voucher [Caution No=0 and Yes=1
y = factor(intake$voucher, 0:2, i18n(c('No','Yes','DNK')))
mar = par(mar=c(5,3,4,0)+.1)
graph.open(my.path('voucher'), width=650, height=650/1.618)
	barplot.percent(y, col=colors.web$blue, cex.names=.9, order=T, space=.1)
	title(main=i18n('graph_voucher'), sub=sub.text, cex.sub=.8)
  title.sub()
graph.close()

out(freq(y), name="voucher", main=i18n('graph_voucher'))

# Condition
vv = survey_labels('intake','condition') 
ii = multiple.freq(intake[, vv ])
colnames(ii)<- i18n(vv)
graph.open(my.path('condition'), width=750, height=500)
	barplot.percent(ii, col=colors.web$blue, cex.names=.8,  las=1)
  title(main=i18n('graph_condition'))
  title.sub()
graph.close()

out(ii, main=i18n('graph_condition'))

# Pregnant
y = factor(intake$pregnant, 0:2, i18n(c('Yes','No','DNK')))
mar = par(mar=c(5,3,4,0)+.1)
graph.open(my.path('pregnant'), width=650, height=650/1.618)
	barplot.percent(y, col=colors.web$blue, cex.names=.8, order=T, space=.1)
	title(main=i18n('graph_pregnant'))
  title.sub()
graph.close()

out(freq(y), name="pregnant", main=i18n('graph_pregnant'))

# Smoker
# Pregnant
y = factor(intake$smoker, 0:6, i18n(survey_labels('intake','smoker')))
mar = par(mar=c(5,3,4,0)+.1)
graph.open(my.path('smoker'), width=650, height=650/1.618)
	barplot.percent(y, col=colors.web$blue, cex.names=.8, order=T, space=.1)
	title(main=i18n('graph_smoker'))
  title.sub()
graph.close()

out(freq(y), name="smoker", main=i18n('graph_smoker'))

# Allergy
vv = survey_labels('intake','allergy') 
ii = multiple.freq(intake[, vv ])
colnames(ii)<- i18n(vv)
graph.open(my.path('allergy'), width=680, height=500)
	barplot.percent(ii, col=colors.web$blue, cex.names=.8,  las=1)
	title(main=i18n('graph_allergy'))
  title.sub()
graph.close()
out(ii, main=i18n('graph_allergy'))

# Diet
vv = survey_labels('intake','diet') 
ii = multiple.freq(intake[, vv ])
colnames(ii)<- i18n(vv)
graph.open(my.path('diet'), width=680, height=500)
	barplot.percent(ii, col=colors.web$blue, cex.names=.8,  las=1)
	title(main=i18n('graph_diet'))
  title.sub()
graph.close()
out(ii, main=i18n('graph_diet'))

# Pets
vv = survey_labels('intake','pets') 
ii = multiple.freq(intake[, vv ])
colnames(ii)<- i18n(vv)
graph.open(my.path('pets'), width=680, height=500)
	barplot.percent(ii, col=colors.web$blue, cex.names=.8,  las=1)
	title(main=i18n('graph_pets'))
  title.sub()
graph.close()
out(ii, main=i18n('graph_pets'))

# Weight
intake$weight[ intake$weight > 200] <- NA
intake$height[ intake$height > 220] <- NA
intake$bmi = intake$weight / ((intake$height/100)^2)
intake$obesity = intake$bmi > 30

graph.open(my.path('height_vs_weight'), width=680, height=500)
  plot(intake$height,intake$weight, col=ifelse(intake$obesity, "red", "blue"), pch=19, cex=0.7, xlab="Height (cm)", ylab="Weight (kg)")
  legend("top", legend=c("BMI <= 30", "BMI > 30"), col=c("blue","red"), pch=19, pt.cex=0.7, horiz=T, bty="n")
  title(main="Height vs Weight")
  title.sub()
graph.close()

graph.open(my.path('height_vs_weight'), width=680, height=500)
  vacc = intake$vacc.curseason == i18n('Yes')
  plot(intake$height,intake$weight, col=ifelse(vacc, "red", "blue"), pch=19, cex=0.7, xlab="Height (cm)", ylab="Weight (kg)")
  legend("top", legend=c("Not vaccinated", "Vaccinated"), col=c("blue", "red"), pch=19, pt.cex=0.7, horiz=T, bty="n")
  title(main="Height vs Weight & Vaccination")
  title.sub()
graph.close()


graph.open(my.path('bmi'), width=680, height=500)
  boxplot(intake$bmi)
graph.close()