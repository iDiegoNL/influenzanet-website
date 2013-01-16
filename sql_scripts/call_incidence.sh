#!/bin/sh

dbname="influweb_it_2012"
username="influweb_it"
psql $dbname $username << EOF

copy (select * from pollster_ili_incidence('2012-10-29', '2013-01-06')) TO STDOUT WITH CSV HEADER;
EOF
