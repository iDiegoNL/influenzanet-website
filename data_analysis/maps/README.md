Aggregated Maps Feature
========================

Design
---------
A table is associated with each geographic level with the following structure:

 id => PK column
 country => (if necessary)
 zip_code_key => id of the area for a given geographic level
 geometry => geometry data

Example Base level Postal zip code or municipality code
 	CREATE TABLE pollster_zip_codes
 	(
   	  id serial NOT NULL,
   	  country text,
      zip_code_key text,
	  geometry geometry,
	  title character varying(50),
    )


A table named geo_levels associate codes for every geographic levels
	CREATE TABLE geo_levels
	(
	  gid serial not null,
	  code_com character(5),
	  code_dep character varying(3),
	  code_reg character(2),
	  CONSTRAINT gis_levels_pkey PRIMARY KEY (gid )
	)

code_com = "Commune" level (municipality), code_dep="Departement" NUTS 3 level, code_reg="Region" NUTS 2 level

Config
----------
List of available geographic tables are defined in the
GEOMETRY_TABLES in settings.py 

	GEOMETRY_TABLES = (
	([table name], [level label]), and can be overridden in local_settings.py
	)

Example for France levels:
	GEOMETRY_TABLES = (
	 ('pollster_zip_codes','zip level'),
	 ('geo_dep_codes','Departement'),
	 ('geo_reg_codes',u'Région')
	)

Create an aggregated Map
-----------------
For each chart you can select the geometry table to use.
The SQL query, must return level codes in a  "zip_code_key" column

For an aggregated map at the "dep" (NUTS 3) level using the geo_levels table
	SELECT 
	  g.code_dep as zip_code_key, 
	  '#0000FF'::text as color,
	  count(distinct global_id) as "Nombre de participants"
	FROM 
	  public.pollster_results_intake i
	  left join 
	  public.geo_levels g
	  on g.code_com=i."Q3"
	GROUP BY g.code_dep



