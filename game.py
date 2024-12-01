import pygame
import random
import sys

width = 64 * 14
height = 64 * 10
tile_size = 64
item_pos = None
lama_ativo_list = [] 
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
is_damaged = False
damage_time = 0
hero_speed = 0.2 #---- VELOCIDADE HEROI
is_attacking = False
attack_time = 0
hero_anim_time = 0
camera_offset = [0, 0]
zumbi_pos_list = []
zumbi_speed_list = []
lama_pos_list = []
lama_speed = 0.09
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
lama_anim_frame_list = []
lama_anim_time_list = []
isMoving = False

def load_mapa(filename):
    global mapa, moedas, zumbi_pos_list, lama_pos_list, chao_pos_list, zumbi_speed_list, item_pos, flag_pos, lama_anim_frame_list, lama_anim_time_list
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
                    zumbi_speed_list.append(0.3)
                    chao_pos_list.append((j * tile_size, i * tile_size))
                elif char == 'L':
                    lama_pos_list.append([j * tile_size, i * tile_size])
                    lama_ativo_list.append(False)
                    lama_anim_frame_list.append(0)
                    lama_anim_time_list.append(0)
                    chao_pos_list.append((j * tile_size, i * tile_size))
                elif char == 'P':
                    item_pos = (j * tile_size, i * tile_size)
                    chao_pos_list.append((j * tile_size, i * tile_size))
                elif char == 'F':
                    flag_pos = (j * tile_size, i * tile_size)
                    chao_pos_list.append((j * tile_size, i * tile_size))

def load():
    global clock, tile, hero_walk, zumbi, lama, coracaoCheio, coracaoVazio, moeda_img, hero_attack_imgRight, zumbi_walk, lama_walk, hero_attack_imgLeft, hero_damage_img, walk_sound, walk_channel, potion_sound, coin_sound, sword_sound, sword_channel, damage_sound, win_sound, ambient_channel, ambient_sound, gameover_sound, kill_sound

    pygame.mixer.init()
    
    walk_channel = pygame.mixer.Channel(1)  # Canal 0 para o som de andar
    sword_channel = pygame.mixer.Channel(3)
    walk_channel.set_volume(0.5)  
    walk_sound = pygame.mixer.Sound("walking.mp3")  
    potion_sound = pygame.mixer.Sound("potiondrink.wav") 
    potion_sound.set_volume(1.0)  # O volume vai de 0.0 (mudo) a 1.0 (máximo)
    coin_sound = pygame.mixer.Sound("coin.wav")  
    ambient_sound = pygame.mixer.Sound("ambient.mp3")  
    sword_sound =  pygame.mixer.Sound("espada.mp3")  
    damage_sound = pygame.mixer.Sound("damage.ogg")
    win_sound = pygame.mixer.Sound("win.mp3")
    gameover_sound = pygame.mixer.Sound("gameover.mp3")
    kill_sound = pygame.mixer.Sound("kill.mp3")
    
    ambient_channel = pygame.mixer.Channel(2)
    ambient_channel.play(ambient_sound, loops=-1)  # Som de ambiente em loop infinito
    ambient_channel.set_volume(0.3)

    lama_walk = []
    hero_attack_imgRight = pygame.image.load("cavaleiroAtaque.png")
    hero_attack_imgLeft = pygame.image.load("cavaleiroAtaque2.png")
    hero_damage_img = pygame.image.load("dano.png")  # Carregar a imagem do herói recebendo dano
    zumbi_walk = []

    for i in range(1, 4):
        lama_walk.append(pygame.image.load(f"monstrolama{i}.png"))
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
    global hero_pos, direction, hero_anim_frame, hero_anim_time, camera_offset, zumbi_pos_list, lama_pos_list, moedas, moedasColetadas, vida, pocao_vida, score, last_collision_time, item_coletado, vitoria, mapa, chao_pos_list, zumbi_anim_frame_list, zumbi_anim_time_list, item_pos, flag_pos, zumbi_speed_list, hero_speed, walk_channel, ambient_channel, ambient_sound


    ambient_channel.play(ambient_sound, loops=-1)
    walk_channel.stop()
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
    item_coletado = False
    vitoria = False

    # Limpar e recarregar o mapa e suas variáveis associadas
    mapa = []
    zumbi_pos_list = []
    zumbi_speed_list = []
    lama_pos_list = []
    chao_pos_list = []
    moedas = []
    moedasColetadas = []
    zumbi_anim_frame_list = []
    zumbi_anim_time_list = []
    item_pos = None
    flag_pos = None
    hero_speed = 0.2

    # Recarregar o mapa
    load_mapa("mapa.txt")

