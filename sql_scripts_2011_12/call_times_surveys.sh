#!/bin/sh

dbname="influweb_it"
username="influweb_it"
psql $dbname $username << EOF

SELECT DISTINCT A.global_id, date_trunc('day', A.timestamp), S.status
      FROM pollster_health_status S,
           pollster_results_weekly A
     WHERE S.pollster_results_weekly_id = A.id
     GROUP BY A.global_id, date_trunc('day', A.timestamp), S.status

EOF
