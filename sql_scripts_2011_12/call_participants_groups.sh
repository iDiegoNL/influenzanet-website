#!/bin/sh

dbname="influweb_it"
username="influweb_it"
psql $dbname $username << EOF


select name, user_id, global_id from survey_surveyuser order by user_id;

EOF
