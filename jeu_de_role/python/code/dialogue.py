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

    def start_reading(self, dialog):  #Démarre la lecture de la boite de dialogue
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog

    def render (self, screen):  #Défini la boite de dialogue
        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):   #Si la lettre actuelle dé passe le nb de lettre dans le texte courant
                self.letter_index = self.letter_index

            screen.blit(self.box, (130, 704))   #Défini la position de la boite de dialogue
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))   #Défini la couleur du texte
            screen.blit(text, (175, 740))   #Défini la position du texte
    
    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            self.reading = False    #Arrête la lecture de la boite de dialogue