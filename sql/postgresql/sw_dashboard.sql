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
		   