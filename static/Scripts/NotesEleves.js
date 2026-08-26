let listeNotes = document.querySelectorAll(".Note");


for(let i=0; i < listeNotes.length; i++){
	if(listeNotes[i].textContent == "A"){
		listeNotes[i].classList.add("absence")
	}
}