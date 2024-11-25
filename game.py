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
zumbi_pos_list = []
zumbi_speed_list = []
lama_pos_list = []
lama_speed = 0.05
multiplicador_tile = 1.3
vida = 3
pocao_vida = 1  # Contador de poções de vida
last_collision_time = 0
collision_delay = 750  # 1000 ms = 1 segundo
score = 0  # Pontuação do jogador

moedas = []  # Lista para armazenar as posições das moedas
moedasColetadas = []
chao_pos_list = []  # Lista para armazenar as posições dos pisos adicionais

def load_mapa(filename):
    global mapa, moedas, zumbi_pos_list, lama_pos_list, chao_pos_list, zumbi_speed_list
    with open(filename, "r") as file:
        for i, line in enumerate(file.readlines()):
            mapa.append(line.strip())
            for j, char in enumerate(line.strip()):
                if char == 'M':
                    moedas.append((j * tile_size, i * tile_size))
                elif char == 'Z':
                    zumbi_pos_list.append([j * tile_size, i * tile_size])
                    zumbi_speed_list.append(0.2)  # Inicializa a velocidade de cada zumbi
                    chao_pos_list.append((j * tile_size, i * tile_size))
                elif char == 'L':
                    lama_pos_list.append([j * tile_size, i * tile_size])
                    chao_pos_list.append((j * tile_size, i * tile_size))

def load():
    global clock, tile, hero_walk, zumbi, lama, coracaoCheio, coracaoVazio, moeda_img
    for i in range(0, 4):
        hero_walk["right"].append(pygame.image.load(f"knight_f_run_anim_f{i}.png"))
    for i in range(4, 8):
        hero_walk["left"].append(pygame.image.load(f"knight_f_run_anim_f{i}.png"))

    tile['C'] = pygame.image.load("chao1.png")
    tile['V'] = pygame.image.load("chao2.png")
    tile['B'] = pygame.image.load("chao3.png")
    tile['E'] = pygame.image.load("espinho.png")
    zumbi = pygame.image.load("zumbi.png")
    lama = pygame.image.load("monstrolama1.png")
    coracaoCheio = pygame.image.load("coracaoCheio.png")
    coracaoVazio = pygame.image.load("coracaoVazio.png")
    moeda_img = pygame.image.load("moeda.png")

    clock = pygame.time.Clock()
    load_mapa("mapa.txt")

def restart_game():
    global hero_pos, direction, hero_anim_frame, hero_anim_time, camera_offset, zumbi_pos_list, lama_pos_list, moedas, moedasColetadas, vida, pocao_vida, score, last_collision_time

    # Redefinindo variáveis para o estado inicial
    hero_pos = [300, 0]
    direction = "right"
    hero_anim_frame = 0
    hero_anim_time = 0
    camera_offset = [0, 0]
    vida = 3
    pocao_vida = 1
    score = 0
    last_collision_time = 0

    # Recarregando inimigos, moedas e chao
    zumbi_pos_list = []
    lama_pos_list = []
    moedas = []
    moedasColetadas = []

    # Recarregar o mapa
    load_mapa("mapa.txt")

def use_pocao_vida():
    global vida, pocao_vida
    if pocao_vida > 0 and vida < 3:
        vida = 3
        pocao_vida -= 1

def check_collision_with_water(hero_rect):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == 'E':
                tile_rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
                if hero_rect.colliderect(tile_rect):
                    return True
    return False

