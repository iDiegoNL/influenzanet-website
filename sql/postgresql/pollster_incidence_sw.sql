CREATE TABLE incidence_com AS
SELECT
  sum(ili::int) count_ili,
  sum(cold) count_cold,
  sum(gastro) count_gastro,
  sum(nosympt) count_nosympt,
  count(*) as active,
  date_trunc('week',date_onset) yw,
  code_com
FROM
(	SELECT 
		-- date_trunc('day',W.timestamp) date_intake, 
		S.status, 
		CASE S.status WHEN 'ILI' THEN 1 ELSE 0 END as ili,
		CASE S.status WHEN 'COMMON-COLD' THEN 1 ELSE 0 END as cold,
		CASE S.status WHEN 'GASTROINTESTINAL' THEN 1 ELSE 0 END as gastro,
		CASE S.status WHEN 'NO-SYMPTOMS' THEN 1 ELSE 0 END as nosympt,
		
		COALESCE( to_date(W."Q3_0_open",'YYYY-MM-DD'), date_trunc('day', W.timestamp)) date_onset ,
		I."Q3" as code_com
	FROM 
		pollster_results_weekly W 
		left join 
			pollster_health_status S on W.id=S.pollster_results_weekly_id
		left join
			-- get the last intake available for each user
			(SELECT DISTINCT ON (global_id) "global_id","Q3"
			  FROM pollster_results_intake
			  ORDER BY global_id, timestamp DESC
			) I on W.global_id=I.global_id
	where W."timestamp" >= current_date - INTERVAL '21 day'
) H
where date_onset >= current_date - INTERVAL '21 day'
group by yw, code_com
order by yw, code_com;

alter table incidence_com owner to epiwork;

SELECT
  sum(count_ili) as ili,
  sum(count_cold) as cold,
  sum(count_gastro) as gastro,
  sum(count_nosympt) as nosympt,
  sum(active) as active,
  yw,
  code_reg
FROM incidence_com i left join geo_levels g on i.code_com=g.code_com
group by yw, code_reg
order by yw,code_reg;
