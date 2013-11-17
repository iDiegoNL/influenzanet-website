CREATE INDEX idx_pollster_results_intake_global_id
  ON pollster_results_intake
  USING btree
  (global_id COLLATE pg_catalog."default" );

CREATE INDEX idx_pollster_results_weekly_global_id
  ON pollster_results_intake
  USING btree
  (global_id COLLATE pg_catalog."default" );

CREATE INDEX idx_pollster_results_intake_user
  ON pollster_results_intake
  USING btree
  ("user"  );  
  
CREATE INDEX idx_pollster_results_weekly_user
  ON pollster_results_weekly
  USING btree
  ("user"  );  