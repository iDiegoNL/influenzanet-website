CREATE TABLE pop_update_log
(
  year integer, -- Target year
  source_year integer, -- Year of the population of the source of the data
  comment text,
  date timestamp with time zone
)
WITH (
  OIDS=FALSE
);
ALTER TABLE pop_update_log
  OWNER TO epiwork;
COMMENT ON COLUMN pop_update_log.year IS 'Target year';
COMMENT ON COLUMN pop_update_log.source_year IS 'Year of the population of the source of the data';

GRANT ALL ON TABLE pop_update_log TO "DBA";
GRANT SELECT, REFERENCES, TRIGGER ON TABLE pop_update_log TO "Statistician";

CREATE TABLE pop_com
(
  year integer NOT NULL,
  code_com character(5) NOT NULL,
  population integer,
  CONSTRAINT pk_pop_com PRIMARY KEY (year , code_com )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE pop_com
  OWNER TO epiwork;

GRANT ALL ON TABLE pop_com TO "DBA";
GRANT SELECT, REFERENCES, TRIGGER ON TABLE pop_com TO "Statistician";
  
  
CREATE TABLE pop_reg
(
  year integer NOT NULL,
  code_reg character(2) NOT NULL,
  population integer,
  CONSTRAINT pk_pop_reg PRIMARY KEY (year , code_reg )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE pop_reg
  OWNER TO epiwork;
  
GRANT ALL ON TABLE pop_reg TO "DBA";
GRANT SELECT, REFERENCES, TRIGGER ON TABLE pop_reg TO "Statistician";
  
  
  
CREATE TABLE pop_dep
(
  year integer NOT NULL,
  code_dep character(3) NOT NULL,
  population integer,
  CONSTRAINT pk_pop_dep PRIMARY KEY (year , code_dep )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE pop_dep
  OWNER TO epiwork;

GRANT ALL ON TABLE pop_dep TO "DBA";
GRANT SELECT, REFERENCES, TRIGGER ON TABLE pop_dep TO "Statistician";

  
ALTER TABLE geo_levels ALTER COLUMN code_dep TYPE character(3);
-- ALTER TABLE geo_dep_codes ALTER COLUMN zip_code_key TYPE character(3);
