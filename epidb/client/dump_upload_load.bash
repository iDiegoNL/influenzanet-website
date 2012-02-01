#!/bin/bash
set -e

#cat /home/ggm/scripts/dump_intake_2_countries.sql | psql > /dev/null
#cat /home/ggm/scripts/dump_weekly_2_countries.sql | psql > /dev/null

cat /home/ggm/scripts/dump_intake.sql | psql > /dev/null
cat /home/ggm/scripts/dump_weekly.sql | psql > /dev/null

pg_dump -t epidb_results_intake -t epidb_results_weekly --clean > /home/ggm/data/epidb_results.sql
grep -v 'ALTER TABLE public.*OWNER TO' /home/ggm/data/epidb_results.sql > /home/ggm/data/epidb_results.sql.tmp
mv /home/ggm/data/epidb_results.sql.tmp /home/ggm/data/epidb_results.sql

scp /home/ggm/data/epidb_results.sql ggm@85.90.70.27: >/dev/null

ssh ggm@85.90.70.27 'cat epidb_results.sql | psql' > /dev/null

