# main.py
from Solveur import Solveur  # Import de la classe Solveur

def main():
    # État initial du puzzle avec une solution
    grille1 = [
        [7, 2, 4],
        [5, 0, 6],
        [8, 3, 1]
    ]

    # État initial du puzzle sans solution
    grille2 = [
        [1, 2, 3],
        [4, 6, 5],
        [8, 7, 0]
    ]

    # Résolution pour la première grille
    solveur1 = Solveur(grille1)  # Crée un solveur pour la première grille
    solution1 = solveur1.astar()  # Exécute l'algorithme A*

    if solution1:  # Vérifie si une solution a été trouvée
        print("Grille 1 résolue :")
        solveur1.afficher_chemin(solution1)  # Affiche le chemin de la solution
    else:
        print("Aucune solution trouvée pour la grille 1.")

    # Résolution pour la deuxième grille
    solveur2 = Solveur(grille2)  # Crée un solveur pour la deuxième grille
    solution2 = solveur2.astar()  # Exécute l'algorithme A*

    if solution2:  # Vérifie si une solution a été trouvée
        print("Grille 2 résolue :")
        solveur2.afficher_chemin(solution2)  # Affiche le chemin de la solution
    else:
        print("Aucune solution trouvée pour la grille 2.")

if __name__ == "__main__":
    main()  # Appelle la fonction principale
