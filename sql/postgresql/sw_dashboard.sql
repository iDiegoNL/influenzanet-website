DROP VIEW IF EXISTS pollster_dashboard_badges;

-- datasource for particpation badge
CREATE OR REPLACE VIEW pollster_dashboard_badges AS 
 SELECT DISTINCT a.global_id, a."user", 
  count(*) OVER (PARTITION BY a.global_id) >= 1 AS is_novice, 
  count(*) OVER (PARTITION BY a.global_id) >= 3 AS is_junior, 
  count(*) OVER (PARTITION BY a.global_id) >= 6 AS is_senior, 
  count(*) OVER (PARTITION BY a.global_id) >= 10 AS is_gold, 
  count(*) OVER (PARTITION BY a.global_id) >= 20 AS is_platinum, 
  sum(a.cold) OVER (PARTITION BY a.global_id) >= 3 AS is_cold_season, 
  sum(a.ili) OVER (PARTITION BY a.global_id) >= 2 AS is_ili_season, 
  sum(a.gastro) OVER (PARTITION BY a.global_id) >= 2 AS is_gastro_season
   FROM ( 
   SELECT DISTINCT 
   w.global_id, 
   w."user", 
   to_char(w."timestamp", 'YYYYWW'::text) AS to_char, 
	CASE true
		WHEN hs.status ~~* '%COLD%'::text THEN 1
		ELSE 0
	END AS cold, 
	CASE true
		WHEN hs.status = 'ILI'::text THEN 1
		ELSE 0
	END AS ili, 
	CASE true
		WHEN hs.status ~~* '%GASTRO%'::text THEN 1
		ELSE 0
	END AS gastro
           FROM pollster_health_status hs
      LEFT JOIN pollster_results_weekly w ON hs.pollster_results_weekly_id = w.id) a;


