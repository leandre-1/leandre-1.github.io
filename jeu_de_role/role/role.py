"""
Programme réalisé par nom, prénom, classe
"""
import pygame,random

#variables du niveau
NB_TILES = 666   #nombre de tiles a chager (ici de 00.png à 26.png) 27 au total !!
TITLE_SIZE=32   #definition du dessin (carré)
largeur=10       #hauteur du niveau
hauteur=8       #largeur du niveau
tiles=[]       #liste d'images tiles
clock = pygame.time.Clock()


#definition du niveau

niveau=[[486,531, 24, 24, 24, 24, 24, 24, 24, 25],
        [486,605,189,189,171, 47, 47, 47, 47, 48],
        [486,531, 47, 47,187, 47, 47, 47, 47, 48],
        [486,531, 47,118,217,120, 47, 47, 47, 48],
        [486,541, 47,141,142,143, 47, 47, 47, 48],
        [486,545, 47,164,165,166, 47, 47, 47, 48],
        [486,489,507,507,507,507,507,507,507,508],
        [486,486,486,486,486,486,486,486,486,531]]

decor=[[  0,  0,  0,  0,140,  0,  0,  0,  0,  0],
       [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
       [  0,  0,184,  0,  0,138,  0,278,279,  0],
       [  0,  0,  0,  0,  0,  0,  0,276,277,  0],
       [  0,  0,  0,  0,  0,  0,  0,299,300,  0],
       [  0,  0,186,  0,  0,  0,  0,  0,  0,  0],
       [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
       [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]


collisions=[[ 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [ 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]



class Personnage(pygame.sprite.Sprite):

    def __init__(self,position,size,img,collisions,nom,vie,xp,niveau):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.size=size
        self.collisions=collisions
        self.x,self.y=position
        self.rect.x=self.x*size
        self.rect.y=self.y*size
        self.nom=nom
        self.vie=vie
        self.maxVie=vie
        self.xp=xp
        self.niveau=niveau

    def testCollisionsDecor(self,x,y):
        if (self.collisions[int(self.y+y)][int(self.x+x)]==0):
            self.x+=x
            self.y+=y

    def droite(self):
        self.testCollisionsDecor(0.1,0)
        self.rect.x=self.x*self.size

    def gauche(self):
        self.testCollisionsDecor(-0.1,0)
        self.rect.x=self.x*self.size

    def haut(self):
        self.testCollisionsDecor(0,-0.1)
        self.rect.y=self.y*self.size

    def bas(self):
        self.testCollisionsDecor(0,0.1)
        self.rect.y=self.y*self.size

    def ajouterVie(self,vie):
        #ajoute de la vie dans self.vie sans dépasser self.maxVie
        self.vie+=vie
        if self.vie>self.maxVie:
            self.vie=self.maxVie

    def retirerVie(self,vie):
        #retire de la vie dans self.vie sans être inférieur à 0
        self.vie-=vie
        if self.vie-vie<=0:
            self.vie = self.estMort()

    def monterExperience(self):
        #ajoute 4 points d’expérience
        #Augmente d’un niveau tous les 10 xp
        #Exemple 30xp = niveau 3
        self.xp+=4
        if  self.xp >=10:
            self.niveau+=1
            self.xp-=10

    def estVivant(self):
        #retourne vrai si le personnage est vivant
        if self.vie > 0:
            return True

    def estMort(self):
        #retourne vrai si le personnage est mort
        if self.vie <= 0:
            return False


class Guerrier(Personnage):
    def __init__(self,position,size,img,collisions,nom,force,vie,xp,niveau):
        super().__init__(position,size,img,collisions,nom,vie,xp,niveau)
        self.force=force
    
    def augmenterForce(self):
        self.force+=1   #augmente de 1 la force du guerrier
    
    def combat(self,adversaire):
        if adversaire.estVivant():     #inflige des dégats à l'ennemi si celui-ci est vivant
            attaque=random.randint(1, 4)
            degats=attaque*self.niveau*self.force-adversaire.niveau
            adversaire.retirerVie(degats)        #retire de la vie à l'ennemi
            print("Dégats du guerrier sur l'ennemi : ",degats)
        if adversaire.estMort():
            print("L'ennemi mort")
            self.augmenterForce()        #augmente la force du guerrier si l'ennemi est mort
            self.monterExperience()      #augmente l'expérience du guerrier si l'ennemi est mort
                                         #Monte si nécessaire en niveau en fonction du nombre de points xp
                    
           
class Magicien(Personnage):
    def __init__(self,position,size,img,collisions,nom,mana,vie,xp,niveau):
        super().__init__(position,size,img,collisions,nom,vie,xp,niveau)
        self.maxMana=mana
        self.mana=mana
    
    def augmenterMana(self): 
        self.maxMana+=10    #augmente de 10 le maxMana du magicien
    
    def ajouterMana(self):
        if self.mana+5<=self.maxMana:
            self.mana+=5    #ajoute 5 en self.mana sans dépasser self.maxMana
    
    def retirerMana(self,mana):
        if self.mana-mana>=0:   #retire mana à self.mana sans descendre en dessous de 0
            self.mana-=mana
            print("Le magicien a lancé un sort")
            return True     #retourne vrai si le magicien à lancé un sort
        else:
            print("Le magicien ne peut plus lancer de sort")    #retourne faux si le magicien ne peut plus lancer de sort
            return False
        
    def combat(self,adversaire):
        if adversaire.estVivant() and self.mana>0:     #inflige des dégats à l'ennemi si celui-ci est vivant et que le magicien dispose de mana
            attaque=random.randint(1, 4)
            degats=attaque*self.niveau*2-adversaire.niveau
            adversaire.retirerVie(degats)        #retire de la vie à l'ennemi
            self.retirerMana(1)                  #retire de la vie au méchant et diminue de 1 self.mana (consommation de magie)
            print("Dégat du magicien sur l'ennemi'",degats)
            
        if adversaire.estMort():
            print("L'ennemi mort")       
            self.monterExperience()     #augmente l'expérience du guerrier si l'ennemi est mort
            self.augmenterMana()        #si l'ennemi est mort augmenter self.maxMana de 10 du magicien
            self.ajouterMana()      


#la taille de la fenetre dépend de la largeur et de la hauteur du niveau
#on rajoute une rangée de 32 pixels en bas de la fentre pour afficher le score d'ou (hauteur +1)
pygame.init()
fenetre = pygame.display.set_mode((largeur*TITLE_SIZE, (hauteur+1)*TITLE_SIZE))
pygame.display.set_caption("Dungeon")
font = pygame.font.Font('freesansbold.ttf', 20)



def chargetiles(tiles):
    """
    fonction permettant de charger les images tiles dans une liste tiles[]
    """
    for n in range(0,NB_TILES):
        #print('data/'+str(n)+'.png')
        tiles.append(pygame.image.load('C:/Users/leandre.temperault/OneDrive/Documents/leandre-1.github.io/jeu_de_role/role/data/'+str(n)+'.png')) #attention au chemin


def afficheNiveau(niveau):
    """
    affiche le niveau a partir de la liste a deux dimensions niveau[][]
    """
    for y in range(hauteur):
        for x in range(largeur):
            fenetre.blit(tiles[niveau[y][x]],(x*TITLE_SIZE,y*TITLE_SIZE))
            if (decor[y][x]>0):
                fenetre.blit(tiles[decor[y][x]],(x*TITLE_SIZE,y*TITLE_SIZE))



def afficheScore(score):
    #affiche le score en bas de la fenetre   
    scoreAafficher = font.render(str(score), True, (255, 255, 255))
    fenetre.blit(scoreAafficher,(120,250))



fenetre.fill((0,0,0))   #efface la fenetre
chargetiles(tiles)  #chargement des images


chevalier = Guerrier([1,1],TITLE_SIZE,"C:/Users/leandre.temperault/OneDrive/Documents/leandre-1.github.io/jeu_de_role/role/data/chevalier_d.png",collisions,'Chevalier',1,10,0,1)
chevalier_ennemi = Guerrier([4,3],TITLE_SIZE,"C:/Users/leandre.temperault/OneDrive/Documents/leandre-1.github.io/jeu_de_role/role/data/chevalier_ennemi_d.png",collisions,'Chevalier ennemi',1,10,0,1)
magicien = Magicien([4,5],TITLE_SIZE,"C:/Users/leandre.temperault/OneDrive/Documents/leandre-1.github.io/jeu_de_role/role/data/magicien_d.png",collisions,'Magicien',5,10,0,1)

aventuriers = pygame.sprite.Group()
aventuriers.add(chevalier)
aventuriers.add(magicien)

mechants = pygame.sprite.Group()
mechants.add(chevalier_ennemi)



loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # fermeture de la fenêtre (croix rouge)
            loop = False
    keys = pygame.key.get_pressed() # Récupère l'état des touches pressées
    if keys[pygame.K_z]:    #est-ce la touche HAUT
        chevalier.haut()
    if keys[pygame.K_s]:    #est-ce la touche BAS
        chevalier.bas()
    if keys[pygame.K_d]:    #est-ce la touche DROITE
        chevalier.droite()
    if keys[pygame.K_q]:    #est-ce la touche GAUCHE
        chevalier.gauche()   
    if keys[pygame.K_ESCAPE]:   #touche échap pour quitter
        loop = False
    

    col = pygame.sprite.collide_rect(chevalier, chevalier_ennemi)
    if col==1:
        print("collision",col)
        mechants.remove(chevalier_ennemi)


    fenetre.fill((0,0,0))
    afficheNiveau(niveau)   #affiche le niveau
    aventuriers.update()
    aventuriers.draw(fenetre)
    mechants.update()
    mechants.draw(fenetre)
    pygame.display.update() #mets à jour la fentre graphique
    pygame.display.flip()
    clock.tick(60)
pygame.quit()