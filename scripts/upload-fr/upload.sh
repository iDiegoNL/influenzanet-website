#!/bin/sh
set -e

HOST=epidb@www.influweb.it:upload/
SOURCE_DBNAME=epiwork
TARGET_DBNAME=epipop
COUNTRY='fr'

DIR=`dirname $0`

echo "Creating export tables"
psql -f $DIR/dump.sql $SOURCE_DBNAME

echo "Creating dump"
pg_dump -Fc -x -O -t epidb_results_intake -t epidb_results_weekly --clean --no-owner $SOURCE_DBNAME > epidb_results_fr.dump

echo "Cleanup target database"
psql -f $DIR/cleanup.sql $TARGET_DBNAME

echo "Installing dump in target db"
pg_restore -d $TARGET_DBNAME --no-owner --create < epidb_results_fr.dump

psql -e -f $DIR/rename.sql $TARGET_DBNAME

echo "Creating final dump from target db"
pg_dump -Fc -x -O -t pollster_results_intake -t pollster_results_weekly $TARGET_DBNAME > pollster_results_$COUNTRY.dump

echo "Uploading"
scp -Cq pollster_results_$COUNTRY.dump $HOST

