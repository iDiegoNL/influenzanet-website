#!/bin/sh

dbname="influweb_it"
username="influweb_it"
psql $dbname $username << EOF

SELECT distinct B.global_id,
       I."Q0" as household,
       I."Q1" as gender,
       I."Q2" as birthdate,
       I."Q3" as CAP,
       I."Q4" as main_activity,
       I."Q4c" as profession,
       I."Q4d_0" as no_formal_qualifications,
       I."Q4d_1" as diploma_scuola_media,
       I."Q4d_2" as diploma_scuola_superiore,
       I."Q4d_3" as laurea_triennale,
       I."Q4d_4" as laurea_magistrale_o_superiore,
       I."Q4d_5" as ancora_in_formazione,
       I."Q6_0" as zero_four,
       I."Q6_0_open" as num_zero_four,
       I."Q6_1" as five_eighteen,
       I."Q6_1_open" as num_five_eighteen,
       I."Q6_2" as nineteen_fourtyfour,
       I."Q6_2_open" as num_nineteen_fourtyfour,
       I."Q6_3" as fourtyfive_sixtyfour,
       I."Q6_3_open" as num_fourtyfive_sixtyfour,
       I."Q6_4" as sixtyfive_plus,
       I."Q6_4_open" as num_sixtyfive_plus,
       I."Q6b" as kids_daycare,
       I."Q7" as transportation,
       I."Q8" as num_sickness,
       I."Q13" as smoke,
       I."Q17_0" as radio_tv,
       I."Q17_1" as journals,
       I."Q17_2" as internet,
       I."Q17_3" as poster,
       I."Q17_4" as friends_family,
       I."Q17_5" as school_work,
       0

FROM pollster_results_intake I,
     stats_pollster_enrolled_users() B
WHERE B.global_id = I.global_id
AND B.global_id not in (select A.global_id from  stats_pollster_participants() A);

EOF
