import pygame
import random
import math
from pygame import mixer
import io


# Inicializar pygame
pygame.init()



#Crear la pantalla
pantalla = pygame.display.set_mode((800,600))


# Titulo, fondo e icono
pygame.display.set_caption("Space Invaders")
icono = pygame.image.load('icono.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('fondo.jpg')

# Agregar musica de fondo
mixer.music.load('musica_fondo.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.4)

# Variables del jugador
img_jugador = pygame.image.load('player.png')
player_x_posicion = 368
player_y_posicion = 500
player_x_cambio = 0


# Variables del enemigo
img_enemigo = []  
enemigo_x_posicion = []
enemigo_y_posicion = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 6
vida_enemigo = []

for enemigos in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('enemigo.png'))
    enemigo_x_posicion.append(random.randint(0,736))      
    enemigo_y_posicion.append(random.randint(50,150))
    enemigo_x_cambio.append(0.20)
    enemigo_y_cambio.append(50)
    vida_enemigo.append(1)

# Variables de la bala
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio= 0.5
bala_visible = False 

# Convertir fuente en bytes
def fuente_bytes(fuente):
    with open(fuente, 'rb') as f:
        otf_bytes = f.read()
        return io.BytesIO(otf_bytes)


# Variable puntaje
puntaje = 0
fuente_como_bytes = fuente_bytes('SpaceNova-6Rpd1.otf')
fuente = pygame.font.Font('SpaceNova-6Rpd1.otf',28)
texto_x = 10
texto_y = 10

# Funcion mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f'Puntaje: {puntaje}', True,(255,255,255))
    pantalla.blit(texto,(x,y))
    
# Texto final del juego
fuente_final = pygame.font.Font('SpaceNova-6Rpd1.otf',50)
def texto_final():
    mi_fuente_final = fuente_final.render('JUEGO TERMINADO', True,(158, 18, 18))
    pantalla.blit(mi_fuente_final,(80,250))
    
# Funcion para dibujar el modelo del jugador
# x,y son las coordenadas del jugador
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))


# Funcion para dibujar el modelo del enemigo
# x,y son las coordenadas del enemigo
def dibujar_enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x,y))
    

def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala,(x + 8,y + 10))
    
# Funcion detectar colisiones
def colision(enemigo_x,enemigo_y,bala_x,bala_y):
    distancia = math.sqrt((math.pow(enemigo_x - bala_x,2) + (math.pow(enemigo_y - bala_y,2))))
    if distancia < 27:
        return True
    else:
        return False
    

# Loop del juego
se_ejecuta = True
while se_ejecuta:
    #Imagen fondo pantalla
    pantalla.blit(fondo,(0,0))
    
    # Iterar en Eventos del teclado
    # pygame.event.get() devuelve una lista de eventos que han ocurrido
    for evento in pygame.event.get():
        # Evento cerrar 
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        # Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                player_x_cambio = -0.30

            if evento.key == pygame.K_RIGHT:
                player_x_cambio = 0.30
            
            if evento.key == pygame.K_SPACE:
                if not bala_visible:
                    sonido_bala = mixer.Sound('laser.mp3')
                    sonido_bala.play()
                    bala_x = player_x_posicion
                    bala_y = player_y_posicion
                    bala_visible = True

        # Evento soltar flechas        
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                player_x_cambio = 0 
     
    # Movimiento bala
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio
        if bala_y <= 0:
            bala_y = 500
            bala_visible = False

    # Modificar ubicacion del jugador           
    player_x_posicion += player_x_cambio
    
    # Mantener al jugador dentro de los bordes
    
    if player_x_posicion <= 0:
        player_x_posicion = 0
    elif player_x_posicion >= 736:
        player_x_posicion = 736
    
    
    # Modificar ubicacion del enemigo
    for enemigo in range(cantidad_enemigos):     
        
        # fin del juego
        if enemigo_y_posicion[enemigo] > 450:
            for enemigo in range(cantidad_enemigos):
                enemigo_y_posicion[enemigo] = 1000
            texto_final()
            break
                     
        enemigo_x_posicion[enemigo] += enemigo_x_cambio[enemigo]
    
        # Mantener al enemigo dentro de los bordes 
        
        if enemigo_x_posicion[enemigo] <= 0:
            enemigo_x_cambio[enemigo] = 0.20
            enemigo_y_posicion[enemigo] += enemigo_y_cambio[enemigo]
            
        elif enemigo_x_posicion[enemigo] >= 736:
            enemigo_x_cambio[enemigo] = -0.20
            enemigo_y_posicion[enemigo] += enemigo_y_cambio[enemigo]
        
        # Detectar colision  
        colision_bala_enemigo = colision(
            enemigo_x_posicion[enemigo], 
            enemigo_y_posicion[enemigo], 
            bala_x, 
            bala_y
        )
        if colision_bala_enemigo and bala_visible:
            sonido_colision = mixer.Sound("golpe.mp3")
            sonido_colision.play()
            sonido_colision.set_volume(0.4)
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x_posicion[enemigo] = random.randint(0, 736)
            enemigo_y_posicion[enemigo] = random.randint(50, 150)
            vida_enemigo[enemigo] = 1

        dibujar_enemigo(enemigo_x_posicion[enemigo],enemigo_y_posicion[enemigo],enemigo)
        
        # Respawn enemigo si la vida es 0
        if vida_enemigo[enemigo] <= 0:
            enemigo_x_posicion[enemigo] = random.randint(0,736)
            enemigo_y_posicion[enemigo] = random.randint(50,150)
            vida_enemigo[enemigo] = 1
    
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False
        
    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio
      

        
    jugador(player_x_posicion,player_y_posicion) 
    
    mostrar_puntaje(texto_x,texto_y)
    
    # Actualizar la pantalla
    pygame.display.update()
    