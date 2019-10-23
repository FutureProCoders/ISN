from tkinter import *
from configuration import *
import numpy
import random
import time


class JEUX:
    def __init__(self, canvas, case, cpu):
        self.cpu = cpu
        self.canvas = canvas
        self.case = case
        self.tour = 0
        self.joueur = 1
        self.tableau = numpy.zeros((NB_RANGÉE, NB_COLONNE))
        self.game_over = False
        self.canvas.bind("<Button-1>", self.pointeur)
        self.dessiner_fond(canvas, case)

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

    def range_libre(self, colonne):
        """
        Cette fonction définie sur quel rangee le pions va se placer dans la colonne choisit.
        :param colonne:
        :return:
        """
        for r in range(NB_RANGÉE):
            if self.tableau[r][colonne] == 0:
                return r

    def placer_jetons(self, rangee, colonne):
        """
        Cette fonction place le jetons dans la colonne desiré en changeant la couleur du rond.
        :param rangee:
        :param colonne:
        :return:
        """
        self.tableau[rangee][colonne] = self.joueur
        ligne = NB_RANGÉE-rangee-1
        self.canvas.itemconfig(self.case[colonne][ligne], fill=COULEUR[self.joueur])
        if self.joueur == 1 or not self.cpu:
            self.canvas.update()
        else:
            time.sleep(1)
            self.canvas.update()

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

    def dessiner_fond(self, canvas, case):
        """
        Cette fonction dessine le tableau de jeu (7 colonnes par 6 rangees avec dans chaques cases un rond noir)
        :param canvas:
        :param case:
        :return:
        """
        for i in range(NB_COLONNE):
            case.append([])
            for j in range(NB_RANGÉE):
                case[i].append(canvas.create_oval(4 + CASE * i, 4 + CASE * j, 96 + CASE * i, 96 + CASE * j, fill="black"))

    def draw(self):
        """
        Cette fonction ecrit sur le canvas 'Égalité' si il n'y a pas de gagnant
        :return:
        """
        self.game_over = True
        self.canvas.create_text(350, 300, fill="white", font=(" ", 100), text="Égalité")

    def gagne(self, joueur):
        """
        Cette fonction ecrit sur le canvas le joueur gagnant.
        :param joueur:
        :return:
        """
        print("le joueur", joueur, "a gagné")
        self.game_over = True
        if joueur == 1:
            self.canvas.create_text(350, 100, fill="red", font=(" ", 50), text="le joueur 1 a gagné")
        else:
            self.canvas.create_text(350, 100, fill="yellow", font=(" ", 50), text="le joueur 2 a gagné")

    def colonnes_disponibles(self):
        colonnes_libres = []
        for colonne in range(NB_COLONNE):
            if self.colonne_libre(colonne):
                colonnes_libres.append(colonne)
        return colonnes_libres

    def winning_move(self, piece, ancienne_colone="default"):

        # Check horizontal right locations for win
        for c in range(NB_COLONNE - 3):
            for r in range(NB_RANGÉE):
                if self.tableau[r][c] == piece and self.tableau[r][c + 1] == piece and self.tableau[r][c + 2] == piece and self.tableau[r][c + 3] == 0:
                    return c + 3

        # Check horizontal left locations for win
        for c in range(NB_COLONNE - 3):
            for r in range(NB_RANGÉE):
                if self.tableau[r][c] == 0 and self.tableau[r][c + 1] == piece and self.tableau[r][c + 2] == piece and self.tableau[r][c + 3] == piece:
                    return c

        # Check vertical  locations for win
        for c in range(NB_COLONNE):
            for r in range(NB_RANGÉE - 3):
                if self.tableau[r][c] == piece and self.tableau[r + 1][c] == piece and self.tableau[r + 2][c] == piece and self.tableau[r + 3][c] == 0:
                    return c

        # Check positively sloped diagonals
        for c in range(NB_COLONNE - 3):
            for r in range(NB_RANGÉE - 3):
                if self.tableau[r][c] == piece and self.tableau[r + 1][c + 1] == piece and self.tableau[r + 2][c + 2] == piece and self.tableau[r + 3][c + 3] == 0:
                    return c + 3

        # Check negatively sloped diaganols
        for c in range(NB_COLONNE - 3):
            for r in range(3, NB_RANGÉE):
                if self.tableau[r][c] == 0 and self.tableau[r - 1][c + 1] == piece and self.tableau[r - 2][c + 2] == piece and self.tableau[r - 3][c + 3] == piece:
                    return c

        if ancienne_colone != "default":
            return ancienne_colone

        elif len(self.colonnes_disponibles()) != 0:
            return random.choice(self.colonnes_disponibles())
        else:
            return "impossible"

    def cpu_action(self):
        self.joueur = 2

        colonne = self.winning_move(1)
        nouvelle_colonne = self.winning_move(2, colonne)
        print(colonne)
        if nouvelle_colonne != "impossible":
            if self.colonne_libre(nouvelle_colonne) and not self.game_over:
                rangee = self.range_libre(nouvelle_colonne)
                self.placer_jetons(rangee, nouvelle_colonne)
                self.afficher_tableau()

                if self.coup_de_grace():
                    self.gagne(self.joueur)

    def jouer_humain(self, colonne):
        if self.tour == 0:
            self.joueur = 1
            if self.colonne_libre(colonne):
                rangee = self.range_libre(colonne)
                self.placer_jetons(rangee, colonne)
                self.afficher_tableau()
                self.tour += 1

                if self.coup_de_grace():
                    self.gagne(self.joueur)

                return

        else:
            self.joueur = 2
            if self.colonne_libre(colonne):
                rangee = self.range_libre(colonne)
                self.placer_jetons(rangee, colonne)
                self.afficher_tableau()
                self.tour += 1

                if self.coup_de_grace():
                    self.gagne(self.joueur)

                return

    def jouer_ordi(self, colonne):
        self.joueur = 1
        if self.colonne_libre(colonne):
            rangee = self.range_libre(colonne)
            self.placer_jetons(rangee, colonne)
            self.afficher_tableau()
            self.tour += 1

            if self.coup_de_grace():
                self.gagne(self.joueur)

            self.cpu_action()

            return

    def pointeur(self, event):
        """
        Cette fonction lance le jeu lorsque un clic est detecté
        :param event:
        :return:
        """
        print(event.x, event.y)
        colonne = int(event.x//CASE)
        if not self.game_over:
            if self.cpu:
                self.jouer_ordi(colonne)
            else:
                self.jouer_humain(colonne)
                self.tour = self.tour % 2

        if numpy.all(self.tableau != 0):
            self.draw()


def nouvelle_partie(cpu):
    fenetre = Tk()
    fenetre.geometry("700x600+0+0")
    fenetre.title("Puissance 4")
    canvas = Canvas(master=fenetre, width=7*CASE, height=6*CASE)
    canvas.pack()
    canvas.create_rectangle(0, 0, 700, 600, fill= "#00F")
    case = []
    JEUX(canvas, case, cpu)
    fenetre.mainloop();

