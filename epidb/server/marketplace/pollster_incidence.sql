-- pollster incidence function for 'epidb'; i.e. for tables w/o the pollster app
-- support function and table for days
CREATE OR REPLACE FUNCTION calendar(date, date) RETURNS SETOF date AS  $$
        SELECT $1 + s.a as days
          FROM generate_series(0,($2 - $1)::int) as s(a)
$$ LANGUAGE SQL;

DROP TABLE IF EXISTS pollster_calendar;
CREATE TABLE pollster_calendar (
    p_day            date,
    p_week           date,
    p_month          date,
    p_quarter        date,
    p_year           date,
    p_week_month     int8,
    p_week_year      int8,
    p_quarter_year   int8,

    PRIMARY KEY (p_day)
);

DROP VIEW IF EXISTS pollster_health_status;
CREATE VIEW pollster_health_status AS
   SELECT global_id as pollster_results_weekly_id,
          case true
              when "Q1_0"
                  then 'NO-SYMPTOMS'
              when "Q5" = 0
               and ("Q1_1" or "Q1_11" or "Q1_8" or "Q1_9")
               and ("Q1_5" or "Q1_6" or "Q1_7")
                  then 'ILI'
              when "Q5" = 1
               and ("Q1_4" or "Q1_5" or "Q1_6" or "Q1_7")
                  then 'COMMON-COLD'
              when "Q1_15" or "Q1_16" or "Q1_17" and "Q1_18"
                  then 'GASTROINTESTINAL'
              else 'NON-INFLUENZA'
          end as status
     FROM epidb_results_weekly;


INSERT INTO pollster_calendar
SELECT day,
       date_trunc('week',day),
       date_trunc('month',day),
       date_trunc('quarter',day),
       date_trunc('year',day),
       to_char(day,'w')::int8,
       to_char(day,'ww')::int8,
       to_char(day,'Q')::int8
FROM (SELECT calendar('1999-1-1','2020-12-31') as day) A;

-- returns the global_id for active users in a given date
CREATE OR REPLACE FUNCTION pollster_active_users (
    date, -- $1 current day
    text  -- $2 country
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
          FROM epidb_results_weekly W
          WHERE country = $2
         GROUP BY W.global_id
       ) AS ranges
       -- to be considered active an user needs at least 4 filled survey
 WHERE rate > 4
       -- the first compiled survey should be at least one day old
   AND date_trunc('day', first) + '1 day' < date_trunc('day', $1)
       -- the last compilation should not be after the current date
   AND date_trunc('day', $1) >= date_trunc('day', latest)
$body$ LANGUAGE 'sql';

-- returns the global_id for active users with ILI onset on a given date
CREATE OR REPLACE FUNCTION pollster_ili_users (
  date, -- $1 current day
  text  -- $2 country
) RETURNS TABLE (
  global_id text
)
AS $body$
SELECT DISTINCT A.global_id
      FROM pollster_health_status S,
           epidb_results_weekly W,
           pollster_active_users($1, $2) A
     WHERE S.pollster_results_weekly_id = W.global_id
       AND W.global_id = A.global_id
       -- consider only user which set the onset date as the current date or
       -- take the submission date as the onset date
       AND date_trunc('day', COALESCE(W."Q3_0_open", W.timestamp)) = date_trunc('day', $1)
       -- filter only ILI-related symptoms
       AND S.status = 'ILI'
       AND W.country = $2
$body$
LANGUAGE 'sql';

-- returns the incidence ratio for a time period, per country
CREATE OR REPLACE FUNCTION pollster_ili_incidence (
  date, -- $1 first day
  date,  -- $2 last day
  text -- $3 country
) RETURNS TABLE (
  "Day"         date,
  "Incidence"   float
)
AS $body$
SELECT p_day AS "Day", CASE active WHEN 0 THEN 0 ELSE ili::float/active END AS "Incidence"
  FROM (
    SELECT p_day,
          (SELECT count(*) FROM pollster_active_users(p_day, $3)) AS active,
          (SELECT count(*) FROM pollster_ili_users(p_day, $3)) AS ili
      FROM pollster_calendar
     WHERE p_day BETWEEN $1 AND $2
     ) AS incidence;
$body$
LANGUAGE 'sql';
