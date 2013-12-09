#!/bin/sh
set -e

HOST=grippenet@epidb.influenzanet.eu
DBNAME=epiwork

DIR=`dirname $0`

echo "Creating export tables"
psql -f $DIR/dump.sql $DBNAME

echo "Creating dump"
pg_dump -t epidb_results_intake -t epidb_results_weekly --clean --no-owner -x $DBNAME > epidb_results.sql

echo "Uploading"
scp -Cq epidb_results.sql $HOST:.

echo "Importing data in target host"
ssh $HOST './import-epidb.sh'
