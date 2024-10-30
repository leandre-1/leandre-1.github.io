import pygame,pytmx,pyscroll
from dialogue import DialogBox
from player import Guerrier, Magicien, NpcMagicien, NpcGuerrier

TITLE_SIZE = 32
LARGEUR = 30  # largeur du niveau
HAUTEUR = 22  # hauteur du niveau

#Creer la fenetre du jeu
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((LARGEUR * TITLE_SIZE, (HAUTEUR + 3) * TITLE_SIZE))   #Défini la taille de la fenêtre
        pygame.display.set_caption("Dungeon")   #Défini le titre de la fenêtre

        #Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("carte/carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        #Génère un joueur      
        classe = input("Veuillez choisir votre classe Guerrier ou Magicien : ")
        if classe == "Guerrier":
            self.player = Guerrier(706, 199, "sprites/chevalier_d.png", 'Chevalier', 1, 10, 0, 1)
        elif classe == "Magicien":
            self.player = Magicien(706, 199, "sprites/chevalier_d.png", 'Magicien', 5, 10, 0, 1)
        else:
            print("Classe inconnue, choix par défaut : Guerrier")
            self.player = Guerrier(706, 199, "sprites/chevalier_d.png", 'Chevalier', 1, 10, 0, 1,)
        
        #Generer les NPC
        self.npc = NpcGuerrier(179, 145, "sprites/chevalier_ennemi_d.png", 'Bouliste', 1, 10, 0, 1, ["Bouuliste !", "Boboy"])
        self.npc_2 = NpcGuerrier(643, 550, "sprites/chevalier_ennemi_d.png", 'Le Laitier', 1, 10, 0, 1, ["Je suis le laitier", "Mon lait est délicieux"])
        self.npc_3 = NpcMagicien(223, 410, "sprites/petit_gandalf.png", 'Gandalf', 5, 10, 0, 1,["Vous ne passerez pas !", "Fuyez, pauvres fous !"])
        self.npc_4 = NpcMagicien(863, 550, "sprites/magicien_d.png", 'Magicien', 5, 10, 0, 1,["", ""])

        self.dialog_box = DialogBox(self.screen, pygame.font.Font(None, 24))    #Défini la boite de dialogue

        #definir une liste qui stocke les collisions
        self.walls = []

        for obj in tmx_data.objects:    
            if obj.type == 'collision':     #Si l'objet est un mur
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height,))    #Ajoute le mur à la liste des collisions

        # Dessiner le grp de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)   #Défini le calque de la carte
        self.group.add(self.player) # Ajoute player
        self.group.add(self.npc)    # Ajoute NPC 
        self.group.add(self.npc_2)  
        self.group.add(self.npc_3)
        self.group.add(self.npc_4)
            
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        # Seul player réagit aux touches car c'est le seul concerné par la fonction handle_input
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
            if sprite.feet.collidelist(self.walls) > -1:    #Si le joueur touche un mur
                sprite.move_back()  

    def check_npc_collision(self, dialog_box):
        if self.player.feet.colliderect(self.npc.rect):
            dialog_box.start_reading(self.npc.dialog, self.npc.nom)
        elif self.player.feet.colliderect(self.npc_2.rect):
            dialog_box.start_reading(self.npc_2.dialog, self.npc_2.nom)
        elif self.player.feet.colliderect(self.npc_3.rect):
            dialog_box.start_reading(self.npc_3.dialog, self.npc_3.nom)
        elif self.player.feet.colliderect(self.npc_4.rect):
            dialog_box.start_reading(self.npc_4.dialog, self.npc_4.nom)

    #Boucle de jeu
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.draw(self.screen)
            self.dialog_box.render(self.screen)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.check_npc_collision(self.dialog_box)
            
            clock.tick(60)

        pygame.quit()