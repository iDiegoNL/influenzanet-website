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
 'sub.text'="Source: GrippeNet.fr, UMR S 707, le",
 'format.date.full'="%d/%m/%Y %H:%M",

# Responses labels
 # symptoms
  'no.sympt'='Aucun sympt\u00F4me',
  'fever'='Fi\u00E8vre', 
  'chills'='Frissons',
  'rhino'='Nez qui coule', 
  'sneeze'='Eternuement', 
  'sorethroat'='Maux de gorge', 
  'cough'='Toux', 
  'dyspnea'='Essoufflement', 
  'headache'='Maux de t\u00EAte', 
  'pain'='Courbatures', 
  'chestpain'='Douleur thoracique', 
  'asthenia'='Fatigue', 
  'anorexia'='Perte d\'app\u00E9tit', 
  'sputum'='Crachats', 
  'wateryeye'='Yeux irrit\u00E9s', 
  'nausea'='Naus\u00E9es', 
  'vomiting'='Vomissements', 
  'diarrhea'='Diarrh\u00E9es', 
  'abdopain'='Douleur abdominale', 
  'sympt.other'='Autre',
  'male'='Homme',
  'female'='Femme',
  'Yes'='Oui',
  'No'='Non',
  'DNK'='Ne sait pas',

 # Hear about
  "hear.radio"="Radio/TV",
  "hear.newspaper"="Presse",
  "hear.internet"="Internet",
  "hear.poster"="Congr\u00E8s",
  "hear.family"="Famille/Amis",
  "hear.work"="Travail",
  'hear.hworker'="Prof de sant\u00E9", 
  'hear.project'='De l\'\u00E9quipe GN',

  # main activity
  'activity.fulltime'='Salari\u00E9',
  'activity.partial'='Temps Partiel',
  'activity.self'='Ind\u00E9pendant',
  'activity.student'='Etudiant',
  'activity.home'='H/F au Foyer',
  'activity.unemployed'='D. d\'emploi',
  'activity.sick'='Cong\u00E9',
  'activity.retired'='Retrait\u00E9',
  'activity.other'='Autre',
 
  # occupation
  'occupation.prof'='Cadre ou Prof Interm',
  'occupation.office'='Travail de bureau',
  'occupation.shop'='Commerce/Hotelerie/Loisir',
  'occupation.worker'='Ouvrier/artisan',
  'occupation.omanual'='Autre manuel',
  'occupation.other'='Autre',

  # Transport time
  'transtime.no'='0',
  'transtime.half'='<30min',
  'transtime.hour'='30m-1h30',
  'transtime.less4h'='<= 4h',
  'transtime.more4h'='> 4h',
  
  'often.never'='Jamais',
  'ofter.once'='1-2 par an',
  'often.3'='3 a 5 par an',
  'often.6'='6 a 10 par an',
  'often.10'='plus de 10',
  'often.dkn'='Ne sait pas',

 # Education
 "education.noqualif"="Sans qualif.",
 "education.gcse"="Brevet",
 "education.alevel"="Baccalaur\u00E9at",
 "education.bachelor"="Licence",
 "education.higher"="Master",
 "education.student"="Etudiant",

 #Contacts
 "contact.children"="Enfants",
 "contact.elder"="Vieux",
 "contact.patient"="Patients",
 "contact.crowd"="Foule/Public",
 "contact.none"="Aucun",
 
 # Q21
	"daycare.school"="Ecole", 
	"daycare.assm"="Assistante", 
	"daycare.share"="Partag\u00E9e", 
	"daycare.center"="Cr\u00E8che", 
	"daycare.fam"="Cr. Familiale", 
	"daycare.garten"="Jardin d'enfants", 
	"daycare.nusery"="Halte-Garderie", 

 # smoker
  'smoker.no'="Ne fume pas",
  'smoker.occas'="Occasionnel",
  'smoker.dailyfew'="Moins de 10/j",
  'smoker.daily'="Plus de 10/j",
  'smoker.dkn'="Ne sait pas",
  'smoker.stopped'="Arret > 1an",
  'smoker.juststop'="Arret < 1an",

 # Allergy
	"allergy.hay"="Rhume des foins", # Hay fever
	"allergy.dust"="Acariens", # Home dust mite
	"allergy.pets"="Animaux", # Domestic pets
	"allergy.other"="Autres", # Other
	"allergy.none"="Aucune", # Hay fever
  
 # Syndromic
  'ili'='Syndrome Grippal',
  'cold'='Rhume',
  'gastroenteritis'='Gastroenterite',
  'sympt.general'='G\u00E9n\u00E9raux',
  'respiratory'='Respiratoires',
  'digestive'='Digestifs',

 # Diet
	"diet.normal"="Normal",
	"diet.vegetarian"="V\u00E9getarien",
	"diet.vegan"="V\u00E9getalien",
	"diet.lowcal"="Hypocalorique",
	"diet.other"="Autre",

 # Q16 Pets
	"pets.none"="Aucun",
	"pets.dog"="Chiens",
	"pets.cat"="Chats",
	"pets.bird"="Oiseaux",
	"pets.other"="Autre",

 # Reason for vaccination
    "vacc.reason.risk"="At risk",
    "vacc.reason.myrisk"="Reduit mon risque", # decrease my risk
    "vacc.reason.spread"="Reduit transmission", # decrease risk of spreading
    "vacc.reason.doctor"="Prescription", # doctor recommended it
    "vacc.reason.work"="Travail", # work & school
    "vacc.reason.available"="Vaccin disponible", # vaccination was available
    "vacc.reason.free"="Vaccin gratuit", # vaccin was free
    "vacc.reason.miss"="Reduit Absenteisme", # I don't want to miss work/school
    "vacc.reason.always"="Toujours vaccin\u00E9", # I always get the vaccine
    "vacc.reason.other"="Autre", # I always get the vaccine
  
  # "notvacc.reason"="Q10d",
    "notvac.reason.plan"="Vaccin pr\u00E9vu",
    "notvac.reason.offer"="Non propos\u00E9", # Haven't been offered
    "notvac.reason.risk"="Pas a risque", # Don't belong to risk group
    "notvac.reason.own"="Bonne immunit\u00E9", # Better to get own immunity
    "notvac.reason.doubt"="Doute sur efficacit\u00E9", # Doubt about vaccine effectiveness
    "notvac.reason.minor"="maladie b\u00E9nigne", # Influenza is a minor illness
    "notvac.reason.likely"="Pas expos\u00E9", # I don't think I am likely to get influenza
    "notvac.reason.cause"="La vaccin rend malade", # I believe that influenza vaccine can cause influenza   
    "notvac.reason.safety"="Vaccin non sur", # I am worried that the vaccine is not safe or will cause illness or other adverse events 
    "notvac.reason.vaccin"="J'aime pas les vaccins", # I don't like having vaccinations
    "notvac.reason.available"="Non disponible", # The vaccine is not readily available to me
    "notvac.reason.free"="Non gratuit", # The vaccine is not free
    "notvac.reason.no"="Aucune", # no particular reason
    "notvac.reason.doctor"="Contre-indication", # Although my doctor recommended a vaccine, I did not get one
    "notvac.reason.other"="Autre", # 
 
 # Transport
	'transport.walk'="Marche",
	'transport.bike'="V\u00E9lo",
	'transport.scooter'="Scooter",
	'transport.car'="Voiture",
	'transport.public'="T.Publiques",
	'transport.other'="Autre", 

	"condition.none"="Aucune",
    "condition.asthma"="Asthme",
    "condition.diabetes"="Diabete",
    "condition.lung"="Poumon",
    "condition.heart"="Coeur",
    "condition.kidney"="Rein",
    "condition.immune"="Immunitaire",

