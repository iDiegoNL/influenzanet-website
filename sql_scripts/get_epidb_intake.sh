#!/bin/sh

dbname="influweb"
username="influweb"
psql $dbname $username << EOF


copy ( 

select country, global_id, "Q3" from epidb_results_intake

) TO STDOUT WITH CSV HEADER;

