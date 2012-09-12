### Global configuration for package hebdo
source('../global.inc.r') # global config and system init
dbConnect()

# load shared libraries
share.lib('survey')
share.lib('i18n')

init.path('web')

i18n.load(share.path('platform/i18n'),'i18n/')

sub.text = paste( i18n('sub.text'), format(Sys.time(), format=i18n('format.date.full')))
