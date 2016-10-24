import pygame
import os
from datos import*


class Fondo():

    def __init__(self, zona, etapa, screen):
        self.screen = screen
        self.zona = zona
        self.etapa = etapa
        self.image = pygame.image.load(os.path.join(".", "media", "imagenes", "menu", "fondo.jpg"))
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.height = self.screen.get_rect().h
        self.rect = self.image.get_rect()
        self.adaptar(self.height)
        self.sigImage = None
        self.sigRect = None
        self.cambiando = False

        self.menu = pygame.image.load(os.path.join(".", "media", "imagenes", "menu", "fondo.jpg"))
        self.menu = pygame.transform.scale(self.menu, (WIDTH, HEIGHT))

    def update(self):
        if self.cambiando:
            self.screen.blit(self.sigImage, self.sigRect)
            self.rect.centerx -= VELOCIDAD_TRANSICION
            self.sigRect.centerx -= VELOCIDAD_TRANSICION
            if self.sigRect.left <= 0:
                self.finalizarCambio()
                pygame.display.update()
        self.screen.blit(self.image, self.rect)

    def adaptar(self, height):
        self.rect.w = (self.rect.w * height) / self.rect.h
        self.rect.h = height
        self.rect.bottom = height
        self.image = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))

    def cambioEscena(self, zona, etapa):
        self.cambiando = True
        self.zona = zona
        self.etapa = etapa
        self.sigImage = pygame.image.load("./media/imagenes/fondos/" + str(zona) + "-" + str(etapa) + ".JPG")
        self.sigRect = self.sigImage.get_rect()
        self.sigRect.w = (self.sigRect.w * self.height) / self.sigRect.h
        self.sigRect.h = self.height
        self.sigImage = pygame.transform.scale(self.sigImage, (self.sigRect.w, self.sigRect.h))
        self.sigRect.left = self.rect.right

    def menu(self):
        self.image = self.menu

    def finalizarCambio(self):
        self.sigRect.left = 0
        self.image = self.sigImage
        self.rect = pygame.Rect(self.sigRect)
        self.sigImage = None
        self.sigRect = None
        self.cambiando = False
        self.screen.blit(self.image, self.rect)