import pygame,pytmx,random

# Constantes
TITLE_SIZE = 32
LARGEUR = 30  # largeur du niveau
HAUTEUR = 20  # hauteur du niveau
clock = pygame.time.Clock()

# Charger la carte à partir d'un fichier .tmx
def chargerCarteTiled(fichier):
    tmx_data = pytmx.util_pygame.load_pygame(fichier)
    return tmx_data

# Afficher la carte
def afficherCarteTiled(fenetre, tmx_data):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    fenetre.blit(tile, (x * TITLE_SIZE, y * TITLE_SIZE))

# Charger les données de collision
def chargerCollisionsTiled(tmx_data):
    collisions = []
    for y in range(tmx_data.height):
        collisions.append([0] * tmx_data.width)
    for obj in tmx_data.objects:
        if obj.name == "collision":
            for x in range(int(obj.x // TITLE_SIZE), int((obj.x + obj.width) // TITLE_SIZE)):
                for y in range(int(obj.y // TITLE_SIZE), int((obj.y + obj.height) // TITLE_SIZE)):
                    collisions[y][x] = 1
    return collisions


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
        self.testCollisionsDecor(1,0)
        self.rect.x=self.x*self.size

    def gauche(self):
        self.testCollisionsDecor(-1,0)
        self.rect.x=self.x*self.size

    def haut(self):
        self.testCollisionsDecor(0,-1)
        self.rect.y=self.y*self.size

    def bas(self):
        self.testCollisionsDecor(0,1)
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
    def __init__(self, position, size, img, collisions, nom, force, vie, xp, niveau):
        super().__init__(position, size, img, collisions, nom, vie, xp, niveau)
        self.force=force

    def augmenterForce(self):
        self.force+=1     #augmente de 1 la force du guerrier

    def combat(self, adversaire):
        if adversaire.estVivant():      #inflige des dégats à l'ennemi si celui-ci est vivant
            attaque=random.randint(1, 4)
            degats=attaque*self.niveau*self.force-adversaire.niveau
            adversaire.retirerVie(degats)       #retire de la vie à l'ennemi
            print("Dégâts du guerrier sur l'ennemi : ", degats)
        if adversaire.vie <= 0:
            print("L'ennemi est mort")
            self.augmenterForce()       #augmente la force du guerrier si l'ennemi est mort
            self.monterExperience()     #augmente l'expérience du guerrier si l'ennemi est mort
                                        #Monte si nécessaire en niveau en fonction du nombre de points xp

class Magicien(Personnage):
    def __init__(self, position, size, img, collisions, nom, mana, vie, xp, niveau):
        super().__init__(position, size, img, collisions, nom, vie, xp, niveau)
        self.maxMana=mana
        self.mana=mana

    def augmenterMana(self):
        self.maxMana+=10      #augmente de 10 le maxMana du magicien

    def ajouterMana(self):
        if self.mana+5<=self.maxMana:
            self.mana+=5      #ajoute 5 en self.mana sans dépasser self.maxMana

    def retirerMana(self, mana):
        if self.mana-mana>=0:    #retire mana à self.mana sans descendre en dessous de 0
            self.mana-=mana
            print("Le magicien a lancé un sort")
            return True     #retourne vrai si le magicien à lancé un sort
        else:
            print("Le magicien ne peut plus lancer de sort")
            return False     #retourne faux si le magicien ne peut plus lancer de sort

    def combat(self, adversaire):
        if adversaire.estVivant() and self.mana>0:  #inflige des dégats à l'ennemi si celui-ci est vivant et que le magicien dispose de mana
            attaque = random.randint(1, 4)
            degats = attaque*self.niveau*2-adversaire.niveau
            adversaire.retirerVie(degats)   #retire de la vie à l'ennemi
            self.retirerMana(1)             #retire de la vie au méchant et diminue de 1 self.mana (consommation de magie)
            print("Dégâts du magicien sur l'ennemi : ", degats)
        
        if adversaire.estMort():
            print("L'ennemi est mort")
            self.monterExperience()     #augmente l'expérience du guerrier si l'ennemi est mort
            self.augmenterMana()        #si l'ennemi est mort augmenter self.maxMana de 10 du magicien
            self.ajouterMana()

# Initialisation de Pygame
pygame.init()
fenetre = pygame.display.set_mode((LARGEUR * TITLE_SIZE, (HAUTEUR + 1) * TITLE_SIZE))
pygame.display.set_caption("Dungeon")

# Charger la carte depuis Tiled
tmx_data = chargerCarteTiled('C:/Users/leandre.temperault/OneDrive/Documents/leandre-1.github.io/jeu_de_role/carte.tmx')

# Charger les collisions
collisions = chargerCollisionsTiled(tmx_data)

# Création des personnages
chevalier = Guerrier([1, 1], TITLE_SIZE, "C:/Users/leandre.temperault/OneDrive/Documents/leandre-1.github.io/jeu_de_role/role/data/chevalier_d.png", collisions, 'Chevalier', 1, 10, 0, 1)
chevalier_ennemi = Guerrier([4, 8], TITLE_SIZE, "C:/Users/leandre.temperault/OneDrive/Documents/leandre-1.github.io/jeu_de_role/role/data/chevalier_ennemi_d.png", collisions, 'Chevalier ennemi', 1, 10, 0, 1)
magicien = Magicien([4, 10], TITLE_SIZE, "C:/Users/leandre.temperault/OneDrive/Documents/leandre-1.github.io/jeu_de_role/role/data/magicien_d.png", collisions, 'Magicien', 5, 10, 0, 1)

aventuriers = pygame.sprite.Group(chevalier, magicien)
mechants = pygame.sprite.Group(chevalier_ennemi)


"""
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
"""   

loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                chevalier.haut()
            elif event.key == pygame.K_s:
                chevalier.bas()
            elif event.key == pygame.K_d:
                chevalier.droite()
            elif event.key == pygame.K_q:
                chevalier.gauche()
            elif event.key == pygame.K_ESCAPE:
                loop = False

    # Vérification de la collision
    if pygame.sprite.collide_rect(chevalier, chevalier_ennemi):
        print("Collision avec un ennemi !")
        mechants.remove(chevalier_ennemi)

    # Mise à jour de l'affichage
    fenetre.fill((0, 0, 0))  # Effacer l'écran
    afficherCarteTiled(fenetre, tmx_data)  # Afficher le niveau
    aventuriers.update()
    aventuriers.draw(fenetre)
    mechants.update()
    mechants.draw(fenetre)   
    pygame.display.flip()
    clock.tick(60)
pygame.quit()