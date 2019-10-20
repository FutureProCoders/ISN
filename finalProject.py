from tkinter import *
import numpy

CASE = 100
NB_RANGÉE = 6
NB_COLONNE = 7


class jeux:
    def __init__(self):
        self.nb_tour = 0
        self.tour = 0
        self.joueur = 1
        self.tableau = numpy.zeros((NB_RANGÉE, NB_COLONNE))
        self.game_over = 0

    def afficher_tableau(self):
        """
        Cette fonction affiche le tableau de 0 qui correspond au tableau de jeu.
        :return:
        """
        print(numpy.flip(self.tableau), 0)

    def colonne_libre(self, colonne):
        """
        Cette fonction vérifie si la colonne choisit est libre (si on peut y placer un jeton).
        :param colonne:
        :return:
        """
        return self.tableau[NB_RANGÉE - 1][colonne] == 0

    def rangée_libre(self, colonne):
        """
        Cette fonction définie sur quel rangée le pions va se placer dans la colonne choisit.
        :param colonne:
        :return:
        """
        for r in range(NB_RANGÉE):
            if self.tableau[r][colonne] == 0:
                return r

    def placer_jetons(self, rangée, colonne):
        """
        Cette fonction place le jetons dans la colonne desiré en changeant la couleur du rond.
        :param rangée:
        :param colonne:
        :return:
        """
        self.tableau[rangée][colonne] = self.joueur
        ligne = NB_RANGÉE-rangée-1
        if self.joueur == 1:
            couleur = "red"
        else:
            couleur = "yellow"
        canvas.itemconfig(case[colonne][ligne], fill=couleur)

    def coup_de_grace(self):
        """
        Cette fonction verifie si il y a 4 pions alignés, ce qui ferait gagner un des deux joueurs et terminerai la partie.
        :return:
        """
        jetons = self.joueur
        # Vérifier l'horizontale
        for c in range(NB_COLONNE - 3):
            for r in range(NB_RANGÉE):
                if self.tableau[r][c] == jetons and self.tableau[r][c + 1] == jetons and self.tableau[r][c + 2] == jetons and \
                        self.tableau[r][c + 3] == jetons:
                    return True

        # Vérifier la verticale
        for c in range(NB_COLONNE):
            for r in range(NB_RANGÉE - 3):
                if self.tableau[r][c] == jetons and self.tableau[r + 1][c] == jetons and self.tableau[r + 2][c] == jetons and \
                        self.tableau[r + 3][c] == jetons:
                    return True

        # Vérifier la diagonale croissante
        for c in range(NB_COLONNE - 3):
            for r in range(NB_RANGÉE - 3):
                if self.tableau[r][c] == jetons and self.tableau[r + 1][c + 1] == jetons and self.tableau[r + 2][c + 2] == jetons and \
                        self.tableau[r + 3][c + 3] == jetons:
                    return True

        # Vérifier la diagonale décroissante
        for c in range(NB_COLONNE - 3):
            for r in range(3, NB_RANGÉE):
                if self.tableau[r][c] == jetons and self.tableau[r - 1][c + 1] == jetons and self.tableau[r - 2][c + 2] == jetons and \
                        self.tableau[r - 3][c + 3] == jetons:
                    return True




def dessiner_fond(canvas, case):
    """
    Cette fonction dessine le tableau de jeu (7 colonnes par 6 rangées avec dans chaques cases un rond noir)
    :param canvas:
    :param case:
    :return:
    """
    for i in range(NB_COLONNE):
        case.append([])
        for j in range(NB_RANGÉE):
            case[i].append(canvas.create_oval(4 + CASE * i, 4 + CASE * j, 96 + CASE * i, 96 + CASE * j, fill="black"))


def draw():
    """
    Cette fonction ecrit sur le canvas 'Égalité' si il n'y a pas de gagnant
    :return:
    """
    JEUX.game_over = 1
    canvas.create_text(350, 300, fill="white", font=(" ", 100), text="Égalité")
    canvas.create_text(355, 300, fill="black", font=(" ", 100), text="Égalité")


def gagnant(joueur):
    """
    Cette fonction ecrit sur le canvas le joueur gagnant.
    :param joueur:
    :return:
    """
    print(JEUX.nb_tour)
    print("le joueur", joueur, "a gagné")
    JEUX.game_over = 1
    if joueur == 1:
        canvas.create_text(350, 100, fill="black", font=(" ", 50), text="le joueur 1 a gagné")
        canvas.create_text(355, 100, fill="red", font=(" ", 50), text="le joueur 1 a gagné")

    else:
        canvas.create_text(350, 100, fill="black", font=(" ", 50), text="le joueur 2 a gagné")
        canvas.create_text(355, 100, fill="yellow", font=(" ", 50), text="le joueur 2 a gagné")


def pointeur(event):
    """
    Cette fonction lance le jeu lorsque un clic est detecté
    :param event:
    :return:
    """
    print(event.x, event.y)
    colonne = int(event.x//CASE)
    if JEUX.game_over == 0:
        if JEUX.tour == 0:
            JEUX.nb_tour += 1
            JEUX.joueur = 1

            if JEUX.colonne_libre(colonne):
                rangée = JEUX.rangée_libre(colonne)
                JEUX.placer_jetons(rangée, colonne)
                JEUX.afficher_tableau()

                if JEUX.coup_de_grace():
                    gagnant(JEUX.joueur)

            else:
                return

        else:
            JEUX.joueur = 2

            if JEUX.colonne_libre(colonne):
                rangée = JEUX.rangée_libre(colonne)
                JEUX.placer_jetons(rangée, colonne)
                JEUX.afficher_tableau()

                if JEUX.coup_de_grace():
                    gagnant(JEUX.joueur)
            else:
                return

        JEUX.tour += 1
        JEUX.tour = JEUX.tour % 2
    if numpy.all(JEUX.tableau != 0):
        draw()


fenetre = Tk()
fenetre.geometry("700x600+0+0")
fenetre.title("Puissance 4")
canvas = Canvas(master=fenetre, width=7*CASE, height=6*CASE)
canvas.pack()
canvas.create_rectangle(0, 0, 700, 600, fill= "#00F")
case = []
dessiner_fond(canvas, case)

canvas.bind("<Button-1>", pointeur)

JEUX = jeux()
