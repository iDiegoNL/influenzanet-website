#!/bin/sh

dbname="influweb_it"
username="influweb_it"
psql $dbname $username << EOF

select * from pollster_ili_incidence('tomorrow'::date-240, 'tomorrow'::date-1);
EOF
