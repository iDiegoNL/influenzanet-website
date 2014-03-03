#!/bin/sh

dbname="influweb"
username="influweb"
psql $dbname $username << EOF


copy (select day, provincia, count(*) active, sum(CASE true WHEN is_ili THEN 1
ELSE 0 END) ili FROM pollster_active_users_stats('2014-02-17',
'2014-02-23') GROUP BY 1,2 ORDER BY 1 ASC) TO STDOUT WITH CSV HEADER;

