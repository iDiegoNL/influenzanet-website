INSERT INTO gis_region (code_reg, geometry, nom_region, id_reg, code_iso) VALUES
('01',NULL,'GUADELOUPE',0,'GP'),
('02',NULL,'MARTINIQUE',0,'MQ'),
('03',NULL,'GUYANE',0,'GF'),
('04',NULL,'REUNION',0,'RE');

INSERT INTO gis_departement   (
  id_geofla,
  code_dept,
  nom_dept,
  code_chf,
  nom_chf,
  x_chf_lieu,
  y_chf_lieu,
  x_centroid,
  y_centroid,
  code_reg,
  nom_region,
  geometry) VALUES
  
  (0,'971','Guadeloupe','105','Basse Terre',0,0,0,0,'01','GUADELOUPE',NULL),
  (0,'972','Martinique','209','FORT-DE-FRANCE',0,0,0,0,'02','MARTINIQUE',NULL),
  (0,'973','Guyane','302','CAYENNE',0,0,0,0,'03','GUYANE',NULL),
  (0,'974','La Réunion','411','SAINT-DENIS',0,0,0,0,'04','LA REUNION',NULL),
  (0,'976','Mayotte','608','DZAOUDZI',0,0,0,0,'06','MAYOTTE',NULL);
  
  

