import time


class Automate:
    "transformation du transitionsramme ecrit dans un fichier sur un dictionnaire"

    def __init__(self, fichier):
        
        with open(fichier) as fichierAutomate:
            self.titre = fichierAutomate.readline().strip()
            self.mode = fichierAutomate.readline().strip()
            self.etatInitial = fichierAutomate.readline().strip()
            self.etatFinals = fichierAutomate.readline().strip().split(',')
            self.transitions = {}
            if fichier.find("tourhai.txt")==-1:
              for line in fichierAutomate:
                 colonnes = line.strip().split(',')
                 key = (colonnes[0], colonnes[1])
                 value = (colonnes[2], colonnes[3], colonnes[4])
                 self.transitions[key] = value
            else:
              for line in fichierAutomate:
                 colonnes = line.strip().split(',')
                 key = (colonnes[0], colonnes[1], colonnes[2], colonnes[3])
                 value = (colonnes[4], colonnes[5], colonnes[6], colonnes[7], colonnes[8], colonnes[9], colonnes[10])
                 self.transitions[key] = value
              print(self.transitions)

    def getTransitions(self):
        "cette methode return la table de trasition sous la forme d'un dictionaire"
        return self.transitions

    def getInformations(self):
        "cette methode return le nom du transitionsramme a faire plus l'etat initiale et l'etat finale et le mode d'utilisation de la machine(reconnaisseur/calculateur) sou la forme d'une liste "
        return [self.titre, self.etatInitial, self.etatFinals, self.mode]


class MachineDeTuring:
    def __init__(self, fichier, instance, N=100):
        "initialisation de la machine avec le programme et l'instance'"
        self.tete = N//2
        self.instance = instance
        self.ruban = ''.join('#'*self.tete)+self.instance + \
            ''.join('#'*self.tete)
        self.automate = Automate(fichier)
        self.titre = self.automate.getInformations()[0]
        self.transitions = self.automate.getTransitions()
        self.etatInitial = self.automate.etatInitial
        self.etatFinals = self.automate.etatFinals
        self.mode = self.automate.mode

    def afficherIteration(self, i):
        "cette methode permet d'afficher et modifier une itération de la machine"
        print(self.ruban)
        print(''.join(' '*i)+'^')
        print("etat courant :" + self.etatCourant)

    def executionInstruction(self, i, transition):
        "cette methode permet d'executer une instruction"
        self.ruban = list(self.ruban)
        self.ruban[i] = transition[1]
        self.ruban = ''.join(self.ruban)
        # self.afficherIteration(i)

        if(transition[2] == 'R'):
            i = i+1
        elif(transition[2] == 'L'):
            i = i-1
        self.etatCourant = transition[0]
        return self.ruban, i

    def execution(self):
        "execution du programme modèlisé par la machine"
        i = self.tete
        self.etatCourant = self.etatInitial
        while self.etatCourant not in self.etatFinals:
            transition = self.transitions.get(
                (self.etatCourant, self.ruban[i]), None)
            if transition:
                val, i = self.executionInstruction(i, transition)
                print(val)

            else:
                if (self.mode == "reconnaisseur"):
                    print("le mot n'est pas reconnu")
                break
            time.sleep(1)

        if(self.etatCourant in self.etatFinals and self.mode == "reconnaisseur"):
            print("le mot est reconnu")

    def console(self):
        print(10*'-' + self.titre + 10*'-')
        self.execution()


"""
MachineDeTuring(
    "C:\\Users\\mohamed\\OneDrive\\Bureau\\mes-projet2\\machine_turing\\gitMachine\\MachineTuring\\aNbN.txt", "aabb").console()

                  print("etat suivant : "+self.etatCourant)
                  print(20*'-')
                  time.sleep(1)

                   transition = self.transitions.get(
            (self.etatCourant, self.ruban[i]), None)
        if transition:
        
         else:
            if(self.mode == "reconnaisseur"):
                print("le mot n'est pas reconnu")
            break
"""
"""
def execution(self):
    "methode d'execution de la machine de Turing"
    position = 0
    while self.etatCourant not in self.etatFinals and position < self.tailleRuban:
        symbol = self.listeItemsText[position].toPlainText()
        if (self.etatCourant, symbol) not in self.transitions:
            QMessageBox.warning(
                self, "information", "transition non definie pour l'etat courant et le symbole actuel.")
            return
        transition = self.transitions[(self.etatCourant, symbol)]
        self.etatCourant = transition[0]
        self.listeItemsText[position].setPlainText(transition[1])
        self.triangle.setPos(
            500 + 62*position + 30, 555)  # déplacer le triangle à la position actuelle
        if transition[2] == 'D':
            position += 1
        else:
            position -= 1
        self.update()  # mettre à jour la vue

    if self.etatCourant in self.etatFinals:
        QMessageBox.information(self, "information", "La machine est arrivée dans un état final.")
    else:
        QMessageBox.information(self, "information", "La machine a dépassé la limite du ruban.")
 
"""
