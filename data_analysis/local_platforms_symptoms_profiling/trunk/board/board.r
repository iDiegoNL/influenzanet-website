source('conf.r')

init.path('board')

perc.table = function(x, nb) {
  p = round(100*x/nb,1)
  data.frame(Effectif=x, Pourcentage=p)
}

share.lib('output')

init.output(my.path(''), 'board', type="html", opts=list(inline.css=T))

xtitle("GrippeNet.fr - Bilan des inscrits et participants, ", Sys.time(), level=1)

xbloc("Les inscrits (utilisateurs avec login/mdp)")

inscrits = dbQuery("SELECT count(*) as nombre, is_active as compte_actif from safe_users group by is_active")

nb.inscrits = inscrits$nombre[ inscrits$compte_actif == 1]

inscrits$compte_actif = factor(inscrits$compte_actif, 0:1, c('Non','Oui'))
out(inscrits, main="Inscrits à GrippeNet (comptes utilisateurs)")

inscrits = dbQuery("SELECT count(*) as nombre, date_trunc('day',date_joined) as date from safe_users where is_active=true  and date_joined > (now() - interval '21 day') group by date ")
inscrits$yw = ISOYearWeek(as.Date(inscrits$date))
inscrits = aggregate(nombre ~ yw, data=inscrits, sum)
if(nrow(inscrits) > 3) {
  inscrits = inscrits[ order(inscrits$yw),]
  inscrits = inscrits[ -1,]
}

out(inscrits, main="Nouveaux inscrits (compte actifs) sur les 3 dernieres semaines")

rm(inscrits)

xblock(end=T)

xblock("Participants")
# Inscrits ayant au moins un questionnaire intake
p = dbQuery("select count(distinct user_id) as nb from survey_surveyuser")
out(perc.table(p$nb, nb.inscrits) , main="Inscrits ayant au moins 1 participant (% d'inscrits actifs)")

# Participants pollster_results_intake
p = dbQuery("select count(*) as nb from survey_surveyuser")
out(p$nb, main="Participants enregistrés")

nb.part = p$nb

part = dbQuery("select user_id as inscrit, count(*) as nb from survey_surveyuser group by user_id")

out(table(part$nb), main="Répartition des nombres de participants par utilisateur inscrit (taille des 'foyers')")

# Participants ayant rempli leur questionnaire
part = dbQuery("SELECT count(distinct s.id) as nombre from pollster_results_intake p left join survey_surveyuser s on p.global_id=s.global_id")

nb.intake = part$nombre

out(perc.table(nb.intake, nb.part), main="Participants ayant remplis au moins 1 questionnaire d'inclusion")

# Repartition geographique des participants

intake = survey_load_results("intake", c('code_com','timestamp'), geo=c('reg','dep'))

# seulement le questionnaire le plus recent
u = aggregate(timestamp ~ person_id, data=intake, max)
intake = merge(u, intake, by=c('person_id','timestamp'), all.x=T)

regions = dbQuery('SELECT code_reg,nom_region from gis_region')

pop.region = dbQuery('SELECT code_reg,population from pop_reg where year=2012')

intake.reg = aggregate(person_id ~ code_reg, data=intake, length)
intake.reg = merge(intake.reg, regions, by='code_reg', all=T)
intake.reg = merge(intake.reg, pop.region, by='code_reg', all=T)
intake.reg = replace.names(intake.reg, effectif="person_id")

intake.reg$nb.pour.100000 = round(intake.reg$effectif * (100000 / intake.reg$population),2)
intake.reg$pourcentage.inscrits = round(100 * intake.reg$effectif / nb.intake, 1)

intake.reg = intake.reg[ order(intake.reg$nb.pour.100000, decreasing=T),]

out(intake.reg, main="R\u00E9partition par r\u00E9gion")
out("Un seul questionnaire est compt\u00E9 par participant : seulement le plus r\u00E9cent")

r = intake[ is.na(intake$code_dep),]

out(r, main="Zone geo inconnue")

rr = dbQuery("select user_id, id as person_id from survey_surveyuser where id in(",paste(r$person_id, collapse=','),")")

r = merge(r, rr, by='person_id', all=T)


xblock(end=T)


xblock("Questionnaires hebdomadaires")

weekly = dbQuery("SELECT count(distinct s.id) as nombre, date_trunc('day',timestamp) as date from pollster_results_weekly p left join survey_surveyuser s on p.global_id=s.global_id group by date")
weekly$date = as.Date(as.character(weekly$date))
weekly$yw = ISOYearWeek(weekly$date)

weekly = aggregate(nombre ~ yw, data=weekly, sum)

weekly$percent = round(100 * weekly$nombre / nb.intake, 1)

out(weekly, main="Questionnaires hebdomadaires (% participants avec intake)")

xblock(end=T)

close.output()
