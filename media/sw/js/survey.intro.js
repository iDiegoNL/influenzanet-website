function startIntro(){
  var intro = introJs();
  intro.setOptions({
  	tooltipClass: 'survey-intro',
	nextLabel: 'Suivant',
	prevLabel: 'Précédent',
	skipLabel: 'Passer',
	doneLabel: 'Terminé',
    steps: [
      { 
        intro: "Bienvenu sur l'espace participants de GrippeNet.fr. Cette introduction va vous monter tout ce qu'il y a a connaitre sur cette page."
      },
      {
        element: '#people-table',
        intro: "Ce tableau vous permet de visualiser les participants de votre compte.",
		position: 'top'
      },
      {
        element: '#' + first_user +'-identity' ,
        intro: "Chaque participant est identifié par une image (avatat) et par un nom. <br/>Pour préserver votre vie privée<br/> utilisez pseudo, surnom ou un mot (papa,...). Ces 'noms' et avatars vous aident à savoir de quel participant il s'agit si votre compte a plusieurs partiicpants. Nous ne les utilisons pas pour traiter nos données.",
		position: 'right',
		tooltipClass: 'survey-intro large-intro'
      },
      {
        element: '#' + first_user +'-edit' ,
        intro: "Cliquer sur cet icone vous permet de modifier un participant : changer son nom ou choisir un autre avatar pour ce participant (vous avez le choix entre une cinquantaine d'avatar possibles).",
		position: 'right'
      },
      {
        element: '#link-add-people' ,
        intro: "Vous pouvez rajouter un nouveau participant sur votre compte en cliquant sur ce lien. Votre compte peut ainsi regrouper les questionnaires de toute la famille.",
		position: 'top'
      },
      {
        element: '#button-delete' ,
        intro: "Vous pouvez également supprimer un participant de votre compte. Cochez la case à gauche du nom du participant puis cliquez sur ce bouton pour le supprimer.",
		position: 'top'
      },
     {
        element: '#' + first_user +'-intake'  ,
        intro: "Pour tout nouveau participant, la première chose à faire est de remplir le questionnaire préliminaire. C'est ce questionnaire qui permet de décrire un participant au début de la saison (si certains éléments change il est possible de le modifier en cours de saison : par exemple la vaccination antigrippale)",
		position: 'top'
      },
     {
        element: '#' + first_user +'-cell-weekly'  ,
        intro: "Après le questionnaire préliminaire, un bouton sera disponible dans cette case pour remplir le questionnaire <i>hebdomadaire</i> qui nous renseignera sur vos symptomes. L'idéal est de le remplir aussi moins chaque semaine, <b>même si vous n'avez pas de symptome</b>",
		position: 'top'
      },
     {
        element: '#button-healthy' ,
        intro: "Si plusieurs participants n'ont pas de symptome, vous pouvez cocher la case à coté de leur nom puis cliquer sur ce bouton pour indiquer que tout va bien.",
		position: 'top'
      },
     {
        element: '#link-help-pages' ,
        intro: "Vous trouverez également un peu d'aide et d'explications sur ces pages.",
		position: 'left'
      },
     {
        element: '#link-dashboard' ,
        intro: "Vous retrouverez sur la page 'Vos résultats' un retour d'information sur les participants de votre compte. ",
		position: 'left'
      },
     {
        element: '#link-group' ,
        intro: "Vous retrouverez sur la page 'Vos résultats' un retour d'information sur les participants de votre compte. ",
		position: 'left'
      }
	]
  });
  intro.start();
}