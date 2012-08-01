
CREATE TABLE geo_reg_codes
(
  id integer NOT NULL DEFAULT nextval('geo_region_codes_id_seq'::regclass),
  country text,
  zip_code_key character(2),
  CONSTRAINT geo_region_codes_pkey PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);

ALTER TABLE geo_reg_codes
  OWNER TO epiwork;

SELECT AddGeometryColumn('','geo_reg_codes','geometry','4326','MULTIPOLYGON',2);

INSERT INTO geo_reg_codes (country, zip_code_key, geometry) select 'fr',code_reg, geometry from gis_region;

CREATE TABLE geo_dep_codes
(
  id serial,
  country text,
  zip_code_key character varying(3),
  CONSTRAINT geo_dep_codes_pkey PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);

ALTER TABLE geo_dep_codes
  OWNER TO epiwork;

SELECT AddGeometryColumn('','geo_dep_codes','geometry','4326','MULTIPOLYGON',2);

INSERT INTO geo_dep_codes (country, zip_code_key, geometry) select 'fr',code_dept, geometry from gis_departement;


-- Gis levels

-- Mise a jour de la table gis_levels

TRUNCATE geo_levels;

INSERT INTO geo_levels (code_com, code_dep, code_reg)
SELECT
  gis_commune.insee_com,
  gis_commune.code_dept,
  gis_commune.code_reg
FROM
  public.gis_commune;
  
  
