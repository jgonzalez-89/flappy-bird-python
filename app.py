import pygame
import sys
import random

# Configuración inicial
pygame.init()
WIDTH, HEIGHT = 288, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Imágenes
bird = pygame.image.load("./assets/bird.png")
bg = pygame.image.load("./assets/bg.png")
pipe_image = pygame.image.load("./assets/pipe.png")
pipe_image = pygame.transform.scale(pipe_image, (52, 512))
ground = pygame.image.load("./assets/base.png")
ground = pygame.transform.scale(ground, (WIDTH, 100))

# Funciones
def create_pipe(x_pos):
    pipe_height = random.randint(200, HEIGHT - 100)
    pipe_offset = 100
    return [x_pos, pipe_height, pipe_height + pipe_offset]


def random_pipe_heights():
    pipe_height = random.randint(200, HEIGHT - 100)
    pipe_offset = 100
    return pipe_height, pipe_height + pipe_offset


def move_pipes(pipes):
    for pipe in pipes:
        pipe[0] -= 5


def collision(pipes, bird_collision_rect):
    for pipe in pipes:
        upper_pipe_rect = pygame.Rect(pipe[0], 0, 52, pipe[1])
        lower_pipe_rect = pygame.Rect(
            pipe[0], pipe[2], 52, HEIGHT - pipe[2] - ground.get_height())

        # Solo verifica las tuberías que están en la pantalla
        if pipe[0] < WIDTH and pipe[0] + 52 > 0:
            if bird_collision_rect.colliderect(upper_pipe_rect) or bird_collision_rect.colliderect(lower_pipe_rect):
                return True
    if bird_collision_rect.top < 0 or bird_collision_rect.bottom > HEIGHT - ground.get_height():
        return True
    return False


def reset_game():
    pipes.clear()
    for i in range(3):
        pipes.append(create_pipe(WIDTH + i * pipe_gap))
    return bird.get_rect(center=(50, HEIGHT // 2))


# Crear tuberías iniciales
pipes = []
pipe_gap = 200
for i in range(3):
    pipes.append(create_pipe(WIDTH + i * pipe_gap))

# Main loop
bird_rect = bird.get_rect(center=(50, HEIGHT // 2))
gravity = 0.25
bird_movement = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 5

    # Movimiento del pájaro
    bird_movement += gravity
    bird_rect.centery += bird_movement
    bird_collision_rect = pygame.Rect(
        bird_rect.x + bird_rect.width * 0.1,
        bird_rect.y + bird_rect.height * 0.1,
        bird_rect.width * 0.8,
        bird_rect.height * 0.8,
    )

    # Dibujar elementos
    WIN.blit(bg, (0, 0))
    WIN.blit(bird, bird_rect)

    # Mover tuberías
    move_pipes(pipes)

    # Dibujar tuberías
    for pipe in pipes:
        upper_pipe_rect = pygame.Rect(pipe[0], 0, 52, pipe[1])
        lower_pipe_rect = pygame.Rect(
            pipe[0], pipe[2], 52, HEIGHT - pipe[2] - ground.get_height())

        # Dibujar tubería superior
        WIN.blit(pygame.transform.flip(pipe_image, False, True),
                (pipe[0], pipe[1] - pipe_image.get_height()))

        # Dibujar tubería inferior
        WIN.blit(pipe_image, (pipe[0], pipe[2]))

    # Debug: dibujar rectángulos de colisión
    # for pipe in pipes:
    #     upper_pipe_rect = pygame.Rect(pipe[0], 0, 52, pipe[1])
    #     lower_pipe_rect = pygame.Rect(
    #         pipe[0], pipe[2], 52, HEIGHT - pipe[2] - ground.get_height())

    #     pygame.draw.rect(WIN, (255, 0, 0), upper_pipe_rect, 2)
    #     pygame.draw.rect(WIN, (255, 0, 0), lower_pipe_rect, 2)

    # pygame.draw.rect(WIN, (0, 255, 0), bird_collision_rect, 2)

    # Crear nuevas tuberías
    if pipes[-1][0] < WIDTH - pipe_gap + 5:
        pipes.append(create_pipe(WIDTH))

    # Dibujar suelo
    WIN.blit(ground, (0, HEIGHT - ground.get_height()))

    if collision(pipes, bird_collision_rect):
        bird_rect = reset_game()
        bird_movement = 0
        pygame.time.delay(1000)

    pygame.display.update()
    clock.tick(60)
