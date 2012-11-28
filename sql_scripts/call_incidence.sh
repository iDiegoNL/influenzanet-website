#!/bin/sh

dbname="influweb_it_2012"
username="influweb_it"
psql $dbname $username << EOF

select * from pollster_ili_incidence('2012-10-29', '2012-11-26');
EOF
