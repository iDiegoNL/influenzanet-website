#!/bin/sh

dbname="influweb"
username="influweb"
psql $dbname $username << EOF


copy ( 

select * from epidb_results_weekly

) TO STDOUT WITH CSV HEADER;

