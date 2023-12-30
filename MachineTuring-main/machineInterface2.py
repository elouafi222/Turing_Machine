from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from machineModule import *
from PyQt5 import QtCore
import time

# cette class definie la tete de lecture

class AnimationTask(QObject, QRunnable):
    finished = pyqtSignal()  # Signal de fin d'animation

    def __init__(self, triangle, sens):
        super().__init__()
        self.triangle = triangle
        self.sens = sens

    def run(self):
        vitesse = 1000  # Contrôle la vitesse de l'animation

        self.animation = QPropertyAnimation(self.triangle, b'pos')
        self.animation.setDuration(vitesse)
        self.animation.setStartValue(QPointF(self.triangle.pos().x(), self.triangle.pos().y()))
        if self.sens == "R":
            self.animation.setEndValue(QPointF(self.triangle.pos().x() + 65, self.triangle.pos().y()))
        elif self.sens=="L":
            self.animation.setEndValue(QPointF(self.triangle.pos().x() - 65, self.triangle.pos().y()))
        else:
            self.animation.setEndValue(QPointF(self.triangle.pos().x(), self.triangle.pos().y()))
        self.animation.start()
        self.animation.finished.connect(self.finished)  # Émet le signal de fin d'animation




class teteLecture(QGraphicsObject):
    def __init__(self,positiontete=4):
        super(teteLecture, self).__init__()
        self.positiontete=positiontete

    def boundingRect(self):
        return QRectF(0, 0, 100, 30)

    def paint(self, painter, option, widget=None):
        painter.setBrush(Qt.red)
        # Déplacez le triangle au centre de la boîte englobante
        painter.drawPolygon(
            QPolygonF([QPointF(50, 0), QPointF(0, 30), QPointF(100, 30)]))

    def deplasserTete(self,x, y=0):
        self.setPos(self.positiontete*x-10,y)
        print(self.x())

# cette class definir l'affichage de la table de transition


class TableTransition(QTableWidget):
    def __init__(self, transitions,nomProgramme):
        super().__init__()
        nRows, nColumns = len(transitions), 5
        self.setColumnCount(nColumns)
        self.setRowCount(nRows)
        header = self.horizontalHeader()
        header.setStyleSheet("background-color: gray;")
        self.titreTabtransition=['Etat', 'Lit', 'Ecrit', 'Déplacement', 'Nouvel Etat']
        self.setHorizontalHeaderLabels(self.titreTabtransition)
        #item.setBackground(QColor(255, 0, 0))
        i = 0
        if nomProgramme=="Tour de hanoi":
            for key, val in transitions.items():
             self.setItem(i, 0, QTableWidgetItem(key[0]))
             self.setItem(i, 1, QTableWidgetItem(key[1]+" , "+key[2]+" , "+key[3]))
             self.setItem(i, 2, QTableWidgetItem(val[1]+" , "+val[2]+" , "+val[3]))
             self.setItem(i, 3, QTableWidgetItem(val[4]+" , "+val[5]+" , "+val[6]))
             self.setItem(i, 4, QTableWidgetItem(val[0]))
             i += 1
        else:
         for key, val in transitions.items():
            self.setItem(i, 0, QTableWidgetItem(key[0]))
            self.setItem(i, 1, QTableWidgetItem(key[1]))
            self.setItem(i, 2, QTableWidgetItem(val[1]))
            self.setItem(i, 3, QTableWidgetItem(val[2]))
            self.setItem(i, 4, QTableWidgetItem(val[0]))
            i += 1

        self.previous_row=-1
        self.previous_column=-1  
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.itemSelectionChanged.connect(self.change_color_selected)
    
           
    def change_color_selected(self):
        current_row=self.currentRow()
        current_column=self.currentColumn()
        if current_row >= 0 and current_column >= 0:
            # Changement de couleur de la cellule précédemment sélectionnée
            if self.previous_row >= 0 and self.previous_column >= 0:
                item = self.item(self.previous_row, self.previous_column)
                item.setBackground(QColor(255, 255, 255))

            # Changement de couleur de la nouvelle cellule sélectionnée
            item = self.item(current_row, current_column)
            item.setBackground(QColor(255, 0, 0))

            self.previous_row = current_row
            self.previous_column = current_column


