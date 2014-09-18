CREATE OR REPLACE FUNCTION sum_if(boolean, integer)
  RETURNS integer
AS
$body$
SELECT CASE WHEN $1 then $2 ELSE 0 END;
$body$
LANGUAGE 'sql';


SELECT week "Settimana",
       sum(q0) "Nessun sintomo",
       sum(q1) "Febbre",
       sum(q2) "Brividi"
       FROM (
        SELECT date_trunc('week', W.timestamp) week,
               sum_if(W."Q1_0",1) q0,
               sum_if(W."Q1_1",1) q1,
               sum_if(W."Q1_2",1) q2

          FROM pollster_results_weekly W ) A
          
GROUP BY 1 ORDER BY 1;
