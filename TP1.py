import heapq

class Noeud:
    def __init__(self, grille, pere=None, g=0):
        self.grille = grille  
        self.pere = pere      
        self.g = g     

    def __str__(self):
        return "\n".join([" ".join(map(str, ligne)) 
                          for ligne in self.grille])

    def __eq__(self, other):
        return self.grille == other.grille

    def calcul_h1(self):
        objectif = [1, 2, 3, 4, 5, 6, 7, 8, 0]  
        grille_flat = sum(self.grille, [])   
        return sum(1 for i in range(len(grille_flat)) 
                        if grille_flat[i] != objectif[i] and grille_flat[i] != 0
                    )

    def calcul_h2(self):
        objectif_positions = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 0: (2, 2)
        }
        distance = 0
        for i in range(3):
            for j in range(3):
                val = self.grille[i][j]
                if val != 0:
                    x, y = objectif_positions[val]
                    distance += abs(i - x) + abs(j - y)
        return distance

    def evaluation(self, heuristique='h1'):
        h = self.calcul_h1() if heuristique == 'h1' else self.calcul_h2()
        return self.g + h

    def est_un_etat_final(self):
        return self.grille == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def position_vide(self):
        for i in range(3):
            for j in range(3):
                if self.grille[i][j] == 0:
                    return (i, j)

    def successeurs(self):
        voisins = []
        x, y = self.position_vide()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # droite, gauche, bas, haut
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                nouvelle_grille = [ligne[:] for ligne in self.grille]  # Copier la grille
                nouvelle_grille[x][y], nouvelle_grille[nx][ny] = nouvelle_grille[nx][ny], nouvelle_grille[x][y]  # Échange
                voisins.append(Noeud(nouvelle_grille, self, self.g + 1))
        return voisins






class Solveur:
    def __init__(self, grille_initiale):
        self.grille_initiale = grille_initiale

    def astar(self):
        liste_ouverte = []  
        liste_fermee = set()  

        noeud_initial = Noeud(self.grille_initiale)

        # Ajout du nœud initial à la liste ouverte
        liste_ouverte.append(noeud_initial)

        while liste_ouverte:
            #le noeud qui a la valeur f minimale
            noeud_courant = min(liste_ouverte, key=lambda n: n.evaluation())
            liste_ouverte.remove(noeud_courant)

            # ajout de nœud à la liste fermée
            liste_fermee.add(tuple(map(tuple, noeud_courant.grille)))

            # on vérifie l'état final si il est atteint
            if noeud_courant.est_un_etat_final():
                return noeud_courant 

            for successeur in noeud_courant.successeurs():                
                if tuple(map(tuple, successeur.grille)) in liste_fermee:
                    continue # on ignore les nœuds explorés

                # successeur n'est pas dans la liste ouverte
                if not any(tuple(map(tuple, n.grille)) == tuple(map(tuple, successeur.grille)) 
                           for n in liste_ouverte):
                    liste_ouverte.append(successeur)

                # successeur existe déjà dans la liste
                else:
                    for n in liste_ouverte:
                        if tuple(map(tuple, n.grille)) == tuple(map(tuple, successeur.grille)):
                            if successeur.evaluation() < n.evaluation(): 
                                liste_ouverte[liste_ouverte.index(n)] = successeur 
                                break 
        # No solution found
        return None
    
    def afficher_chemin(self, noeud):
        chemin = []
        while noeud:
            chemin.append(noeud)
            noeud = noeud.pere

        chemin.reverse()
        for etat in chemin:
            print(etat)
            print("-----")
        print(f"Nombre de mouvements: {len(chemin) - 1}")
        
        

#------------------------------------
#------------------------------------

grille_initiale = [
    [9, 2, 4],
    [3, 0, 7],
    [6, 8, 1]
]

noeud_initial = Noeud(grille_initiale)

print("État du nœud :")
print(noeud_initial)

h1 = noeud_initial.calcul_h1()
h2 = noeud_initial.calcul_h2()
print("\nValeur h1 (nombre de cases mal placées) :", h1)
print("Valeur h2 (somme des distances de Manhattan) :", h2)

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
    [1, 8, 3],
    [6, 4, 5],
    [2, 0, 7]
]

solveur1 = Solveur(grille1)
solution1 = solveur1.astar()

if solution1:
    print("Grille 1 résolue :")
    solveur1.afficher_chemin(solution1)
else:
    print("Aucune solution trouvée pour la grille 1.")

solveur2 = Solveur(grille2)
solution2 = solveur2.astar()

if solution2:
    print("Grille 2 résolue :")
    solveur2.afficher_chemin(solution2)
else:
    print("Aucune solution trouvée pour la grille 2.")
