import os


#Fonction qui lit et retourne le semestre en cours
def get_semestre():
	with open(os.path.dirname(os.path.abspath(__file__))+"/semestre.txt", "r") as file:
			content = file.read()
			semestre = int(content)

			return semestre