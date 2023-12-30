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
            for line in fichierAutomate:
                colonnes = line.strip().split(',')
                key = (colonnes[0],colonnes[1])
                value = (colonnes[2],colonnes[3], colonnes[4])
                self.transitions[key]=value
            '''
            print(self.titre)
            print(self.mode)
            print(self.etatInitial)
            print(self.etatFinals)
            print(self.transitions)
            '''
                      

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
        self.ruban = ''.join('#'*self.tete)+self.instance+''.join('#'*self.tete)
        self.automate = Automate(fichier)
        self.titre = self.automate.getInformations()[0]
        self.transitions = self.automate.getTransitions()
        self.etatInitial = self.automate.etatInitial
        self.etatFinals = self.automate.etatFinals
        self.mode = self.automate.mode


    def afficherIteration(self, i):
        "cette methode permet d'afficher une itération de la machine"
        print(self.ruban)
        print(''.join(' '*i)+'^')
        print("etat courant :" + self.etatCourant)


    def execution(self):
        "execution du programme modèlisé par la machine"
        i = self.tete
        self.etatCourant = self.etatInitial
        while self.etatCourant not in self.etatFinals:
            transition = self.transitions.get((self.etatCourant, self.ruban[i]),None)
            if transition:
                self.ruban = list(self.ruban)
                self.ruban[i] = transition[1]
                
                self.ruban = ''.join(self.ruban)
                self.afficherIteration(i)

                if(transition[2] == 'R'):
                    i = i+1
                elif(transition[2] == 'L'):
                    i = i-1
                
                self.etatCourant = transition[0]
                print("etat suivant : "+self.etatCourant)
                print(20*'-')
                time.sleep(1)

            else:
                if(self.mode == "reconnaisseur"):
                    print("le mot n'est pas reconnu")
                break
        if(self.etatCourant in self.etatFinals and self.mode == "reconnaisseur"):
            print("le mot est reconnu")
        
    def console(self):
        print(10*'-' + self.titre + 10*'-')
        print()
        self.execution()


MachineDeTuring("aNbNcN.txt","bbcc").console()

