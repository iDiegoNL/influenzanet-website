#!/bin/sh

dbname="influweb"
username="influweb"
psql $dbname $username << EOF

copy (select * from pollster_ili_incidence('2013-11-04', '2013-11-11')) TO STDOUT WITH CSV HEADER;
EOF
