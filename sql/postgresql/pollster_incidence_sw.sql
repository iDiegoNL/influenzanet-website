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


--- Carte v1
-- Actif = Nombre de questionnaire sur une semaine
SELECT 
	zip_code_key,
	-- 0x007F00, 0x19BA00, 0xB2E800, 0xFFEB00, 0xFFBF00, 0xFF9800, 0xFF6E00, 0xFF3B00, 0xFF0000
        CASE true
 	 WHEN prop  > 0.50 THEN '#FF0000'
 	 WHEN prop > 0.40 THEN '#FF3B00'
 	 WHEN prop > 0.30 THEN '#FF6E00'
 	 WHEN prop > 0.20 THEN '#FF9800'
 	 WHEN prop > 0.15 THEN '#FFEB00'
 	 WHEN prop > 0.10 THEN '#B2E800'
 	 WHEN prop > 0.05 THEN '#19BA00'
 	 ELSE '#007F00' END AS color,
	count_ili as "présentent un syndromes grippaux (ECDC)",
	count_notili as "ne présentent pas de syndrome grippal",
	total as  "Nombre de questionnaire",
	prop as "Proportion de syndromes grippaux (ECDC)"
from (
SELECT zip_code_key,
       count(ili) AS count_ili,
       count(not_ili) AS count_notili,
       sum(total) as total,
       round( round(count(ili),3) / round(sum(total),3),2) as prop
  FROM (
	SELECT 
		g.code_reg AS zip_code_key,
		NULLIF(S.status = 'ILI', false) AS ili,
		NULLIF(S.status != 'ILI', false) AS not_ili,
		1 as total
	FROM 
		pollster_health_status AS S,
		pollster_results_intake AS I,
		geo_levels as g,
		-- get the last weekly submitted for each user and
		-- ensure that is not older than 7 days
		(SELECT DISTINCT ON (global_id) *
			FROM pollster_results_weekly
			WHERE timestamp BETWEEN 'today'::date-7 AND 'today'
			ORDER BY global_id, timestamp DESC
		) AS W
	WHERE 
		S.pollster_results_weekly_id = W.id AND W.global_id = I.global_id AND
		g.code_com=I."Q3"
  ) AS statuses
GROUP BY zip_code_key
) as wok

--- Carte v2
-- Participant = Participant ayant un questionnaire sur 3 semaines
--  ILI = nombre de nouveau cas (cas incident),   
SELECT 
	zip_code_key,
	-- 0x007F00, 0x19BA00, 0xB2E800, 0xFFEB00, 0xFFBF00, 0xFF9800, 0xFF6E00, 0xFF3B00, 0xFF0000
        CASE true
 	 WHEN prop  > 0.50 THEN '#FF0000'
 	 WHEN prop > 0.40 THEN '#FF3B00'
 	 WHEN prop > 0.30 THEN '#FF6E00'
 	 WHEN prop > 0.20 THEN '#FF9800'
 	 WHEN prop > 0.15 THEN '#FFEB00'
 	 WHEN prop > 0.10 THEN '#B2E800'
 	 WHEN prop > 0.05 THEN '#19BA00'
 	 ELSE '#007F00' END AS color,
	count_ili as "présentent un syndromes grippaux (ECDC)",
	active as  "Nombre de participants sur 3 semaines",
	round(prop,2) as "Proportion de syndromes grippaux (ECDC)"
from (	
	select 
		code_reg as zip_code_key, 
		sum(count_ili) as count_ili, 
		sum(active) as active, 
		sum(count_ili) / sum(active) as prop
	from 
		incidence_com i 
			left join geo_levels g on g.code_com=i.code_com 
	where yw=isoyearweek( date(current_date - interval '6 day')) and i.code_com != '' and i.code_com is not null
	group by code_reg
) t


CREATE OR REPLACE FUNCTION isoyearweek(int) returns int
as $body$
   return extract(isoyear from $1) * 100 + extract(week from $1);
$body$
LANGUAGE 'sql';