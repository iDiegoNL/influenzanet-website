DROP TABLE lk_intake_Q2;
create table lk_intake_Q2 (
    value_inf      integer,
    value_sup      integer,
    PRIMARY KEY (value_inf, value_sup)
);

INSERT INTO lk_intake_q2
(value_inf, value_sup)
VALUES
(0, 5);

INSERT INTO lk_intake_q2
(value_inf, value_sup)
VALUES
(6, 12);

INSERT INTO lk_intake_q2
(value_inf, value_sup)
VALUES
(13, 19);

INSERT INTO lk_intake_q2
(value_inf, value_sup)
VALUES
(20, 39);

INSERT INTO lk_intake_q2
(value_inf, value_sup)
VALUES
(40, 59);


INSERT INTO lk_intake_q2
(value_inf, value_sup)
VALUES
(60, 100);


select G.value_inf || '-' || G.value_sup label, count(*) FROM 
lk_intake_q2 G, pollster_results_intake I 
WHERE     extract ('year' from age(to_date(replace(I."Q2",'/','-'), 'YYYY-MM'))) BETWEEN G.value_inf AND G.value_sup
GROUP BY 1 order by 1;

select I.id, age(to_date(replace(I."Q2",'/','-'), 'YYYY-MM'))  from pollster_results_intake I limit 100 ;


