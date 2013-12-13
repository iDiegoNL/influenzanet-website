DROP VIEW IF EXISTS pollster_dashboard_badges;

-- datasource for particpation badge
-- Remove syndrom (because count distinct produce errornous count of weekly participation
-- by separating each distinct row with a different status
CREATE OR REPLACE VIEW pollster_dashboard_badges AS 
 SELECT DISTINCT a.global_id, a."user", 
  count(*) OVER (PARTITION BY a.global_id) >= 1 AS is_novice, 
  count(*) OVER (PARTITION BY a.global_id) >= 3 AS is_junior, 
  count(*) OVER (PARTITION BY a.global_id) >= 6 AS is_senior, 
  count(*) OVER (PARTITION BY a.global_id) >= 10 AS is_gold, 
  count(*) OVER (PARTITION BY a.global_id) >= 20 AS is_platinum 
   FROM ( SELECT DISTINCT w.global_id, w."user", to_char(w."timestamp", 'YYYYWW'::text) AS yw 
           FROM pollster_results_weekly w 
	) a;

DROP VIEW IF EXISTS pollster_results_last_intake;
DROP VIEW IF EXISTS pollster_results_last_location;
DROP VIEW IF EXISTS pollster_results_last_intake_id;

--- Get the last intake id for each participant
CREATE VIEW pollster_results_last_intake_id AS 
	SELECT distinct global_id, first_value(pollster_results_intake.id) OVER (PARTITION BY pollster_results_intake.global_id ORDER BY pollster_results_intake."timestamp" DESC)  AS intake_id
   FROM pollster_results_intake;

-- Get the last intake profile
CREATE VIEW pollster_results_last_location AS
    SELECT "Q3", timestamp, "user", l.global_id from
	 pollster_results_last_intake_id l left join pollster_results_intake i  on i.id=l.intake_id;
	
CREATE VIEW pollster_results_last_intake AS
    SELECT i.* from
	 pollster_results_last_intake_id l left join pollster_results_intake i on i.id=l.intake_id;
	 
DROP VIEW IF EXISTS pollster_dashboard_weekly_count;
CREATE VIEW pollster_dashboard_weekly_count as
SELECT DISTINCT a.global_id, a."user", 
   count(*) OVER (PARTITION BY a.global_id) as count_week
   FROM ( SELECT DISTINCT w.global_id, w."user", to_char(w."timestamp", 'YYYYWW'::text) AS to_char 
           FROM pollster_results_weekly w ) a;

DROP VIEW IF EXISTS pollster_dashboard_badges2;
CREATE VIEW pollster_dashboard_badges2 as
 SELECT  global_id, "user",
  "count_week" >= 1 AS is_novice, 
  "count_week" >= 3 AS is_junior, 
  "count_week" >= 6 AS is_senior, 
  "count_week" >= 10 AS is_gold, 
  "count_week" >= 20 AS is_platinum 
  from pollster_dashboard_weekly_count;


-- neighborhood_users
CREATE OR REPLACE FUNCTION pollster_dashboard_neighborhood_users(
        text -- $1 zip_code_key
) RETURNS TABLE (
  user_id       integer,
  global_id     text,
  zip_code_key  text,
  "timestamp"     timestamptz
)
AS  $$
SELECT I."user" as user_id, 
               global_id, 
               zip_code_key, 
               I.timestamp 
        FROM (SELECT country, zip_code_key 
                FROM pollster_zip_codes 
               WHERE ST_Touches(geometry, (SELECT geometry FROM pollster_zip_codes WHERE zip_code_key = $1))
              ) A 
	INNER JOIN pollster_results_last_intake I ON (A.zip_code_key = I."Q3");

$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION pollster_dashboard_neighborhood_users_count(
        text -- $1 zip_code_key
) RETURNS integer
AS  $$
        SELECT count(DISTINCT global_id)::integer 
          FROM pollster_dashboard_neighborhood_users($1);	
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION pollster_dashboard_neighborhood_users_avg(
        text -- $1 zip_code_key
) RETURNS decimal
AS  $$
        SELECT  avg(n) FROM (
                SELECT count(DISTINCT global_id) n, zip_code_key 
                FROM pollster_dashboard_neighborhood_users($1) 
            GROUP BY 2) A;	
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION pollster_dashboard_users_by_zip_code(
        text -- $1 zip_code_key
) RETURNS TABLE (
  "user"       integer,
  global_id     text,
  zip_code_key  text,
  "timestamp"     timestamptz
)
AS  $$
        SELECT I."user", 
               I.global_id, 
               I."Q3" AS zip_code_key,
               I.timestamp 
        FROM pollster_results_intake I 
       WHERE (I."Q3" = $1);
	
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION pollster_dashboard_users_by_zip_code_count(
        text -- $1 zip_code_key
) RETURNS integer
AS  $$
        SELECT count(DISTINCT global_id)::integer 
          FROM pollster_dashboard_users_by_zip_code($1);	
$$ LANGUAGE SQL;

DROP VIEW IF EXISTS pollster_dashboard_neighborhood;
CREATE VIEW pollster_dashboard_neighborhood AS
        SELECT DISTINCT O.global_id, O."user",
	        pollster_dashboard_users_by_zip_code_count(O."Q3") AS same_zip_count,
		pollster_dashboard_neighborhood_users_count(O."Q3") AS neighbors_count, 
		pollster_dashboard_neighborhood_users_avg(O."Q3") AS neighbors_avg
           FROM pollster_results_last_intake O;
           
CREATE VIEW pollster_dashboard_neighborhood_ili AS
SELECT zip_code_key,
       count(ili) AS ili,
       count(active) AS active,
       round(CAST(count(ili)::float/count(active)::float*100 AS numeric), 2) as percent
  FROM (
SELECT 
  P.zip_code_key AS zip_code_key,
       NULLIF(S.status = 'ILI', false) AS ili
  FROM pollster_health_status AS S,
       pollster_results_intake AS I,
       pollster_zip_codes AS P,
      (SELECT DISTINCT ON (global_id) *
         FROM pollster_results_weekly
        WHERE timestamp BETWEEN 'tomorrow'::date-21 AND 'tomorrow'
        ORDER BY global_id, timestamp DESC) AS W
     WHERE S.pollster_results_weekly_id = W.id
       AND W.global_id = I.global_id
       AND I."Q3" = P.zip_code_key
       ) AS active
  GROUP BY zip_code_key;		              


SELECT zip_code_key,
       CASE true
  	 WHEN percent  > 10 THEN '#FF0000'
 	 WHEN percent > 7 THEN '#FF3B00'
 	 WHEN percent > 5 THEN '#FF6E00'
 	 WHEN percent > 4 THEN '#FF9800'
 	 WHEN percent > 1 THEN '#FFEB00'
 	 WHEN percent > 0.5 THEN '#B2E800'
 	 WHEN percent <= 0.5 THEN '#007F00'
 	 ELSE '#EEEEEE' END as color,       
       ili AS "Cas de syndromes grippaux",
       active AS "Participants",
       percent as "%%"
  FROM pollster_dashboard_neighborhood_ili;
