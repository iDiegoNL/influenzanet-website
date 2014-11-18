SELECT zip_code_key,
       CASE true
  	 WHEN percent  > 10 THEN '#FF0000'
 	 WHEN percent > 7 THEN '#FF3B00'
 	 WHEN percent > 5 THEN '#FF6E00'
 	 WHEN percent > 4 THEN '#FF9800'
 	 WHEN percent > 1 THEN '#FFEB00'
 	 WHEN percent > 0.5 THEN '#B2E800'
 	 WHEN percent <= 0.5 THEN '#007F00'
 	 ELSE '#EEEEEE' END as color,       
       ili AS "Cas de syndromes grippaux",
       active AS "Participants",
       percent as "%%"
  FROM pollster_dashboard_neighborhood_ili;
