CREATE TABLE gis_commune
(
  gid integer NOT NULL DEFAULT nextval('commune_project_gid_seq'::regclass),
  id_geofla numeric(10,0),
  code_comm character varying(3),
  insee_com character varying(5),
  nom_comm character varying(50),
  statut character varying(20),
  x_chf_lieu integer,
  y_chf_lieu integer,
  x_centroid integer,
  y_centroid integer,
  z_moyen smallint,
  superficie numeric(10,0),
  population double precision,
  code_cant character varying(2),
  code_arr character varying(1),
  code_dept character varying(2),
  nom_dept character varying(30),
  code_reg character varying(2),
  nom_region character varying(30),
  CONSTRAINT commune_project_pkey PRIMARY KEY (gid )
)
WITH (
  OIDS=FALSE
);

SELECT AddGeometryColumn('','gis_commune','geometry','4326','MULTIPOLYGON',2);

ALTER TABLE gis_commune
  OWNER TO epiwork;
GRANT ALL ON TABLE gis_commune TO epiwork;
GRANT SELECT ON TABLE gis_commune TO "Statistician";
GRANT ALL ON TABLE gis_commune TO "DBA";

CREATE TABLE gis_region
(
  gid serial NOT NULL,
  nom_region character varying(64),
  code_rs integer, -- Sentinelles internal code
  geometry geometry,
  code_reg character(2), -- INSEE code
  code_iso character(2), -- ISO 3166-2 code
  CONSTRAINT gis_region_pkey PRIMARY KEY (gid )
)
WITH (
  OIDS=FALSE
);

ALTER TABLE gis_region
  OWNER TO epiwork;
GRANT ALL ON TABLE gis_region TO epiwork;
GRANT SELECT ON TABLE gis_region TO "DBA";

SELECT AddGeometryColumn('','gis_region','geometry','4326','MULTIPOLYGON',2);

CREATE TABLE gis_departement
(
  gid serial NOT NULL,
  id_geofla numeric(10,0),
  code_dept character varying(2),
  nom_dept character varying(30),
  code_chf character varying(3),
  nom_chf character varying(50),
  x_chf_lieu integer,
  y_chf_lieu integer,
  x_centroid integer,
  y_centroid integer,
  code_reg character varying(2),
  nom_region character varying(30),
  geometry geometry,
  CONSTRAINT gis_departement_pkey PRIMARY KEY (gid )
)
WITH (
  OIDS=FALSE
);

ALTER TABLE gis_departement
  OWNER TO epiwork;
GRANT ALL ON TABLE gis_departement TO epiwork;
GRANT SELECT ON TABLE gis_departement TO "DBA";

SELECT AddGeometryColumn('','gis_departement','geometry','4326','MULTIPOLYGON',2);
