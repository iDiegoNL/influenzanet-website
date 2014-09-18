survey_default_language = 'it'

# Colors

# website colors 
colors.web = list('red'="#CE2626","grey"="#939393")

# definition of epiwork tables
epiwork.tables = list(
 intake=list(
   survey_id=14,
   table = "pollster_results_intake",
   aliases=list(
#   code_com="Q3",
    "gender"="Q1",
    "date.birth"="Q2",
    "main.activity"="Q4",
    "occup.place"="Q4b",
    "occupation"="Q4c",
    "education"="Q4d",
    "contact.type"="Q5",
    "transport"="Q7",
    "time.transport"="Q7b",
    "often.ili"="Q8",
    "vacc.lastseason"="Q9",
    "vacc.curseason"="Q10",
    "vacc.when"="Q10b",
    "vacc.reason"="Q10c",
    "notvacc.reason"="Q10d",
    "condition.none"="Q11_0",
    "condition.asthma"="Q11_1",
    "condition.diabetes"="Q11_2",
    "condition.lung"="Q11_3",
    "condition.heart"="Q11_4",
    "condition.kidney"="Q11_5",
    "condition.immune"="Q11_6",
    "pregnant"="Q12",
    "smoker"="Q13",
    "allergy"="Q14",
    "diet"="Q15",
    "pets"="Q16",
    "hear.radio"="Q17_0",
    "hear.newspaper"="Q17_1",
    "hear.internet"="Q17_2",
    "hear.poster"="Q17_3",
    "hear.family"="Q17_4",
    "hear.work"="Q17_5"
   ),
#   geo.column="Q3",
   aliases.regex=list("Q4d","Q5","Q6","Q10c","Q10d","Q11","Q14","Q15","Q16","Q17")
 ),
 weekly=list(
   survey_id=15,
   table = "pollster_results_weekly",
   aliases=list(
    "same.episode"="Q2",
    "sympt.start"="Q3_0_open",
    "sympt.end"="Q4_0_open",
    'sympt.sudden'="Q5",
    "fever.start"="Q6_1_open",
    "fever.sudden"="Q6b",
    "take.temp"="Q6c",
    "highest.temp"="Q6d",
    "visit.no"="Q7_0",
    "visit.GP"="Q7_1",
    "visit.sau"="Q7_3",
    "visit.hosp"="Q7_2",
    "visit.other"="Q7_4",
    "visit.delay"="Q7b",
    "medic.no"="Q9_0",
    "medic.pain"="Q9_1",
    "medic.cough"="Q9_2"
    )
  )
)

##
# Geographic Tables
##

# level code of the information in the survey
#geo.level.base = 'com'

# geographic levels
# name=level code
# value = column name in assoc table geo_levels
#geo.levels = c(
# 'com'='code_com',
# 'dep'='code_dep',
# 'reg'='code_reg'
#)

# List of geographic tables
# name=level code
#geo.tables = list(
# 'com'=list(table='pollster_zip_codes', title=NULL,'code'),
# 'dep'=list(table='gis_departement',title='nom_dept', column='code_dept'),
# 'reg'=list(table='gis_region', title='nom_region', column='code_region')
#)

# Population table = no config (should have the same structure @see share/lib/geography.r)