class Ruban:
    def __init__(self, rect_count, rect_width, rect_height, rect_gap,scene,declage):
        self.rect_count = rect_count
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.rect_gap = rect_gap
        self.scene = scene
        self.cells = []
        self.decalge = declage
        self.initialiserRuban()

    def creationObjetQgraphicsText(self, caractere, position):
        rect = self.scene.addRect(position * (self.rect_width + self.rect_gap), self.decalge, self.rect_width,
                                  self.rect_height, pen=QPen(QColor("white")), brush=QBrush(QColor("#33B9FF")))
        text = QGraphicsTextItem(caractere)
        text.setFont(QFont("Arial", 25))
        text_rect = text.boundingRect()
        text.setDefaultTextColor(QColor("white"))
        text_x = position * (self.rect_width + self.rect_gap) + (self.rect_width - text_rect.width()) / 2
        text_y = ((self.rect_height - text_rect.height()) / 2) + self.decalge
        text.setPos(text_x, text_y)
        self.scene.addItem(text)
        self.cells.append(text)

    def initialiserRuban(self):
        self.cells = []
        for i in range(self.rect_count):
            self.creationObjetQgraphicsText("#", i)   
    
    def ajouterProblemeAuRubban(self,probleme,tetelecture):
     "Méthode permettant d'insérer le problème dans le ruban"
     self.tete = tetelecture.positiontete
     if probleme.strip():
         for indice in range(len(probleme)):
            if indice < len(self.cells) - self.tete:
                self.cells[indice + self.tete].setPlainText(probleme[indice])
            else:
                self.creationObjetQgraphicsText(probleme[indice], indice + self.tete)
         tetelecture.deplasserTete(self.rect_width)
     else:
        QMessageBox.information(self, "Information", "Entrez une valeur valide.")
        
        

class machineInterface(QMainWindow,QRunnable):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
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
        self.rect_count = 8
        self.cells = []
        self.decalge1 = -70
        
        # création du ruban et initialisation
        self.ruban1=Ruban(self.rect_count,self.rect_width,self.rect_height,self.rect_gap,self.scene,self.decalge1)
 
        # creation de la tete de lecture
        self.triangle=self.creationTetelecture()
        self.tete=self.triangle.positiontete
     
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
        self.buttonCommencer.clicked.connect(self.executionProgramme)
        self.buttonChoisirProgramme.clicked.connect(self.chargerProgramme)
        self.buttonValider.clicked.connect(self.ajouterProblemeAuRubban)
        self.buttonRecommancer.clicked.connect(self.rocommencer)
        
# methode permet de cree la tete de lecture 
    def creationTetelecture(self,postionx=-20,positiony=0):
        nomTeteLecture = teteLecture(1)
        nomTeteLecture.setPos(postionx,positiony)
        self.scene.addItem(nomTeteLecture)
        self.vue.ensureVisible(nomTeteLecture, 50, 50)
        return nomTeteLecture
        
        
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
        self.nomProgramme=self.automate.getInformations()[0]
        self.tableTransition = TableTransition(self.transitions,self.nomProgramme)

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
        
        if self.nomProgramme=="Tour de hanoi":
            self.initialisationPourTourHanoi()

# methode permet d'ajouter une instance du prbleme au ruban

    def ajouterProblemeAuRubban(self):
     "Méthode permettant d'insérer le problème dans le ruban"
     self.probleme = self.lineEditProbleme.text()
     self.ruban1.ajouterProblemeAuRubban(self.probleme,self.triangle)
     
        

# methode permet de recommencer l'execution 
    
    def rocommencer(self):
        self.etatCourant=self.etaIital
        
        for item in self.scene.items():
            self.scene.removeItem(item)
            
        self.creationTetelecture()
        self.ruban1.initialiserRuban()
        self.ruban1.ajouterProblemeAuRubban(self.probleme,self.triangle)
        #print(self.probleme)
        #print(self.tete)
        
