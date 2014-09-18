SELECT P.provincia AS zip_code_key, count(distinct I.global_id) as partecipanti
  FROM pollster_results_intake AS I,
       rel_cap_province AS P
  WHERE I."Q3" = P.cap group by zip_code_key order by partecipanti DESC

