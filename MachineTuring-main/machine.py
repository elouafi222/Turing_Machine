import time


class TableTransition:
    "transformation du programme ecrit dans un fichier sur un dictionnaire"

    def __init__(self, fichier):
        self.prog = {}
        fichierPro = open(fichier, 'r')
        self.titre = fichierPro.readline()
        self.mode = (fichierPro.readline()).split(":")[1]
        etat = fichierPro.readline()
        while 1:
            line = fichierPro.readline()
            if line == "":
                break
            line1 = line.split(',')
            self.prog[(line1[0], line1[1])] = (line1[2], line1[3], line1[4])
        fichierPro.close()
        self.etatInitial = etat.split()[0]
        self.etatFinal = etat.split()[1]

    def get_programme(self):
        "cette methode return la table de trasition sous la forme d'un dictionaire"
        return self.prog

    def get_information(self):
        "cette methode return le nom du programme a faire plus l'etat initiale et l'etat finale et le mode d'utilisation de la machine(accepteur/calculateur) sou la forme d'une liste "
        return [self.titre, self.etatInitial, self.etatFinal, self.mode]


class machineTuring:
    def __init__(self, programme, probleme, etaInital, etaFinal, modeDutilisation, N=100):
        "initialisation de la machine avec le probleme et le progrmme"
        self.tete = N//2
        self.prob = probleme
        self.bande = ''.join('#'*self.tete)+self.prob+''.join('#'*self.tete)
        self.prog = programme
        self.etaIn = etaInital
        self.etaFin = etaFinal
        self.etatCourant = self.etaIn
        self.modeDutilisation = modeDutilisation

    def afficherInstruction(self, i):
        "cette methode permet d'afficher une configuration de la machine"
        print(self.bande)
        print(''.join(' '*i)+'^')
        print("etat courant :" + self.etatCourant)

    def execution(self):
        "execution du programme sur la machine "
        i = self.tete
        while self.etatCourant != self.etaFin:
           # print(self.prog[(self.etatCourant, self.bande[i])])
            if self.prog.__contains__((self.etatCourant, self.bande[i])) == True:
                self.bande = list(self.bande)
                val1 = self.bande[i]
                self.bande[i] = self.prog[(self.etatCourant, self.bande[i])][1]
                self.bande = ''.join(self.bande)
                self.afficherInstruction(i)
                if(self.prog[(self.etatCourant, val1)][2] == 'R'):
                    i = i+1
                elif(self.prog[(self.etatCourant, val1)][2] == 'L'):
                    i = i-1
                self.etatCourant = self.prog[(self.etatCourant, val1)][0]
                print("etat suivant : "+self.etatCourant)
                print("-------------------------------------------")
                time.sleep(1)

            else:
                if(self.modeDutilisation == "accepteur"):
                    print("le mot n'est pas roconnue")
                break
        if(self.etatCourant == self.etaFin and self.modeDutilisation == "accepteur"):
            print("le mot est rocconue")


class machineTuringRun:
    "l'execution de programme sur la machine de turing"

    def __init__(self, fichier, probleme):
        tab = TableTransition(fichier)
        self.probleme = probleme
        self.programme = tab.get_programme()
        self.titre = tab.get_information()[0]
        self.etaIital = tab.get_information()[1]
        self.etaFinal = tab.get_information()[2]
        self.mode = tab.get_information()[3]

    def execution(self):
        print('------------------------- ' + self.titre + '------------')
        print()
        mt = machineTuring(self.programme, self.probleme,
                           self.etaIital, self.etaFinal, self.mode)
        mt.execution()


mt = machineTuringRun('lesProgrammes\\aNbN.txt', 'aaaabbbb')
mt.execution()
