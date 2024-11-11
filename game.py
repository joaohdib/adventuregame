import pygame
import time

width = 64 * 14
height = 64 * 10
tile_size = 64
mapa = []
tile = {}
hero_walk = {"right": [],"left": []}
direction = "right"
hero_anim_frame = 0
hero_pos = [300, 0]
hero_speed = 0.4
hero_anim_time = 0
camera_offset = [0, 0]
zumbi_pos = [400, 300]
zumbi_direction = "down"
zumbi_speed = 0.2
multiplicador_tile = 1.3
vida = 3
last_collision_time = 0
collision_delay = 1000  # 1000 ms = 1 segundo

def load_mapa(filename):
    global mapa
    with open(filename, "r") as file:
        for line in file.readlines():
            mapa.append(line.strip())

def load():
    global clock, tile, hero_walk, zumbi, coracaoCheio, coracaoVazio
    for i in range(0, 4):
        hero_walk["right"].append(pygame.image.load(f"knight_f_run_anim_f{i}.png"))
    for i in range(4, 8):
        hero_walk["left"].append(pygame.image.load(f"knight_f_run_anim_f{i}.png"))

    tile['C'] = pygame.image.load("chao1.png")
    tile['V'] = pygame.image.load("chao2.png")
    tile['B'] = pygame.image.load("chao3.png")
    tile['E'] = pygame.image.load("espinho.png")
    zumbi = pygame.image.load("zumbi.png")
    coracaoCheio = pygame.image.load("coracaoCheio.png")
    coracaoVazio = pygame.image.load("coracaoVazio.png")

    clock = pygame.time.Clock()
    load_mapa("mapa.txt")

def check_collision_with_water(hero_rect):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == 'E':
                tile_rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
                if hero_rect.colliderect(tile_rect):
                    return True
    return False

def update(dt):
    global hero_anim_frame, hero_pos, hero_anim_time, direction, camera_offset, zumbi_pos, zumbi_direction, running, vida, last_collision_time
    keys = pygame.key.get_pressed()

    old_pos = list(hero_pos)

    if keys[pygame.K_RIGHT]:
        hero_pos[0] += hero_speed * dt
        direction = "right"
    elif keys[pygame.K_LEFT]:
        hero_pos[0] -= hero_speed * dt
        direction = "left"
    elif keys[pygame.K_UP]:
        hero_pos[1] -= hero_speed * dt
        direction = "right"
    elif keys[pygame.K_DOWN]:
        hero_pos[1] += hero_speed * dt
        direction = "right"
    else:
        hero_anim_frame = 0

    hero_rect = pygame.Rect(hero_pos[0], hero_pos[1]+15, tile_size*0.7, tile_size * 0.8)

    current_time = pygame.time.get_ticks()
    if current_time - last_collision_time > collision_delay:
        if check_collision_with_water(hero_rect):
            vida -= 1
            last_collision_time = current_time

    hero_anim_time += dt
    if hero_anim_time > 100:
        hero_anim_frame = (hero_anim_frame + 1) % len(hero_walk[direction])
        hero_anim_time = 0

    camera_offset[0] = hero_pos[0] - width // 2
    camera_offset[1] = hero_pos[1] - height // 2

    # Atualiza a posição do zumbi
    if zumbi_direction == "down":
        zumbi_pos[1] -= zumbi_speed * dt
        if zumbi_pos[1] < 100:  # Limite para mudar direção
            zumbi_direction = "up"
    elif zumbi_direction == "up":
        zumbi_pos[1] += zumbi_speed * dt
        if zumbi_pos[1] > 400:  # Limite para mudar direção
            zumbi_direction = "down"

    # Verifica colisão com o zumbi
    zumbi_rect = pygame.Rect(zumbi_pos[0], zumbi_pos[1], tile_size, tile_size * multiplicador_tile)
    if current_time - last_collision_time > collision_delay:
        if hero_rect.colliderect(zumbi_rect):
            vida -= 1
            last_collision_time = current_time
    
    if vida == 0:
        running = False
        print("GAME OVER")

def draw_screen(screen):
    screen.fill((0, 0, 0))
    for i in range(vida):
        screen.blit(coracaoCheio,(i*65,10))
    
    for i in range(3 - vida):
        screen.blit(coracaoVazio, ((2 - i) * 65, 10))

    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            tile_type = mapa[i][j]
            if tile_type in tile:
                screen.blit(tile[tile_type], 
                            (j * tile_size - camera_offset[0], i * tile_size - camera_offset[1]))
    
    screen.blit(hero_walk[direction][hero_anim_frame], 
                (width // 2, height // 2))
    
    # Desenha o zumbi
    screen.blit(zumbi, (zumbi_pos[0] - camera_offset[0], zumbi_pos[1] - camera_offset[1]))

    # Desenha o retângulo de colisão do zumbi
    zumbi_rect = pygame.Rect(zumbi_pos[0], zumbi_pos[1], tile_size, tile_size * multiplicador_tile)
    pygame.draw.rect(screen, (255, 0, 0), (zumbi_rect.x - camera_offset[0], zumbi_rect.y - camera_offset[1], zumbi_rect.width, zumbi_rect.height), 2)

    # Desenha o retângulo de colisão do personagem principal
    hero_rect = pygame.Rect(hero_pos[0], hero_pos[1]+15, tile_size*0.7, tile_size * 0.8)
    pygame.draw.rect(screen, (0, 255, 0), (hero_rect.x - camera_offset[0], hero_rect.y - camera_offset[1], hero_rect.width, hero_rect.height), 2)

def main_loop(screen):
    global clock, running
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break

        clock.tick(60)
        dt = clock.get_time()
        update(dt)
        draw_screen(screen)
        pygame.display.update()

pygame.init()
screen = pygame.display.set_mode((width, height))
load()
main_loop(screen)
pygame.quit()
