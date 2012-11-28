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


-- returns the global_id for ILI users in a given date
DROP FUNCTION IF EXISTS pollster_ILI_only_users (date);

CREATE FUNCTION pollster_ILI_only_users (
    date -- $1 current day
) RETURNS TABLE (
    global_id text,
    first timestamptz
) AS $body$
SELECT global_id, first
  FROM (
        SELECT Z.global_id, 
              min(Z.timestamp) AS first
          FROM pollster_health_status W,
               pollster_results_weekly Z
          WHERE W.pollster_results_weekly_id = Z.id
          AND W.status = 'ILI'
         GROUP BY Z.global_id
       ) AS ILI_cases
$body$ LANGUAGE 'sql';

DROP FUNCTION IF EXISTS pollster_ili_cases_users (date);

-- returns the global_id for active users with ILI onset on a given date
CREATE OR REPLACE FUNCTION pollster_ili_cases_users (
  date -- $1 current day
) RETURNS TABLE (
  global_id text
)
AS $body$
SELECT DISTINCT W.global_id
     FROM  pollster_results_weekly W,
           pollster_ILI_only_users($1) A,
           pollster_health_status Z
     WHERE W.global_id = A.global_id
       -- consider only user which set the onset date as the current date or
       -- take the submission date as the onset date
      AND date_trunc('day', COALESCE(W."Q3_0_open", W.timestamp)) = date_trunc('day', $1)
      AND Z.status = 'ILI'
      AND Z.pollster_results_weekly_id = W.id
      AND COALESCE(W."Q3_0_open", W.timestamp)::date > A.first::date

$body$
LANGUAGE 'sql';

DROP FUNCTION IF EXISTS pollster_ili_only_incidence (date, date);

-- returns the incidence ratio for a time period
CREATE OR REPLACE FUNCTION pollster_ili_only_incidence (
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
          (SELECT count(*) FROM pollster_ILI_only_users(p_day))::integer AS active,
          (SELECT count(*) FROM pollster_ili_cases_users(p_day))::integer AS ili
      FROM pollster_calendar
     WHERE p_day BETWEEN $1 AND $2
     ) AS incidence;
$body$
LANGUAGE 'sql';