def use_pocao_vida():
    global vida, pocao_vida, potion_sound
    if pocao_vida > 0 and vida < 3:
        vida = 3
        pocao_vida -= 1
        potion_sound.play()

def check_collision_with_spike(hero_rect):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == 'E':
                tile_rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
                if hero_rect.colliderect(tile_rect):
                    return True
    return False

def check_collision_with_coin(hero_rect):
    global moedas, score, coin_sound
    for moeda in moedas[:]:
        moeda_rect = pygame.Rect(moeda[0], moeda[1], tile_size // 2, tile_size // 2)
        if (hero_rect.colliderect(moeda_rect)) and (moeda not in moedasColetadas):
            moedasColetadas.append(moeda)
            coin_sound.play()
            score += 10

def check_attack():
    global zumbi_pos_list, lama_pos_list, score, last_attack_time, attack_cooldown, score, kill_sound

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
                        return True
                for lama_pos in lama_pos_list[:]:
                    lama_rect = pygame.Rect(lama_pos[0], lama_pos[1], tile_size, tile_size)
                    if hero_rect.right < lama_rect.left and hero_rect.colliderect(lama_rect.inflate(tile_size, 0)):
                        lama_pos_list.remove(lama_pos)
                        score += 20
                        return True
            elif direction == "left":
                for zumbi_pos in zumbi_pos_list[:]:
                    zumbi_rect = pygame.Rect(zumbi_pos[0], zumbi_pos[1], tile_size, tile_size * multiplicador_tile)
                    if hero_rect.left > zumbi_rect.right and hero_rect.colliderect(zumbi_rect.inflate(tile_size, 0)):
                        zumbi_pos_list.remove(zumbi_pos)
                        score += 20
                        return True
                for lama_pos in lama_pos_list[:]:
                    lama_rect = pygame.Rect(lama_pos[0], lama_pos[1], tile_size, tile_size)
                    if hero_rect.left > lama_rect.right and hero_rect.colliderect(lama_rect.inflate(tile_size, 0)):
                        lama_pos_list.remove(lama_pos)
                        score += 20
                        return True
    return False

def show_start_screen(screen):
    pygame.font.init()

    # Carregar fontes e definir cores
    title_font = pygame.font.Font(None, 120)  # Fonte maior para o título
    text_font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 40)
    command_font = pygame.font.Font(None, 36)  # Fonte menor para os comandos

    # Cores
    title_color = (255, 223, 0)  # Dourado para o título
    title_shadow_color = (0, 0, 0)  # Sombra preta para o brilho
    text_color = (255, 255, 255)  # Branco
    command_color = (200, 200, 200)  # Cinza claro para os comandos
    highlight_color = (255, 255, 0)  # Amarelo para destaque

    # Carregar imagem de fundo do castelo
    castle_image = pygame.image.load("castelo.png")
    castle_image = pygame.transform.scale(castle_image, (width, height))

    # Controlador de animação de piscar
    blink_time = 0
    show_press_key = True

    waiting = True
    while waiting:
        # Desenhar o fundo do castelo
        screen.blit(castle_image, (0, 0))

        # Criar o efeito de sombra no título
        title_text = title_font.render("Castle Crusader", True, title_shadow_color)
        shadow_offset = 5  # Deslocamento da sombra
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2 + shadow_offset, height // 2 - 220 + shadow_offset))
        
        # Texto do título com a cor dourada
        title_text = title_font.render("Castle Crusader", True, title_color)
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 220))

        # Texto de instrução
        instruction_text = text_font.render("Resgate a princesa e retorne em segurança!", True, text_color)
        screen.blit(instruction_text, (width // 2 - instruction_text.get_width() // 2, height // 2 - 120))

        # Comandos do jogador
        commands = [
            "WASD - Andar",
            "E - Usar poção de vida",
            "R - Reiniciar o jogo",
            "Botão esquerdo do mouse - Atacar"
        ]
        for i, command in enumerate(commands):
            command_text = command_font.render(command, True, command_color)
            screen.blit(command_text, (width // 2 - command_text.get_width() // 2, height // 2 - 60 + i * 30))

        # Texto para iniciar o jogo (piscar)
        blink_time += 1
        if blink_time > 30:
            blink_time = 0
            show_press_key = not show_press_key

        if show_press_key:
            start_text = small_font.render("Pressione qualquer tecla para começar", True, highlight_color)
            screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 + 150))

        # Atualizar a tela
        pygame.display.flip()

        # Esperar pela entrada do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

    # Parar a música de fundo ao sair da tela de início
    pygame.mixer.music.stop()

def show_end_screen(screen, message):
    global running, win_sound, score, ambient_channel  # Adicione 'score' como variável global
    win_sound.play()
    ambient_channel.stop()

    # Carregar fontes e definir cores
    pygame.font.init()
    title_font = pygame.font.Font(None, 80)  # Fonte maior para o título
    text_font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 30)

    # Cores
    background_color = (0, 0, 50)  # Azul escuro
    title_color = (255, 223, 0)  # Dourado
    text_color = (255, 255, 255)  # Branco
    highlight_color = (50, 205, 50)  # Verde claro para destaque

    # Preencher a tela com uma cor de fundo estilizada
    screen.fill(background_color)

    # Desenhar um título com efeito de sombra para destaque
    shadow_offset = 5
    title_text = title_font.render("Vitória!", True, (0, 0, 0))
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2 + shadow_offset, height // 2 - 150 + shadow_offset))
    title_text = title_font.render("Vitória!", True, title_color)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 150))

    # Desenhar o texto principal da mensagem de vitória
    message_text = text_font.render(message, True, text_color)
    screen.blit(message_text, (width // 2 - message_text.get_width() // 2, height // 2 - 50))

    # Exibir o score final
    score_text = text_font.render(f"Score Final: {score}", True, highlight_color)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 + 10))  # Ajuste a posição conforme necessário

    # Instruções para o jogador
    restart_text = text_font.render("Pressione 'R' para reiniciar ou qualquer outra tecla para sair", True, highlight_color)
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 80))

    # Partículas
    particles = []
    for _ in range(100):
        particles.append({
            'x': random.randint(0, width),
            'y': random.randint(0, height),
            'radius': random.randint(2, 5),
            'color': (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
            'velocity': random.uniform(0.5, 2.0)
        })

    waiting = True
    while waiting:
        screen.fill(background_color)  # Re-pintar o fundo a cada frame

        # Desenhar elementos de texto
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 150))
        screen.blit(message_text, (width // 2 - message_text.get_width() // 2, height // 2 - 50))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 + 10))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 80))

        # Atualizar e desenhar as partículas de confete
        for particle in particles:
            particle['y'] += particle['velocity']
            if particle['y'] > height:
                particle['y'] = -10  # Reseta a posição para dar efeito de "chuva infinita"
                particle['x'] = random.randint(0, width)
            pygame.draw.circle(screen, particle['color'], (particle['x'], int(particle['y'])), particle['radius'])

        # Atualizar a tela
        pygame.display.flip()

        # Esperar pela entrada do jogador
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

def show_death_screen(screen):
    global running, gameover_sound, ambient_channel
    # Carregar fontes e definir cores
    pygame.font.init()
    ambient_channel.stop()
    gameover_sound.play()
    title_font = pygame.font.Font(None, 80)  # Fonte maior para o título
    text_font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 30)

    # Cores sombrias e perturbadoras
    background_color = (0, 0, 0)  # Preto
    title_color = (200, 0, 0)  # Vermelho sangue
    text_color = (255, 255, 255)  # Branco
    highlight_color = (255, 0, 0)  # Vermelho intenso para destaques
    shadow_color = (50, 50, 50)  # Sombras sombrias

    # Preencher a tela com uma cor de fundo escura
    screen.fill(background_color)

    # Distorção no título para criar um efeito perturbador
    shadow_offset = 10
    title_text = title_font.render("VOCÊ MORREU", True, shadow_color)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2 + random.randint(-5, 5), height // 3 - 150 + random.randint(-5, 5)))
    title_text = title_font.render("VOCÊ MORREU", True, title_color)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3 - 150))

    # Instruções para o jogador, destacando o que fazer
    restart_text = text_font.render("Pressione 'R' para reiniciar ou qualquer outra tecla para sair", True, highlight_color)
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 100))

    # Efeito de partículas flutuantes e aleatórias para criar um clima de desolação
    particles = []
    for _ in range(100):
        gray_value = random.randint(50, 100)  # Gera um valor de cinza entre 50 e 100 (escuro)
        particles.append({
            'x': random.randint(0, width),
            'y': random.randint(0, height),
            'radius': random.randint(2, 5),
            'color': (gray_value, gray_value, gray_value),
            'velocity': random.uniform(0.5, 2.0)
        })

    waiting = True
    while waiting:
        screen.fill(background_color)  # Re-pintar o fundo a cada frame

        # Desenhar elementos de texto com distorção
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3 - 150))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 100))

        # Atualizar e desenhar partículas flutuantes para aumentar o efeito de terror
        for particle in particles:
            particle['y'] += particle['velocity']
            if particle['y'] > height:
                particle['y'] = -10  # Reseta a posição para dar efeito de "chuva infinita"
                particle['x'] = random.randint(0, width)
            pygame.draw.circle(screen, particle['color'], (particle['x'], int(particle['y'])), particle['radius'])

        # Efeito de tremor
        shake_offset_x = random.randint(-5, 5)
        shake_offset_y = random.randint(-5, 5)
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2 + shake_offset_x, height // 3 - 150 + shake_offset_y))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2 + shake_offset_x, height // 2 + 100 + shake_offset_y))

        # Atualizar a tela
        pygame.display.flip()

        # Esperar pela entrada do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # Reinicia o jogo
                    running = True
                    restart_game()  # Sua função para reiniciar o jogo
                else:
                    pygame.quit()
                    sys.exit()

        # Limita a taxa de quadros para não sobrecarregar o processamento
        pygame.time.Clock().tick(60)

