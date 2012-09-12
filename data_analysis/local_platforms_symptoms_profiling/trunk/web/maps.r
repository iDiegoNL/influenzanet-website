source('conf.r')

library(maps)

week.point = ISOYearWeek(Sys.Date() - 7)

load(share.data.path('map.fr.reg.RData'))

inc = dbQuery('select zip_code_key as code_reg, color from pollster_charts_weekly_reg_health')

inc$color = as.character(inc$color)

# match with internal rs code (for the map)
reg = dbQuery('select code_reg,code_rs,cheflieu from gis_region')

# total by region
inc = merge(inc, reg, by='code_reg')

i = match(inc$code_rs, map.fr.reg$id) # index of each region in the map order
inc = inc[order(i),] # reorder inc

#pref = dbQuery("select nom_comm,x_chf_lieu,y_chf_lieu from gis_commune where insee_com IN(", paste( paste("'",reg$cheflieu,"'",sep=''), collapse=','),")")

graph.open(my.path(paste('map_ili',week.point,sep='_')), width=800, height=800)
  map(map.fr.reg, col=inc$color, fill=T, mar=c(2,1,1,1), lwd=0.2)
  title(sub=sub.text,line=1, cex.sub=.8)
  #points(pref$x_chf_lieu*100, pref$y_chf_lieu*100, type="p", pch=18, cex=0.5)
  #text(pref$x_chf_lieu*100, pref$y_chf_lieu*100, pref$nom_comm, cex=0.5, adj=c(.5,1))
graph.close()