### Global configuration for package hebdo
source('../global.inc.r') # global config and system init
dbConnect()

# load shared libraries
share.lib('survey')
share.lib('i18n')

init.path('web')

i18n.load(paste('i18n/',.Share$platform,'.r',sep=''))

sub.text = paste( i18n('sub.text'), format(Sys.time(), format=i18n('format.date.full')))
