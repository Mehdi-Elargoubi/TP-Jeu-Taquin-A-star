# solveur.py
from Noeud import Noeud  # Import de la classe Noeud

class Solveur:
    def __init__(self, grille_initiale):
        """
        Initialise le solveur avec l'état initial du puzzle.
        grille_initiale : état de départ du puzzle (matrice 3x3).
        """
        self.grille_initiale = grille_initiale

    def astar(self):
        """
        Implémente l'algorithme A* pour résoudre le puzzle.
        Retourne le nœud final représentant l'état résolu ou None s'il n'y a pas de solution.
        """
        liste_ouverte = []  # Liste des nœuds à explorer
        liste_fermee = set()  # Ensemble des nœuds déjà explorés

        noeud_initial = Noeud(self.grille_initiale)  # Crée le nœud initial
        liste_ouverte.append(noeud_initial)  # Ajoute le nœud initial à la liste ouverte

        while liste_ouverte:
            # Sélectionne le nœud avec la plus faible évaluation f(n)
            noeud_courant = min(liste_ouverte, key=lambda n: n.evaluation())
            liste_ouverte.remove(noeud_courant)  # Retire le nœud courant de la liste ouverte

            # Ajoute le nœud courant à la liste fermée (exploré)
            liste_fermee.add(tuple(map(tuple, noeud_courant.grille)))

            # Si l'état final est atteint, retourne ce nœud
            if noeud_courant.est_un_etat_final():
                return noeud_courant

            # Génère les successeurs du nœud courant
            for successeur in noeud_courant.successeurs():
                if tuple(map(tuple, successeur.grille)) in liste_fermee:
                    continue  # Si le successeur est déjà exploré, on l'ignore

                # Si le successeur n'est pas dans la liste ouverte, on l'ajoute
                if not any(tuple(map(tuple, n.grille)) == tuple(map(tuple, successeur.grille)) 
                           for n in liste_ouverte):
                    liste_ouverte.append(successeur)
                else:
                    # Si le successeur existe déjà dans la liste ouverte, on met à jour
                    for n in liste_ouverte:
                        if tuple(map(tuple, n.grille)) == tuple(map(tuple, successeur.grille)):
                            if successeur.evaluation() < n.evaluation():
                                liste_ouverte[liste_ouverte.index(n)] = successeur
                                break
        return None  # Retourne None si aucune solution n'est trouvée

    def afficher_chemin(self, noeud):
        """
        Affiche le chemin du nœud initial à l'état final, ainsi que le nombre de mouvements.
        """
        chemin = []
        while noeud:
            chemin.append(noeud)
            noeud = noeud.pere  # Remonte à travers les parents pour reconstruire le chemin

        chemin.reverse()  # Inverse le chemin pour avoir l'ordre chronologique
        for etat in chemin:
            print(etat)
            print("-----")
        print(f"Nombre de mouvements: {len(chemin) - 1}")
