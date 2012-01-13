#!/bin/bash
set -e

#cat dump_intake_2_countries.sql | psql
#cat dump_weekly_2_countries.sql | psql

cat dump_intake.sql | psql
cat dump_weekly.sql | psql

pg_dump -t epidb_results_intake -t epidb_results_weekly --clean > epidb_results.sql
grep -v 'ALTER TABLE public.*OWNER TO' epidb_results.sql.tmp
mv epidb_results.sql.tmp epidb_results.sql

scp epidb_results.sql YOURUSER@85.90.70.27:

ssh YOURUSER@85.90.70.27 'cat epidb_results.sql | psql'

