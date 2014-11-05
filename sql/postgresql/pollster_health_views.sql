CREATE OR REPLACE VIEW pollster_health_status AS 
 SELECT pollster_results_weekly.id AS pollster_results_weekly_id, 
        CASE true
            WHEN pollster_results_weekly."Q1_0" THEN 'NO-SYMPTOMS'::text
            WHEN (pollster_results_weekly."Q5" = 0 OR pollster_results_weekly."Q6b" = 0) AND (pollster_results_weekly."Q1_1" OR pollster_results_weekly."Q1_2" OR pollster_results_weekly."Q6d" = 3 OR pollster_results_weekly."Q6d" = 4 OR pollster_results_weekly."Q6d" = 5 OR pollster_results_weekly."Q1_11" OR pollster_results_weekly."Q1_8" OR pollster_results_weekly."Q1_9") AND (pollster_results_weekly."Q1_5" OR pollster_results_weekly."Q1_6" OR pollster_results_weekly."Q1_7") THEN 'ILI'::text
            WHEN NOT pollster_results_weekly."Q1_1" AND NOT pollster_results_weekly."Q1_2" AND (pollster_results_weekly."Q6d" = 0 OR pollster_results_weekly."Q6d" IS NULL) AND (pollster_results_weekly."Q1_3" OR pollster_results_weekly."Q1_4" OR pollster_results_weekly."Q1_14") AND pollster_results_weekly."Q11" = 2 AND (
            CASE true
                WHEN pollster_results_weekly."Q1_17" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_15" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_16" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_18" THEN 1
                ELSE 0
            END) >= 2 THEN 'ALLERGY-or-HAY-FEVER-and-GASTROINTESTINAL'::text
            WHEN NOT pollster_results_weekly."Q1_1" AND NOT pollster_results_weekly."Q1_2" AND (pollster_results_weekly."Q6d" = 0 OR pollster_results_weekly."Q6d" IS NULL) AND (pollster_results_weekly."Q1_3" OR pollster_results_weekly."Q1_4" OR pollster_results_weekly."Q1_14") AND pollster_results_weekly."Q11" = 2 THEN 'ALLERGY-or-HAY-FEVER'::text
            WHEN (
            CASE true
                WHEN pollster_results_weekly."Q1_3" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_4" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_6" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_5" THEN 1
                ELSE 0
            END) >= 2 AND (
            CASE true
                WHEN pollster_results_weekly."Q1_17" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_15" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_16" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_18" THEN 1
                ELSE 0
            END) >= 2 THEN 'COMMON-COLD-and-GASTROINTESTINAL'::text
            WHEN (
            CASE true
                WHEN pollster_results_weekly."Q1_3" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_4" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_6" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_5" THEN 1
                ELSE 0
            END) >= 2 THEN 'COMMON-COLD'::text
            WHEN (
            CASE true
                WHEN pollster_results_weekly."Q1_17" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_15" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_16" THEN 1
                ELSE 0
            END + 
            CASE true
                WHEN pollster_results_weekly."Q1_18" THEN 1
                ELSE 0
            END) >= 2 THEN 'GASTROINTESTINAL'::text
            ELSE 'NON-SPECIFIC-SYMPTOMS'::text
        END AS status
   FROM pollster_results_weekly;

ALTER TABLE pollster_health_status
  OWNER TO epiwork;
GRANT ALL ON TABLE pollster_health_status TO postgres;
GRANT ALL ON TABLE pollster_health_status TO epiwork;
GRANT ALL ON TABLE pollster_health_status TO "DBA";
GRANT REFERENCES ON TABLE pollster_health_status TO "Statistician";
GRANT SELECT ON TABLE pollster_health_status TO "Statistician" WITH GRANT OPTION;