def update(dt):
    global hero_anim_frame, hero_pos, hero_anim_time, direction, camera_offset, zumbi_pos_list, lama_pos_list, running, vida, last_collision_time, zumbi_speed_list, is_attacking, attack_time, item_coletado, vitoria, item_pos, hero_speed, damage_time, isMoving, walk_channel, walk_sound, potion_sound, sword_channel, damage_sound, kill_sound
    keys = pygame.key.get_pressed()

    isMoving = False
    if keys[pygame.K_r]:
        restart_game()
    if keys[pygame.K_e]:
        use_pocao_vida()
    if keys[pygame.K_d] and hero_pos[0] < 2800:
        isMoving = True
        hero_pos[0] += hero_speed * dt
        direction = "right"
        hero_anim_time += dt
        if hero_anim_time > 100:
            hero_anim_frame = (hero_anim_frame + 1) % len(hero_walk[direction])
            hero_anim_time = 0
    elif keys[pygame.K_a] and hero_pos[0] > 0:
        hero_pos[0] -= hero_speed * dt
        isMoving = True
        direction = "left"
        hero_anim_time += dt
        if hero_anim_time > 100:
            hero_anim_frame = (hero_anim_frame + 1) % len(hero_walk[direction])
            hero_anim_time = 0
    elif keys[pygame.K_w] and hero_pos[1] > -10:
        hero_pos[1] -= hero_speed * dt
        isMoving = True
        hero_anim_time += dt
        if hero_anim_time > 100:
            hero_anim_frame = (hero_anim_frame + 1) % len(hero_walk[direction])  # Mantém a direção atual (esquerda ou direita)
            hero_anim_time = 0
    elif keys[pygame.K_s] and hero_pos[1] < 440:
        hero_pos[1] += hero_speed * dt
        isMoving = True
        hero_anim_time += dt
        if hero_anim_time > 100:
            hero_anim_frame = (hero_anim_frame + 1) % len(hero_walk[direction])  # Mantém a direção atual (esquerda ou direita)
            hero_anim_time = 0
    else:
        hero_anim_frame = 0
        hero_anim_time = 0

    if isMoving:
        if not walk_channel.get_busy():
            walk_channel.play(walk_sound, loops=-1)  # Toca o som de andar em loop enquanto o personagem se move  # Para o som de andar quando o personagem parar
    else:
        walk_channel.stop()
    
    for i, lama_pos in enumerate(lama_pos_list):
        lama_rect = pygame.Rect(lama_pos[0], lama_pos[1], tile_size, tile_size)
        hero_rect = pygame.Rect(hero_pos[0], hero_pos[1] + 18, tile_size * 0.7, tile_size * 0.8)

        # Se o herói "ver" o monstro (colidindo com a visão)
        if hero_rect.colliderect(lama_rect.inflate(450, 450)):
            lama_ativo_list[i] = True

    hero_rect = pygame.Rect(hero_pos[0], hero_pos[1] + 18, tile_size * 0.7, tile_size * 0.8)

    current_time = pygame.time.get_ticks()
    if current_time - last_collision_time > collision_delay:
        if check_collision_with_spike(hero_rect):
            vida -= 1
            damage_sound.play()
            last_collision_time = current_time
            is_damaged = True  # Define o estado de dano
            damage_time = current_time  # Registra o momento do dano

    if not item_coletado:
        item_rect = pygame.Rect(item_pos[0], item_pos[1], tile_size, tile_size)
        if hero_rect.colliderect(item_rect):
            item_coletado = True
            hero_speed = 0.15

    if flag_pos is not None and item_coletado:
        flag_rect = pygame.Rect(flag_pos[0], flag_pos[1], tile_size, tile_size)
        if hero_rect.colliderect(flag_rect):
            vitoria = True

    check_collision_with_coin(hero_rect)
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  # Botão esquerdo do mouse pressionado
        is_attacking = True
        attack_time = pygame.time.get_ticks()
        if not check_attack():  # Continue verificando se acertou algum monstro
            if not sword_channel.get_busy():
                sword_channel.play(sword_sound)
        else:
            kill_sound.play()
       

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
    for i, lama_pos in enumerate(lama_pos_list):
        # Atualiza o tempo de animação
        lama_anim_time_list[i] += dt
        if lama_anim_time_list[i] > 200:  # Trocar frame a cada 200 ms
            lama_anim_frame_list[i] = (lama_anim_frame_list[i] + 1) % len(lama_walk)
            lama_anim_time_list[i] = 0

        # Atualiza a posição do lama se ele estiver ativo
        if lama_ativo_list[i]:  # Verifica se o lama está ativo
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
                damage_sound.play()
                last_collision_time = current_time

    # Verifica colisão com os monstros de lama
    for lama_pos in lama_pos_list:
        lama_rect = pygame.Rect(lama_pos[0], lama_pos[1], tile_size, tile_size)
        if current_time - last_collision_time > collision_delay:
            if hero_rect.colliderect(lama_rect):
                vida -= 1
                damage_sound.play()
                last_collision_time = current_time

    if current_time - damage_time > 500:  # O estado de dano dura 500 ms
        is_damaged = False

    if vida == 0:
        running = False
        walk_channel.stop()
        show_death_screen(screen)

    if vitoria:
        running = False
        walk_channel.stop()
        show_end_screen(screen, "Você venceu! Pressione qualquer tecla para sair.")

