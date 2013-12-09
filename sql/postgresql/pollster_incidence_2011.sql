-- Template for incidence for a given year
-- Each season is in separated table to be considered independently (since participation is restarted on each season)

DROP FUNCTION IF EXISTS pollster_active_users_2011();
-- returns the global_id for active users in a given date
CREATE OR REPLACE FUNCTION pollster_active_users_2011 (
  date, -- $1 current day
  min_survey int default 4 -- $2 min number of survey needed to be active
) RETURNS TABLE (
    global_id text
) AS $body$ 
SELECT global_id
  FROM (
        -- extract the time of the first submission, the time of
        -- the last one and the number of submitted symptoms surveys
        SELECT W.global_id,
               min(W.timestamp) AS first,
               max(W.timestamp) AS latest,
               count(*) AS rate
          FROM pollster_results_weekly_2011 W
         GROUP BY W.global_id
       ) AS ranges
       -- to be considered active an user needs at least 4 filled survey
 WHERE rate > $2
       -- the first compiled survey should be at least one day old
   AND date_trunc('day', first) + '1 day' < date_trunc('day', $1)
       -- the last compilation should not be after the current date
   AND date_trunc('day', $1) <= date_trunc('day', latest)
$body$ LANGUAGE 'sql';

DROP FUNCTION IF EXISTS pollster_ili_users_2011();
-- returns the global_id for active users with ILI onset on a given date
CREATE OR REPLACE FUNCTION pollster_ili_users_2011 (
  date, -- $1 current day
  min_survey int default 4 -- $2 min number of survey needed to be active
) RETURNS TABLE (
  global_id text
)
AS $body$
SELECT DISTINCT A.global_id
      FROM pollster_health_status_2011 S,
           pollster_results_weekly_2011 W,
           pollster_active_users_2011($1,$2) A
     WHERE S.pollster_results_weekly_id = W.id
       AND W.global_id = A.global_id
       -- consider only user which set the onset date as the current date or
       -- take the submission date as the onset date
       AND date_trunc('day', COALESCE(to_date(W."Q3_0_open",'YYYY-MM-DD'), W.timestamp)) = date_trunc('day', $1)
       -- filter only ILI-related symptoms
       AND S.status = 'ILI'
$body$
LANGUAGE 'sql';

DROP FUNCTION IF EXISTS pollster_ili_incidence_2011();

CREATE FUNCTION pollster_ili_incidence_2011 (
  date, -- $1 first day
  date  -- $2 last day
) RETURNS TABLE (
  "day"         date,
  "incidence"   float,
  "active"	bigint,
  "ili"		bigint
)
AS $body$
SELECT 
     p_day AS "Day", 
	 CASE active WHEN 0 THEN 0 ELSE ili::float/active END AS "incidence",
	 active,
	 ili
  FROM (
    SELECT p_day,
          (SELECT count(*) FROM pollster_active_users_2011(p_day)) AS active,
          (SELECT count(*) FROM pollster_ili_users_2011(p_day)) AS ili
      FROM pollster_calendar
     WHERE p_day BETWEEN $1 AND $2
     ) AS incidence;
$body$
LANGUAGE 'sql';

GRANT EXECUTE ON FUNCTION pollster_active_users_2011(date, integer) TO GROUP "DBA";
GRANT EXECUTE ON FUNCTION pollster_active_users_2011(date, integer) TO GROUP "Statistician";
GRANT EXECUTE ON FUNCTION pollster_ili_incidence_2011(date, date) TO GROUP "DBA";
GRANT EXECUTE ON FUNCTION pollster_ili_incidence_2011(date, date) TO GROUP "Statistician";
GRANT EXECUTE ON FUNCTION pollster_ili_users_2011(date, integer) TO GROUP "DBA";
GRANT EXECUTE ON FUNCTION pollster_ili_users_2011(date, integer) TO GROUP "Statistician";
