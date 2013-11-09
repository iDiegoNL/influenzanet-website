SELECT DISTINCT 
 global_id,
 "user",
 count(*) OVER (PARTITION BY global_id) >= 1 AS is_novice,
 count(*) OVER (PARTITION BY global_id) >= 3 AS is_junior,
 count(*) OVER (PARTITION BY global_id) >= 6 AS is_senior,
 count(*) OVER (PARTITION BY global_id) >= 10 AS is_gold,
 count(*) OVER (PARTITION BY global_id) >= 20 AS is_platinum,
 sum(cold) OVER (PARTITION BY global_id) >= 3 AS is_cold_season,
 sum(ili) OVER (PARTITION BY global_id)  >= 2 AS is_ili_season,
 sum(gastro) OVER (PARTITION BY global_id) >= 2 AS is_gastro_season
FROM (
	SELECT DISTINCT global_id,
	   "user" ,			 
	   to_char(timestamp, 'YYYYWW'),
	   CASE true WHEN (status ILIKE '%COLD%') THEN 1 ELSE 0 END as cold,
	   CASE true WHEN (status = 'ILI') THEN 1 ELSE 0 END as ili,
	   CASE true WHEN (status ILIKE '%GASTRO%') THEN 1 ELSE 0 END as gastro
	FROM pollster_health_status HS left join pollster_results_weekly w on HS.pollster_results_weekly_id=w.id 
) A;