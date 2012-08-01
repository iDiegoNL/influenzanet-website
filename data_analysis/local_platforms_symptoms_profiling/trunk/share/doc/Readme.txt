==========================================
= Sentiweb R micro-framework 			=
==========================================

Purpose
============
The purpose of this framework is to allow script running on different settings (platform, files organization,...).

Some library are made to wrap R libraries in order to write script without taking account of which R library is currently 
used or where files are really located (graph.* functions or db* functions).
It also sets a strict organization of files and rules for files location : it is based on the "convention over configuration" principle.

Organization
===========================

A workspace is a directory containing several R analysis project which share a workspace configuration (for example DB settings, a platform type, ...).
Each R analysis project is located in a sub-directory of this workspace.

Using subversion (and external repositories feature), it is possible to share projects between workspaces. If the project uses the coding
convention of the framework, it will run on the new environment without any modification (if not, it's time to improve the framework).

On the root of the workspace directory, there a 2 files
 * global.inc.r : this is the global configuration of the workspace and the file called by all the projects in the workspace. It is under version.
	So all the code should be abstract from the running env (see location). You shouldn't have to modify it
 * location.r : This is the environment specific configuration file, containing all the local configurations. It's not under version.

- The "share" directory is shared by all the workspaces on all the platforms.
 * system.r : the (tiny) core of the (micro)framework
 * lib/ contains the share librairies
 * data/ should contains some data files
 * cache/ contains 
 * plateform/ contains plateform specific configuration     

- Others directories are the R projects

A project is whatever you want (all scripts for a kind of data, of analysis, or a theme...). 
  
Organization of a project.
-----------------------
The framework does not force any organization for a project, but there is a convention.

First, a little file, called "conf.r" contains all the project-specific configuration.
The first line (and sometimes the only one) of this file is source("../global.inc.r")

One thing to know : all the script in a project will be runned with it's own directory as working directory.
So all path are based on the directory of the script.
A project should only know one file outside its own directory : global.inc.r, all other files should not be reach directly.
If a project need a file outside its directory, it should be a shared library, so use share.lib() function.

By convention, all scripts that should be directly runned by R (except for conf.r) are in the project directory.
All files containing only functions, variables definition (called "library") should be in a lib/ sub-directory.
  
Running a file of a project
=========================
To run a script, the working directory of R must be the directory of the project. All path should be relative to this directory (never use absolute path).

So  R --vanilla < myscript.r 

Developping using the framework
====================================

Coding convention
-------------------

- variables should be in lower case. Some upper case variable should be considered as constant = GLOBAL CONF, not mutable.
- function comment uses a javadoc style tag mainly @param, @return 
- only one instruction on one line : banish ';'
- indentation is the way of life
- always mark a block start with a '{' and the end with a '}', even with a short if()
- add a space after a comma, between operators and to mark a blank parameter (column selection)
	a==b&i<3 =>  (a == b) & (i < 3) # 
	m[,]  => m[, ]
	
Global variables
----------------------------------
 * .Share contains all global parameters of the framework (the running "environment" of the framework)
 * share.option() allow to access to its values
 
 * SHARE_LIB_PATH, SHARE_DATA_PATH : "constant" with absolute path to share/lib and share/data (using function share.*.path is better)

Managing file paths
---------------------------------- 
## Never use absolute path. (allowed only in location.r)
 
 * share.lib(name) : Load a shared library (name is the file name in share/lib, or the relative path in it) without the '.r' extension
 * share.path(file) : return a file path in share 
 * share.data.path(file) : return a file path in share/data
 
- Output path 
 * init.path(dir) : add a directory in the current output path and make it as default output path
 * my.path(file) : return the file path in the current output path
 
Database functions
----------------

* dQuery(...) : run a query (if several parameters are provided they are collapsed without separation (simple concatenation)
* dbConnect() : reconnect to the db

Database configuration
DB_DRIVER variable, should be defined in the "location.r" file, and it is the name of the DB library used.
DB_DSN is either a connection name (for RODBC for example) or a list of connection parameters

Graphics functions
-------------------

This functions are device graphic function wrappers. Default use 'png()' function, but for some config others graphics devices could be used.

* graph.open(file, ...) : starts a graphic output in a file 
* graph.close() : ends the output
* graph.hook(fn) : register a hook function called after the graphic output (the file is created)

ISO 8601 week calculation functions
------------------------------

* ISOYearWeek(dates) : yearweek number of each date
* weeksbydates(from, to) : yearweek numbers for each date of a date interval
* mondayOfDate(d) -> Monday of the date
* WeekStart(yw) -> Monday of a yearweek vector
* YearStart(year) -> Date of the first monday of the year
* makeWeekIndex(yw) -> data.frame with a sequential index of weeks

Others function
------------------

* replace.names(df, ...) : replace names of a data.frame, parameters are  newname="oldname"
* merge.list() : merge 2 list
