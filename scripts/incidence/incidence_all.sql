SELECT CASE WHEN a<20 THEN '<20'
            WHEN a>=20 AND a<45 THEN '20..44'
            WHEN a>=45 THEN '45++'
            END AS agegroup,
       count(ili) AS "ILI",
       count(non_ili) AS "No ILI",
       CASE WHEN (count(ili) + count(non_ili) > 0) THEN
         cast(cast(count(ili) AS numeric)/(count(ili)+count(non_ili))
              AS numeric(3,2))
       ELSE 0
       END AS "Incidence",
       CASE WHEN (count(ili) > 0) THEN
         cast(cast(count(visited) AS numeric)/(count(ili)) 
           AS numeric(3,2))
       ELSE 0
       END AS "Health service visited",
       CASE WHEN (count(ili) > 0) THEN
         cast(cast(count(consulted) AS numeric)/(count(ili)) 
           AS numeric(3,2)) 
       ELSE 0
       END AS "Health service consulted",
       CASE WHEN (count(ili) > 0) THEN
         cast(cast(count(consultedorvisited) AS numeric)/count(ili)
           AS numeric(3,2)) 
       ELSE 0
       END AS "Health service all"
  FROM (
SELECT extract(year from age(to_timestamp(I."Q2",'YYYY-MM'))) AS a,
       NULLIF(S.status = 'ILI' AND (W."Q2" IS NULL OR W."Q2" != 0),
            false) AS ili,     
       NULLIF(NOT (S.status = 'ILI') OR NOT (W."Q2" IS NULL OR W."Q2"
            != 0), false) AS non_ili, 
       NULLIF((S.status = 'ILI' AND (W."Q2" IS NULL OR W."Q2" != 0)
            AND (W."Q7_1" OR W."Q7_2" OR W."Q7_3" OR W."Q7_4" OR
            W."Q7_5")), false) AS visited,
       NULLIF((S.status = 'ILI' AND (W."Q2" IS NULL OR W."Q2" != 0)
            AND (W."Q8_1" OR W."Q8_2" OR W."Q8_3" OR W."Q8_4" OR
            W."Q8_5")), false) AS consulted,
       NULLIF((S.status = 'ILI'  AND (W."Q2" IS NULL OR W."Q2" != 0)
            AND (W."Q8_1" OR W."Q8_2" OR W."Q8_3" OR W."Q8_4" OR
            W."Q8_5" OR W."Q7_1" OR W."Q7_2" OR W."Q7_3" OR W."Q7_4"
            OR W."Q7_5")), false) AS consultedorvisited
  FROM (SELECT DISTINCT ON (global_id) *
        FROM pollster_results_intake
        ORDER BY global_id, timestamp DESC) AS I,
       pollster_health_status AS S,
       (SELECT DISTINCT ON (global_id) *,  
        NULLIF(S.status = 'ILI' AND (W."Q2" IS NULL OR W."Q2" != 0),
            false) AS ili
        FROM pollster_results_weekly as W, pollster_health_status as S
        WHERE timestamp BETWEEN 'today'::date-8 AND 'today'::date-1
        AND S.pollster_results_weekly_id = W.id
        ORDER BY global_id, ili) AS W
 WHERE S.pollster_results_weekly_id = W.id
   AND W.global_id = I.global_id AND extract(year from age(to_timestamp(I."Q2",'YYYY-MM'))) >= 0
       ) AS statuses
 GROUP BY agegroup ORDER BY agegroup;
