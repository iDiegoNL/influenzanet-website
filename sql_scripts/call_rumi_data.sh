#!/bin/sh

dbname="influweb"
username="influweb"
psql $dbname $username << EOF

copy (
-- symptoms NO
select count(global_id) as symptoms_NO from pollster_results_weekly where "Q1_0" = true and timestamp::date > '2013-11-01'
) TO STDOUT WITH CSV HEADER;

copy (
-- symptoms YES
select count(global_id) as symptoms_YES from pollster_results_weekly where "Q1_0" = false and timestamp::date > '2013-11-01' 
) TO STDOUT WITH CSV HEADER;

copy (
-- symptoms YES visit NO 
select count(global_id) as symptoms_YES_visit_NO from pollster_results_weekly where "Q1_0" = false and "Q7_0" = true and timestamp::date > '2013-11-01'
) TO STDOUT WITH CSV HEADER;

copy (
-- symptoms YES visit YES GP
select count(global_id) as symptoms_YES_visit_YES_GP from pollster_results_weekly where "Q1_0" = false and "Q7_0" = false and "Q7_1" = true and timestamp::date > '2013-11-01' 
) TO STDOUT WITH CSV HEADER;

copy (
-- symptoms YES visit YES HOSPITAL
select count(global_id) as symptoms_YES_visit_YES_Hospital from pollster_results_weekly where "Q1_0" = false and "Q7_0" = false and "Q7_2" = true and timestamp::date > '2013-11-01'
) TO STDOUT WITH CSV HEADER;

copy (
-- symptoms YES visit YES ER 
select count(global_id) as symptoms_YES_visit_YES_ER from pollster_results_weekly where "Q1_0" = false and "Q7_0" = false and "Q7_3" = true and timestamp::date > '2013-11-01'
) TO STDOUT WITH CSV HEADER;
