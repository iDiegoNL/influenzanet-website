DROP TABLE lk_intake_Q1;
create table lk_intake_Q1 (
    value      integer,
    label      text,
    PRIMARY KEY (value)
);

INSERT INTO lk_intake_q1 (value, label) VALUES (1, 'Donne');
INSERT INTO lk_intake_q1 (value, label) VALUES (0, 'Uomini');


SELECT  G.label, count(*) 
  FROM  lk_intake_q1 G, pollster_results_intake I 
 WHERE I."Q1" = G.value
 GROUP BY 1;
