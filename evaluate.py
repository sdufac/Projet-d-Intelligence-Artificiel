import os

'''
autoclomplétion avec copilot
'''

print("Veuillez choisir les paramètres de l'évaluation (greedy par défaut):")
s0 = input("Choisir stratégie pour S0 :") or "greedy"
s1 = input("Choisir stratégie pour S1 :") or "greedy"

dimension = input("Choisir la dimension du cube (3 par défaut) :") or "3"
nombreParties = input("Choisir le nombre de parties a jouer (10 par défaut) :") or "10"


# Réinitialiser le fichier de sortie
open("output.txt", "w", encoding="utf-8").close()
bashCommand = (
    f"python main.py --graph cube --d {dimension} --s0 {s0} --s1 {s1} --verbose "
    f"| tee >(grep '^Winner:' >> output.txt)"
)

for i in range(1, int(nombreParties) + 1):

    os.system(f'bash -lc "{bashCommand}"')

compteurWinner0 = 0
compteurWinner1 = 0
with open("output.txt", "r", encoding="utf-8") as f:
    lignes = f.readlines()
    for ligne in lignes:
        ligne = ligne.strip()
        if ligne == "Winner: 0":
            compteurWinner0 += 1
        elif ligne == "Winner: 1":
            compteurWinner1 += 1


print("\n")            
print("Résultats de l'évaluation :")
print(f" Le joueur s0 avec la stratégie {s0} a gagné {compteurWinner0} parties, winrate : {compteurWinner0/int(nombreParties)*100} %")
print(f" Le joueur s1 avec la stratégie {s1} a gagné {compteurWinner1} parties, winrate : {compteurWinner1/int(nombreParties)*100} %")


print("Test terminée")