def check_collision_with_coin(hero_rect):
    global moedas, score
    for moeda in moedas[:]:
        moeda_rect = pygame.Rect(moeda[0], moeda[1], tile_size // 2, tile_size // 2)
        if (hero_rect.colliderect(moeda_rect)) and (moeda not in moedasColetadas):
            moedasColetadas.append(moeda)
            score += 10

def check_attack():
    global zumbi_pos_list, lama_pos_list, score
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  # Botão esquerdo do mouse pressionado
        hero_rect = pygame.Rect(hero_pos[0], hero_pos[1]+18, tile_size*0.7, tile_size * 0.8)
        # Verifica se o herói está olhando para algum zumbi ou lama e o ataca
        if direction == "right":
            for zumbi_pos in zumbi_pos_list[:]:
                zumbi_rect = pygame.Rect(zumbi_pos[0], zumbi_pos[1], tile_size, tile_size * multiplicador_tile)
                if hero_rect.right < zumbi_rect.left and hero_rect.colliderect(zumbi_rect.inflate(tile_size, 0)):
                    zumbi_pos_list.remove(zumbi_pos)
                    score += 20
            for lama_pos in lama_pos_list[:]:
                lama_rect = pygame.Rect(lama_pos[0], lama_pos[1], tile_size, tile_size)
                if hero_rect.right < lama_rect.left and hero_rect.colliderect(lama_rect.inflate(tile_size, 0)):
                    lama_pos_list.remove(lama_pos)
                    score += 20
        elif direction == "left":
            for zumbi_pos in zumbi_pos_list[:]:
                zumbi_rect = pygame.Rect(zumbi_pos[0], zumbi_pos[1], tile_size, tile_size * multiplicador_tile)
                if hero_rect.left > zumbi_rect.right and hero_rect.colliderect(zumbi_rect.inflate(tile_size, 0)):
                    zumbi_pos_list.remove(zumbi_pos)
                    score += 20
            for lama_pos in lama_pos_list[:]:
                lama_rect = pygame.Rect(lama_pos[0], lama_pos[1], tile_size, tile_size)
                if hero_rect.left > lama_rect.right and hero_rect.colliderect(lama_rect.inflate(tile_size, 0)):
                    lama_pos_list.remove(lama_pos)
                    score += 20

def update(dt):
    global hero_anim_frame, hero_pos, hero_anim_time, direction, camera_offset, zumbi_pos_list, lama_pos_list, running, vida, last_collision_time, zumbi_speed_list
    keys = pygame.key.get_pressed()

    old_pos = list(hero_pos)


    if keys[pygame.K_r]:
        restart_game()
    if keys[pygame.K_e]:
        use_pocao_vida()
    if keys[pygame.K_d]:
        hero_pos[0] += hero_speed * dt
        direction = "right"
        hero_anim_time += dt
        if hero_anim_time > 100:
            hero_anim_frame = (hero_anim_frame + 1) % len(hero_walk[direction])
            hero_anim_time = 0
    elif keys[pygame.K_a] and hero_pos[0] > 0:
        hero_pos[0] -= hero_speed * dt
        direction = "left"
        hero_anim_time += dt
        if hero_anim_time > 100:
            hero_anim_frame = (hero_anim_frame + 1) % len(hero_walk[direction])
            hero_anim_time = 0
    elif keys[pygame.K_w] and hero_pos[1] > -10:
        hero_pos[1] -= hero_speed * dt
        direction = "right"
        hero_anim_time += dt
        if hero_anim_time > 100:
            hero_anim_frame = (hero_anim_frame + 1) % len(hero_walk[direction])
            hero_anim_time = 0
    elif keys[pygame.K_s] and hero_pos[1] < 440:
        hero_pos[1] += hero_speed * dt
        direction = "right"
        hero_anim_time += dt
        if hero_anim_time > 100:
            hero_anim_frame = (hero_anim_frame + 1) % len(hero_walk[direction])
            hero_anim_time = 0
    else:
        hero_anim_frame = 0
        hero_anim_time = 0

    hero_rect = pygame.Rect(hero_pos[0], hero_pos[1]+18, tile_size*0.7, tile_size * 0.8)

    current_time = pygame.time.get_ticks()
    if current_time - last_collision_time > collision_delay:
        if check_collision_with_water(hero_rect):
            vida -= 1
            last_collision_time = current_time

    check_collision_with_coin(hero_rect)
    check_attack()

    camera_offset[0] = hero_pos[0] - width // 2
    camera_offset[1] = hero_pos[1] - height // 2

    # Atualiza a posição dos zumbis
    for i, zumbi_pos in enumerate(zumbi_pos_list):
        if zumbi_pos[1] <= -10 or zumbi_pos[1] >= 440:
            zumbi_speed_list[i] = -zumbi_speed_list[i]
        zumbi_pos[1] += zumbi_speed_list[i] * dt

    # Atualiza a posição dos monstros de lama (seguem o jogador)
    for lama_pos in lama_pos_list:
        if lama_pos[0] < hero_pos[0]:
            lama_pos[0] += lama_speed * dt
        elif lama_pos[0] > hero_pos[0]:
            lama_pos[0] -= lama_speed * dt

        if lama_pos[1] < hero_pos[1]:
            lama_pos[1] += lama_speed * dt
        elif lama_pos[1] > hero_pos[1]:
            lama_pos[1] -= lama_speed * dt

    # Verifica colisão com os zumbis
    for zumbi_pos in zumbi_pos_list:
        zumbi_rect = pygame.Rect(zumbi_pos[0], zumbi_pos[1], tile_size, tile_size * multiplicador_tile)
        if current_time - last_collision_time > collision_delay:
            if hero_rect.colliderect(zumbi_rect):
                vida -= 1
                last_collision_time = current_time

    # Verifica colisão com os monstros de lama
    for lama_pos in lama_pos_list:
        lama_rect = pygame.Rect(lama_pos[0], lama_pos[1], tile_size, tile_size)
        if current_time - last_collision_time > collision_delay:
            if hero_rect.colliderect(lama_rect):
                vida -= 1
                last_collision_time = current_time

    if vida == 0:
        running = False 
        print("GAME OVER")

def draw_screen(screen):
    screen.fill((0, 0, 0))

    # Desenha as moedas
    for moeda in moedas:
        # Desenhar o piso original antes da moeda
        screen.blit(tile['C'], (moeda[0] - camera_offset[0], moeda[1] - camera_offset[1]))
        if moeda not in moedasColetadas:
            moeda_x = moeda[0] + (tile_size - moeda_img.get_width()) // 2
            moeda_y = moeda[1] + (tile_size - moeda_img.get_height()) // 2
            screen.blit(moeda_img, (moeda_x - camera_offset[0], moeda_y - camera_offset[1]))

    # Desenha os pisos adicionais para zumbis e monstros de lama
    for chao_pos in chao_pos_list:
        screen.blit(tile['C'], (chao_pos[0] - camera_offset[0], chao_pos[1] - camera_offset[1]))

    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            tile_type = mapa[i][j]
            if tile_type in tile:
                screen.blit(tile[tile_type], (j * tile_size - camera_offset[0], i * tile_size - camera_offset[1]))
                
    screen.blit(hero_walk[direction][hero_anim_frame], 
                (width // 2, height // 2))

    # Desenha os zumbis
    for zumbi_pos in zumbi_pos_list:
        screen.blit(zumbi, (zumbi_pos[0] - camera_offset[0], zumbi_pos[1] - camera_offset[1]))

    # Desenha os monstros de lama
    for lama_pos in lama_pos_list:
        screen.blit(lama, (lama_pos[0] - camera_offset[0], lama_pos[1] - camera_offset[1]))

    # Desenha o retângulo de colisão do personagem principal
    hero_rect = pygame.Rect(hero_pos[0], hero_pos[1]+18, tile_size*0.7, tile_size * 0.8)
    #pygame.draw.rect(screen, (0, 255, 0), (hero_rect.x - camera_offset[0], hero_rect.y - camera_offset[1], hero_rect.width, hero_rect.height), 2)

    # Desenha os corações de vida
    for i in range(vida):
        screen.blit(coracaoCheio,(i*65,10))
    
    for i in range(3 - vida):
        screen.blit(coracaoVazio, ((2 - i) * 65, 10))

    # Desenha a pontuação
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Pontuação: {score}", True, (255, 255, 255))
    screen.blit(score_text, (width - 200, 10))
    pocao_text = font.render(f"Poções de Vida: {pocao_vida}", True, (255, 255, 255))
    screen.blit(pocao_text, (width - 250, 50))

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
