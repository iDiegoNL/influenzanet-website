#!/bin/sh
set -e

HOST=grippenet@85.90.70.27
DBNAME=epiwork

DIR=`dirname $0`

echo "Creating export tables"
psql -f $DIR/dump.sql $DBNAME

echo "Creating dump"
pg_dump -t epidb_results_intake -t epidb_results_weekly --clean --no-owner $DBNAME > epidb_results.sql

echo "Uploading"
scp -v epidb_results.sql $HOST

echo "Importing data in target host"
ssh $HOST 'psql -f epidb_results.sql'
