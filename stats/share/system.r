##
# Bootstrap Loader of global configuration
##

## Global convention
# share contains all shared libraries
# As it could be in different place on different server you should NEVER use absolute path to share
# convenience function share.*.path have to be used.
# share.lib must be used to load a a share library

# Path to share directory
SHARE_PATH <- paste(BASE_PATH,'share/',sep='')

# @deprecated: old name, do not use
SHARE_LIB_PATH <- SHARE_PATH

# get options for the share environ
share.option <- function(...) {
  opts = list(...)
  if(length(opts) == 0) {
    return(.Share)
  }
  nn = names(opts)
  for(i in 1:length(opts)) {
    n = nn[i]
    o = opts[[i]]
    .Share[n] <<- o
  }
}

# .Share : list of share environment configurations
# Do not access to it directly !!
share.option(
 base.out.path = OUT_PATH, # base path to output files
 out.path = OUT_PATH, # current output files path (could be modified by init.path())
 share.cache = paste(BASE_PATH,'share/cache/',sep=''), # path to cache directory
 share.data = paste(BASE_PATH,'share/data/',sep=''), # path to data directory
 loaded.libs = c() # list loaded share libraries
)

# Path helpers  xxx.path(file) return file in the given path for xxxx

# path of a file in share/
share.path <- function(file='') { 
	return(paste(SHARE_PATH, file, sep='')) 
}

# path of a file in cache files
share.cache.path <- function(file='') { 
	return(paste(.Share$share.cache, file, sep='')) 
} 
# path of a file in data 
share.data.path <- function(file='') { 
	return(paste(.Share$share.data, file, sep='')) 
} 

# Load a share library
#@param file name of the library to load (name of the .r file, without extension)
share.lib <- function(file, force=F) {
  if(!force && (file %in% .Share$loaded.libs)) {
    warning(paste(file, " library is already loaded"))
  }
  .Share$loaded.libs <<- unique( c(.Share$loaded.libs,file) )
  source(paste(SHARE_LIB_PATH,'lib/',file,'.r',sep=''),local=F) 
}

# now load basic libraries
share.lib('graph') # graph functions
share.lib('week')  # week calculation
share.lib('db') # database functions

# Wrapper of cat() for output
# You car redirect by using sink() function
.msgLevel = 0
msg = function(..., ln=TRUE, level = 0) {
 n = ifelse( (.msgLevel > 0) & ln, rep(" ", .msgLevel) , "")
 cat(n, ..., ifelse(ln, "\n", "") ) 
 if (level != 0) {
  .msgLevel = .msgLevel + level
  .msgLevel = max(0, .msgLevel)
 }
}

# Define an ouput path for files, usable by my.path()
# by default, the path is added to the base path, unless the parameter full.path is TRUE
# @param char p path 
# @param logical full.path, if TRUE p is considered as an absolute path
init.path <- function(p, full.path=F) {
 path = ifelse(as.logical(full.path), p, paste(.Share$base.out.path, p, sep=''))
 .Share$out.path <<- path # update current output path
 .Share$out.path.sep <<- ifelse( any(grep("/$",path)==1) , "", "/") # check for directory separator
 if( !file.exists(path) ) {
  dir.create(path, recursive=T)
 }
 return(path)
}

# Return the path of a file in the current ouput path
my.path <- function(x='') {
 return(paste(.Share$out.path, .Share$out.path.sep, x,sep=''))
}

# replace names with given pairlist where value are old names and key are new names
# replace.names(data.frame(), new.name=old.name,...)
# ex replace.names(d, toto="x") replace column "x" by "toto"
replace.names <- function(x, ...) {
 nn = list(...)
 if(is.list(nn[[1]])) {
  nn = nn[[1]]
 }
 if( !is.list(nn) ) {
  stop("replacements should be a list")
 }
 old.names = names(x)
 new.names = names(nn) # new names are key of args
 u = match(nn, old.names)
 if( any(is.na(u)) ) {
  warning(paste('unknown columns ', paste(nn[is.na(u)],collapse=',')))
 }
 f = match(old.names, nn)
 i = !is.na(f) # NA= unknown old names in new names
 f = f[i]
 if(length(f) > 0) {
   old.names[i] = new.names[f]
   str(old.names)
   names(x) <- old.names
 } else {
  warning("nothing to replace")
 }
 return(x)
}

# Merge two lists
# from RCurl 0.94.0
merge.list <- function(x, y)
{
  if(length(x) == 0)
    return(y)

  if(length(y) == 0)
    return(x)

  i = match(names(y), names(x))
  i = is.na(i)
  if(any(i))
    x[names(y)[which(i)]] = y[which(i)]
  x
}

## aggregate.formula from R.13.0 for R 2.8
if( !exists('aggregate.formula', mode='function') ) {
  aggregate.formula <-
  function(formula, data, FUN, ..., subset, na.action = na.omit)
  {
      if(missing(formula) || !inherits(formula, "formula"))
          stop("'formula' missing or incorrect")
      if(length(formula) != 3L)
          stop("'formula' must have both left and right hand sides")

      m <- match.call(expand.dots = FALSE)
      if(is.matrix(eval(m$data, parent.frame())))
          m$data <- as.data.frame(data)
      m$... <- m$FUN <- NULL
      m[[1L]] <- as.name("model.frame")

      if(as.character(formula[[2L]] == ".")) {
          ## LHS is a dot, expand it ...
          rhs <- unlist(strsplit(deparse(formula[[3L]]), " *[:+] *"))
          ## <NOTE>
          ## Note that this will not do quite the right thing in case the
          ## RHS contains transformed variables, such that
          ##   setdiff(rhs, names(data))
          ## is non-empty ...
          lhs <- sprintf("cbind(%s)",
                         paste(setdiff(names(data), rhs), collapse = ","))
          ## </NOTE>
          m[[2L]][[2L]] <- parse(text = lhs)[[1L]]
      }
      mf <- eval(m, parent.frame())

      if(is.matrix(mf[[1L]])) {
          ## LHS is a cbind() combo, convert to data frame and fix names.
          lhs <- as.data.frame(mf[[1L]])
          names(lhs) <- as.character(m[[2L]][[2L]])[-1L]
          aggregate.data.frame(lhs, mf[-1L], FUN = FUN, ...)
      }
      else
          aggregate.data.frame(mf[1L], mf[-1L], FUN = FUN, ...)
  }
}