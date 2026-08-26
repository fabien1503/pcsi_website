//Modification du choix du semestre
const SEMESTRE = document.getElementById("semestre").textContent



//Définition des variables
const delaiAttente = 200
const formulaireColle = document.getElementById("formColle")
const choixSemestre = document.getElementById("choixSemestre")
const aujourdhui = document.getElementById("datecolle").getAttribute("value")

//listener du nouvelle colle
const ajouterColle = document.getElementById("ajouterColle")
ajouterColle.addEventListener("click", NouvelleColle)

//listener du choix de semestre
choixSemestre.addEventListener("change",ChoixSemestreChange)

//listener du choix du groupe
const selectedGroup = document.getElementById("groupColle")
selectedGroup.addEventListener("change", ElevesGroupeSelected)

//listener de modification d'une colle
const boutonsModifier = document.getElementsByClassName("boutonmodifiercolle")
for (const bouton of boutonsModifier){
	bouton.addEventListener("click", ModifierColle)
}

//listener de suppression d'une colle
const boutonsSupprimer = document.getElementsByClassName("boutonsupprimercolle")
for (const bouton of boutonsSupprimer){
	bouton.addEventListener("click", SupprimerColle)
}


//On récupère les données et on les cache
const listeDonnees = document.getElementById("listedonnees")
const groupesS1 = []
const groupesS2 = []
const listeGroupeDonnee = listeDonnees.getElementsByTagName("groupeColle")

for (const groupe of listeGroupeDonnee) {
	groupe.hidden=true
	tableauGroupe = groupe.children
	if (tableauGroupe[0].firstChild.textContent == 1){
		groupesS1.push(groupe)
	}
	else{
		groupesS2.push(groupe)
	}
}

const listeColles = listeDonnees.getElementsByTagName("colle")
for (const colle of listeColles){
	colle.hidden=true
}


//On enlève le formulaire du DOM
const parent = formulaireColle.parentElement
parent.removeChild(formulaireColle)


//Définition des fonctions

//Fonction pour créer et afficher le formulaire d'une colle
function NouvelleColle(event){
	//On remets bien le titre
	const titre = formulaireColle.getElementsByTagName("h2")
	titre[0].setHTML("Ajout d'une nouvelle colle")
	//On affiche le formulaire juste avant la liste des colles effectuées
	let nodeAfter = document.getElementById("liste des colles effectuees")
	parent.insertBefore(formulaireColle, nodeAfter)
	//Créer un listener du choix du semestre
	let options = choixSemestre.getElementsByTagName("option")
	for (const option of options){
		if (option.value == SEMESTRE){
			option.setAttribute("selected", "")
		}
		else{option.removeAttribute("selected")}
	}
	choixSemestre.removeAttribute("disabled")

	//Réactivé le selected du choix de groupe
	selectedGroup.removeAttribute("disabled")
	//listener du bouton du formulaire
	const boutonForm = document.getElementById("boutonform")
	boutonForm.removeEventListener("click", modifierAncienneColle)
	boutonForm.addEventListener("click", enregistrerNouvelleColle)
	boutonForm.setAttribute("value", "Enregistrer")
	//Ajouter les bons groupes dans le selected du choix du groupe
	ChoixGroupeSelected()
	//Mise à zéro du formulaire
	MiseAZeroForm()
}

//Fonction appélée lorsque le choix du semestre est changé
function ChoixSemestreChange(event){
	ChoixGroupeSelected()
}

//Fonction qui va chercher les bons groupes de colle et qui les affecte dans le selected du choix du groupe
function ChoixGroupeSelected()
{
	//On récupère les données
	const semestre = choixSemestre.value
	const selectedGroup = document.getElementById("groupColle")
	const listeGroupes = listeGroupesSemestre(semestre)

	//On mets les numéros et leur valeur (id du groupe de colle) dans la liste déroulante
	let liste = []
	for (let groupe of listeGroupes){

		let option = document.createElement("option")
		option.setAttribute("value", groupe.getAttribute("groupecolleid"))
		option.setHTML(groupe.children[1].textContent)

		liste.push(option)
	}
	selectedGroup.replaceChildren(...liste)

	ElevesGroupeSelected()

}

//Fonction qui va chercher les groupes du semestre sélectionné
function listeGroupesSemestre(semestre){
	let listeGroupes
	if (semestre == 1){
		listeGroupes = groupesS1
	}
	if (semestre == 2){
		listeGroupes = groupesS2
	}

	return listeGroupes
}

