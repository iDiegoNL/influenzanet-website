#echo ggm
pg_dump -t epidb_results_intake -t epidb_results_weekly ggm --clean > /home/epidb/data/epidb_results.sql
#pg_dump --data-only -t epidb_results_intake -t epidb_results_weekly aggat >> /home/epidb/data/epidb_results.sql
#pg_dump --data-only -t epidb_results_intake -t epidb_results_weekly aggch >> /home/epidb/data/epidb_results.sql
#pg_dump --data-only -t epidb_results_intake -t epidb_results_weekly aggde >> /home/epidb/data/epidb_results.sql
#echo flusurvey
pg_dump --data-only -t epidb_results_intake -t epidb_results_weekly flusurvey >> /home/epidb/data/epidb_results.sql

#echo gripenet
pg_dump --data-only -t epidb_results_intake -t epidb_results_weekly gripenet >> /home/epidb/data/epidb_results.sql

#echo grippenet
#pg_dump --data-only -t epidb_results_intake -t epidb_results_weekly grippenet >> /home/epidb/data/epidb_results.sql

#echo influensakoll
# influensakoll appears to be broken
#pg_dump --data-only -t epidb_results_intake -t epidb_results_weekly influensakoll >> /home/epidb/data/epidb_results.sql

#echo influweb
pg_dump --data-only -t epidb_results_intake -t epidb_results_weekly influweb >> /home/epidb/data/epidb_results.sql

grep -v -e '^GRANT' -e '^REVOKE' -e 'OWNER TO' /home/epidb/data/epidb_results.sql > /home/epidb/data/epidb_results.sql.tmp
mv /home/epidb/data/epidb_results.sql.tmp /home/epidb/data/epidb_results.sql

echo 'DROP TABLE epidb_results_weekly CASCADE;' | psql
echo 'DROP TABLE epidb_results_intake CASCADE;' | psql

psql < /home/epidb/data/epidb_results.sql

cat /home/epidb/scripts/pollster_incidence.sql | psql

