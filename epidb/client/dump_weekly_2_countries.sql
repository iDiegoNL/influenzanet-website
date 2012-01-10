DROP TABLE IF EXISTS epidb_results_weekly;

CREATE TABLE epidb_results_weekly (
    country character(2),
    global_id character varying(36),
    "timestamp" timestamp with time zone,
    "Q1_0" boolean NOT NULL,
    "Q1_1" boolean NOT NULL,
    "Q1_2" boolean NOT NULL,
    "Q1_3" boolean NOT NULL,
    "Q1_4" boolean NOT NULL,
    "Q1_5" boolean NOT NULL,
    "Q1_6" boolean NOT NULL,
    "Q1_7" boolean NOT NULL,
    "Q1_8" boolean NOT NULL,
    "Q1_9" boolean NOT NULL,
    "Q1_10" boolean NOT NULL,
    "Q1_11" boolean NOT NULL,
    "Q1_12" boolean NOT NULL,
    "Q1_13" boolean NOT NULL,
    "Q1_14" boolean NOT NULL,
    "Q1_15" boolean NOT NULL,
    "Q1_16" boolean NOT NULL,
    "Q1_17" boolean NOT NULL,
    "Q1_18" boolean NOT NULL,
    "Q1_19" boolean NOT NULL,
    "Q2" integer,
    "N1" text,
    "Q3" integer,
    "Q3_0_open" date,
    "Q4" integer,
    "Q4_0_open" date,
    "Q5" integer,
    "Q6" integer,
    "Q6_1_open" date,
    "Q6b" integer,
    "Q6c" integer,
    "Q6d" integer,
    "Q7_0" boolean NOT NULL,
    "Q7_1" boolean NOT NULL,
    "Q7_3" boolean NOT NULL,
    "Q7_2" boolean NOT NULL,
    "Q7_4" boolean NOT NULL,
    "Q7_5" boolean NOT NULL,
    "Q7b" integer,
    "Q8_0" boolean NOT NULL,
    "Q8_1" boolean NOT NULL,
    "Q8_2" boolean NOT NULL,
    "Q8_3" boolean NOT NULL,
    "Q8_4" boolean NOT NULL,
    "Q8_5" boolean NOT NULL,
    "Q8b" integer,
    "Q9_0" boolean NOT NULL,
    "Q9_1" boolean NOT NULL,
    "Q9_2" boolean NOT NULL,
    "Q9_3" boolean NOT NULL,
    "Q9_4" boolean NOT NULL,
    "Q9_5" boolean NOT NULL,
    "Q9_6" boolean NOT NULL,
    "Q9b" integer,
    "Q10" integer,
    "Q10b" integer,
    "Q10c" integer,
    "Q11" integer,
    "Q12_multi_row1_col1" integer,
    "Q13_multi_row1_col1" integer,
    CONSTRAINT "pollster_results_weekly_Q10_check1" CHECK (("Q10" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q10b_check1" CHECK (("Q10b" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q10c_check1" CHECK (("Q10c" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q11_check1" CHECK (("Q11" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q12_multi_row1_col1_check1" CHECK (("Q12_multi_row1_col1" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q13_multi_row1_col1_check1" CHECK (("Q13_multi_row1_col1" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q2_check1" CHECK (("Q2" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q3_check1" CHECK (("Q3" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q4_check1" CHECK (("Q4" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q5_check1" CHECK (("Q5" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q6_check1" CHECK (("Q6" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q6b_check1" CHECK (("Q6b" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q6c_check1" CHECK (("Q6c" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q6d_check1" CHECK (("Q6d" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q7b_check1" CHECK (("Q7b" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q8b_check1" CHECK (("Q8b" >= 0)),
    CONSTRAINT "pollster_results_weekly_Q9b_check1" CHECK (("Q9b" >= 0))
);


INSERT INTO epidb_results_weekly
SELECT i."Qcountry", w.global_id, w."timestamp", w."Q1_0", w."Q1_1", w."Q1_2", w."Q1_3", w."Q1_4", w."Q1_5", w."Q1_6", w."Q1_7", w."Q1_8", w."Q1_9", w."Q1_10", w."Q1_11", w."Q1_12", w."Q1_13", w."Q1_14", w."Q1_15", w."Q1_16", w."Q1_17", w."Q1_18", w."Q1_19", w."Q2", w."N1", w."Q3", w."Q3_0_open", w."Q4", w."Q4_0_open", w."Q5", w."Q6", w."Q6_1_open", w."Q6b", w."Q6c", w."Q6d", w."Q7_0", w."Q7_1", w."Q7_3", w."Q7_2", w."Q7_4", w."Q7_5", w."Q7b", w."Q8_0", w."Q8_1", w."Q8_2", w."Q8_3", w."Q8_4", w."Q8_5", w."Q8b", w."Q9_0", w."Q9_1", w."Q9_2", w."Q9_3", w."Q9_4", w."Q9_5", w."Q9_6", w."Q9b", w."Q10", w."Q10b", w."Q10c", w."Q11", w."Q12_multi_row1_col1", w."Q13_multi_row1_col1" FROM pollster_results_weekly AS w
JOIN 

    (SELECT i1."Qcountry", i1.global_id
    FROM pollster_results_intake i1 LEFT JOIN pollster_results_intake i2 
    ON (i1.global_id = i2.global_id AND i1.timestamp < i2.timestamp)
    WHERE i2.id IS NULL) AS i

ON w.global_id = i.global_id;


