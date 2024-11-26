import pygame

width = 64 * 14
height = 64 * 10
tile_size = 64
item_pos = None
flag_pos = None
mapa = []
tile = {}
attack_cooldown = 500  
last_attack_time = 0   
item_coletado = False
vitoria = False
hero_walk = {"right": [],"left": []}
direction = "right"
hero_anim_frame = 0
hero_pos = [300, 0]
hero_speed = 0.2 #---- VELOCIDADE HEROI
is_attacking = False
attack_time = 0
hero_anim_time = 0
camera_offset = [0, 0]
zumbi_pos_list = []
zumbi_speed_list = []
lama_pos_list = []
lama_speed = 0.05
multiplicador_tile = 1.3
vida = 3
pocao_vida = 1  
last_collision_time = 0
collision_delay = 1000
score = 0  
moedas = []  
moedasColetadas = []
chao_pos_list = []  
zumbi_walk = []
zumbi_anim_frame_list = []
zumbi_anim_time_list = []

def load_mapa(filename):
    global mapa, moedas, zumbi_pos_list, lama_pos_list, chao_pos_list, zumbi_speed_list, item_pos, flag_pos
    with open(filename, "r") as file:
        for i, line in enumerate(file.readlines()):
            mapa.append(line.strip())
            for j, char in enumerate(line.strip()):
                if char == 'M':
                    moedas.append((j * tile_size, i * tile_size))
                elif char == 'Z':
                    zumbi_anim_frame_list.append(0)
                    zumbi_anim_time_list.append(0)
                    zumbi_pos_list.append([j * tile_size, i * tile_size])
                    zumbi_speed_list.append(0.2)
                    chao_pos_list.append((j * tile_size, i * tile_size))
                elif char == 'L':
                    lama_pos_list.append([j * tile_size, i * tile_size])
                    chao_pos_list.append((j * tile_size, i * tile_size))
                elif char == 'P':
                    item_pos = (j * tile_size, i * tile_size)
                    chao_pos_list.append((j * tile_size, i * tile_size))  
                elif char == 'F':
                    flag_pos = (j * tile_size, i * tile_size)
                    chao_pos_list.append((j * tile_size, i * tile_size))  

def load():
    global clock, tile, hero_walk, zumbi, lama, coracaoCheio, coracaoVazio, moeda_img, hero_attack_img, zumbi_walk
    hero_attack_img = pygame.image.load("cavaleiroAtaque.png")
    zumbi_walk = []

    for i in range(1, 5):
        zumbi_walk.append(pygame.image.load(f"zumbi ({i}).png"))

    for i in range(0, 4):
        hero_walk["right"].append(pygame.image.load(f"knight_f_run_anim_f{i}.png"))
    for i in range(4, 8):
        hero_walk["left"].append(pygame.image.load(f"knight_f_run_anim_f{i}.png"))

    tile['C'] = pygame.image.load("chao1.png")
    tile['V'] = pygame.image.load("chao2.png")
    tile['B'] = pygame.image.load("chao3.png")
    tile['E'] = pygame.image.load("espinho.png")
    tile['F'] = pygame.image.load('bandeira.png')
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
    global zumbi_pos_list, lama_pos_list, score, last_attack_time, attack_cooldown

    current_time = pygame.time.get_ticks()  # Tempo atual em milissegundos
    if current_time - last_attack_time >= attack_cooldown:  # Verificar se o cooldown terminou
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:  # Botão esquerdo do mouse pressionado
            # Registrar o momento do ataque
            last_attack_time = current_time

            # Definir a área de colisão do herói
            hero_rect = pygame.Rect(hero_pos[0], hero_pos[1] + 18, tile_size * 0.7, tile_size * 0.8)

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

def show_start_screen(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    # Texto de boas-vindas
    text = font.render("Bem-vindo!", True, (255, 255, 255))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2 - 40))

    # Texto de instrução
    instruction_text = font.render("Você deve resgatar a princesa e retornar com ela para a bandeira", True, (255, 255, 255))
    screen.blit(instruction_text, (width // 2 - instruction_text.get_width() // 2, height // 2 - instruction_text.get_height() // 2))

    # Texto para iniciar o jogo
    start_text = font.render("Pressione qualquer tecla para começar", True, (255, 255, 255))
    screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 - start_text.get_height() // 2 + 40))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def show_end_screen(screen, message):
    global running  
    screen.fill((0, 0, 0))  # Preenche a tela de preto
    font = pygame.font.Font(None, 40)
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    restart_text = font.render("Pressione 'R' para reiniciar ou outra tecla para sair", True, (255, 255, 255))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 100))

    pygame.display.flip()  # Atualiza a tela

    # Espera o jogador pressionar 'R' para reiniciar ou qualquer outra tecla para sair
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    running = True
                    restart_game()
                else:
                    pygame.quit()
                    quit()

