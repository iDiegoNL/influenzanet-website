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
DROP FUNCTION IF EXISTS pollster_active_users (date, text);

CREATE FUNCTION pollster_active_users (
    date, -- $1 current day    
    text  -- $2 provincia
) RETURNS TABLE (
    day       date,
    global_id text,
    provincia text, 
    first timestamptz,
    last timestamptz,
    rate integer
) AS $body$
SELECT $1, global_id, provincia, first, latest, rate
  FROM (
        -- extract the time of the first submission, the time of
        -- the last one and the number of submitted symptoms surveys
        SELECT W.global_id,
               P.provincia,
               min(W.timestamp) AS first,
               max(W.timestamp) AS latest,
               count(*)::integer AS rate
          FROM pollster_results_weekly W,
               rel_cap_province as P,
               pollster_results_intake as I
         WHERE date_trunc('day', W.timestamp) > '2012-11-01'
           AND P.cap = I."Q3" 
           AND I.global_id = W.global_id
           AND ($2 Is NULL OR $2 = P.provincia)
         GROUP BY W.global_id, P.provincia
       ) AS ranges
       -- to be considered active an user needs at least 3 filled survey
 WHERE rate >=2
       -- the first compiled survey should be at least one day old
   AND date_trunc('day', first) + '1 day' < date_trunc('day', $1)
       -- the last compilation should not be after the current date
   AND date_trunc('day', $1) <= date_trunc('day', latest)
       -- include only users who have compiled at least one symptoms questionnaire every three weeks, on average
   AND ( (latest::date - first::date) / rate::float) < 21   
$body$ LANGUAGE 'sql';


DROP FUNCTION IF EXISTS pollster_ili_users (date);
DROP FUNCTION IF EXISTS pollster_ili_users (date, text);

-- returns the global_id for active users with ILI onset on a given date
CREATE OR REPLACE FUNCTION pollster_ili_users (
  date, -- $1 current day  
  text  -- $2 provincia
) RETURNS TABLE (
  day       date,
  global_id text,
  provincia text
)
AS $body$
SELECT  DISTINCT $1, A.global_id, P.provincia
      FROM pollster_health_status S,
           pollster_results_weekly W,
           pollster_active_users($1,$2) A,
           rel_cap_province P,
           pollster_results_intake as I
           
     WHERE S.pollster_results_weekly_id = W.id      
       AND W.global_id = A.global_id
       AND W.global_id = I.global_id
       AND P.cap = I."Q3" 
       -- consider only user which set the onset date as the current date or
       -- take the submission date as the onset date
       AND date_trunc('day', COALESCE(W."Q3_0_open", W.timestamp)) = date_trunc('day', $1)
       -- Ignore any symptoms which started more than 15 days before the 1st survey
       AND COALESCE(W."Q3_0_open", W.timestamp)::date > A.first::date-15
       -- filter only ILI-related symptoms
       AND S.status = 'ILI'
       AND ($2 IS NULL OR $2 = P.provincia)       
$body$
LANGUAGE 'sql';


DROP FUNCTION IF EXISTS pollster_ili_incidence_province (date);
DROP FUNCTION IF EXISTS pollster_ili_incidence_province (date, text);

-- returns the incidence ratio on a given date
CREATE OR REPLACE FUNCTION pollster_ili_incidence_province (
  date, -- $1 day  
  text -- $2 provincia
) RETURNS TABLE (
  "Day" date,
  "Prov" text, 
  "Active" integer,
   "ILI" integer
)
AS $body$
        SELECT day, provincia, sum(active)::integer AS active, sum(ili)::integer as ili 
        FROM (
                SELECT day, provincia, global_id, 1 as active, 0 as ili FROM pollster_active_users($1, $2) 
                UNION 
                SELECT day, provincia, global_id, 0 as active, 1 as ili FROM pollster_ili_users($1, $2) ) A
        GROUP BY day, provincia;
$body$
LANGUAGE 'sql';


DROP FUNCTION IF EXISTS pollster_ili_incidence_province_period (date, date);

-- returns the incidence ratio on a given date
CREATE OR REPLACE FUNCTION pollster_ili_incidence_province_period (
  date, -- $1 first day  
  date -- $2 last day  
) RETURNS TABLE (
  "Day" date,
  "Prov" text, 
  "Active" integer,
   "ILI" integer
)
AS $body$
        SELECT p_day, provincia, sum(active)::integer AS active, sum(ili)::integer as ili 
        FROM (
                SELECT p_day, provincia, (SELECT count(*) FROM pollster_active_users(p_day, provincia))  as active, 0 as ili FROM
                       pollster_calendar, rel_cap_province
                 WHERE p_day BETWEEN $1 AND $2
                UNION 
                SELECT p_day, provincia, 0  as active, (SELECT count(*) FROM pollster_ili_users(p_day, provincia)) as ili FROM
                       pollster_calendar, rel_cap_province
                 WHERE p_day BETWEEN $1 AND $2) A
                      
        GROUP BY p_day, provincia;
$body$
LANGUAGE 'sql';


DROP FUNCTION IF EXISTS pollster_active_users_stats (date, date);
-- returns the users active on a given period

CREATE OR REPLACE FUNCTION pollster_active_users_stats (
  date, -- $1 first day  
  date -- $2 last day  
) RETURNS TABLE (
  day       date,
  global_id text,
  provincia text,
  first     timestamptz,
  latest    timestamptz,
  rate      integer,
  is_ili    boolean
)
AS $body$

        SELECT DISTINCT 
                day, 
                global_id, 
                provincia, 
                first, 
                latest, 
                rate, 
                first_value(ili) OVER (PARTITION BY day, global_id ORDER BY ili DESC) AS is_ili 
                FROM (
                        SELECT DISTINCT C.p_day AS day, 
                                        U.global_id, 
                                        U.provincia, 
                                        U.first, 
                                        U.latest, 
                                        U.rate::integer, 
                                        (status = 'ILI' AND U.ili_day = p_day AND U.ili_day > U.first::date - 15) AS ili  
                                        FROM pollster_calendar C LEFT OUTER  JOIN 
                                                (SELECT DISTINCT	
                                                               date_trunc('day', W.timestamp) AS day,
							       W.global_id,
               	                                               P.provincia,               		
							       min(W.timestamp) OVER BYG  AS first,
                                                               max(W.timestamp) OVER BYG  AS latest,
                                                               count(*) OVER BYG AS rate,
                                                               S.status, 
                                                               date_trunc('day', COALESCE(W."Q3_0_open", W.timestamp)::date) AS ili_day
                                                          FROM pollster_results_weekly W LEFT OUTER JOIN 
                                                               pollster_health_status S ON (S.pollster_results_weekly_id = W.id),
                                                               rel_cap_province as P,               
                                                               pollster_results_intake as I           
                                                         WHERE date_trunc('day', W.timestamp) > '2011-11-01'
                                                           AND P.cap = I."Q3" 
                                                           AND I.global_id = W.global_id           
			                                WINDOW BYG AS (PARTITION BY W.global_id) ) AS U 
			                                   ON (rate >= 2 
			                                       AND date_trunc('day', first) + '1 day' < date_trunc('day', p_day)
                                                               AND date_trunc('day', p_day) <= date_trunc('day', latest)
                                                               AND ( (latest::date - first::date) / rate::float) < 21 )) A
 			  WHERE day BETWEEN $1 AND $2;

$body$
LANGUAGE 'sql';

