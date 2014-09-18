-- support function and table for days



-- returns the global_id for active users in a given date
DROP FUNCTION IF EXISTS stats_pollster_enrolled_users ();

CREATE FUNCTION stats_pollster_enrolled_users (
) RETURNS TABLE (
    global_id text
) AS $body$
SELECT Z.global_id
  FROM (
        -- extract the global_id of enrolled participants
        SELECT DISTINCT W.global_id,
        COUNT(W.timestamp) as numdate
        FROM 
        (      
        SELECT global_id,
        min(timestamp) as mindate, date_trunc('day', min(timestamp))::date + 15 as participationdate
        FROM pollster_results_weekly GROUP by global_id, timestamp
        ) X, pollster_results_weekly W
        WHERE W.timestamp < participationdate and W.timestamp >= X.mindate
        and X.global_id = W.global_id
        GROUP BY W.global_id
        ) Z
        WHERE numdate >=2
$body$ LANGUAGE 'sql';

-- returns the global_id for active users 

DROP FUNCTION IF EXISTS stats_pollster_participants ();

CREATE OR REPLACE FUNCTION stats_pollster_participants (
) RETURNS TABLE (
  global_id text
)
AS $body$
SELECT Z.global_id
       FROM (
       SELECT DISTINCT X.global_id,
       COUNT(X.timestamp) as numdate
       FROM
       (
       SELECT global_id,
       min(timestamp) as mindate,
       date_trunc('day', min(timestamp))::date + 45 AS startdate,
       date_trunc('day', min(timestamp))::date + 75 AS enddate
       FROM  pollster_results_weekly group by global_id
       ) XX, pollster_results_weekly X
       WHERE XX.global_id = X.global_id
       AND date_trunc('day', X.timestamp)::date > XX.startdate
       AND date_trunc('day', X.timestamp)::date < XX.enddate
       GROUP BY X.global_id
       ) Z, stats_pollster_enrolled_users() W
       WHERE Z.numdate >=2 
       AND Z.global_id = W.global_id
       GROUP BY Z.global_id
$body$
LANGUAGE 'sql';

SELECT A.global_id, 
       I."Q0" as household,
       I."Q1" as gender,
       I."Q2" as birthdate,
       I."Q3" as CAP,
       I."Q4" as main_activity,
       I."Q4c" as profession,
       I."Q4d_0" as professional,
       I."Q4d_1" as office_work,
       I."Q4d_2" as sales,
       I."Q4d_3" as skilled_manual_worker,
       I."Q4d_4" as other_manual_work,
       I."Q4d_5" as other,
       I."Q6_0" as zero_four,
       I."Q6_0_open" as num_zero_four,
       I."Q6_1" as five_eighteen,
       I."Q6_1_open" as num_five_eighteen,
       I."Q6_2" as nineteen_fourtyfour,
       I."Q6_2_open" as num_nineteen_fourtyfour,
       I."Q6_3" as fourtyfive_sixtyfour,
       I."Q6_3_open" as num_fourtyfive_sixtyfour,
       I."Q6_4" as sixtyfive_plus,
       I."Q6_4_open" as num_sixtyfive_plus,
       I."Q6b" as kids_daycare,
       I."Q7" as transportation,
       I."Q8" as num_sickness,
       I."Q13" as smoke,
       I."Q17_0" as radio_tv,
       I."Q17_1" as journals,
       I."Q17_2" as internet,
       I."Q17_3" as poster,
       I."Q17_4" as friends_family,
       I."Q17_5" as school_work

FROM pollster_results_intake I,
     stats_pollster_participants() A
WHERE A.global_id = I.global_id;