def draw_screen(screen):
    global direction, is_damaged
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
                
    if is_damaged:
        screen.blit(hero_damage_img, (width // 2, height // 2))
    elif is_attacking:
        if direction == 'right':
            screen.blit(hero_attack_imgRight, (width // 2, height // 2))
        elif direction == 'left':
            screen.blit(hero_attack_imgLeft, (width // 2, height // 2))
    else:
        screen.blit(hero_walk[direction][hero_anim_frame], (width // 2, height // 2))

    # Desenha os zumbis
    for i, zumbi_pos in enumerate(zumbi_pos_list):
        zumbi_frame = zumbi_walk[zumbi_anim_frame_list[i]]
        screen.blit(zumbi_frame, (zumbi_pos[0] - camera_offset[0], zumbi_pos[1] - camera_offset[1]))

    # Desenha os monstros de lama
    for i, lama_pos in enumerate(lama_pos_list):
        lama_frame = lama_walk[lama_anim_frame_list[i]]  # Pega o frame atual do lama
        screen.blit(lama_frame, (lama_pos[0] - camera_offset[0], lama_pos[1] - camera_offset[1]))

    # Desenha o retânguloS de colisão do personagem principal
    hero_rect = pygame.Rect(hero_pos[0], hero_pos[1]+18, tile_size*0.7, tile_size * 0.8)
    #pygame.draw.rect(screen, (0, 255, 0), (hero_rect.x - camera_offset[0], hero_rect.y - camera_offset[1], hero_rect.width, hero_rect.height), 2)

    # Desenha os corações de vida
    for i in range(vida):
        screen.blit(coracaoCheio,(i*65,10))
    
    for i in range(3 - vida):
        screen.blit(coracaoVazio, ((2 - i) * 65, 10))
    
    if not item_coletado and item_pos is not None:
        item_img = pygame.image.load("princess.png")
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
