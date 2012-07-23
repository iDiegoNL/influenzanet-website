survey_default_language = 'fr'

# Colors

# website colors 
colors.web = list('green'="#7AB800","blue"="#007AB8")

# definition of epiwork tables
epiwork.tables = list(
 intake=list(
   survey_id=8,
   table = "pollster_results_intake",
   aliases=list(
    code_com="Q3",
    "gender"="Q1",
    "date.birth"="Q2",
    "main.activity"="Q4",
    "occup.place"="Q4b",
    "occupation"="Q4c",
    "transport"="Q7",
    "time.transport"="Q7b",
    "often.ili"="Q8",
    
  # Education
    "education.noqualif"="Q4d_0",
    "education.gcse"="Q4d_1",
    "education.alevel"="Q4d_2",
    "education.bachelor"="Q4d_3",
    "education.higher"="Q4d_4",
    "education.student"="Q4d_5",

  # Contact type
    "contact.children"="Q5_0",
    "contact.elder"="Q5_1",
    "contact.patient"="Q5_2",
    "contact.crowd"="Q5_3",
    "contact.none"="Q5_4",

  # Keeping
	"daycare.school"="Q21_0", # Ecole0
	"daycare.assm"="Q21_1", # Assistante maternelle1
	"daycare.share"="Q21_2", # Garde partagée2
	"daycare.center"="Q21_3", # Crèche (collective, parentale, micro-crèche)3
	"daycare.fam"="Q21_4", # Crèche familiale4
	"daycare.garten"="Q21_5", # Jardin d'enfant5
	"daycare.nusery"="Q21_6", #Halte-garderie6  
	
  # houseold
    "house.0"="Q6_0", # 0-4 yo
    "house.5"="Q6_1", # 5- 18 yo
    "house.19"="Q6_2", # 19- 44 yo
    "house.45"="Q6_3", # 45- 64 yo
    "house.65"="Q6_4", # 45- 64 yo

    "house.0.num"="Q6_0_open", # 0-4 yo
    "house.5.num"="Q6_1_open", # 5- 18 yo
    "house.19.num"="Q6_2_open", # 19- 44 yo
    "house.45.num"="Q6_3_open", # 45- 64 yo
    "house.65.num"="Q6_4_open", # 45- 64 yo

	# Vaccination
	"vacc.lastseason"="Q9",		
    "vacc.curseason"="Q10",
    "vacc.when"="Q10b",
	"vacc.date"="Q10b_1_open",

  # "vacc.reason"="Q10c",
    "vacc.reason.risk"="Q10c_0",
    "vacc.reason.myrisk"="Q10c_1", # decrease my risk
    "vacc.reason.spread"="Q10c_2", # decrease risk of spreading
    "vacc.reason.doctor"="Q10c_3", # doctor recommended it
    "vacc.reason.work"="Q10c_4", # work & school
    "vacc.reason.available"="Q10c_5", # vaccination was available
    "vacc.reason.free"="Q10c_6", # vaccin was free
    "vacc.reason.miss"="Q10c_7", # I don't want to miss work/school
    "vacc.reason.always"="Q10c_8", # I always get the vaccine
    "vacc.reason.other"="Q10c_9", # I always get the vaccine
  
  # "notvacc.reason"="Q10d",
    "notvac.reason.plan"="Q10d_0",
    "notvac.reason.offer"="Q10d_1", # Haven't been offered
    "notvac.reason.risk"="Q10d_2", # Don't belong to risk group
    "notvac.reason.own"="Q10d_3", # Better to get own immunity
    "notvac.reason.doubt"="Q10d_4", # Doubt about vaccine effectiveness
    "notvac.reason.minor"="Q10d_5", # Influenza is a minor illness
    "notvac.reason.likely"="Q10d_6", # I don't think I am likely to get influenza
    "notvac.reason.cause"="Q10d_7", # I believe that influenza vaccine can cause influenza   
    "notvac.reason.safety"="Q10d_8", # I am worried that the vaccine is not safe or will cause illness or other adverse events 
    "notvac.reason.vaccin"="Q10d_9", # I don't like having vaccinations
    "notvac.reason.available"="Q10d_10", # The vaccine is not readily available to me
    "notvac.reason.free"="Q10d_11", # The vaccine is not free
    "notvac.reason.no"="Q10d_12", # no particular reason
    "notvac.reason.doctor"="Q10d_13", # Although my doctor recommended a vaccine, I did not get one
    "notvac.reason.other"="Q10d_14", # 
    
	# Q11 Condition
	"condition.none"="Q11_0",
    "condition.asthma"="Q11_1",
    "condition.diabetes"="Q11_2",
    "condition.lung"="Q11_3",
    "condition.heart"="Q11_4",
    "condition.kidney"="Q11_5",
    "condition.immune"="Q11_6",
    
	# Q12 Pregnant
	"pregnant"="Q12",
	"pregnant.trim"="Q12b",

    "smoker"="Q13",
    
	# Q14 Allergy
	"allergy.hay"="Q14_1", # Hay fever
    "allergy.dust"="Q14_2", # Home dust mite
	"allergy.pets"="Q14_3", # Domestic pets
	"allergy.other"="Q14_4", # Other
	"allergy.none"="Q14_5", # Hay fever
	
	# Q15 Diet
	"diet.normal"="Q15_0",
	"diet.vegetarian"="Q15_1",
	"diet.vegan"="Q15_2",
	"diet.lowcal"="Q15_3",
	"diet.other"="Q15_4",
    
	# Q16 Pets
	"pets.none"="Q16_0",
	"pets.dog"="Q16_1",
	"pets.cat"="Q16_2",
	"pets.bird"="Q16_3",
	"pets.other"="Q16_4",

	# Hear about us
	"hear.radio"="Q17_0",
	"hear.newspaper"="Q17_1",
	"hear.internet"="Q17_2",
	"hear.poster"="Q17_3",
	"hear.family"="Q17_4",
	"hear.work"="Q17_5",
	'hear.hworker'='Q17_6', # health worker
	'hear.project'='Q17_7', # from someone working on the project
	
	voucher="Q18",
	height="Q19",
	weight="Q20"
   ),
   geo.column="Q3",
   # List of labels codes (usable in i18n)
   codes=list(
	   activities=c(0:8),
	   occupation=c(0:5),
	   transport=c(0:5),
	   time.transport=c(0:4),
	   often.ili=c(0:4),
	   smoker = c(0:6)
  ),
  # list of labels names or aliases for a question or a group of questions (for ex. multiple options)
  # these labels could be used in i18n to get the human readable text suitable for a table or a graphic legend
  # If only one value is given, a glob pattern is expected (parsed from aliases so it only works for multple columns questions)
  labels=list(
   # Single option (set all possible labels)
  	activities= c('activity.fulltime','activity.partial','activity.self', 'activity.student','activity.home','activity.unemployed','activity.sick','activity.retired', 'activity.other'),
  	occupation=c('occupation.prof','occupation.office', 'occupation.shop', 'occupation.worker', 'occupation.omanual', 'occupation.other'),
  	transport=c('transport.walk','transport.bike','transport.scooter','transport.car','transport.public','transport.other'),
  	time.transport=c('transtime.no','transtime.half','transtime.hour','transtime.less4h','transtime.more4h'),
  	often.ili=c('often.never','ofter.once','often.3','often.6','often.10','often.dkn'),
  	smoker=c('smoker.no','smoker.occas','smoker.dailyfew','smoker.daily','smoker.dkn','smoker.stopped','smoker.juststop'),
   # multiple options questions (one label=one column=one alias)
  	hear.about="hear.*",
    education='education.*',
  	condition='condition.*',
  	allergy="allergy.*",
  	daycare='daycare.*',
  	contact='contact.*',
  	diet='diet.*',
  	pets='pets.*',
  	house='house.*',
  	vacc.reason='vacc.reason.*',
  	notvac.reason='notvac.reason.*'
   )
 ),
 weekly=list(
   survey_id=9,
   table = "pollster_results_weekly",
   aliases=list(
    # symptoms
    'no.sympt'='Q1_0',
    'fever'='Q1_1', 
    'chills'='Q1_2',
    'rhino'='Q1_3', 
    'sneeze'='Q1_4', 
    'sorethroat'='Q1_5', 
    'cough'='Q1_6', 
    'dyspnea'='Q1_7', 
    'headache'='Q1_8', 
    'pain'='Q1_9', 
    'chestpain'='Q1_10', 
    'asthenia'='Q1_11', 
    'anorexia'='Q1_12', 
    'sputum'='Q1_13', 
    'wateryeye'='Q1_14', 
    'nausea'='Q1_15', 
    'vomiting'='Q1_16', 
    'diarrhea'='Q1_17', 
    'abdopain'='Q1_18', 
    'sympt.other'='Q1_19',
   
    # About the symptoms
    "same.episode"="Q2",
    "sympt.when"="Q3",
	  "sympt.start"="Q3_0_open",
    "sympt.when.end"="Q4",
	  "sympt.end"="Q4_0_open",
    'sympt.sudden'="Q5",
    "fever.when"="Q6",
	  "fever.start"="Q6_1_open",
    "fever.sudden"="Q6b",
    "take.temp"="Q6c",
    "highest.temp"="Q6d",
	  "location"="Q15",
	
	# not used
  	"contactmed.reception"="Q8_1",
  	"contactmed.doctor"="Q8_2",
  	"contactmed.nhs"="Q8_3",
  	"contactmed.npfs"="Q8_4",
  	"contactmed.no"="Q8_0",
  	"contactmed.other"="Q8_5",
  	"contactmed.when"="Q8b",
  	"website"="Q8c",
  	"hospitalization"="Q14",
	
	# visits
    "visit.no"="Q7_0",
    "visit.GP"="Q7_1",
	  "visit.plan"="Q7_5",
    "visit.spe"="Q7_6",
    "visit.sau"="Q7_3",
    "visit.hosp"="Q7_2",
    "visit.other"="Q7_4",
    "visit.delay"="Q7b",
	
	# medication
    "medic.no"="Q9_0",
    "medic.pain"="Q9_1",
    "medic.cough"="Q9_2",
  	"medic.antiviral"="Q9_3",
  	"medic.antibio"="Q9_4",
  	"medic.other"="Q9_5",
  	"medic.dkn"="Q9_6",
  	
  # Antiviral questions
  	"antiviro.med"="Q9c_0",
  	"antiviro.home"="Q9c_1",
  	"antiviro.when"="Q9b",

  # antibio
  	"antibio.med"="Q9d_0",
  	"antibio.home"="Q9d_1",
  	
  	"change.routine"="Q10",
  	"off.work"="Q10b",
  	"off.workdelay"="Q10c",
  	"sympt.cause"="Q11",
  	"household.flu"="Q12_multi_row1_col1",
  	"household.meet"="Q13_multi_row1_col1"
  ),
	labels=list(
		location=c("location.home","location.country","location.foreign"),
		sympt.cause=c("cause.ili","cause.cold","cause.allergy","cause.gastro","cause.other","cause.dkn"),
		contactmed=c("contactmed.reception", "contactmed.doctor", "contactmed.nhs", "contactmed.npfs", "contactmed.no", "contactmed.other"),
		visit=c("visit.no", "visit.GP", "visit.plan", "visit.spe", "visit.sau", "visit.hosp", "visit.other"),
    medic="medic.*",
		antibio=c("antibio.med","antibio.home"),
		antiviro=c("antiviro.med","antiviro.home"),
		"contactmed.when"=c(), # todo
		symptoms= c('no.sympt', 'fever', 'chills','rhino', 'sneeze', 'sorethroat', 'cough', 'dyspnea', 'headache', 'pain', 'chestpain', 'asthenia', 
    'anorexia', 'sputum', 'wateryeye', 'nausea', 'vomiting', 'diarrhea', 'abdopain', 'sympt.other'),
    'change.routine'=c('routine.no','routine.yes','routine.off')
	 )
  )
)

##
# Geographic Tables
##

# level code of the information in the survey
geo.level.base = 'com'

# geographic levels
# name=level code
# value = column name in assoc table geo_levels
geo.levels = c(
 'com'='code_com',
 'dep'='code_dep',
 'reg'='code_reg'
)

# List of geographic tables
# name=level code
geo.tables = list(
 'com'=list(table='pollster_zip_codes', title=NULL, column='zip_code_key'),
 'dep'=list(table='gis_departement',title='nom_dept', column='code_dept', zones=list('reg'='code_reg')),
 'reg'=list(table='gis_region', title='nom_region', column='code_reg')
)

# Population table = no config (should have the same structure @see share/lib/geography.r)