import pygame, random

class Personnage(pygame.sprite.Sprite):

    def __init__(self, x, y,img,nom,vie,xp,niveau):
        super().__init__()
        self.image=pygame.image.load(img)
        self.rect=self.image.get_rect()
        self.position= [x,y]
        self.nom=nom
        self.vie=vie
        self.maxVie=vie
        self.xp=xp
        self.niveau=niveau
        self.images = {
            'left': pygame.image.load('sprites/chevalier_g.png'),
            'right': pygame.image.load('sprites/chevalier_d.png')          
        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 10)
        self.old_position = self.position.copy()
        self.speed = 4

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, direction):
        self.image = self.images[direction]

    def move_right(self):
        self.position[0] += self.speed
    
    def move_left(self):
        self.position[0] -= self.speed
    
    def move_up(self):
        self.position[1] -= self.speed
    
    def move_down(self):
        self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def ajouterVie(self,vie):
        self.vie+=vie   #ajoute de la vie dans self.vie sans dépasser self.maxVie
        if self.vie>self.maxVie:
            self.vie=self.maxVie

    def retirerVie(self,vie):
        self.vie-=vie   #retire de la vie dans self.vie sans être inférieur à 0
        if self.vie-vie<=0:
            self.vie = self.estMort()

    def monterExperience(self):
        self.xp+=4          #ajoute 4 points d’expérience
        if  self.xp >=10:   #augmente d’un niveau tous les 10 xp
            self.niveau+=1
            self.xp-=10
            print (f"Tu monte au niveau {self.niveau}")

    def estVivant(self):
        if self.vie > 0:    #retourne vrai si le personnage est vivant
            return True

    def estMort(self):
        if self.vie <= 0:   #retourne vrai si le personnage est mort
            return False

class Guerrier(Personnage):
    def __init__(self, x, y, img, nom, force, vie, xp, niveau):
        super().__init__(x, y,img,nom,vie,xp,niveau)
        self.force=force

    def augmenterForce(self):
        self.force+=1    #augmente de 1 la force du guerrier

    def combat(self, adversaire):
        if adversaire.estVivant():     #inflige des dégats à l'ennemi si celui-ci est vivant
            attaque=random.randint(1, 4)
            degats=attaque*self.niveau*self.force-adversaire.niveau
            adversaire.retirerVie(degats)       #retire de la vie à l'ennemi
            print(f"Tu as infligé {degats} de dégats à {adversaire.nom}")
        if adversaire.vie <= 0:
            print(f"{adversaire.nom} est mort")
            self.augmenterForce()       #augmente la force du guerrier si l'ennemi est mort
            self.monterExperience()     #augmente l'expérience du guerrier si l'ennemi est mort
                                        #monte si nécessaire en niveau en fonction du nombre de points xp

class Magicien(Personnage):
    def __init__(self, x, y, img, nom, mana, vie, xp, niveau):
        super().__init__(x, y,img,nom,vie,xp,niveau)
        self.maxMana=mana
        self.mana=mana

    def augmenterMana(self):
        self.maxMana+=10      #augmente de 10 le maxMana du magicien

    def ajouterMana(self):
        if self.mana+5<=self.maxMana:
            self.mana+=5      #ajoute 5 en self.mana sans dépasser self.maxMana

    def retirerMana(self, mana, adversaire):
        if self.mana-mana>=0:    #retire mana à self.mana sans descendre en dessous de 0
            self.mana-=mana
            print(f"Tu as lancé un sort sur {adversaire.nom}")
            return True     #retourne vrai si le magicien à lancé un sort
        else:
            print("Tu ne peut plus lancer de sort")
            return False     #retourne faux si le magicien ne peut plus lancer de sort

    def combat(self, adversaire):
        if adversaire.estVivant() and self.mana>0:  #inflige des dégats à l'ennemi si celui-ci est vivant et que le magicien dispose de mana
            attaque=random.randint(1, 4)
            degats=attaque*self.niveau*2-adversaire.niveau
            adversaire.retirerVie(degats)   #retire de la vie à l'ennemi
            self.retirerMana(1)             #retire de la vie au méchant et diminue de 1 self.mana (consommation de magie)
            print(f"Tu as infligé {degats} de dégats à {adversaire.nom}")
        
        if adversaire.estMort():
            print(f"{adversaire.nom} est mort")
            self.monterExperience()     #augmente l'expérience du guerrier si l'ennemi est mort
            self.augmenterMana()        #si l'ennemi est mort augmenter self.maxMana de 10 du magicien
            self.ajouterMana()

class NpcMagicien(Magicien):
    def __init__(self, x, y, img, nom, mana, vie, xp, niveau, dialog):
        super().__init__(x, y,img,nom,mana,vie,xp,niveau)
        self.dialog=dialog

class NpcGuerrier(Guerrier):
    def __init__(self, x, y, img, nom, force, vie, xp, niveau, dialog):
        super().__init__(x, y,img,nom,force,vie,xp,niveau)
        self.dialog=dialog