
survey.xml = list(
  shortname="satisfaction",
  questions=list(
	
	"question-253"=list(
		title="Compilation Date",
		id="question-253",
		dataname="timestamp",
		type="builtin",
		data_type="wok.pollster.datatypes.Timestamp",
		mandatory="false",
		options=list(
			
		)
	),
	"question-288"=list(
		title="",
		id="question-288",
		dataname="timestart",
		type="text",
		data_type="wok.pollster.datatypes.TimeElapsed",
		mandatory="false",
		options=list(
			
		)
	),
	"question-254"=list(
		title="",
		id="question-254",
		dataname="Q0",
		type="single-choice",
		data_type="wok.pollster.datatypes.Text",
		mandatory="false",
		options=list(
			
		)
	),
	"question-255"=list(
		title="Nous souhaitons continuer le suivi GrippeNet.fr l’hiver prochain. Pensez-vous participer lors de cette seconde saison ?",
		id="question-255",
		dataname="Q1",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q1",
				text="Oui", 
				open="false"
			),
			list(
				value="0",
				name="Q1",
				text="Non", 
				open="false"
			),
			list(
				value="2",
				name="Q1",
				text="Je ne sais pas", 
				open="false"
			)
		)
	),
	"question-281"=list(
		title="Comment avez-vous rempli les questionnaires hebdomadaires de GrippeNet.fr au cours de la saison ?",
		id="question-281",
		dataname="Q1bis",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="0",
				name="Q1bis",
				text="Je n’ai jamais rempli les questionnaires hebdomadaires de GrippeNet.fr", 
				open="false"
			),
			list(
				value="4",
				name="Q1bis",
				text="Je les ai remplis régulièrement à partir du moment où je me suis inscrit(e)", 
				open="false"
			),
			list(
				value="3",
				name="Q1bis",
				text="Je les ai remplis au début, puis j’ai arrêté de les remplir", 
				open="false"
			),
			list(
				value="2",
				name="Q1bis",
				text="Je les ai remplis au début, j’ai arrêté de les remplir pendant quelques semaines, et j’ai repris le suivi", 
				open="false"
			),
			list(
				value="1",
				name="Q1bis",
				text="Je les ai remplis de façon irrégulière", 
				open="false"
			)
		)
	),
	"question-256"=list(
		title="Si vous ne pensez pas participer à la prochaine saison de GrippeNet.fr, et/ou si vous avez arrêté de participer en cours de saison, pourriez-vous nous en préciser les raisons ?",
		id="question-256",
		dataname="Q2",
		type="multiple-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q2_1",
				text="Cela me prend trop de temps", 
				open="false"
			),
			list(
				value="2",
				name="Q2_2",
				text="Je me suis lassé(e)", 
				open="false"
			),
			list(
				value="3",
				name="Q2_3",
				text="Je ne vois pas l’intérêt de participer", 
				open="false"
			),
			list(
				value="4",
				name="Q2_4",
				text="Le retour d’information (newsletter, résultats mis en ligne sur le site…) ne m’intéresse pas", 
				open="false"
			),
			list(
				value="5",
				name="Q2_5",
				text="J’en ai assez d’entendre parler de la grippe", 
				open="false"
			),
			list(
				value="6",
				name="Q2_6",
				text="Je ne suis jamais/rarement malade", 
				open="false"
			),
			list(
				value="7",
				name="Q2_7",
				text="Je n’ai pas eu la grippe cette année", 
				open="false"
			),
			list(
				value="8",
				name="Q2_8",
				text="J’ai rencontré des problèmes informatiques pour remplir les questionnaires", 
				open="false"
			),
			list(
				value="9",
				name="Q2_9",
				text="Je ne vis plus en France métropolitaine", 
				open="false"
			),
			list(
				value="10",
				name="Q2_10",
				text="Autre", 
				open="false"
			)
		)
	),
	"question-257"=list(
		title="Si vous avez répondu `Autre` à la question précédente, pourriez-vous s'il-vous-plaît préciser votre réponse ?",
		id="question-257",
		dataname="Q2bis",
		type="text",
		data_type="wok.pollster.datatypes.Text",
		mandatory="false",
		options=list(
			
		)
	),
	"question-259"=list(
		title="A combien de personnes avez-vous conseillé de s’inscrire à l’étude ?",
		id="question-259",
		dataname="Q3",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="0",
				name="Q3",
				text="0 personne", 
				open="false"
			),
			list(
				value="1",
				name="Q3",
				text="1 personne", 
				open="false"
			),
			list(
				value="2",
				name="Q3",
				text="2 à 5 personnes", 
				open="false"
			),
			list(
				value="3",
				name="Q3",
				text="6 à 10 personnes", 
				open="false"
			),
			list(
				value="4",
				name="Q3",
				text="Au moins 11 personnes", 
				open="false"
			)
		)
	),
	"question-284"=list(
		title="Utilisez-vous actuellement les réseaux sociaux ou des applications sociales (Facebook, Twitter…)?",
		id="question-284",
		dataname="Q4",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q4",
				text="Oui", 
				open="false"
			),
			list(
				value="0",
				name="Q4",
				text="Non", 
				open="false"
			),
			list(
				value="2",
				name="Q4",
				text="Je ne sais pas ce dont il s’agit", 
				open="false"
			)
		)
	),
	"question-285"=list(
		title="Seriez-vous intéressé(e) par l’utilisation d’une nouvelle fonctionnalité GrippeNet.fr pouvant être liée aux réseaux sociaux ou à des applications sociales (par exemple pour partager des résultats) ?",
		id="question-285",
		dataname="Q4bis",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q4bis",
				text="Oui", 
				open="false"
			),
			list(
				value="0",
				name="Q4bis",
				text="Non", 
				open="false"
			)
		)
	),
	"question-289"=list(
		title="Combien de temps avez-vous mis pour remplir votre questionnaire préliminaire (le tout premier questionnaire que vous avez rempli)?",
		id="question-289",
		dataname="Q5",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q5",
				text="Moins de 30 secondes", 
				open="false"
			),
			list(
				value="2",
				name="Q5",
				text="Entre 30 secondes et 1 minute", 
				open="false"
			),
			list(
				value="3",
				name="Q5",
				text="Entre 1 et 2 minutes", 
				open="false"
			),
			list(
				value="4",
				name="Q5",
				text="Entre 2 et 5 minutes", 
				open="false"
			),
			list(
				value="5",
				name="Q5",
				text="Entre 5 et 10 minutes", 
				open="false"
			),
			list(
				value="6",
				name="Q5",
				text="Plus de 10 minutes", 
				open="false"
			)
		)
	),
	"question-260"=list(
		title="Est-ce que vous avez trouvé le questionnaire préliminaire trop long ?",
		id="question-260",
		dataname="Q5bis",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q5bis",
				text="Oui", 
				open="false"
			),
			list(
				value="0",
				name="Q5bis",
				text="Non", 
				open="false"
			),
			list(
				value="2",
				name="Q5bis",
				text="Sans opinion", 
				open="false"
			)
		)
	),
	"question-290"=list(
		title="Combien de temps mettez-vous en moyenne pour remplir votre questionnaire hebdomadaire ?",
		id="question-290",
		dataname="Q6",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q6",
				text="Moins de 30 secondes", 
				open="false"
			),
			list(
				value="2",
				name="Q6",
				text="Entre 30 secondes et 1 minute", 
				open="false"
			),
			list(

				value="3",
				name="Q6",
				text="Entre 1 et 2 minutes", 
				open="false"
			),
			list(
				value="4",
				name="Q6",
				text="Entre 2 et 5 minutes", 
				open="false"
			),
			list(
				value="5",
				name="Q6",
				text="Entre 5 et 10 minutes", 
				open="false"
			),
			list(
				value="6",
				name="Q6",
				text="Plus de 10 minutes", 
				open="false"
			)
		)
	),
	"question-261"=list(
		title="Est-ce que le questionnaire hebdomadaire vous prend trop de temps ?",
		id="question-261",
		dataname="Q6bis",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q6bis",
				text="Oui", 
				open="false"
			),
			list(
				value="0",
				name="Q6bis",
				text="Non", 
				open="false"
			),
			list(
				value="2",
				name="Q6bis",
				text="Sans opinion", 
				open="false"
			)
		)
	),
	"question-263"=list(
		title="Seriez-vous prêt à répondre à des questionnaires supplémentaires, posés ponctuellement, pendant la saison grippale ?",
		id="question-263",
		dataname="Q8",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="2",
				name="Q8",
				text="Oui, quelle que soit la thématique de santé concernée", 
				open="false"
			),
			list(
				value="1",
				name="Q8",
				text="Oui, mais uniquement si cela concerne la grippe", 
				open="false"
			),
			list(
				value="0",
				name="Q8",
				text="Non", 
				open="false"
			),
			list(
				value="2",
				name="Q8",
				text="Je ne sais pas", 
				open="false"
			)
		)
	),
	"question-264"=list(
		title="Seriez-vous prêt à répondre à des questionnaires supplémentaires, posés ponctuellement, en dehors de la saison grippale (cet été par exemple)?",
		id="question-264",
		dataname="Q9",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="2",
				name="Q9",
				text="Oui, quelle que soit la thématique de santé concernée", 
				open="false"
			),
			list(
				value="1",
				name="Q9",
				text="Oui, mais uniquement si cela concerne la grippe", 
				open="false"
			),
			list(
				value="0",
				name="Q9",
				text="Non", 
				open="false"
			),
			list(
				value="3",
				name="Q9",
				text="Je ne sais pas", 
				open="false"
			)
		)
	),
	"question-265"=list(
		title="Lisez-vous la newsletter (envoyée tous les mercredis pendant la saison grippale)?",
		id="question-265",
		dataname="Q10",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="3",
				name="Q10",
				text="Oui, toutes les semaines", 
				open="false"
			),
			list(
				value="2",
				name="Q10",
				text="Oui, assez souvent", 
				open="false"
			),
			list(
				value="1",
				name="Q10",
				text="Rarement", 
				open="false"
			),
			list(
				value="0",
				name="Q10",
				text="Jamais", 
				open="false"
			)
		)
	),
	"question-266"=list(
		title="Que pensez-vous de la newsletter  ?",
		id="question-266",
		dataname="Q11",
		type="multiple-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q11_1",
				text="Elle est intéressante", 
				open="false"
			),
			list(
				value="2",
				name="Q11_2",
				text="Elle n’est pas intéressante", 
				open="false"
			),
			list(
				value="3",
				name="Q11_3",
				text="Elle est trop courte", 
				open="false"
			),
			list(
				value="4",
				name="Q11_4",
				text="Elle est trop longue", 
				open="false"
			),
			list(
				value="5",
				name="Q11_5",
				text="Elle est de la bonne longueur", 
				open="false"
			)
		)
	),
	"question-267"=list(
		title="Que pensez-vous de la fréquence à laquelle la newsletter est envoyée pendant la saison grippale (tous les mercredis)?",
		id="question-267",
		dataname="Q12",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q12",
				text="Elle est envoyée trop fréquemment", 
				open="false"
			),
			list(
				value="2",
				name="Q12",
				text="Elle est envoyée à la bonne fréquence", 
				open="false"
			),
			list(
				value="3",
				name="Q12",
				text="Elle n’est pas envoyée assez fréquemment", 
				open="false"
			)
		)
	),
	"question-268"=list(
		title="Que proposeriez-vous pour améliorer la newsletter ?",
		id="question-268",
		dataname="Q13",
		type="multiple-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q13_1",
				text="Qu’elle donne des informations sur d’autres maladies", 
				open="false"
			),
			list(
				value="2",
				name="Q13_2",
				text="Qu’elle donne des informations plus scientifiques", 
				open="false"
			),
			list(
				value="3",
				name="Q13_3",
				text="Qu’elle donne des résultats plus détaillés", 
				open="false"
			),
			list(
				value="4",
				name="Q13_4",
				text="Qu’elle donne des actualités plus détaillées", 
				open="false"
			),
			list(
				value="5",
				name="Q13_5",
				text="Qu’elle donne d’avantage de conseils de prévention", 
				open="false"
			),
			list(
				value="6",
				name="Q13_6",
				text="Rien, la newsletter me convient telle qu’elle est", 
				open="false"
			),
			list(
				value="7",
				name="Q13_7",
				text="Autre", 
				open="false"
			)
		)
	),
	"question-269"=list(
		title="Si vous avez répondu `Autre` à la question précédente, pourriez-vous s'il-vous-plaît préciser votre réponse ?",
		id="question-269",
		dataname="Q13bis",
		type="text",
		data_type="wok.pollster.datatypes.Text",
		mandatory="false",
		options=list(
			
		)
	),
	"question-270"=list(
		title="Souhaiteriez-vous recevoir, en dehors de la saison grippale, une newsletter de temps en temps ?",
		id="question-270",
		dataname="Q14",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q14",
				text="Oui, tous les mois", 
				open="false"
			),
			list(
				value="2",
				name="Q14",
				text="Oui, tous les deux mois", 
				open="false"
			),
			list(
				value="0",
				name="Q14",
				text="Non", 
				open="false"
			),
			list(
				value="3",
				name="Q14",
				text="Sans opinion", 
				open="false"
			)
		)
	),
	"question-271"=list(
		title="Avez-vous regardé les différentes pages du site Internet ?",
		id="question-271",
		dataname="Q15",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q15",
				text="Oui", 
				open="false"
			),
			list(
				value="0",
				name="Q15",
				text="Non", 
				open="false"
			)
		)
	),
	"question-287"=list(
		title="Quand visitez-vous le site Internet www.grippenet.fr ?",
		id="question-287",
		dataname="Q16",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="0",
				name="Q16",
				text="Uniquement quand je remplis mon questionnaire", 
				open="false"
			),
			list(
				value="1",
				name="Q16",
				text="Je viens parfois sur le site sans remplir mon questionnaire", 
				open="false"
			)
		)
	),
	"question-291"=list(
		title="Sans compter le temps passé à remplir vos questionnaires, combien de temps passez-vous en moyenne sur le site Internet www.grippenet.fr ?",
		id="question-291",
		dataname="Q17",
		type="single-choice",
		data_type="wok.pollster.datatypes.Text",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q17",
				text="Moins d'une minute", 
				open="false"
			),
			list(
				value="2",
				name="Q17",
				text="Entre 1 et 2 minutes", 
				open="false"
			),
			list(
				value="3",
				name="Q17",
				text="Entre 2 et 5 minutes", 
				open="false"
			),
			list(
				value="4",
				name="Q17",
				text="Entre 5 et 10 minutes", 
				open="false"
			),
			list(
				value="5",
				name="Q17",
				text="Plus de 10 minutes", 
				open="false"
			)
		)
	),
	"question-272"=list(
		title="Trouvez-vous le site Internet agréable à utiliser ?",
		id="question-272",
		dataname="Q18",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q18",
				text="Oui", 
				open="false"
			),
			list(
				value="0",
				name="Q18",
				text="Non", 
				open="false"
			),
			list(
				value="2",
				name="Q18",
				text="Sans opinion", 
				open="false"
			)
		)
	),
	"question-273"=list(
		title="Quelle est votre opinion concernant les informations disponibles sur le site Internet ?",
		id="question-273",
		dataname="Q19",
		type="multiple-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q19_1",
				text="Elles sont facilement accessibles", 
				open="false"
			),
			list(
				value="2",
				name="Q19_2",
				text="Elles ne sont pas facilement accessibles", 
				open="false"
			),
			list(
				value="3",
				name="Q19_3",
				text="Elles sont intéressantes", 
				open="false"
			),
			list(
				value="4",
				name="Q19_4",
				text="Elles ne sont pas intéressantes", 
				open="false"
			),
			list(
				value="5",
				name="Q19_5",
				text="Elles sont suffisamment détaillées", 
				open="false"
			),
			list(
				value="6",
				name="Q19_6",
				text="Elles ne sont pas assez détaillées", 
				open="false"
			),
			list(
				value="7",
				name="Q19_7",
				text="Elles sont suffisamment scientifiques", 
				open="false"
			),
			list(
				value="8",
				name="Q19_8",

				text="Elles ne sont pas assez scientifiques", 
				open="false"
			)
		)
	),
	"question-277"=list(
		title="Regardez-vous les cartes et graphiques présentant les résultats de l’étude ?",
		id="question-277",
		dataname="Q20",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="3",
				name="Q20",
				text="Oui, je les regarde souvent", 
				open="false"
			),
			list(
				value="2",
				name="Q20",
				text="Oui, je les regarde de temps en temps", 
				open="false"
			),
			list(
				value="1",
				name="Q20",
				text="Oui, je les ai regardés une ou deux fois", 
				open="false"
			),
			list(
				value="0",
				name="Q20",
				text="Non, je ne les ai jamais regardés", 
				open="false"
			)
		)
	),
	"question-276"=list(
		title="Trouvez-vous les cartes et graphiques :",
		id="question-276",
		dataname="Q21",
		type="multiple-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q21_1",
				text="Faciles à comprendre", 
				open="false"
			),
			list(
				value="2",
				name="Q21_2",
				text="Trop compliqués", 
				open="false"
			),
			list(
				value="3",
				name="Q21_3",
				text="Intéressants", 
				open="false"
			),
			list(
				value="4",
				name="Q21_4",
				text="Pas ou peu intéressants", 
				open="false"
			),
			list(
				value="5",
				name="Q21_5",
				text="Suffisants", 
				open="false"
			),
			list(
				value="6",
				name="Q21_6",
				text="Insuffisants (je voudrai d’avantage de retour d’information)", 
				open="false"
			),
			list(
				value="7",
				name="Q21_7",
				text="Autre", 
				open="false"
			)
		)
	),
	"question-286"=list(
		title="Si vous avez répondu `Autre` à la question précédente, pourriez-vous s'il-vous-plaît préciser votre réponse ?",
		id="question-286",
		dataname="Q21bis",
		type="text",
		data_type="wok.pollster.datatypes.Text",
		mandatory="false",
		options=list(
			
		)
	),
	"question-278"=list(
		title="Conseillerez-vous à vos proches et à vos amis de s’inscrire à GrippeNet.fr pour la prochaine saison grippale ?",
		id="question-278",
		dataname="Q22",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q22",
				text="Oui", 
				open="false"
			),
			list(
				value="0",
				name="Q22",
				text="Non", 
				open="false"
			)
		)
	),
	"question-279"=list(
		title="Si non, pourquoi ?",
		id="question-279",
		dataname="Q22bis",
		type="text",
		data_type="wok.pollster.datatypes.Text",
		mandatory="false",
		options=list(
			
		)
	),
	"question-280"=list(
		title="Avez-vous des choses à rajouter ?",
		id="question-280",
		dataname="Q23",
		type="text",
		data_type="wok.pollster.datatypes.Text",
		mandatory="false",
		options=list(
			
		)
	),
	"question-293"=list(
		title="QUESTIONS SUBSIDIAIRES :",
		id="question-293",
		dataname="subsidiaire",
		type="single-choice",
		data_type="wok.pollster.datatypes.Text",
		mandatory="false",
		options=list(
			
		)
	),
	"question-294"=list(
		title="En général, avez-vous un sentiment positif ou négatif, lorsque vous remplissez les questionnaires hebdomadaires de GrippeNet.fr ?",
		id="question-294",
		dataname="Q24",
		type="single-choice",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="1",
				name="Q24",
				text="Positif", 
				open="false"
			),
			list(
				value="0",
				name="Q24",
				text="Négatif", 
				open="false"
			),
			list(
				value="2",
				name="Q24",
				text="Ni l'un ni l'autre", 
				open="false"
			)
		)
	),
	"question-292"=list(
		title="Indiquez dans quelle mesure, en participant au projet GrippeNet.fr, vous vous êtes senti :",
		id="question-292",
		dataname="Q25",
		type="matrix-select",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="0",
				name="",
				text="Je ne souhaite pas répondre", 
				open="false"
			),
			list(
				value="1",
				name="",
				text="Très peu ou pas du tout", 
				open="false"
			),
			list(
				value="2",
				name="",
				text="Un peu", 
				open="false"
			),
			list(
				value="3",
				name="",
				text="Modérément", 
				open="false"
			),
			list(
				value="4",
				name="",
				text="Beaucoup", 
				open="false"
			),
			list(
				value="5",
				name="",
				text="Enormément", 
				open="false"
			)
		)
	),
	"question-295"=list(
		title="Indiquez dans quelle mesure vous êtes d’accord avec les affirmations suivantes :",
		id="question-295",
		dataname="Q26",
		type="matrix-select",
		data_type="wok.pollster.datatypes.Numeric",
		mandatory="false",
		options=list(
			
			list(
				value="0",
				name="",
				text="Je ne souhaite pas répondre", 
				open="false"
			),
			list(
				value="1",
				name="",
				text="Pas du tout d'accord", 
				open="false"
			),
			list(
				value="2",
				name="",
				text="Pas d'accord", 
				open="false"
			),
			list(
				value="3",
				name="",
				text="Ni d’accord ni pas d'accord", 
				open="false"
			),
			list(
				value="4",
				name="",
				text="D'accord", 
				open="false"
			),
			list(
				value="5",
				name="",
				text="Tout à fait d'accord", 
				open="false"
			)
		)
	)
  )
)


# Build convinients lists
survey_build = function(survey) {
  titles = list()
  labels = list()
  for(question in survey$questions) {
    #cat(question$id,"\n")
    #str(question)
    if(question$type == "multiple-choice") {
       for(option in question$options) {
         titles[[option$name]] = option$text
       }
     }
     if(question$type %in% c("single-choice","text","builtin")) {
       titles[[question$dataname]] = question$title 
    }
    if(question$type == "single-choice") {
      labs = list()
      if(length(question$options) > 0) {
        for(option in question$options) {
          labs[option$value] = option$text
        }
        labels[[question$dataname]] = as.list(labs)
      }
    }
  }
  list(titles=titles, labels=labels)
}

as.labels = function(x, question) {
  labels = survey$labels[[question]]
  if(is.null(labels)) {
    return(x)
  }
  values = names(labels)
  texts = unlist(labels)
  factor(x, values, texts)
}

question_title = function(question) {
 survey$title[[question]]
}

names.glob = function(data, p) {
  n = names(data)
  n[grep(glob2rx(p),n)]
}

survey = survey_build(survey.xml)


