import pygame

class DialogBox:

    def __init__(self, screen, font):  #Initialise la boite de dialogue
        self.box = pygame.image.load('dialogue/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 96))  #Défini la dimension de la boite de dialogue
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font('dialogue/Blender-Pro-Bold.ttf', 23)    #Défini la police de la boite de dialogue
        self.reading = False

    def start_reading(self, dialog, nom):  #Démarre la lecture de la boite de dialogue
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog
            self.npc_name = nom

    def render (self, screen):  #Défini la boite de dialogue
        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):   #Si la lettre actuelle dépasse le nb de lettre dans le texte courant
                self.letter_index = self.letter_index    #La lettre actuelle est égale a la dernière lettre

            screen.blit(self.box, (130, 704))   #Défini la position de la boite de dialogue

            npc_name = self.font.render(self.npc_name, False, (0, 0, 0))
            screen.blit(npc_name, (175, 720))  # Ajuste la position pour qu'elle soit au-dessus du texte
            
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))   #Défini la couleur du texte
            screen.blit(text, (175, 750))   #Défini la position du texte
    
    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            self.reading = False    #Arrête la lecture de la boite de dialogue