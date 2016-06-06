-- support function and table for days
CREATE OR REPLACE FUNCTION calendar(date, date) RETURNS SETOF date AS $$
        SELECT $1 + s.a as days
          FROM generate_series(0,($2 - $1)::int) as s(a)
$$ LANGUAGE SQL;

DROP TABLE IF EXISTS pollster_calendar;
CREATE TABLE pollster_calendar (
    p_day date,
    p_week date,
    p_month date,
    p_quarter date,
    p_year date,
    p_week_month int8,
    p_week_year int8,
    p_quarter_year int8,

    PRIMARY KEY (p_day)
);

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


DROP FUNCTION IF EXISTS pollster_ili_users_ourversion_doctor (date);

-- returns the global_id for active users with ILI onset on a given date
CREATE OR REPLACE FUNCTION pollster_ili_users_ourversion_doctor (
  date -- $1 current day
) RETURNS TABLE (
  global_id text
)
AS $body$
SELECT DISTINCT W.global_id
      FROM pollster_health_status S,
           pollster_results_weekly W
           --pollster_active_users($1) A
     WHERE S.pollster_results_weekly_id = W.id
       --AND W.global_id = A.global_id
       -- consider only user which set the onset date as the current date or
       -- take the submission date as the onset date
       AND date_trunc('day', COALESCE(W."Q3_0_open", W.timestamp)) = date_trunc('day', $1)
       -- Ignore any symptoms which started more than 15 days before the 1st survey
       --AND COALESCE(W."Q3_0_open", W.timestamp)::date > A.first::date-15
       -- filter only ILI-related symptoms
       AND S.status = 'ILI'
       -- filter if has seen a GP
       AND W."Q7_0" = False AND (W."Q7_1" = True OR W."Q7_2" = True OR W."Q7_3" = True OR W."Q7_4" = True OR W."Q7_5" = True);       
$body$
LANGUAGE 'sql';

DROP FUNCTION IF EXISTS pollster_ili_incidence_ourversion_doctor (date, date);

-- returns the incidence ratio for a time period
CREATE OR REPLACE FUNCTION pollster_ili_incidence_ourversion_doctor (
  date, -- $1 first day
  date -- $2 last day
) RETURNS TABLE (
  "Day" date,
  "Active" integer,
   "ILI" integer
)
AS $body$
SELECT p_day AS "Day", active AS "Active", ili AS "ILI"
  FROM (
   SELECT p_day,
          (SELECT count(*) FROM pollster_active_users_ourversion(p_day))::integer AS active,
          (SELECT count(*) FROM pollster_ili_users_ourversion_doctor(p_day))::integer AS ili
      FROM pollster_calendar
     WHERE p_day BETWEEN $1 AND $2
     ) AS incidence;
$body$
LANGUAGE 'sql';

