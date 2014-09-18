# Global configuration of scripts

.Share = list() # global config

# Local config scripts
source('../location.r') # should always in the upper directory from working dir

# load platform specific configs
source(paste(BASE_PATH,'share/platform/',.Share$platform,'.r', sep=''))

if( is.null(.Share$system) ) {
  .Share$system = T
  # load system bootstrap script
  source(paste(BASE_PATH,'share/system.r',sep=''))
}

