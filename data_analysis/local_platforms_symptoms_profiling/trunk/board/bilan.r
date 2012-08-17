source('conf.r')
share.lib( c('survey','output','stats','i18n','syndrom') )

init.path('bilan')

library(RColorBrewer)

my.colors = function(n) {
 pal = ifelse(n > 8, "Set3","Set2")
 brewer.pal(n, pal)
}

# load i18n texts
i18n.load(share.path('platform/i18n'), 'i18n/bilan', language='en')

# sub text for graphs
sub.text = paste(i18n('sub.text'),format(Sys.Date(),format=i18n("format.date.full")) )

title.sub = function() {
 title(sub=sub.text, cex.sub=0.7)
}

## load data
# to recalculate 
# source('bilan/loader.r')
load('data/grippenet-2012-05-02-ffTBcOrx.RData')

init.output(my.path(''), 'intake', type="html", opts=list(inline.css=T))

source('bilan/intake.r')

close.output()

############################
### Analyse weekly surveys
############################

par(las=1)

init.output(my.path(''), 'weekly', type="html", opts=list(inline.css=T))

source('bilan/weekly.r')

close.output()