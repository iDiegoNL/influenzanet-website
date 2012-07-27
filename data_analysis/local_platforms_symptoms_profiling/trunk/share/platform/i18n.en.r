# Attention EDITER en UTF-8 (pas avec TinnR)
#U+00E0	LATIN SMALL LETTER A WITH GRAVE
#U+00E1	LATIN SMALL LETTER A WITH ACUTE
#U+00E2	LATIN SMALL LETTER A WITH CIRCUMFLEX
#U+00E3	LATIN SMALL LETTER A WITH TILDE
#U+00E4	LATIN SMALL LETTER A WITH DIAERESIS
# U+00E8	LATIN SMALL LETTER E WITH GRAVE
# U+00E9	LATIN SMALL LETTER E WITH ACUTE
# U+00EA	LATIN SMALL LETTER E WITH CIRCUMFLEX
# U+00EB	LATIN SMALL LETTER E WITH DIAERESIS
# U+00EE	LATIN SMALL LETTER I WITH CIRCUMFLEX
# U+00EF	LATIN SMALL LETTER I WITH DIAERESIS
# U+00F4	LATIN SMALL LETTER O WITH CIRCUMFLEX
# U+00F6	LATIN SMALL LETTER O WITH DIAERESIS

i18n = list(
# system
 'sub.text'="Source: GrippeNet.fr, UMR S 707, build at ",
 'format.date.full'="%d/%m/%Y %H:%M",

# Responses labels
 # symptoms
  'no.sympt'='No symptom',
  'fever'='Fever', 
  'chills'='Chills',
  'rhino'='Runny nose', 
  'sneeze'='Sneeze', 
  'sorethroat'='Sore throat', 
  'cough'='Cough', 
  'dyspnea'='Dyspnea', 
  'headache'='Headache', 
  'pain'='Muscle pain', 
  'chestpain'='Chest pain', 
  'asthenia'='Asthenia', 
  'anorexia'='Anorexia', 
  'sputum'='Sputum', 
  'wateryeye'='Watery Eye', 
  'nausea'='Nausea', 
  'vomiting'='Vomiting', 
  'diarrhea'='Diarrhea', 
  'abdopain'='Abdo pain', 
  'sympt.other'='Other',
  'male'='Male',
  'female'='Female',
  'Yes'='Yes',
  'No'='No',
  'DNK'='Dont Know',

 # Hear about
  "hear.radio"="Radio/TV",
  "hear.newspaper"="News",
  "hear.internet"="Internet",
  "hear.poster"="Poster",
  "hear.family"="Family",
  "hear.work"="Work",
  'hear.hworker'="Health worker", 
  'hear.project'='Team',

  # main activity
  'activity.fulltime'='Fulltime job',
  'activity.partial'='Partial',
  'activity.self'='Self. Emp.',
  'activity.student'='Student',
  'activity.home'='At home',
  'activity.unemployed'='Unemployed',
  'activity.sick'='Vacation',
  'activity.retired'='Retired',
  'activity.other'='Other',
 
  # occupation
  'occupation.prof'='Professional ',
  'occupation.office'='Office',
  'occupation.shop'='Retail/Shop',
  'occupation.worker'='Worker',
  'occupation.omanual'='Other manual',
  'occupation.other'='Otehr',

  # Transport time
  'transtime.no'='0',
  'transtime.half'='<30min',
  'transtime.hour'='30m-1h30',
  'transtime.less4h'='<= 4h',
  'transtime.more4h'='> 4h',
  
  'often.never'='Never',
  'ofter.once'='1-2 per yer',
  'often.3'='3 a 5 per yer',
  'often.6'='6 a 10 per yer',
  'often.10'='over 10',
  'often.dkn'='Dont know',

 # Education
 "education.noqualif"="No qualif.",
 "education.gcse"="GCSE",
 "education.alevel"="A-level",
 "education.bachelor"="Bachelor",
 "education.higher"="Master+",
 "education.student"="Student",

 #Contacts
 "contact.children"="Children",
 "contact.elder"="Elder",
 "contact.patient"="Patients",
 "contact.crowd"="Crowd",
 "contact.none"="None",
 
 # Q21
	"daycare.school"="School", 
	"daycare.assm"="Assistante", 
	"daycare.share"="Shared care", 
	"daycare.center"="Daycare", 
	"daycare.fam"="Fam. Daycare", 
	"daycare.garten"="Kitten Garten", 
	"daycare.nusery"="Nursery", 

 # smoker
  'smoker.no'="No",
  'smoker.occas'="Occasionnal",
  'smoker.dailyfew'="<10/d",
  'smoker.daily'=">10/d",
  'smoker.dkn'="DKN",
  'smoker.stopped'="Stop > 1y",
  'smoker.juststop'="Stop < 1y",

 # Allergy
	"allergy.hay"="Hay fever", # Hay fever
	"allergy.dust"="Dust mite", # Home dust mite
	"allergy.pets"="Pets", # Domestic pets
	"allergy.other"="Other", # Other
	"allergy.none"="None", # Hay fever
  
 # Syndromic
  'ili'='Flu-like',
  'cold'='Cold',
  'gastroenteritis'='Gastroenteritis',
  'sympt.general'='General',
  'respiratory'='Respiratory',
  'digestive'='Digestive',

 # Diet
	"diet.normal"="Normal",
	"diet.vegetarian"="Vegetarian",
	"diet.vegan"="Vegan",
	"diet.lowcal"="Low carb.",
	"diet.other"="Other",

 # Q16 Pets
	"pets.none"="Aucun",
	"pets.dog"="Dogs",
	"pets.cat"="Cats",
	"pets.bird"="Birds",
	"pets.other"="Other",

 # Reason for vaccination
    "vacc.reason.risk"="At risk",
    "vacc.reason.myrisk"="Reduce my risk", # decrease my risk
    "vacc.reason.spread"="decrease spreading", # decrease risk of spreading
    "vacc.reason.doctor"="Prescription", # doctor recommended it
    "vacc.reason.work"="Work/School", # work & school
    "vacc.reason.available"="Available", # vaccination was available
    "vacc.reason.free"="Free", # vaccin was free
    "vacc.reason.miss"="Reduce Absenteism", # I don't want to miss work/school
    "vacc.reason.always"="Always vaccinated", # I always get the vaccine
    "vacc.reason.other"="Other", # I always get the vaccine
  
  # "notvacc.reason"="Q10d",
    "notvac.reason.plan"="Planned",
    "notvac.reason.offer"="Not offered", # Haven't been offered
    "notvac.reason.risk"="not at risk", # Don't belong to risk group
    "notvac.reason.own"="Own immunity", # Better to get own immunity
    "notvac.reason.doubt"="Doubt effectiveness", # Doubt about vaccine effectiveness
    "notvac.reason.minor"="Minor illness", # Influenza is a minor illness
    "notvac.reason.likely"="Not likely", # I don't think I am likely to get influenza
    "notvac.reason.cause"="Vaccine cause flu", # I believe that influenza vaccine can cause influenza   
    "notvac.reason.safety"="Not safe", # I am worried that the vaccine is not safe or will cause illness or other adverse events 
    "notvac.reason.vaccin"="Dont like", # I don't like having vaccinations
    "notvac.reason.available"="Not available", # The vaccine is not readily available to me
    "notvac.reason.free"="Not free", # The vaccine is not free
    "notvac.reason.no"="No particular", # no particular reason
    "notvac.reason.doctor"="Recommended", # Although my doctor recommended a vaccine, I did not get one
    "notvac.reason.other"="Other", # 
 
 # Transport
	'transport.walk'="Walk",
	'transport.bike'="Bike",
	'transport.scooter'="Scooter",
	'transport.car'="Car",
	'transport.public'="Public T",
	'transport.other'="Other", 

	"condition.none"="None",
    "condition.asthma"="Asthma",
    "condition.diabetes"="Diabetes",
    "condition.lung"="Lung",
    "condition.heart"="Heart",
    "condition.kidney"="Kidney",
    "condition.immune"="Immune",

# Medical contact
	"visit.no"="No",
    "visit.GP"="GP",
	"visit.plan"="Planned",
	"visit.spe"="Specialist",
    "visit.sau"="Emergency",
    "visit.hosp"="Hospital",
    "visit.other"="Other",
    "visit.delay"="Delay",

# Medication
  "medic.no"="No",
  "medic.pain"="Pain killer",
  "medic.cough"="Cough",
	"medic.antiviral"="Antiviral",
	"medic.antibio"="Antibiotic",
	"medic.other"="Other",
	"medic.dkn"="DKN",
  
  'antiviro'='Antiviral medication',
  'antiviro.med'='Prescribed by doctor',
  'antiviro.home'='Already have',
  'antibio'='Antibiotics',
  'antibio.med'='Prescribed by doctor',
  'antibio.home'='Already have',
	
# Percieved Cause
	"cause.ili"="Flu-like",
	"cause.cold"="Cold",
	"cause.allergy"="Allergy",
	"cause.gastro"="Gastro",
	"cause.other"="Other",
	"cause.dkn"="Dont know",

# Change routine
  "routine.no"="No",
  "routine.yes"="Yes, but work",
  "routine.off"="Yes and off",

 # location
  "location"="Location",
  "location.home"="Home location",
  "location.country"="Same Country",
  "location.foreign"="Foreign",
 
	"contactmed.reception"="Receptionist",
	"contactmed.doctor"="Health worker",
	"contactmed.nhs"="NHS",
	"contactmed.npfs"="NPFS",
	"contactmed.no"="None",
	"contactmed.other"="Other",

# graph labels
  'week_by_monday'='Week (monday date)',
  'symptoms_by_week'="Symptoms by week",
  'graph.hear.about'='Hear about GrippeNet.fr ?',
  'graph.participants'='GrippeNet.fr Participants',
  'number_of_person'="Number of person",
  'sex_of_participants'="Gender",
  'age_of_participants'="Age",
  'age_of_participants_by_sex'="Age by gender",
  'percentage'="Percentage",
  'age_group'="Age-group",
  'graph_main_activity'='Main activity'
)