//fonction affichant les champs de notes des élèves sélectionnés
function ElevesGroupeSelected()
{
	//On récupère les données
	const groupeSelectionne = document.getElementById("groupColle")
	const tableau = document.getElementById("listeElevesColle")
	const idGroupe = groupeSelectionne.value
	const semestre = choixSemestre.value
	const listeGroupes = listeGroupesSemestre(semestre)
	let listeEleves

	//On va chercher dans les données les élèves du groupe sélectionné
	for (groupe of listeGroupes){
		//console.log(groupe["groupeColleId"])
		if (groupe.getAttribute("groupeColleId") == idGroupe){
			listeEleves = groupe.getElementsByTagName("eleve")
		}
	}

	let listelignes = []
	//Puis on affiche dans le formulaire la liste des champs de note pour chaque élèves
	for(const eleve of listeEleves){
		const nom = eleve.firstElementChild.textContent
		const prenom = eleve.lastElementChild.textContent
		const eleveId = eleve.getAttribute("eleveid")

		listelignes.push(createLigne(nom, prenom, eleveId))
	}
	tableau.replaceChildren(...listelignes)

}

//fonction qui crée une ligne du tableau des notes de colle
function createLigne(nom, prenom, eleveId, note=""){
	let ligne = document.createElement("tr")

	let colonnePrenomNom = document.createElement("td")
	let label = document.createElement("label")
	label.setAttribute("for", "noteColleEleve"+eleveId)
	label.setHTML(prenom+" "+nom)
	colonnePrenomNom.appendChild(label)
	ligne.appendChild(colonnePrenomNom)

	let colonneNote = document.createElement("td")
	let input = document.createElement("input")
	input.setAttribute("type", "text")
	input.setAttribute("name", "noteColleEleve"+eleveId)
	input.setAttribute("size", "3")
	input.setAttribute("maxlength", "2")
	input.setAttribute("required", "")
	input.setAttribute("value", note)
	colonneNote.appendChild(input)
	ligne.appendChild(colonneNote)

	return ligne
}

//fonction qui vérifie la validité des données du formulaire
function verifForm(){
	//Test des variables entrées dans le formulaire
	//On va chercher les notes du formulaire
	const tableau = document.getElementById("listeElevesColle")
	const lignes = tableau.getElementsByTagName("tr")
	let testPass = true
	let messageErreur =""


	//On teste la validité des données
	for (const ligne of lignes){
		const colonneNote = ligne.lastElementChild
		const note = colonneNote.firstElementChild.value
		const colonnePrenomNom = ligne.firstElementChild
		const eleve = colonnePrenomNom.firstElementChild.firstChild.textContent

		noteNum = Number(note)
		if(note == ""){
			testPass = false
			messageErreur += " la note de "+eleve+" doit être renseignée"
		}
		if (Number.isInteger(noteNum)){
			if (note < 0 || note > 20){
				testPass = false
				messageErreur += " la note de "+eleve+" doit être comprise entre 0 et 20"
			}
		}
		else{
			if(note !=="NN" && note !=="A"){
				testPass = false
				messageErreur += " la note de "+eleve+" doit être numérique, A (absent) ou bien NN (non noté)"
			}
		}
	}

	//Si il y a une erreur, on affiche un message d'erreur
	if (testPass == false){
		//Si il existe déja un paragraphe d'erreur on va le chercher sinon on le crée
		const paragrapheBouton = document.getElementById("boutonform").parentElement
		let paragrapheErreur = document.getElementById("paragrapheerreur")
		if (paragrapheErreur == null){
			paragrapheErreur = document.createElement("p")
			paragrapheErreur.setAttribute("id", "paragrapheerreur")
			paragrapheBouton.before(paragrapheErreur)
		}
		
		paragrapheErreur.setHTML(messageErreur)
	}

	return testPass
}


//fonction d'envoi du formulaire
function enregistrerNouvelleColle(event){
	

	//Si tout est ok on envoie du formulaire au serveur

	if(verifForm()){
		const XHR = new XMLHttpRequest()
		const form = document.getElementById("formulaire")
		const donneesForm = new FormData(form)

		//On prépare la requette
		XHR.open("POST", "http://127.0.0.1:8000/notes/colleur/nouvellecolle")
		XHR.send(donneesForm)//On envoie les données du formulaire
		setTimeout(rechargerPage, delaiAttente)//On recharge la page après l'envoi au serveur
	}
}

//Fonction pour recharger une page
function rechargerPage(){
	location.reload(forceGet=true)
}

//Fonction de remise à Zero du formulaire
function MiseAZeroForm(){
	//Mise à zéro de la date
	document.getElementById("datecolle").setAttribute("value", aujourdhui)
	//Mise à zéro de l'horaire
	document.getElementById("horaireColle").setAttribute("value", "")
	//Mise à zéro de la salle
	document.getElementById("salleColle").setAttribute("value", "")
	//Mise à zéro du sujet
	document.getElementById("sujetColle").setAttribute("value", "")
}

