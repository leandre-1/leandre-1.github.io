import pygame,pytmx,pyscroll
from player import Guerrier, Magicien

TITLE_SIZE = 32
LARGEUR = 30  # largeur du niveau
HAUTEUR = 22  # hauteur du niveau

#Creer la fenetre du jeu
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((LARGEUR * TITLE_SIZE, (HAUTEUR + 2) * TITLE_SIZE))
        pygame.display.set_caption("Dungeon")

        #Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("map/carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        #generer un joueur
        classe = input("Veuillez choisir votre classe Guerrier ou Magicien : ")
        if classe == "Guerrier":
            self.player = Guerrier(706, 199, "sprites/chevalier_d.png", 'Chevalier', 1, 10, 0, 1)
        elif classe == "Magicien":
            self.player = Magicien(706, 199, "sprites/chevalier_d.png", 'Magicien', 5, 10, 0, 1)
        else:
            print("Classe inconnue, choix par défaut : Guerrier")
            self.player = Guerrier(706, 199, "sprites/chevalier_d.png", 'Chevalier', 1, 10, 0, 1)
        self.npc = Guerrier(179, 145, "sprites/chevalier_ennemi_d.png", 'Chevalier ennemi', 1, 10, 0, 1)
        self.npc_2 = Guerrier(643, 550, "sprites/chevalier_ennemi_d.png", 'Chevalier ennemi', 1, 10, 0, 1)
        self.npc_3 = Magicien(223, 410, "sprites/magicien_d.png", 'Magicien', 5, 10, 0, 1)
        self.npc_4 = Magicien(863, 550, "sprites/magicien_d.png", 'Magicien', 5, 10, 0, 1)

        #definir une liste qui stocke les collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height,))

        # Dessiner le grp de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player) # Ajoute Player 1
        self.group.add(self.npc)    # Ajoute NPC 
        self.group.add(self.npc_2)  
        self.group.add(self.npc_3)
        self.group.add(self.npc_4)
            
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        # Seul Player 1 réagit aux touches car c'est le seul concerné par la fonction handle_input
        if pressed[pygame.K_z]:
            self.player.move_up()
        elif pressed[pygame.K_s]:
            self.player.move_down()
        elif pressed[pygame.K_q]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_d]:
            self.player.move_right()
            self.player.change_animation('right')
    
    def update(self):
        self.group.update()
        #vérification de la collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    #Boucle de jeu
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.draw(self.screen)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            clock.tick(60)

        pygame.quit()