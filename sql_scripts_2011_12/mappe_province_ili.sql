SELECT zip_code_key,
       CASE true
       WHEN (count(ili)::float/count(active)*100 >= 0 AND count(ili)::float/count(active)*100 < 0.5) THEN '#FF9933'
       WHEN (count(ili)::float/count(active)*100 >= 0.5 AND count(ili)::float/count(active)*100 <= 1) THEN '#F9933'
       WHEN (count(ili)::float/count(active)*100 > 1 AND count(ili)::float/count(active)*100 <= 4) THEN '#FF9900'
       WHEN (count(ili)::float/count(active)*100 > 4 AND count(ili)::float/count(active)*100 <= 5) THEN '#FF9900'
       WHEN (count(ili)::float/count(active)*100 > 5 AND count(ili)::float/count(active)*100 <= 7) THEN '#FF6600'
       WHEN (count(ili)::float/count(active)*100 > 7 AND count(ili)::float/count(active)*100 <= 10) THEN '#FF3300'
       --WHEN count(ili)::float/count(active)*100 > 10 THEN '#FF0000'


       ELSE '#FF0000' END AS color,
       count(ili) AS "Casi di ILI",
       count(active) AS "Utenti attivi nelle ultime tre settimane",
       round(CAST(count(ili)::float/count(active)::float*100 AS numeric), 2) as "%"



  FROM (
SELECT P.provincia AS zip_code_key,
       NULLIF(S.status = 'ILI', false) AS ili
  FROM pollster_health_status AS S,
       pollster_results_intake AS I,
       rel_cap_province AS P,

       -- get the last weekly submitted for each user and
       -- ensure that is not older than 21 days
      (SELECT DISTINCT ON (global_id) *
         FROM pollster_results_weekly
        WHERE timestamp BETWEEN 'tomorrow'::date-21 AND 'tomorrow'
        ORDER BY global_id, timestamp DESC) AS W
     WHERE S.pollster_results_weekly_id = W.id
       AND W.global_id = I.global_id
       AND I."Q3" = P.cap
       ) AS active
  GROUP BY zip_code_key
