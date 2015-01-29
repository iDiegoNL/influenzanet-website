#!/bin/sh
set -e

TARGET_HOST=epidb@www.influweb.it:upload/
SOURCE_DBNAME=epiwork
COUNTRY='fr'

TABLE_NS='epidb_fr'

# Provide local config vars : DB_HOST,DB_USER,DB_NAME
source $HOME/location.sh

DIR=`dirname $0`

# Connexion string
DB_CNX=" --host=$DB_HOST --user=$DB_USER"

echo "Creating export tables"
psql $DB_CNX  -f $DIR/dump-2014.sql $DB_NAME

echo "Creating dump"
pg_dump $DB_CNX -Fc -x -O -t $TABLE_NS.pollster_results_intake -t $TABLE_NS.pollster_results_weekly --clean --no-owner $DB_NAME > pollster_results_$COUNTRY.dump

echo "Uploading"
scp -Cq pollster_results_$COUNTRY.dump $TARGET_HOST
