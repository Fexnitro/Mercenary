import pygame
import sys
from pygame.locals import*
from datos import*
from clases import*


class Mercenary:
    pygame.mixer.pre_init(22050, -16, 2, 64)
    pygame.mixer.init()
    pygame.init()
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    def __init__(self):
        self.collisionManager = CollisionManager()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        self.fondo = Fondo(self.screen)
        self.sonidos = CajaSonidos()
        self.gameState = GameState(self.fondo)
        self.musica = CajaMusica()

        self.presentar()

        self.musica.taberna()
        self.jugador = pygame.sprite.GroupSingle()
        self.enemigos = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.proyectiles = pygame.sprite.Group()

        self.items = pygame.sprite.Group()
        self.personaje = Sprite("jugador", "swordman", False)
        self.personaje.posicionar(WIDTH / 2, HEIGHT / 2)

        self.enemySpawner = EnemySpawner(self.gameState, self.enemigos, DIFICULTAD, self.personaje)
        self.itemSpawner = ItemSpawner(self.items, DIFICULTAD)
        self.jugador.add(self.personaje)

        self.menu = MenuPrincipal(self.personaje)
        self.hud = Hud(self.jugador, self.enemigos, self.gameState)

    def keyHandler(self, event):
        if event.type == KEYDOWN:
            key = pygame.key.name(event.key)
            if key == "q":
                pygame.quit()
                sys.exit()
            if key == "z":
                self.personaje.saltar()
            if key == "t":
                self.itemSpawner.spawn()
            if key == "left":
                self.personaje.correr("left")
            if key == "right":
                self.personaje.correr("right")
            if key == "p":
                self.gameState.pausar()
            if key == "r" and self.gameState.estado == "gameover":  # REINICIAR
                self.gameState.reiniciarEtapa()
                self.enemySpawner.reiniciar()
                self.itemSpawner.reiniciar()
                self.personaje.reiniciar()
                self.proyectiles.empty()
                self.hud.reiniciar()
                self.jugador.add(self.personaje)
                self.musica.reiniciar()
            if key == "x":
                if self.gameState.estado == "jugando":
                    self.personaje.atacar()
                if self.gameState.estado == "menu":
                    if self.menu.getOpcion(self.personaje) == "jugar":
                        self.gameState.jugar()
                        self.musica.reiniciar()
                        self.enemySpawner.reiniciar()
                    if self.menu.getOpcion(self.personaje) == "salir":
                        pygame.quit()
                        sys.exit()
            if key == "a":
                self.enemySpawner.spawnEnemy()
            if key == "o":
                pygame.display.toggle_fullscreen()
            if key == "t" and self.gameState.estado == "gameover":
                self.proyectiles.empty()
                self.hud.reiniciar()
                self.itemSpawner.reiniciar()
                self.enemySpawner.reiniciar()
                self.gameState.taberna()
                self.personaje.reiniciar()
                self.jugador.add(self.personaje)
                self.musica.taberna()
        if event.type == KEYUP:
            key = pygame.key.name(event.key)
            if key == "left":
                self.personaje.detener("left")
            if key == "right":
                self.personaje.detener("right")

    def update(self):
        self.musica.update()
        self.fondo.update()
        self.gameState.update()
        if self.gameState.estado == "jugando":
            if not self.gameState.pausa:
                self.jugador.update()
                self.enemigos.update()
                self.items.update()
                self.collisionManager.colisionConGrupo(self.personaje, self.enemigos)
                self.proyectiles.update()
                self.collisionManager.collisionProyectiles(self.personaje, self.enemigos, self.proyectiles)
                self.hud.update()
                self.enemySpawner.update()
                self.itemSpawner.update(self.jugador.sprite)
                self.proyectiles.update()
        if self.gameState.estado == "menu":
            self.jugador.update()
            self.menu.update()

    def draw(self):
        if self.gameState.estado == "jugando":
            self.items.draw(self.screen)
            self.enemigos.draw(self.screen)
            self.jugador.draw(self.screen)
            self.proyectiles.draw(self.screen)
            self.hud.draw(self.screen)
        if self.gameState.estado == "menu":
            self.menu.draw(self.screen)
            self.jugador.draw(self.screen)
        if self.gameState.estado == "gameover":
            self.gameState.drawGameOver(self.screen)
        if self.gameState.pausa:
            self.hud.drawPausa(self.screen)
        self.fondo.drawBlackScreen()

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN or event.type == KEYUP:
                    self.keyHandler(event)
                if event.type == MUERTO:
                    self.gameState.gameOver()
                    self.musica.gameOver()
                if event.type == ATAQUE_MELE:
                    self.collisionManager.colisionArma(event.weaponRect, event.esEnemigo, self.jugador.sprite, self.enemigos, event.dano, event.direccion)
                if event.type == PROYECTIL:
                    self.proyectiles.add(event.proyectil)
                if event.type == ENEMIGO_MUERTO:
                    self.hud.enemigoMuerto()
                    muerto = Muerto(event.posicion)
                    self.enemigos.add(muerto)
                if event.type == META_COMPLETADA:
                    self.gameState.siguienteEtapa()
                    self.enemySpawner.reiniciar()
                    self.itemSpawner.reiniciar()
                if event.type == SONIDO:
                    self.sonidos.reproducir(event.sonido)

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(60)

    def presentar(self):
        fondo = pygame.Surface((WIDTH, HEIGHT))
        fondoRect = fondo.get_rect()
        fondoRect.left, fondoRect.top = 0, 0
        fondo.fill((0, 0, 0))
        imagen = pygame.image.load("./media/imagenes/micifux.jpg")
        imagenRect = imagen.get_rect()
        alpha = 0
        direccion = 1
        while True:
            pygame.event.get()
            self.screen.blit(fondo, fondoRect)
            self.screen.blit(imagen, imagenRect)
            alpha += 2 * direccion
            if alpha >= 255:
                direccion *= -1
            if alpha < 0:
                break
            imagen.set_alpha(alpha)
            pygame.display.update()
            self.clock.tick(60)