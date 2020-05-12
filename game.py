import pygame
from pygame import font as pyfont
import sys
import random

class DoodleJump(object):
    def __init__(self):
        pyfont.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.playerRight_1 = pygame.image.load("img/perso/right_1.png").convert_alpha()
        self.playerRight = pygame.image.load("img/perso/right.png").convert_alpha()
        self.playerLeft = pygame.image.load("img/perso/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("img/perso/left_1.png").convert_alpha()
        self.monstersSprite = pygame.image.load("img/monstres/monstres.jfif").convert_alpha()
        self.cameray = 0
        self.playerx = 400
        self.playery = 400
        self.xmovement = 0
        self.jump = 0
        self.direction = 0
        self.gravity = 0
        self.green = pygame.image.load("img/green.png").convert_alpha()
        self.platforms = [[400, 500]]
        self.monsters = [[400, 500]]
        self.font = pygame.font.SysFont("arial", 32)

    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()
        #self.generateMonsters()
        while True:
            self.screen.fill((255, 255, 255))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if self.playery - self.cameray > 700:
                    self.cameray = 0
                    self.platforms = [[400, 500]]
                    self.generatePlatforms()
                    self.playerx = 400
                    self.playery = 400
            self.drawPlatforms()
            #self.drawMonsters()
            self.updatePlatforms()
            #self.updateMonsters()
            self.updatePlayer()
            self.generateScore()
            pygame.display.flip()

    def generateScore(self):
        text = self.font.render(str(-self.cameray/10), 3, (0, 0, 0))
        self.screen.blit(text, (5, 5))

    def drawPlatforms(self):
        for plat in self.platforms:
            regenerate = self.platforms[1][1] - self.cameray
            if regenerate > 600:
                self.platforms.append((random.randint(0, 700), self.platforms[-1][1] - 50))
                self.platforms.pop(0)
            self.screen.blit(self.green, (plat[0], plat[1] - self.cameray))

    def drawMonsters(self):
        for plat in self.monsters:
            regenerate = self.monsters[1][1] - self.cameray
            if regenerate > 600:
                self.monsters.append((random.randint(0, 700), self.monsters[-1][1] - 50))
                self.monsters.pop(0)
            self.screen.blit(self.monstersSprite, (plat[0], plat[1] - self.cameray))

    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10, self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                self.jump = 15
                self.gravity = 0

    def updateMonsters(self):
        for p in self.monsters:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10, self.playerRight.get_height())
            if rect.colliderect(player):
                self.playery = 700
                self.cameray = 0

    def generatePlatforms(self):
            y = 700
            while y > -100:
                x = random.randint(0, 700)
                if self.playerx - x > 100:
                    self.platforms.append((x, y))
                self.platforms.append((x, y))
                y -= 50

    def generateMonsters(self):
        y = -100
        while y > -200:
            x = random.randint(0, 700)
            self.monsters.append((x, y))
            y -= 500

    def updatePlayer(self):
        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
            print(-self.cameray/10)
            self.generateScore()
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0
        elif key[pygame.K_LEFT]:
                if self.xmovement > -10:
                    self.xmovement -= 1
                self.direction = 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if not self.jump:
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1

DoodleJump().run()