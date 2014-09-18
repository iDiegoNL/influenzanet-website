#!/bin/sh

dbname="influweb"
username="influweb"
psql $dbname $username << EOF


copy (SELECT country, global_id, "user", count("user") OVER (PARTITION BY country, "user" ORDER BY country, "user") FROM (SELECT DISTINCT country, global_id, "user" FROM epidb_results_intake) A) TO STDOUT WITH CSV HEADER;
