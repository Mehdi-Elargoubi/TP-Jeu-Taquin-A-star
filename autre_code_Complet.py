class Noeud:
    def _init_(self, grille, pere=None, g=0):
        self.grille = grille  # Current state of the puzzle as a 2D list
        self.pere = pere  # Parent node
        self.g = g  # Cost to reach this node (number of moves)

    def _str_(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.grille]) + '\n'

    def _eq_(self, other):
        return self.grille == other.grille

    def trouver_case_vide(self):
        # Find the position of the empty space (0)
        for i in range(len(self.grille)):
            for j in range(len(self.grille[i])):
                if self.grille[i][j] == 0:
                    return i, j

    def calculer_h1(self, but):
        # h1: Number of misplaced tiles
        return sum([1 if self.grille[i][j] != 0 and self.grille[i][j] != but[i][j] else 0 
                    for i in range(len(self.grille)) for j in range(len(self.grille[i]))])

    def calculer_h2(self, but):
        # h2: Sum of Manhattan distances of tiles from their goal positions
        h = 0
        for i in range(len(self.grille)):
            for j in range(len(self.grille[i])):
                if self.grille[i][j] != 0:
                    valeur = self.grille[i][j]
                    # Find target position of valeur
                    for x in range(len(but)):
                        for y in range(len(but[x])):
                            if but[x][y] == valeur:
                                h += abs(i - x) + abs(j - y)
        return h

    def f(self, but, heuristique='h1'):
        # Evaluation function: f = g + h
        if heuristique == 'h1':
            return self.g + self.calculer_h1(but)
        else:
            return self.g + self.calculer_h2(but)

    def est_un_etat_final(self, but):
        return self.grille == but

    def successeurs(self):
        voisins = []
        x, y = self.trouver_case_vide()
        mouvements = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

        for dx, dy in mouvements:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grille) and 0 <= ny < len(self.grille[0]):
                nouvelle_grille = [row[:] for row in self.grille]
                nouvelle_grille[x][y], nouvelle_grille[nx][ny] = nouvelle_grille[nx][ny], nouvelle_grille[x][y]
                voisins.append(Noeud(nouvelle_grille, self, self.g + 1))

        return voisins
    
    
class Solveur:
    def _init_(self, grille_initiale, grille_but):
        self.grille_initiale = grille_initiale
        self.grille_but = grille_but

    def astar(self, heuristique='h1'):
        ouvert = [Noeud(self.grille_initiale)]  # Open list (nodes to explore)
        ferme = []  # Closed list (explored nodes)

        while ouvert:
            # Select the node with the smallest f(n)
            courant = min(ouvert, key=lambda noeud: noeud.f(self.grille_but, heuristique))
            ouvert.remove(courant)

            if courant.est_un_etat_final(self.grille_but):
                return courant  # Return the final node

            ferme.append(courant)

            for succ in courant.successeurs():
                if succ in ferme:
                    continue

                if succ not in ouvert:
                    ouvert.append(succ)
                else:
                    for noeud in ouvert:
                        if noeud == succ and succ.f(self.grille_but, heuristique) < noeud.f(self.grille_but, heuristique):
                            ouvert.remove(noeud)
                            ouvert.append(succ)

        return None  # No solution found

    def afficher_chemin(self, noeud):
        chemin = []
        while noeud:
            chemin.append(noeud)
            noeud = noeud.pere

        chemin.reverse()
        for etat in chemin:
            print(etat)
        print(f"Nombre de mouvements: {len(chemin) - 1}")
        
if __name__ == 'main':
    grille_initiale = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]

    grille_but = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    solveur = Solveur(grille_initiale, grille_but)
    resultat = solveur.astar('h2')  # Using h2 heuristic (Manhattan distance)

    if resultat:
        solveur.afficher_chemin(resultat)
    else:
        print("Aucune solution trouvée.")