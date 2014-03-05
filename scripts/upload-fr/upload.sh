#!/bin/sh
set -e

HOST=epidb@www.influweb.it:upload/
DBNAME=epiwork
COUNTRY='fr'

DIR=`dirname $0`

echo "Creating export tables"
psql -f $DIR/dump.sql $DBNAME

echo "Creating dump"
pg_dump -Fc -x -O -t epidb_results_intake -t epidb_results_weekly --clean --no-owner $DBNAME > epidb_results_fr.dump

echo "Installing dump"
pg_restore -d epipop --no-owner --clean --create < epidb_results_fr.dump

psql -e -f $DIR/rename.sql epipop

echo "Creating final dump"
pg_dump -Fc -x -O -t pollster_results_intake -t pollster_results_weekly epipop > pollster_results_$COUNTRY.dump

echo "Uploading"
scp -Cq pollster_results_$COUNTRY.dump $HOST

