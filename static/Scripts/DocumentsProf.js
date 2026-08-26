//Constantes
const delaiAttente = 200
const adresse = "http://127.0.0.1:8000"

//On enlève le choix correction du selected
const nature = document.getElementById("id_nature")
nature.lastElementChild.remove()

//listener de suppression d'une colle
const boutonsSupprimer = document.getElementsByClassName("boutonsuppression")
for (const bouton of boutonsSupprimer){
	bouton.addEventListener("click", SupprimerDoc)
}

//listener d'ajout d'une correction
const boutonsAjoutCorrection = document.getElementsByClassName("boutton_ajout")
for (const bouton of boutonsAjoutCorrection){
	bouton.addEventListener("click", AjoutCorrection)
}

//Fonction pour recharger une page
function rechargerPage(){
	location.reload(forceGet=true)
}

//Fonction appelé lors de la suppression d'un document
function SupprimerDoc(event){
	//On va chercher le document à supprimer
	const docASupprimer = event.target.getAttribute("doc_id")

	//Demande de confirmation de la suppression du document
	const resultat = confirm("Êtes vous sûr de vouloir supprimer le document ?")

	//On envoie la demande de suppression au serveur
	if (resultat){
	const XHR = new XMLHttpRequest()
		XHR.open("GET", adresse+"/documents/supprimer/"+docASupprimer)
		XHR.send()
		setTimeout(rechargerPage,delaiAttente)
	}
}

//Fonction appelé lors de l'ajout d'une correction
function AjoutCorrection(event){
	//On va chercher le nom et l'ID du document dont on veut ajouter la correction
	const doc_id = event.target.getAttribute("doc_id")
	const doc_titre = event.target.getAttribute("doc_titre")

	//On modifie le formulaire pour poster la correction
	const titreFormulaire = document.getElementById("titre_formulaire")
	titreFormulaire.setHTML("Poster correction "+doc_titre)
	//Modification du titre
	const titreCorrection = document.getElementById("id_titre")
	titreCorrection.setAttribute("value", "Correction du "+doc_titre)
	//Modification du select et mise sur Correction
	if (nature.lastElementChild.value != "CO"){
		while(nature.firstChild){
			nature.removeChild(nature.firstChild)
		}
		const option = document.createElement("option")
		option.setAttribute("value", "CO")
		option.setHTML("Correction")
		option.setAttribute("selected", "")
		nature.appendChild(option)
	}
	//nature.setAttribute("disabled", true)
	//ajout d'un champ caché contenant l'ID du document
	const docInput = document.createElement("input")
	docInput.setAttribute("hidden", true)
	docInput.setAttribute("name", "DocId")
	docInput.setAttribute("value", doc_id)
	const formulaire = document.getElementById("formulaire")
	formulaire.appendChild(docInput)
	//Modification du bouton d'envoi

}