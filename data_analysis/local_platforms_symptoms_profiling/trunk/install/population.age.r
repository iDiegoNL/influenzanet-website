source('conf.r')             
share.lib('geography')

dbConnect()
dep = load_geo_zone('dep')

update.source = function(geo, year, year.ref, source) {
  file.source = share.data.path('pop_source.csv')
  if(file.exists(file.source)) {
   r = read.csv2(file.source, header=T)
   r = r[ !(r$geo == geo & r$year == year),]
   r$date = as.Date(r$date)
  } else {
    r = data.frame()
  }
  r = rbind(r, data.frame(geo=geo, year=year, year.ref=year.ref, source=source, date=Sys.Date()))
  write.csv2(r, file=file.source, row.names=F)
}

file = 'pop_2010_dep_age5.csv'
data.source = 'INSEE ELP 2010 Departement & age quinquenaux'
year.insee = 2010
year = 2012

pop = read.csv2(file, header=T)

pop$year = year
pop$year.insee = year.insee

pop = replace.names(pop, "code_dep"="dep","all"="Ensemble","male"="Homme","female"="Femme", "age.min"="age")

age.min = sort(unique(pop$age.min))
age = data.frame(age.min=age.min, age.max=c(age.min[-1]-1,NA))

pop = merge(pop, age, by='age.min', all.x=T)

pop = pop[, c('age.min','age.max','code_dep','year','all','male','female')]

write.csv2(pop, share.data.path('pop_dep_age5.csv'), row.names=F)

update.source('dep', year, year.insee,'INSEE ELP 2010 Departement & age quinquenaux')


dep = dep[,c('code_dep','zone.reg')]

pop = merge(pop, dep, by='code_dep')

# verifie qu'un departement est bien affecté à une région
r = apply(table(pop$code_dep, pop$zone.reg) > 0, 1, sum)
stopifnot(all(r==1))

pop.reg = aggregate(cbind(all,male,female) ~ age.min + zone.reg, data=pop, sum)
pop.reg = replace.names(pop.reg, "code_reg"="zone.reg")

pop.reg$year = year

pop.reg = merge(pop.reg, age, by='age.min',all.x=T)

pop.reg = pop.reg[, c('age.min','age.max','code_reg','year','all','male','female')]

write.csv2(pop.reg, share.data.path('pop_reg_age5.csv'), row.names=F)
update.source('reg', year, year.insee,'INSEE ELP 2010 Departement & age quinquenaux')