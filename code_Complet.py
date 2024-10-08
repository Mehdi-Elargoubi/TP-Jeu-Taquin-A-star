
# Classe représentant un nœud de l'arbre de recherche
class Noeud:
    def __init__(self, grille, pere=None, g=0):
        # grille : état du puzzle
        # pere : parent du nœud courant (pour retracer le chemin)
        # g : coût du chemin depuis l'état initial
        self.grille = grille  
        self.pere = pere      
        self.g = g     

    def __str__(self):
        # Représente la grille sous forme de chaîne de caractères
        return "\n".join([" ".join(map(str, ligne)) 
                          for ligne in self.grille])

    def __eq__(self, other):
        # Comparaison de deux nœuds, basée sur leur grille
        return self.grille == other.grille

    def calcul_h1(self):
        # Heuristique h1 : nombre de cases mal placées
        objectif = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # État final
        grille_flat = sum(self.grille, [])   # Aplatissement de la grille en une seule liste
        return sum(1 for i in range(len(grille_flat)) 
                        if grille_flat[i] != objectif[i] and grille_flat[i] != 0
                    )

    def calcul_h2(self):
        # Heuristique h2 : somme des distances de Manhattan
        objectif_positions = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 0: (2, 2)
        }
        distance = 0
        # Parcourt la grille et calcule la distance de chaque case à sa position finale
        for i in range(3):
            for j in range(3):
                val = self.grille[i][j]
                if val != 0:  # On ne considère pas la case vide (0)
                    x, y = objectif_positions[val]
                    distance += abs(i - x) + abs(j - y)
        return distance

    def evaluation(self, heuristique='h1'):
        # Calcule la fonction d'évaluation f(n) = g(n) + h(n)
        h = self.calcul_h1() if heuristique == 'h1' else self.calcul_h2()
        return self.g + h

    def est_un_etat_final(self):
        # Vérifie si la grille correspond à l'état final
        return self.grille == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def position_vide(self):
        # Trouve la position de la case vide (0) dans la grille
        for i in range(3):
            for j in range(3):
                if self.grille[i][j] == 0:
                    return (i, j)

    def successeurs(self):
        # Génère les nœuds successeurs en déplaçant la case vide
        voisins = []
        x, y = self.position_vide()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # droite, gauche, bas, haut
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                # Copier la grille et échanger la case vide avec son voisin
                nouvelle_grille = [ligne[:] for ligne in self.grille]
                nouvelle_grille[x][y], nouvelle_grille[nx][ny] = nouvelle_grille[nx][ny], nouvelle_grille[x][y]
                voisins.append(Noeud(nouvelle_grille, self, self.g + 1))
        return voisins

# Classe représentant le solveur du puzzle utilisant l'algorithme A*
class Solveur:
    def __init__(self, grille_initiale):
        # grille_initiale : état initial du puzzle
        self.grille_initiale = grille_initiale

    def astar(self):
        # Liste ouverte : nœuds à explorer
        liste_ouverte = []  
        # Liste fermée : nœuds déjà explorés
        liste_fermee = set()  

        noeud_initial = Noeud(self.grille_initiale)
        # Ajout du nœud initial à la liste ouverte
        liste_ouverte.append(noeud_initial)

        while liste_ouverte:
            # Choisir le nœud avec la plus faible valeur f(n) = g(n) + h(n)
            noeud_courant = min(liste_ouverte, key=lambda n: n.evaluation())
            liste_ouverte.remove(noeud_courant)

            # Ajouter le nœud courant à la liste fermée (déjà exploré)
            liste_fermee.add(tuple(map(tuple, noeud_courant.grille)))

            # Vérifier si l'état final est atteint
            if noeud_courant.est_un_etat_final():
                return noeud_courant 

            # Générer les successeurs
            for successeur in noeud_courant.successeurs():
                # Si le successeur a déjà été exploré, on l'ignore
                if tuple(map(tuple, successeur.grille)) in liste_fermee:
                    continue 

                # Si le successeur n'est pas dans la liste ouverte, on l'ajoute
                if not any(tuple(map(tuple, n.grille)) == tuple(map(tuple, successeur.grille)) 
                           for n in liste_ouverte):
                    liste_ouverte.append(successeur)
                else:
                    # Si le successeur existe déjà, on met à jour s'il a un meilleur coût
                    for n in liste_ouverte:
                        if tuple(map(tuple, n.grille)) == tuple(map(tuple, successeur.grille)):
                            if successeur.evaluation() < n.evaluation():
                                liste_ouverte[liste_ouverte.index(n)] = successeur 
                                break
        # Aucun chemin trouvé (pas de solution)
        return None
    
    def afficher_chemin(self, noeud):
        # Retrouver et afficher le chemin du nœud initial à l'état final
        chemin = []
        while noeud:
            chemin.append(noeud)
            noeud = noeud.pere

        chemin.reverse()  # On retourne le chemin pour avoir l'ordre correct
        for etat in chemin:
            print(etat)
            print("-----")
        print(f"Nombre de mouvements: {len(chemin) - 1}")
        
# Partie principale pour tester l'algorithme
grille_initiale = [
    [5, 2, 4],
    [3, 0, 7],
    [6, 8, 1]
]

noeud_initial = Noeud(grille_initiale)

# Affichage de l'état initial
print("État du nœud :")
print(noeud_initial)

# Calcul des heuristiques h1 et h2 pour le nœud initial
h1 = noeud_initial.calcul_h1()
h2 = noeud_initial.calcul_h2()
print("\nValeur h1 (nombre de cases mal placées) :", h1)
print("Valeur h2 (somme des distances de Manhattan) :", h2)

# Générer et afficher les successeurs du nœud initial
successeurs = noeud_initial.successeurs()
print("\nSuccesseurs du nœud :")
for i, successeur in enumerate(successeurs):
    print(f"Successeur {i + 1} :")
    print(successeur)



# État initial avec solution 
grille1 = [
    [7, 2, 4],
    [5, 0, 6],
    [8, 3, 1]
]

# État initial sans solution
grille2 = [
    [1, 2, 3],
    [4, 6, 5],
    [8, 7, 0]
]

# État initial d'une grille qui n'a pas de solution
grilleNonSol = [
    [1, 2, 3],
    [5, 4, 6],
    [7, 0, 8]
]

# Création des solveurs pour les deux grilles
solveur1 = Solveur(grille1)
solution1 = solveur1.astar()

# Résolution de la grille 1
if solution1:
    print("Grille 1 résolue :")
    solveur1.afficher_chemin(solution1)
else:
    print("Aucune solution trouvée pour la grille 1.")

solveur2 = Solveur(grille2)
solution2 = solveur2.astar()

# Résolution de la grille 2
if solution2:
    print("Grille 2 résolue :")
    solveur2.afficher_chemin(solution2)
else:
    print("Aucune solution trouvée pour la grille 2.")