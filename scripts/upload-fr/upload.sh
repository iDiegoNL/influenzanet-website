#!/bin/sh
set -e

HOST=epidb@www.influweb.it:upload/
SOURCE_DBNAME=epiwork.epidb
COUNTRY='fr'

DIR=`dirname $0`

echo "Creating export tables"
psql -f $DIR/dump-2014.sql $SOURCE_DBNAME

echo "Creating dump"
pg_dump -Fc -x -O -t pollster_results_intake -t pollster_results_weekly --clean --no-owner $SOURCE_DBNAME > pollster_results_$COUNTRY.dump

echo "Uploading"
scp -Cq pollster_results_$COUNTRY.dump $HOST

