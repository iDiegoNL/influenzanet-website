#!/bin/bash
set -e

#cat /home/ggm/scripts/dump_intake_2_countries.sql | psql > /dev/null
#cat /home/ggm/scripts/dump_weekly_2_countries.sql | psql > /dev/null

psql -f /var/www/influweb.it/httpdocs/epiwork-website/epidb/client/dump_weekly.sql -d influweb_it_2012 > /dev/null
psql -f /var/www/influweb.it/httpdocs/epiwork-website/epidb/client/dump_intake.sql -d influweb_it_2012 > /dev/null

pg_dump influweb_it_2012 -t epidb_results_intake -t epidb_results_weekly --clean > /var/www/influweb.it/httpdocs/epiwork-website/epidb/client/epidb_results.sql

grep -v 'ALTER TABLE public.*OWNER TO' /var/www/influweb.it/httpdocs/epiwork-website/epidb/client/epidb_results.sql > /var/www/influweb.it/httpdocs/epiwork-website/epidb/client/epidb_results.sql.tmp
mv /var/www/influweb.it/httpdocs/epiwork-website/epidb/client/epidb_results.sql.tmp /var/www/influweb.it/httpdocs/epiwork-website/epidb/client/epidb_results.sql

scp /var/www/influweb.it/httpdocs/epiwork-website/epidb/client/epidb_results.sql influweb@epidb.influenzanet.eu: > /dev/null

ssh influweb@epidb.influenzanet.eu 'psql -f epidb_results.sql' > /dev/null
ssh influweb@epidb.influenzanet.eu 'echo "GRANT SELECT ON epidb_results_intake, epidb_results_weekly TO epidb" | psql' > /dev/null
