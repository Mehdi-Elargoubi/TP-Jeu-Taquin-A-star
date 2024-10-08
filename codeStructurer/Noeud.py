# noeud.py

class Noeud:
    def __init__(self, grille, pere=None, g=0):
        """
        Initialise un nœud.
        grille : état de la grille du puzzle (une matrice 3x3).
        pere : nœud parent (permet de retracer le chemin jusqu'à l'état initial).
        g : coût du chemin parcouru depuis l'état initial.
        """
        self.grille = grille  # Grille du puzzle
        self.pere = pere      # Nœud parent
        self.g = g            # Coût du chemin parcouru (g(n))

    def __str__(self):
        """
        Représente la grille comme une chaîne de caractères pour l'affichage.
        """
        return "\n".join([" ".join(map(str, ligne)) 
                          for ligne in self.grille])

    def __eq__(self, other):
        """
        Permet de comparer deux nœuds en vérifiant si leur grille est identique.
        """
        return self.grille == other.grille

    def calcul_h1(self):
        """
        Calcule l'heuristique h1 : le nombre de cases mal placées.
        """
        objectif = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # État final souhaité
        grille_flat = sum(self.grille, [])   # Aplatit la grille en une liste 1D
        return sum(1 for i in range(len(grille_flat)) 
                   if grille_flat[i] != objectif[i] and grille_flat[i] != 0)

    def calcul_h2(self):
        """
        Calcule l'heuristique h2 : la somme des distances de Manhattan pour chaque case.
        """
        # Dictionnaire donnant les positions finales de chaque case
        objectif_positions = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 0: (2, 2)
        }
        distance = 0
        # Parcourt chaque case et calcule la distance entre la position actuelle et finale
        for i in range(3):
            for j in range(3):
                val = self.grille[i][j]
                if val != 0:  # On ignore la case vide
                    x, y = objectif_positions[val]
                    distance += abs(i - x) + abs(j - y)  # Distance de Manhattan
        return distance

    def evaluation(self, heuristique='h1'):
        """
        Calcule la fonction d'évaluation f(n) = g(n) + h(n).
        h(n) est choisie selon l'heuristique (h1 ou h2).
        """
        h = self.calcul_h1() if heuristique == 'h1' else self.calcul_h2()
        return self.g + h  # f(n) = coût du chemin + heuristique

    def est_un_etat_final(self):
        """
        Vérifie si la grille correspond à l'état final (grille résolue).
        """
        return self.grille == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def position_vide(self):
        """
        Trouve la position de la case vide (0) dans la grille.
        """
        for i in range(3):
            for j in range(3):
                if self.grille[i][j] == 0:
                    return (i, j)

    def successeurs(self):
        """
        Génère les nœuds successeurs en déplaçant la case vide dans les directions permises.
        """
        voisins = []
        x, y = self.position_vide()  # Trouve la position de la case vide
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Droite, gauche, bas, haut
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Si la nouvelle position est valide (dans les limites de la grille)
            if 0 <= nx < 3 and 0 <= ny < 3:
                # Crée une nouvelle grille en échangeant la case vide avec son voisin
                nouvelle_grille = [ligne[:] for ligne in self.grille]
                nouvelle_grille[x][y], nouvelle_grille[nx][ny] = nouvelle_grille[nx][ny], nouvelle_grille[x][y]
                # Crée un nouveau nœud avec la grille modifiée
                voisins.append(Noeud(nouvelle_grille, self, self.g + 1))
        return voisins