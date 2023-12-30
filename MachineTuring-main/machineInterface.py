from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from machineModule import *
from PyQt5 import QtCore
import time

# cette class definie la tete de lecture


class teteLecture(QGraphicsObject):
    def __init__(self):
        super(teteLecture, self).__init__()

    def boundingRect(self):
        return QRectF(0, 0, 100, 30)

    def paint(self, painter, option, widget=None):
        painter.setBrush(Qt.red)
        # Déplacez le triangle au centre de la boîte englobante
        painter.drawPolygon(
            QPolygonF([QPointF(50, 0), QPointF(0, 30), QPointF(100, 30)]))

    def deplasserTete(self, x, y):
        "methode permet de deplacer la tete de lecture"
        self.setPos(x, y)

# cette class definir l'affichage de la table de transition


class TableTransition(QTableWidget):
    def __init__(self, transitions):
        super().__init__()
        nRows, nColumns = len(transitions), 5
        self.setColumnCount(nColumns)
        self.setRowCount(nRows)
        header = self.horizontalHeader()
        header.setStyleSheet("background-color: gray;")
        self.setHorizontalHeaderLabels(
            ['Etat', 'Lit', 'Ecrit', 'Déplacement', 'Nouvel Etat'])
        #item.setBackground(QColor(255, 0, 0))
        i = 0
        for key, val in transitions.items():
            self.setItem(i, 0, QTableWidgetItem(key[0]))
            self.setItem(i, 1, QTableWidgetItem(key[1]))
            self.setItem(i, 2, QTableWidgetItem(val[1]))
            self.setItem(i, 3, QTableWidgetItem(val[2]))
            self.setItem(i, 4, QTableWidgetItem(val[0]))
            i += 1

        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def detecterInstructionExectuter(self, etat, lire, ecrire, nouveau):
        pass


class machineInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Machine de Turing")
        # self.setFixedSize(1080, 720)
        self.resize(1080, 720)
        # self.setStyleSheet("background-color: #E7F7F7;")

        # definition des font utiler
        fonttitre = QFont()
        fonttitre.setPointSize(24)

        fontText = QFont()
        fontText.setPointSize(16)

        # creation du widget principale
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # creation du premiere ligne du box0 qui contient le titre du programme
        # a executer par default vide
        self.label_programme = QLabel("Nom programme")

        # création des trois niveaux de l'interface
        self.niveau1 = QHBoxLayout()
        self.niveau2 = QHBoxLayout()
        self.niveau3 = QHBoxLayout()
        self.niveau4 = QHBoxLayout()
        self.niveau5 = QHBoxLayout()
        self.niveau6 = QHBoxLayout()

        # création des widgets pour niveau 1
        self.label_programme = QLabel("Nom du programme")
        self.label_programme.setFont(fonttitre)

        # creation des widgets pour niveau 2
        self.label_etat = QLabel("Etat:")
        self.label_message = QLabel("Etat depart:")
        self.label_reponce = QLabel("")

        self.label_etat.setFont(fontText)
        self.label_message.setFont(fontText)
        self.label_reponce.setFont(fontText)

        # creation des widgets pour niveau 3
        self.scene = QGraphicsScene()
        self.vue = QGraphicsView(self.scene)
        self.vue.resize(1080, 720)
        self.rectPrincipal = self.scene.addRect(self.scene.sceneRect())
        self.vue.setScene(self.scene)
        self.vue.fitInView(self.rectPrincipal, Qt.KeepAspectRatio)

        self.rect_width = 60
        self.rect_height = 60
        self.rect_gap = 5
        self.rect_count = 16
        self.cells = []
        self.ruban = "#"*16

        # création du ruban et initialisation
        decalge = -70
        for i in range(self.rect_count):
            rect = self.scene.addRect(i * (self.rect_width + self.rect_gap), decalge, self.rect_width,
                                      self.rect_height, pen=QPen(QColor("white")), brush=QBrush(QColor("#33B9FF")))
            text = QGraphicsTextItem("#")
            text.setFont(QFont("Arial", 25))
            text_rect = text.boundingRect()
            text.setDefaultTextColor(QColor("white"))
            text_x = i * (self.rect_width + self.rect_gap) + \
                (self.rect_width - text_rect.width()) / 2
            text_y = ((self.rect_height - text_rect.height()) / 2)+decalge
            text.setPos(text_x, text_y)
            self.scene.addItem(text)
            self.cells.append(text)

           # creation de la tete de lecture

        self.triangle = teteLecture()
        self.triangle.setPos(-20, 0)
        self.scene.addItem(self.triangle)
        self.vue.ensureVisible(self.triangle, 50, 50)
        self.transitions = {}

        # creation des widgets pour niveau 4
        self.lineEditProbleme = QLineEdit()
        self.buttonValider = QPushButton("valider")
        self.buttonChoisirProgramme = QPushButton("Choisir Programme")

        # creation des widgets pour niveau 5
        self.buttonCommencer = QPushButton("Commencer")
        self.buttonPause = QPushButton("Pause")
        self.buttonRecommancer = QPushButton("Recommencer")

        # niveau1
        self.niveau1.addStretch()
        self.niveau1.addWidget(self.label_programme)
        self.niveau1.addStretch()

        # niveau2
        self.niveau2.addSpacing(10)
        self.niveau2.addWidget(self.label_etat)
        self.niveau2.addStretch()
        self.niveau2.addWidget(self.label_message)
        self.niveau2.addStretch()
        self.niveau2.addWidget(self.label_reponce)
        self.niveau2.addSpacing(10)
        # niveau3
        self.niveau3.addSpacing(10)
        self.niveau3.addWidget(self.vue)
        self.niveau3.addSpacing(10)

        # niveau4
        self.niveau4.addStretch()
        self.niveau4.addWidget(self.lineEditProbleme)
        self.niveau4.addWidget(self.buttonValider)
        self.niveau4.addSpacing(10)
        self.niveau4.addWidget(self.buttonChoisirProgramme)
        self.niveau4.addStretch()

        # niveau5
        self.niveau5.addStretch()
        self.niveau5.addWidget(self.buttonCommencer)
        self.niveau5.addSpacing(10)
        self.niveau5.addWidget(self.buttonPause)
        self.niveau5.addSpacing(10)
        self.niveau5.addWidget(self.buttonRecommancer)
        self.niveau5.addStretch()
        self.tableTransition = None

        # ajout des niveaux à la fenêtre
        self.box0 = QVBoxLayout(self.central_widget)
        self.box0.addLayout(self.niveau1)
        self.box0.addSpacing(20)
        self.box0.addLayout(self.niveau2)
        self.box0.addSpacing(50)
        self.box0.addLayout(self.niveau3)
        self.box0.addSpacing(10)
        self.box0.addLayout(self.niveau6)
        self.box0.addSpacing(10)
        self.box0.addLayout(self.niveau4)
        self.box0.addSpacing(20)
        self.box0.addLayout(self.niveau5)

        # ajouter les evenement pour les button
        self.buttonCommencer.clicked.connect(self.execution)
        self.buttonChoisirProgramme.clicked.connect(self.chargerProgramme)
        self.buttonValider.clicked.connect(self.ajouterProblemeAuRubban)


# mathode permet d'ajouter la table de transition

    def chargerProgramme(self):
        self.fichier, filte = QFileDialog.getOpenFileName(
            self, "Selectionner un fichier pour importer", "", "les ficier texte (*.txt)")
        var = ""
        if self.fichier:
            var = "le fichier est bien importer"
        else:
            var = "le fichier n'exite pas"
        QMessageBox.information(
            self, "inforation", var)
        # cree une intance de la class automate
        self.automate = Automate(self.fichier)

        # cree une instance de la class tableTransition
        self.transitions = self.automate.getTransitions()
        self.tableTransition = TableTransition(self.transitions)

        self.label_programme.setText(self.automate.getInformations()[0])
        self.etaIital = self.automate.getInformations()[1]
        self.etatFinals = self.automate.getInformations()[2]
        self.mode = self.automate.getInformations()[3]
        self.etatCourant = self.etaIital

        self.label_etat.setText("Etat : "+self.etaIital)
        self.label_message.setText("Etat depart : "+self.etaIital)

        # niveau6
        self.niveau6.addSpacing(10)
        self.niveau6.addWidget(self.tableTransition)
        self.niveau6.addSpacing(10)