# Medical contact
	"visit.no"="Aucun",
    "visit.GP"="Generaliste",
	"visit.plan"="Pr\u00E9vue",
	"visit.spe"="Sp\u00E9cialiste",
    "visit.sau"="Urgence",
    "visit.hosp"="Hopital",
    "visit.other"="Autre",
    "visit.delay"="D\u00E9lai",

# Medication
  "medic.no"="Aucun",
  "medic.pain"="Anti-douleurs",
  "medic.cough"="Anti-tussifs",
	"medic.antiviral"="Antiviraux",
	"medic.antibio"="Antibio",
	"medic.other"="Autre",
	"medic.dkn"="NSP",
  
  'antiviro'='Antiviraux',
  'antiviro.med'='Prescrits par un m\u00E9decin',
  'antiviro.home'='D\u00E9ja \u00E0 la maison',
  'antibio'='Antibiotiques',
  'antibio.med'='Prescrits par un m\u00E9decin',
  'antibio.home'='D\u00E9ja \u00E0 la maison',
	
# Percieved Cause
	"cause.ili"="Grippe",
	"cause.cold"="Rhume",
	"cause.allergy"="Allergie",
	"cause.gastro"="Gastro",
	"cause.other"="Autre",
	"cause.dkn"="NSP",

# Change routine
  "routine.no"="Non",
  "routine.yes"="Oui, mais travaille",
  "routine.off"="Oui + arret travail",

 # location
  "location"="Localisation",
  "location.home"="Dep. de r\u00E9sidence",
  "location.country"="Dans le pays",
  "location.foreign"="A l'étranger",
 
	"contactmed.reception"="Reception/Accueil",
	"contactmed.doctor"="Medecin",
	"contactmed.nhs"="NHS",
	"contactmed.npfs"="NPFS",
	"contactmed.no"="Aucun",
	"contactmed.other"="Autre",

# graph labels
  'week_by_monday'='Semaine (date du lundi)',
  'symptoms_by_week'="R\u00E9partition des sympt\u00F4mes par semaine",
  'graph.hear.about'='Comment avez vous connu GrippeNet.fr ?',
  'graph.participants'='Participants \u00E0 GrippeNet.fr',
  'number_of_person'="Nombre de personnes",
  'sex_of_participants'="Sexe des participants",
  'age_of_participants'="Age des participants",
  'age_of_participants_by_sex'="Age des participants par sexe",
  'percentage'="Pourcentage",
  'age_group'="Tranches d'\u00E2ge",
  'graph_main_activity'='Activit\u00E9 principale des participants'
)