#methode permet de pauser l'execution du programme 
    
    def pause(self):
        pass

    def deplacementTeteLecture(self,triangle,sens):    
         self.animationTete(triangle,sens)
         
    
    def animationTete(self, triangle, sens):
       task = AnimationTask(triangle, sens)
       task.run()
       if self.nomProgramme=="Tour de hanoi":
        task.finished.connect(self.executionTourhanoi)  # Connecte le signal de fin d'animation à la méthode d'exécution
       else:
        task.finished.connect(self.execution) 
       self.threadpool.start(task)  # Démarre la tâche d'animation dans le pool de threads

# methode permet d'executer les instructions de la table de transition
    
    def executionProgramme(self):
        #print(self.nomProgramme)
        if self.nomProgramme=="Tour de hanoi":
            self.executionTourhanoi()
        else:
            self.execution()


    def execution(self):
        self.val = 1  # controler la vitesse d'execution  
        self.cells=self.ruban1.cells
        if self.etatCourant not in self.etatFinals:
            
            if self.tete>=len(self.cells):
                  self.creationCellule(self.ruban1) #creation d'une nouvelle case si on a arriver a la fin du ruban
            
                  
            cle =(self.etatCourant, self.cells[self.tete].toPlainText())
            self.transition = self.transitions.get(cle, None)

            if self.transition:
                self.getposition(cle,'Etat')
                self.getposition(cle,'Lit')
                self.cells[self.tete].setPlainText(self.transition[1])
                self.getposition(cle,'Ecrit')
                if(self.transition[2] == 'R'):
                    self.tete += 1
                    self.getposition(cle,'Déplacement')
                    
                elif(self.transition[2] == 'L'):
                    self.tete -= 1
                    self.getposition(cle,'Déplacement')
                  
                self.deplacementTeteLecture(self.triangle,self.transition[2]) #! deplacement la tete de lecture  
                
                self.etatCourant = self.transition[0]
                self.label_etat.setText("Etat : "+self.transition[0])
                self.getposition(cle,'Nouvel Etat')
   
            else:
                if (self.mode == "reconnaisseur"):
                    self.label_reponce.setText("n'est pas reconnu")
                    self.label_reponce.setStyleSheet("color: red;")
                # break
        if self.etatCourant in self.etatFinals and self.mode == "reconnaisseur":
            self.label_reponce.setText("reconnu")
            self.label_reponce.setStyleSheet("color: green;")
        
    
        
    
    def initialisationPourTourHanoi(self):
        "initialisation du la vue avec les 3 rubans"
        
        self.decalge2 = self.rect_height + self.rect_gap
        self.decalge3 = self.decalge2*3
        
        # création du ruban et initialisation
        self.ruban2=Ruban(self.rect_count,self.rect_width,self.rect_height,self.rect_gap,self.scene,self.decalge2)
        self.ruban3=Ruban(self.rect_count,self.rect_width,self.rect_height,self.rect_gap,self.scene,self.decalge3)
 
        # creation de la tete de lecture
        self.triangle2=self.creationTetelecture(-20,self.rect_height+self.decalge2+10)
        self.triangle2.deplasserTete(self.rect_width,self.rect_height+self.decalge2+10)
        self.triangle3=self.creationTetelecture(-20,self.rect_height+self.decalge3+10)
        self.triangle3.deplasserTete(self.rect_width,self.rect_height+self.decalge3+10)
        
        # recuperation de la position de la tete de lecture 
        self.tete2=self.triangle2.positiontete
        self.tete3=self.triangle3.positiontete
        

    def deplacementTeteLectures(self,sens1,sens2,sens3):
        if sens1 == "R":
          self.animationTete(self.triangle,sens1)
        elif sens1 == "L":
            self.animationTete(self.triangle,sens1)
        elif sens1=="S":
            self.animationTete(self.triangle3,sens1)
        
        if sens2 == "R":
          self.animationTete(self.triangle2,sens2)
        elif sens2 == "L":
           self.animationTete(self.triangle2,sens2)
        elif sens2=="S":
            self.animationTete(self.triangle3,sens2)
        
        if sens3 == "R":
          self.animationTete(self.triangle3,sens3)
        elif sens3 == "L":
           self.animationTete(self.triangle3,sens3)
        elif sens3=="S":
            self.animationTete(self.triangle3,sens3)         
       
    
        
    def executionTourhanoi(self):
        self.val = 1  # controler la vitesse d'execution
        self.cells=self.ruban1.cells
        self.cells2=self.ruban2.cells
        self.cells3=self.ruban3.cells
        print(self.etatCourant)
        if self.etatCourant not in self.etatFinals:
            print(self.etatCourant)
            if self.tete>=len(self.cells):
                 self.creationCellule(self.ruban1)
                 
            if self.tete2>=len(self.cells):
                 self.creationCellule(self.ruban1)
            
            if self.tete3>=len(self.cells):
                 self.creationCellule(self.ruban1)
                 
            cle =(self.etatCourant, self.cells[self.tete].toPlainText(),self.cells2[self.tete2].toPlainText(),self.cells3[self.tete3].toPlainText())
            #print(cle)
            self.transition = self.transitions.get(cle, None)
            #self.getposition(cle,'Etat')
    
            #self.getposition(cle,'Lit')
            if self.transition:
                
                #self.getposition(cle,'Ecrit')
                self.cells[self.tete].setPlainText(self.transition[1])
                self.cells2[self.tete2].setPlainText(self.transition[2])
                self.cells3[self.tete3].setPlainText(self.transition[3])
                print(self.cells[self.tete].toPlainText(),self.cells2[self.tete2].toPlainText(),self.cells3[self.tete3].toPlainText())
                self.deplacementTeteLectures(self.transition[4],self.transition[5],self.transition[6]) #! deplacement la tete de lecture

                # deplacement des rubants
                if(self.transition[4] == 'R'):
                    self.tete += 1
                    #self.getposition(cle,'Déplacement')
                elif(self.transition[4] == 'L'):
                    self.tete -= 1
                    #self.getposition(cle,'Déplacement')
                    
                if(self.transition[5] == 'R'):
                    self.tete2 += 1
                    #self.getposition(cle,'Déplacement')
                    
                elif(self.transition[5] == 'L'):
                    self.tete2 -= 1
                    #self.getposition(cle,'Déplacement')
                    
                if(self.transition[6] == 'R'):
                    self.tete3 += 1
                    #self.getposition(cle,'Déplacement')
                
                elif(self.transition[6] == 'L'):
                    self.tete3 -= 1
                    #self.getposition(cle,'Déplacement')
    
               
                self.etatCourant = self.transition[0]
                self.label_etat.setText("Etat : "+self.transition[0])
                print(self.tete,self.tete2,self.tete3)
                #self.getposition(cle,'Nouvel Etat')
                
                
            else:
                if (self.mode == "reconnaisseur"):
                    self.label_reponce.setText("n'est pas reconnu")
                    self.label_reponce.setStyleSheet("color: red;")
                print("aucune transition existe")
                # break
        if self.etatCourant in self.etatFinals and self.mode == "reconnaisseur":
            self.label_reponce.setText("reconnu")
            self.label_reponce.setStyleSheet("color: green;")
        time.sleep(1)
            
            
    def creationCellule(self,nom):
        nom.creationObjetQgraphicsText('#',self.tete) #creation d'une nouvelle case si on a arriver a la fin du ruban
    
    
    # autre methode pour l'aide
    def getposition(self,cle,valeur):
        "methode permet de returner la position de la case en cour de traiter"
        
        line=list(self.transitions.keys()).index(cle)
        colone=self.tableTransition.titreTabtransition.index(valeur)
        self.tableTransition.setCurrentCell(line,colone)
        
        #['Etat', 'Lit', 'Ecrit', 'Déplacement', 'Nouvel Etat']
        if valeur==self.tableTransition.titreTabtransition[2]:
         self.label_message.setText(
                "Symbole lit : "+self.cells[self.tete].toPlainText())
        
         
        elif valeur==self.tableTransition.titreTabtransition[3]:
            self.label_message.setText("Symbole ecrit : "+self.transition[1])
           
        elif valeur==self.tableTransition.titreTabtransition[4] and self.transition[2] == 'R':
            self.label_message.setText(
                      "Mouvement de rubant : vers la droite")
        elif self.tableTransition.titreTabtransition[4] and self.transition[2] == 'L':
            self.label_message.setText(
                      "Mouvement de rubant : vers la gauche")
            
        else:
            self.label_message.setText("Etat : "+self.transition[0])
        


app = QApplication(sys.argv)
machine = machineInterface()
machine.show()
app.exec_()