# methode permet d'ajouter une instance du prbleme au ruban

    def ajouterProblemeAuRubban(self):
        "methode permet d'inserer le probleme dans le ruban"
        self.tete = 4
        self.probleme = self.lineEditProbleme.text()
        if self.lineEditProbleme.text().strip():
            i = 0
            for indice in range(self.tete, len(self.cells)):
                if i < len(self.probleme):
                    self.cells[indice].setPlainText(self.probleme[i])
                    i += 1
            self.triangle.setPos((self.tete)*60, 0)
            print(self.triangle.x())
        else:
            QMessageBox.information(
                self, "inforation", "entree une valeur valide ")

# methode permet de deplacer la tete le delecture

    def deplacementRuban(self, R):
        vitesse = 1000  # controler la vitesse d'animation
        print(self.triangle.pos().x())
        self.animation = QPropertyAnimation(
            self.triangle, b'pos')  # remplacer l'objet d'animation
        self.triangle.update()
        self.animation.setDuration(vitesse)
        self.animation.setStartValue(
            QPointF(self.triangle.pos().x(), self.triangle.pos().y()))
        if R == "R":
            self.animation.setEndValue(
                QPointF(self.triangle.pos().x()+65, self.triangle.pos().y()))
        else:
            self.animation.setEndValue(
                QPointF(self.triangle.pos().x()-65, self.triangle.pos().y()))

        # self.animation.setLoopCount(-1)
        self.triangle.update()
        self.animation.finished.connect(self.execution)
        self.animation.start()
        position = QPointF(self.triangle.pos().x(), 0)
        self.vue.centerOn(QPointF(self.triangle.pos().x(), 0))

# methode permet d'executer les instructions de la table de transition
    def execution(self):
        val = 0.2  # controler la vitesse d'execution
        "execution des instruction da la table de transition sur la la machine"
        if self.etatCourant not in self.etatFinals:
            transition = self.transitions.get(
                (self.etatCourant, self.cells[self.tete].toPlainText()), None)
            self.label_message.setText(
                "Symbole lit : "+self.cells[self.tete].toPlainText())
            time.sleep(val)
            if transition:
                self.deplacementRuban(transition[2])
                self.cells[self.tete].setPlainText(transition[1])
                self.label_message.setText("Symbole ecrit : "+transition[1])
                time.sleep(val)

                if(transition[2] == 'R'):
                    self.tete += 1
                    self.label_message.setText(
                        "Mouvement de rubant : vers la droite")
                elif(transition[2] == 'L'):
                    self.tete -= 1
                    self.label_message.setText(
                        "Mouvement de rubant : vers la gauche")
                self.etatCourant = transition[0]
                time.sleep(val)
                self.label_etat.setText("Etat : "+transition[0])
                time.sleep(val)
            else:
                if (self.mode == "reconnaisseur"):
                    self.label_reponce.setText("n'est pas reconnu")
                    self.label_reponce.setStyleSheet("color: red;")
                # break
        if self.etatCourant in self.etatFinals and self.mode == "reconnaisseur":
            self.label_reponce.setText("reconnu")
            self.label_reponce.setStyleSheet("color: green;")

# cette methode permet
    def afficherInstruction(self, etatActuelle, tableTransition):
        self.label_etat.setText(
            self.label_etat.text().split(" ")[0]+etatActuelle)
        self.label_message
        #self.tableTransition.setItem(row, column, item)


app = QApplication(sys.argv)
machine = machineInterface()
machine.show()
app.exec_()
