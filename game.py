import pygame

width = 64 * 14
height = 64 * 10
tile_size = 64
mapa = []
tile = {}
hero_walk = {"right": [],"left": []}
direction = "right"
hero_anim_frame = 0
hero_pos = [300, 0]
hero_speed = 0.2
hero_anim_time = 0
camera_offset = [0, 0]

def load_mapa(filename):
    global mapa
    with open(filename, "r") as file:
        for line in file.readlines():
            mapa.append(line.strip())

def load():
    global clock, tile, hero_walk
    for i in range(0, 4):
        hero_walk["right"].append(pygame.image.load(f"knight_f_run_anim_f{i}.png"))
    for i in range(4, 8):
        hero_walk["left"].append(pygame.image.load(f"knight_f_run_anim_f{i}.png"))

    tile['C'] = pygame.image.load("chao1.png")
    tile['V'] = pygame.image.load("chao2.png")
    tile['B'] = pygame.image.load("chao3.png")
    tile['E'] = pygame.image.load("espinho.png")

    clock = pygame.time.Clock()
    load_mapa("mapa.txt")

def check_collision_with_water(hero_rect):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == 'A':
                tile_rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
                if hero_rect.colliderect(tile_rect):
                    return True
    return False

def update(dt):
    global hero_anim_frame, hero_pos, hero_anim_time, direction, camera_offset
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
        return

    hero_rect = pygame.Rect(hero_pos[0]+30, hero_pos[1], tile_size, tile_size * 2)

    if check_collision_with_water(hero_rect):
        hero_pos = old_pos

    hero_anim_time += dt
    if hero_anim_time > 100:
        hero_anim_frame = (hero_anim_frame + 1) % len(hero_walk[direction])
        hero_anim_time = 0

    camera_offset[0] = hero_pos[0] - width // 2
    camera_offset[1] = hero_pos[1] - height // 2

def draw_screen(screen):
    screen.fill((0, 0, 0))
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            tile_type = mapa[i][j]
            if tile_type in tile:
                screen.blit(tile[tile_type], 
                            (j * tile_size - camera_offset[0], i * tile_size - camera_offset[1]))
    
    screen.blit(hero_walk[direction][hero_anim_frame], 
                (width // 2, height // 2))

    hero_rect = pygame.Rect(hero_pos[0]+30, hero_pos[1], tile_size, tile_size * 2)

def main_loop(screen):
    global clock
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
