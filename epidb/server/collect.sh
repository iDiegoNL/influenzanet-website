# -x : no grant/revoke
# -O : no owner
# -Fc: custom format

#echo ggm
pg_dump -x -O -Fc -t epidb_results_intake -t epidb_results_weekly ggm --clean > /home/epidb/data/epidb_results.custom
pg_dump -x -O -Fc --data-only -t epidb_results_intake -t epidb_results_weekly flusurvey >> /home/epidb/data/epidb_results.custom 

#echo gripenet
pg_dump -x -O -Fc --data-only -t epidb_results_intake -t epidb_results_weekly gripenet >> /home/epidb/data/epidb_results.custom

#echo grippenet
pg_dump -x -O -Fc --data-only -t epidb_results_intake -t epidb_results_weekly grippenet >> /home/epidb/data/epidb_results.custom

#echo influensakoll
pg_dump -x -O -Fc --data-only -t epidb_results_intake -t epidb_results_weekly influensakoll >> /home/epidb/data/epidb_results.custom

#echo influweb
pg_dump -x -O -Fc --data-only -t epidb_results_intake -t epidb_results_weekly influweb >> /home/epidb/data/epidb_results.custom

echo 'DROP TABLE epidb_results_weekly CASCADE;' | psql 2>/dev/null > /dev/null
echo 'DROP TABLE epidb_results_intake CASCADE;' | psql 2>/dev/null > /dev/null

cat '/home/epidb/data/epidb_results.custom' | pg_restore --dbname=epidb 2>/dev/null

cat /home/epidb/scripts/pollster_incidence.sql | psql 2>/dev/null > /dev/null

