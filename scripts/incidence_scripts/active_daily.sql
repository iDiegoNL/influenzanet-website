-- support function and table for days
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


-- returns the global_id for active users in a given date
DROP FUNCTION IF EXISTS pollster_active_users (date);

CREATE FUNCTION pollster_active_users (
    date -- $1 current day
) RETURNS TABLE (
    rate integer
) AS $body$
SELECT rate
  FROM (
  select count(*)::integer AS rate 
  from auth_user 
  where date_trunc('day',date_joined) < $1
        -- extract the time of the first submission, the time of
        -- the last one and the number of submitted symptoms surveys
        --SELECT   count(*)::integer AS rate
         -- FROM auth_user AS AU
         --WHERE date_trunc('day', AU.date_joined) < $1
       ) AS range;
$body$ LANGUAGE 'sql';


DROP FUNCTION IF EXISTS pollster_act_daily (date, date);

-- returns the incidence ratio for a time period
CREATE OR REPLACE FUNCTION pollster_act_daily (
  date, -- $1 first day
  date -- $2 last day
) RETURNS TABLE (
  "Day" date,
  "Active" integer
)
AS $body$
SELECT p_day AS "Day", active AS "Active"
  FROM (
   SELECT p_day,
          (SELECT * FROM pollster_active_users(p_day))::integer AS active
      FROM pollster_calendar
     WHERE p_day BETWEEN $1 AND $2
     ) AS incidence;
$body$
LANGUAGE 'sql';

