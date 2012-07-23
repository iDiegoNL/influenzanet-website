
-- reg_health graph
SELECT
    zip_code_key,
    -- 0x007F00, 0x19BA00, 0xB2E800, 0xFFEB00, 0xFFBF00, 0xFF9800, 0xFF6E00, 0xFF3B00, 0xFF0000
        CASE true
      WHEN prop  > 0.10 THEN '#FF0000'
      WHEN prop > 0.07 THEN '#FF3B00'
      WHEN prop > 0.05 THEN '#FF6E00'
      WHEN prop > 0.04 THEN '#FF9800'
      WHEN prop > 0.03 THEN '#FFEB00'
      WHEN prop > 0.02 THEN '#B2E800'
      WHEN prop > 0.01 THEN '#19BA00'
      ELSE '#007F00' END AS color,
    count_ili as "Participants présentant un syndrome grippal",
    active as  "Participants actifs sur 3 semaines",
    round(100*prop,2) as "Pourcentage de syndromes grippaux"
from (   
    select
        code_reg as zip_code_key,
        sum(count_ili) as count_ili,
        sum(active) as active,
        sum(count_ili) / sum(active) as prop
    from
        incidence_com i
            left join geo_levels g on g.code_com=i.code_com
    where yw=(select max(yw) from incidence_yw) and i.code_com != '' and i.code_com is not null and code_reg !=''
    group by code_reg
) t


