COPY (SELECT * FROM crosstab($$SELECT "CAP", "Giorno", "Attivi" FROM stats_pollster_cap_active('2011-09-01','today') ORDER BY 1, 2$$, $$SELECT DISTINCT "Giorno" FROM stats_pollster_cap_active('2011-09-01','today') ORDER BY 1$$) AS ("CAP" text,
"2011-11-11" integer, "2011-11-12" integer, "2011-11-13" integer, "2011-11-14" integer, "2011-11-15" integer, "2011-11-16" integer, "2011-11-17" integer, "2011-11-18" integer, "2011-11-19" integer, "2011-11-20" integer, "2011-11-21" integer, "2011-11-22" integer, "2011-11-23" integer, "2011-11-24" integer, "2011-11-25" integer, "2011-11-26" integer, "2011-11-27" integer, "2011-11-28" integer, "2011-11-29" integer, "2011-11-30" integer, "2011-12-01" integer, "2011-12-02" integer, "2011-12-03" integer, "2011-12-04" integer, "2011-12-05" integer, "2011-12-06" integer, "2011-12-07" integer, "2011-12-08" integer, "2011-12-09" integer, "2011-12-10" integer, "2011-12-11" integer, "2011-12-12" integer, "2011-12-13" integer, "2011-12-14" integer, "2011-12-15" integer, "2011-12-16" integer, "2011-12-17" integer, "2011-12-18" integer, "2011-12-19" integer, "2011-12-20" integer, "2011-12-21" integer, "2011-12-22" integer, "2011-12-23" integer, "2011-12-24" integer, "2011-12-25" integer, "2011-12-26" integer, "2011-12-27" integer, "2011-12-28" integer, "2011-12-29" integer, "2011-12-30" integer, "2011-12-31" integer, "2012-01-01" integer, "2012-01-02" integer, "2012-01-03" integer, "2012-01-04" integer, "2012-01-05" integer, "2012-01-06" integer, "2012-01-07" integer, "2012-01-08" integer, "2012-01-09" integer, "2012-01-10" integer, "2012-01-11" integer, "2012-01-12" integer, "2012-01-13" integer, "2012-01-14" integer, "2012-01-15" integer, "2012-01-16" integer, "2012-01-17" integer, "2012-01-18" integer, "2012-01-19" integer, "2012-01-20" integer, "2012-01-21" integer, "2012-01-22" integer, "2012-01-23" integer, "2012-01-24" integer, "2012-01-25" integer, "2012-01-26" integer, "2012-01-27" integer, "2012-01-28" integer, "2012-01-29" integer, "2012-01-30" integer, "2012-01-31" integer, "2012-02-01" integer, "2012-02-02" integer, "2012-02-03" integer, "2012-02-04" integer, "2012-02-05" integer, "2012-02-06" integer, "2012-02-07" integer, "2012-02-08" integer, "2012-02-09" integer, "2012-02-10" integer, "2012-02-11" integer, "2012-02-12" integer, "2012-02-13" integer, "2012-02-14" integer, "2012-02-15" integer, "2012-02-16" integer, "2012-02-17" integer, "2012-02-18" integer, "2012-02-19" integer, "2012-02-20" integer, "2012-02-21" integer, "2012-02-22" integer, "2012-02-23" integer, "2012-02-24" integer, "2012-02-25" integer, "2012-02-26" integer, "2012-02-27" integer, "2012-02-28" integer, "2012-02-29" integer, "2012-03-01" integer, "2012-03-02" integer, "2012-03-03" integer, "2012-03-04" integer, "2012-03-05" integer, "2012-03-06" integer, "2012-03-07" integer, "2012-03-08" integer, "2012-03-09" integer, "2012-03-10" integer, "2012-03-11" integer, "2012-03-12" integer
)) TO STDOUT WITH CSV HEADER;
