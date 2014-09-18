-------------------------------------------------------------------------------
-- support function and table for days
-------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION stats_calendar(date, date) RETURNS SETOF date AS $$
        SELECT $1 + s.a as days
          FROM generate_series(0,($2 - $1)::int) as s(a)
$$ LANGUAGE SQL;

DROP TABLE IF EXISTS stats_pollster_calendar;
CREATE TABLE stats_pollster_calendar (
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

INSERT INTO stats_pollster_calendar
  SELECT day,
         date_trunc('week',day),
         date_trunc('month',day),
         date_trunc('quarter',day),
         date_trunc('year',day),
         to_char(day,'w')::int8,
         to_char(day,'ww')::int8,
         to_char(day,'Q')::int8
    FROM (SELECT stats_calendar('1999-1-1','2020-12-31') as day) A;


-------------------------------------------------------------------------------
-- return the maximum distance in days between surveys submissions
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_max_days ();

CREATE OR REPLACE FUNCTION stats_max_days (
) RETURNS TABLE (gids text, days integer)
AS $body$
  DECLARE
    a date;
    b integer;
    i text;
    j date;
  BEGIN
    FOR i IN SELECT DISTINCT "global_id" FROM pollster_results_weekly LOOP
      a := (SELECT "timestamp" FROM pollster_results_weekly WHERE "global_id" = i ORDER BY "timestamp" ASC LIMIT 1);
      b := 0;
      FOR j IN SELECT "timestamp" FROM pollster_results_weekly WHERE "global_id" = i ORDER BY "timestamp" ASC LOOP
        IF (j::date - a::date) > b THEN
          b := (j::date - a::date);
        END IF;
        a := j;
      END LOOP;
      gids := i;
      days := b;
      RETURN NEXT;
    END LOOP;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- support table and populate function for max distance based active users
-------------------------------------------------------------------------------
DROP TABLE IF EXISTS stats_max_days_users;

CREATE TABLE stats_max_days_users (
    gid text
);


DROP FUNCTION IF EXISTS stats_max_days_users_populate (integer);

CREATE OR REPLACE FUNCTION stats_max_days_users_populate (
    integer -- $1 number of days to use as max distance
) RETURNS void
AS $body$
  BEGIN
    DELETE FROM stats_max_days_users;
    INSERT INTO stats_max_days_users SELECT DISTINCT gids FROM stats_max_days() WHERE days < $1;
    RETURN;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- support table and populate function for users to not consider new ILI
-------------------------------------------------------------------------------
DROP TABLE IF EXISTS stats_window_users;

CREATE TABLE stats_window_users (
    gid text,
    wid integer,
    date date
);


DROP FUNCTION IF EXISTS stats_window_users_populate (integer);

CREATE OR REPLACE FUNCTION stats_window_users_populate (
    integer -- $1 number of days to use as window to ignore users
) RETURNS void
AS $body$
  DECLARE
    a date;
    i text;
    j record;
  BEGIN
    DELETE FROM stats_window_users;
    INSERT INTO stats_window_users SELECT W."global_id",
                                          W."id",
                                          COALESCE(W."Q3_0_open", W."timestamp")::date
                                     FROM pollster_health_status S,
                                          pollster_results_weekly W
                                     WHERE S."pollster_results_weekly_id" = W."id"
                                       AND S."status" = 'ILI'
                                     ORDER BY 3 ASC
    ;
    FOR i IN SELECT DISTINCT "gid" FROM stats_window_users LOOP
      a := '1970-01-01';
      FOR j IN SELECT "date", "wid" FROM stats_window_users WHERE "gid" = i ORDER BY "date" ASC LOOP
        IF (j."date" - a) <= $1 THEN
          DELETE FROM stats_window_users WHERE "wid" = j."wid";
        ELSE
          a := j."date";
        END IF;
      END LOOP;
    END LOOP;
    RETURN;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- returns the global_id for active users in a given date
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_active_users (date);

CREATE FUNCTION stats_pollster_active_users (
    date -- $1 current day
) RETURNS TABLE (
    global_id text,
    first timestamptz,
    last timestamptz,
    submitted integer
) AS $body$
SELECT global_id, first, last, submitted
  FROM (
        -- extract the time of the first submission, the time of
        -- the last one and the number of submitted symptoms surveys
        SELECT W.global_id,
               min(W.timestamp) AS first,
               max(W.timestamp) AS last,
               count(*)::integer AS submitted
          FROM pollster_results_weekly W
          GROUP BY W.global_id
       ) AS ranges
       -- to be considered active an user needs at least 3 filled survey
  WHERE submitted >=3
       -- the first compiled survey should be at least one day old
-- AND date_trunc('day', first) < date_trunc('day', $1)
       -- the last compilation should not be *BEFORE* the current date
   AND date_trunc('day', $1) <= date_trunc('day', last)
       -- include only users who have compiled at least one symptoms questionnaire every N days, on average
   AND ( (last::date - first::date) / submitted::float ) < 28
   -- ignore users based on max distance between surveys submissions
   -- (remember to call the populate function first!
   --  we do it in upper level calling functions,
   --  e.g. stats_pollster_prov_active)
-- AND global_id IN (SELECT "gid" FROM stats_max_days_users)
$body$ LANGUAGE 'sql';


-------------------------------------------------------------------------------
-- returns the global_id for active users with ILI onset on a given date
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_ili_users (date);

CREATE OR REPLACE FUNCTION stats_pollster_ili_users (
  date -- $1 current day
) RETURNS TABLE (
  global_id text
)
AS $body$
SELECT DISTINCT A.global_id
  FROM pollster_health_status S,
       pollster_results_weekly W,
       stats_pollster_active_users($1) A
  WHERE S.pollster_results_weekly_id = W.id
   AND W.global_id = A.global_id
   -- consider only user which set the onset date as the current date or
   -- take the submission date as the onset date
   AND date_trunc('day', COALESCE(W."Q3_0_open", W.timestamp)) = date_trunc('day', $1)
   -- filter only ILI-related symptoms
   AND S.status = 'ILI'
   -- ignore users inside specified window
   -- (remember to call the populate function first!
   --  we do it in upper level calling functions,
   --  e.g. stats_pollster_prov_active_ili)
-- AND W.id IN (SELECT "wid" FROM stats_window_users)
$body$
LANGUAGE 'sql';


-------------------------------------------------------------------------------
-- returns the global_id for total users with ILI onset on a given date
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_total_ili_users (date);

CREATE OR REPLACE FUNCTION stats_pollster_total_ili_users (
  date -- $1 current day
) RETURNS TABLE (
  global_id text
)
AS $body$
SELECT DISTINCT W.global_id
  FROM pollster_health_status S,
       pollster_results_weekly W
  WHERE S.pollster_results_weekly_id = W.id
   -- consider only user which set the onset date as the current date or
   -- take the submission date as the onset date
   AND date_trunc('day', COALESCE(W."Q3_0_open", W.timestamp)) = date_trunc('day', $1)
   -- filter only ILI-related symptoms
   AND S.status = 'ILI'
$body$
LANGUAGE 'sql';


-------------------------------------------------------------------------------
-- returns active users by day
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_national_active (date, date);

CREATE OR REPLACE FUNCTION stats_pollster_national_active (
  date, -- $1 first day
  date -- $2 last day
) RETURNS TABLE (
  "Giorno" date,
  "Attivi" integer,
  "ILI" integer
)
AS $body$
SELECT p_day AS "Giorno", active AS "Attivi", ili AS "ILI"
  FROM (
    SELECT p_day,
           (SELECT count(*) FROM (SELECT DISTINCT ON ("global_id") "Q3", "provincia" FROM pollster_results_intake JOIN rel_cap_province_new ON "Q3" = "cap" WHERE "global_id" IN (SELECT "global_id" FROM stats_pollster_active_users(p_day)) AND "Q3" IS NOT NULL ORDER BY "global_id", "timestamp" DESC) AS provs)::integer AS active,
           (SELECT count(*) FROM (SELECT DISTINCT ON ("global_id") "Q3", "provincia" FROM pollster_results_intake JOIN rel_cap_province_new ON "Q3" = "cap" WHERE "global_id" IN (SELECT "global_id" FROM stats_pollster_ili_users(p_day)) AND "Q3" IS NOT NULL ORDER BY "global_id", "timestamp" DESC) AS provs)::integer AS ili
      FROM stats_pollster_calendar
      WHERE p_day BETWEEN $1 AND $2
    ) AS foo;
$body$
LANGUAGE 'sql';


-------------------------------------------------------------------------------
-- returns total ILI users by day
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_national_total_ili (date, date);

CREATE OR REPLACE FUNCTION stats_pollster_national_total_ili (
  date, -- $1 first day
  date -- $2 last day
) RETURNS TABLE (
  "Giorno" date,
  "ILI" integer
)
AS $body$
SELECT p_day AS "Giorno", ili AS "ILI"
  FROM (
    SELECT p_day,
           (SELECT count(*) FROM (SELECT DISTINCT ON ("gid") gid FROM stats_window_users WHERE date = p_day ORDER BY gid, date DESC) AS ilis)::integer AS ili
      FROM stats_pollster_calendar
      WHERE p_day BETWEEN $1 AND $2
    ) AS foo;
$body$
LANGUAGE 'sql';

-------------------------------------------------------------------------------
-- returns province for active users
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_prov_active (date, date);

CREATE OR REPLACE FUNCTION stats_pollster_prov_active (
  in date, -- $1 first day
  in date,  -- $2 last day
  out "Provincia" text,
  out "Giorno" date,
  out "Attivi" integer
) RETURNS SETOF RECORD
AS $body$
  DECLARE
    cday date;
  BEGIN
--  PERFORM stats_max_days_users_populate(28);
    FOR cday IN SELECT p_day FROM pollster_calendar WHERE p_day BETWEEN $1 AND $2 LOOP
      RETURN QUERY
        (SELECT "provincia"::text, cday::date, count(*)::integer FROM (SELECT DISTINCT ON ("global_id") "Q3", "provincia" FROM pollster_results_intake JOIN rel_cap_province_new ON "Q3" = "cap" WHERE "global_id" IN (SELECT "global_id" FROM stats_pollster_active_users(cday)) AND "Q3" IS NOT NULL ORDER BY "global_id", "timestamp" DESC) AS provs GROUP BY "provincia" ORDER BY "provincia")
        UNION
        (SELECT "provincia"::text, cday::date, 0 FROM rel_cap_province_new WHERE "provincia" NOT IN (SELECT "provincia"::text FROM (SELECT DISTINCT ON ("global_id") "Q3", "provincia" FROM pollster_results_intake JOIN rel_cap_province_new ON "Q3" = "cap" WHERE "global_id" IN (SELECT "global_id" FROM stats_pollster_active_users(cday)) AND "Q3" IS NOT NULL ORDER BY "global_id", "timestamp" DESC) AS provs) GROUP BY "provincia" ORDER BY "provincia")
        ORDER BY "provincia";
    END LOOP;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- returns province for active ili users
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_prov_active_ili (date, date);

CREATE OR REPLACE FUNCTION stats_pollster_prov_active_ili (
  in date, -- $1 first day
  in date,  -- $2 last day
  out "Provincia" text,
  out "Giorno" date,
  out "Attivi ILI" integer
) RETURNS SETOF RECORD
AS $body$
  DECLARE
    cday date;
  BEGIN
--  PERFORM stats_window_users_populate(500);
    FOR cday IN SELECT p_day FROM pollster_calendar WHERE p_day BETWEEN $1 AND $2 LOOP
      RETURN QUERY
        (SELECT "provincia"::text, cday::date, count(*)::integer FROM (SELECT DISTINCT ON ("global_id") "Q3", "provincia" FROM pollster_results_intake JOIN rel_cap_province_new ON "Q3" = "cap" WHERE "global_id" IN (SELECT "global_id" FROM stats_pollster_ili_users(cday)) AND "Q3" IS NOT NULL ORDER BY "global_id", "timestamp" DESC) AS provs GROUP BY "provincia" ORDER BY "provincia")
        UNION
        (SELECT "provincia"::text, cday::date, 0 FROM rel_cap_province_new WHERE "provincia" NOT IN (SELECT "provincia"::text FROM (SELECT DISTINCT ON ("global_id") "Q3", "provincia" FROM pollster_results_intake JOIN rel_cap_province_new ON "Q3" = "cap" WHERE "global_id" IN (SELECT "global_id" FROM stats_pollster_ili_users(cday)) AND "Q3" IS NOT NULL ORDER BY "global_id", "timestamp" DESC) AS provs) GROUP BY "provincia" ORDER BY "provincia")
        ORDER BY "provincia";
    END LOOP;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- returns province for total ili users
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_prov_total_ili (date, date);

CREATE OR REPLACE FUNCTION stats_pollster_prov_total_ili (
  in date, -- $1 first day
  in date,  -- $2 last day
  out "Provincia" text,
  out "Giorno" date,
  out "Totali ILI" integer
) RETURNS SETOF RECORD
AS $body$
  DECLARE
    cday date;
  BEGIN
    FOR cday IN SELECT p_day FROM pollster_calendar WHERE p_day BETWEEN $1 AND $2 LOOP
      RETURN QUERY
        (SELECT "provincia"::text, cday::date, count(*)::integer FROM (SELECT DISTINCT ON ("global_id") "Q3", "provincia" FROM pollster_results_intake JOIN rel_cap_province_new ON "Q3" = "cap" WHERE "global_id" IN (SELECT "global_id" FROM stats_pollster_total_ili_users(cday)) AND "Q3" IS NOT NULL ORDER BY "global_id", "timestamp" DESC) AS provs GROUP BY "provincia" ORDER BY "provincia")
        UNION
        (SELECT "provincia"::text, cday::date, NULL FROM rel_cap_province_new WHERE "provincia" NOT IN (SELECT "provincia"::text FROM (SELECT DISTINCT ON ("global_id") "Q3", "provincia" FROM pollster_results_intake JOIN rel_cap_province_new ON "Q3" = "cap" WHERE "global_id" IN (SELECT "global_id" FROM stats_pollster_total_ili_users(cday)) AND "Q3" IS NOT NULL ORDER BY "global_id", "timestamp" DESC) AS provs) GROUP BY "provincia" ORDER BY "provincia")
        ORDER BY "provincia";
    END LOOP;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- returns cap for active users
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_cap_active (date, date);

CREATE OR REPLACE FUNCTION stats_pollster_cap_active (
  in date, -- $1 first day
  in date,  -- $2 last day
  out "CAP" text,
  out "Giorno" date,
  out "Attivi" integer
) RETURNS SETOF RECORD
AS $body$
  DECLARE
    cday date;
  BEGIN
    FOR cday IN SELECT p_day FROM pollster_calendar WHERE p_day BETWEEN $1 AND $2 LOOP
      RETURN QUERY SELECT "Q3"::text, cday::date, count(*)::integer FROM (SELECT DISTINCT ON ("global_id") "Q3" FROM pollster_results_intake WHERE "global_id" IN (SELECT DISTINCT "global_id" FROM stats_pollster_active_users(cday)) AND "Q3" IS NOT NULL ORDER BY "global_id", "timestamp" DESC) AS caps GROUP BY "Q3" ORDER BY "Q3";
    END LOOP;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- returns cap for active ili users
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_cap_active_ili (date, date);

CREATE OR REPLACE FUNCTION stats_pollster_cap_active_ili (
  in date, -- $1 first day
  in date,  -- $2 last day
  out "CAP" text,
  out "Giorno" date,
  out "Attivi ILI" integer
) RETURNS SETOF RECORD
AS $body$
  DECLARE
    cday date;
  BEGIN
    FOR cday IN SELECT p_day FROM pollster_calendar WHERE p_day BETWEEN $1 AND $2 LOOP
      RETURN QUERY SELECT "Q3"::text, cday::date, count(*)::integer FROM (SELECT DISTINCT ON ("global_id") "Q3" FROM pollster_results_intake WHERE "global_id" IN (SELECT DISTINCT "global_id" FROM stats_pollster_ili_users(cday)) AND "Q3" IS NOT NULL ORDER BY "global_id", "timestamp" DESC) AS caps GROUP BY "Q3" ORDER BY "Q3";
    END LOOP;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- returns cap for total ili users
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_cap_total_ili (date, date);

CREATE OR REPLACE FUNCTION stats_pollster_cap_total_ili (
  in date, -- $1 first day
  in date,  -- $2 last day
  out "CAP" text,
  out "Giorno" date,
  out "Totali ILI" integer
) RETURNS SETOF RECORD
AS $body$
  DECLARE
    cday date;
  BEGIN
    FOR cday IN SELECT p_day FROM pollster_calendar WHERE p_day BETWEEN $1 AND $2 LOOP
      RETURN QUERY SELECT "Q3"::text, cday::date, count(*)::integer FROM (SELECT DISTINCT ON ("global_id") "Q3" FROM pollster_results_intake WHERE "global_id" IN (SELECT DISTINCT "global_id" FROM stats_pollster_total_ili_users(cday)) AND "Q3" IS NOT NULL ORDER BY "global_id", "timestamp" DESC) AS caps GROUP BY "Q3" ORDER BY "Q3";
    END LOOP;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- number of users by number of surveys submissions
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_users_by_surveys ();

CREATE OR REPLACE FUNCTION stats_users_by_surveys (
) RETURNS TABLE (questionari integer, utenti integer)
AS $body$
  DECLARE
    t integer;
  BEGIN
    FOR i IN 1..150 LOOP
      t := (SELECT count(*) FROM (SELECT count(*) AS utenti_totali FROM pollster_results_weekly GROUP BY global_id) AS totali WHERE totali.utenti_totali = i);
      questionari := i;
      utenti := t;
      RETURN NEXT;
    END LOOP;
    RETURN;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- number of at least once ILI users by number of surveys submissions
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_ili_users_by_surveys ();

CREATE OR REPLACE FUNCTION stats_ili_users_by_surveys (
) RETURNS TABLE (questionari integer, utenti integer)
AS $body$
  DECLARE
    t integer;
  BEGIN
    PERFORM stats_window_users_populate(-1);
    FOR i IN 1..150 LOOP
      t := (SELECT count(*) FROM (SELECT count(*) AS utenti_totali FROM pollster_results_weekly WHERE global_id IN (SELECT gid FROM stats_window_users) GROUP BY global_id) AS totali WHERE totali.utenti_totali = i);
      questionari := i;
      utenti := t;
      RETURN NEXT;
    END LOOP;
    RETURN;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- number of users by number of ILI surveys submissions
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_users_by_ili_surveys ();

CREATE OR REPLACE FUNCTION stats_users_by_ili_surveys (
) RETURNS TABLE (questionari integer, utenti integer)
AS $body$
  DECLARE
    t integer;
  BEGIN
    PERFORM stats_window_users_populate(-1);
    FOR i IN 1..150 LOOP
      t := (SELECT count(*) FROM (SELECT count(*) AS utenti_totali FROM stats_window_users GROUP BY gid) AS totali WHERE totali.utenti_totali = i);
      questionari := i;
      utenti := t;
      RETURN NEXT;
    END LOOP;
    RETURN;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- number of ILI surveys by distance betweeb ILI surveys submissions
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_ili_surveys_by_distance_ili_surveys (integer);

CREATE OR REPLACE FUNCTION stats_ili_surveys_by_distance_ili_surveys (
  integer -- $1 number of ILI surveys that users need to have to be incldued
) RETURNS TABLE (intervallo integer, questionari integer)
AS $body$
  DECLARE
    a date;
    j text;
    k date;
    t integer;
    w integer;
  BEGIN
    PERFORM stats_window_users_populate(-1);
    FOR i IN 0..300 LOOP
      t := 0;
      FOR j IN SELECT DISTINCT ON ("gid") "gid" FROM stats_window_users GROUP BY "gid" HAVING count(*) = $1 ORDER BY "gid" LOOP
        a := (SELECT "date" FROM stats_window_users WHERE "gid" = j ORDER BY "date", "wid" ASC LIMIT 1);
        w := (SELECT "wid" FROM stats_window_users WHERE "gid" = j ORDER BY "date", "wid" ASC LIMIT 1);
        FOR k IN SELECT "date" FROM stats_window_users WHERE "gid" = j AND "wid" != w ORDER BY "date" ASC LOOP
          IF (k - a) = i THEN
            t := t + 1;
          END IF;
          a := k;
        END LOOP;
      END LOOP;
      intervallo := i;
      questionari := t;
      RETURN NEXT;
    END LOOP;
    RETURN;
  END;
$body$
LANGUAGE 'plpgsql';


-------------------------------------------------------------------------------
-- returns the global_id for strict active users in a given range
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS stats_pollster_active_users_strict (date, date);

CREATE FUNCTION stats_pollster_active_users_strict (
    date, -- $1 start of season
    date -- $2 end of season
) RETURNS TABLE (
    global_id text,
    first timestamptz,
    last timestamptz,
    submitted integer
) AS $body$
SELECT global_id, first, last, submitted
  FROM (
        -- extract the time of the first submission, the time of
        -- the last one and the number of submitted symptoms surveys
        SELECT W.global_id,
               min(W.timestamp) AS first,
               max(W.timestamp) AS last,
               count(*)::integer AS submitted
          FROM pollster_results_weekly W
          GROUP BY W.global_id
       ) AS ranges
       -- to be considered active an user needs at least 1 survey per month
  WHERE submitted >= (($2 - $1) / 28)
       -- the first compiled survey should be at least in the first month
   AND date_trunc('day', first)::date <= ($1 + 28)
       -- the last compilation should be at least in the last month
   AND date_trunc('day', last)::date >= ($2 - 28)
   -- ignore users based on max distance between surveys submissions
   AND global_id IN (SELECT "gid" FROM stats_max_days_users)
$body$ LANGUAGE 'sql';