//Affiche le formulaire de modification d'une colle
function ModifierColle(event){	
	//On va chercher dans les données la colle à modifier
	const colleAModifier = document.getElementById(event.target.name)
	const children = colleAModifier.children
	const semestre = children[0].textContent
	const date = children[1].textContent
	const horaire = children[2].textContent
	const salle = children[3].textContent
	const sujet = children[4].textContent
	const groupeNum = children[5].textContent
	const colleId = children[6].textContent

	const listeNotes = colleAModifier.getElementsByTagName("note")


	//On affiche le formulaire avec les données remplies par les données
	//Modification du titre du formulaire
	const titre = formulaireColle.getElementsByTagName("h2")
	titre[0].setHTML("Modification d'une colle")
	//On affiche le formulaire dans le DOM
	let nodeAfter = document.getElementById("liste des colles effectuees")
	parent.insertBefore(formulaireColle, nodeAfter)
	//Mise à jour du selected du choix du semestre
	let options = choixSemestre.getElementsByTagName("option")
	for (const option of options){
		if (option.value == semestre){
			option.setAttribute("selected", "")
		}
		else{option.removeAttribute("selected")}
	}
	choixSemestre.setAttribute("disabled", true)

	//Mise à jour de la date
	const formDate = document.getElementById("datecolle")
	formDate.setAttribute("value", date)
	//Mise à jour de l'horaire
	const formHoraire = document.getElementById("horaireColle")
	formHoraire.setAttribute("value", horaire)
	//Mise à jour de la salle
	const formSalle = document.getElementById("salleColle")
	formSalle.setAttribute("value", salle)
	//Mise à jour du sujet
	const formSujet = document.getElementById("sujetColle")
	formSujet.setAttribute("value", sujet)
	//Mise à jour du tableau des notes
	const tableau = document.getElementById("listeElevesColle")
	let listelignes=[]
	for (note of listeNotes){
		//On récupère le nom, le prénom et la valeur de la note ainsi que l'ID de la note
		const eleve = note.firstElementChild
		const nom = eleve.getAttribute("elevenom")
		const prenom = eleve.getAttribute("eleveprenom")
		const eleveId = eleve.getAttribute("eleveid")
		const valeur = note.lastElementChild.textContent
		listelignes.push(createLigne(nom, prenom, eleveId, valeur))
	}
	tableau.replaceChildren(...listelignes)
	//Mise à jour du numéro du groupe
	const selectedGroup = document.getElementById("groupColle")
	let option = document.createElement("option")
	option.setAttribute("value", groupeNum)
	option.setHTML(groupeNum)
	selectedGroup.replaceChildren(option)
	selectedGroup.setAttribute("disabled", true)
	//Création ou modification d'un nouveau paragraphe caché contenant l'ID de la colle
	let paragrapheColleId = document.getElementById("paragraphecolleid")
	if (paragrapheColleId == null){
		paragrapheColleId = document.createElement("p")
		paragrapheColleId.setAttribute("id", "paragraphecolleid")
		paragrapheColleId.setAttribute("hidden", true)
		const paragrapheBouton = document.getElementById("boutonform").parentElement
		paragrapheBouton.before(paragrapheColleId)
	}
	paragrapheColleId.setAttribute("colleid", colleId)

	//On gère le listener du formulaire modifié
	const boutonForm = document.getElementById("boutonform")
	boutonForm.removeEventListener("click", enregistrerNouvelleColle)
	boutonForm.addEventListener("click", modifierAncienneColle)
	boutonForm.setAttribute("value", "Modifier")
}

//Fonction qui envoie le formulaire pour enregistrer les modifs dans la bdd après vérifications
function modifierAncienneColle(event){
	const paragrapheColleId = document.getElementById("paragraphecolleid")
	colleId = paragrapheColleId.getAttribute("colleid")
	//Si tout est ok on envoie du formulaire au serveur

	if(verifForm()){
		const XHR = new XMLHttpRequest()
		const form = document.getElementById("formulaire")
		const donneesForm = new FormData(form)

		
		//On prépare la requette
		XHR.open("POST", "http://127.0.0.1:8000/notes/colleur/modifiercolle/"+colleId)
		XHR.send(donneesForm)//On envoie les données du formulaire
		setTimeout(rechargerPage,delaiAttente)
	}
}

//Fonction appelé lors de la suppression d'une colle
function SupprimerColle(event){
	//On va chercher dans les données la colle à modifier
	const colleASupprimer = document.getElementById(event.target.name)
	const children = colleASupprimer.children
	const colleId = children[6].textContent


	//Demande de confirmation de la suppression de colle
	const resultat = confirm("Êtes vous sûr de vouloir supprimer la colle ?")

	//On envoie la demande de suppression au serveur
	if (resultat){
	const XHR = new XMLHttpRequest()
		XHR.open("GET", "http://127.0.0.1:8000/notes/colleur/supprimercolle/"+colleId)
		XHR.send()
		setTimeout(rechargerPage,delaiAttente)
	}
}