def update(dt):
    global hero_anim_frame, hero_pos, hero_anim_time, direction, camera_offset, zumbi_pos_list, lama_pos_list, running, vida, last_collision_time, zumbi_speed_list, is_attacking, attack_time, item_coletado, vitoria, item_pos, hero_speed
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
    
    if not item_coletado:
        item_rect = pygame.Rect(item_pos[0], item_pos[1], tile_size, tile_size)
        hero_rect = pygame.Rect(hero_pos[0], hero_pos[1] + 18, tile_size * 0.7, tile_size * 0.8)
        if hero_rect.colliderect(item_rect):
            item_coletado = True
            hero_speed = 0.15

    if flag_pos is not None and item_coletado:
        flag_rect = pygame.Rect(flag_pos[0], flag_pos[1], tile_size, tile_size)
        hero_rect = pygame.Rect(hero_pos[0], hero_pos[1] + 18, tile_size * 0.7, tile_size * 0.8)
        if hero_rect.colliderect(flag_rect):
            vitoria = True

    check_collision_with_coin(hero_rect)
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  # Botão esquerdo do mouse pressionado
        is_attacking = True
        attack_time = pygame.time.get_ticks()
        check_attack()  # Continue verificando se acertou algum monstro

    if is_attacking:
        current_time = pygame.time.get_ticks()
        if current_time - attack_time > 200:
            is_attacking = False

    

    camera_offset[0] = hero_pos[0] - width // 2
    camera_offset[1] = hero_pos[1] - height // 2

    # Atualiza a posição dos zumbis
    for i, zumbi_pos in enumerate(zumbi_pos_list):
        # Atualiza a posição do zumbi
        if zumbi_pos[1] <= -10 or zumbi_pos[1] >= 440:
            zumbi_speed_list[i] = -zumbi_speed_list[i]
        zumbi_pos[1] += zumbi_speed_list[i] * dt

        # Atualiza a animação do zumbi
        zumbi_anim_time_list[i] += dt
        if zumbi_anim_time_list[i] > 200:  # Trocar frame a cada 200 ms
            zumbi_anim_frame_list[i] = (zumbi_anim_frame_list[i] + 1) % len(zumbi_walk)
            zumbi_anim_time_list[i] = 0

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
        show_end_screen(screen, "Você perdeu! Pressione qualquer tecla para sair.")

    if vitoria:
        running = False
        show_end_screen(screen, "Você venceu! Pressione qualquer tecla para sair.")

def draw_screen(screen):
    font = pygame.font.Font(None, 36)
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
                
    if is_attacking:
         screen.blit(hero_attack_img, (width // 2, height // 2))
    else:
         screen.blit(hero_walk[direction][hero_anim_frame], (width // 2, height // 2))

    # Desenha os zumbis
    for i, zumbi_pos in enumerate(zumbi_pos_list):
        zumbi_frame = zumbi_walk[zumbi_anim_frame_list[i]]
        screen.blit(zumbi_frame, (zumbi_pos[0] - camera_offset[0], zumbi_pos[1] - camera_offset[1]))

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
    
    if not item_coletado and item_pos is not None:
        item_img = pygame.image.load("item.png")
        item_width = item_img.get_width()
        item_height = item_img.get_height()

        # Calcular a posição para centralizar o item no tile
        item_x = item_pos[0] - camera_offset[0] + (tile_size - item_width) // 2
        item_y = item_pos[1] - camera_offset[1] + (tile_size - item_height) // 2

        screen.blit(item_img, (item_x, item_y))
    else:
        textoPrincesa = font.render(f"Carregando princesa", True, (252, 15, 192))
        screen.blit(textoPrincesa, (width - 270, 100))
        pass


    # Desenha a pontuação

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

# Mostrar a tela de início
show_start_screen(screen)

# Carregar o jogo e iniciar o loop principal
load()
main_loop(screen)
pygame.quit()
