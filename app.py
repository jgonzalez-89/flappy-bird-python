import os
import pygame
import random
import argparse
from pygame.locals import *
import sys

# Configuración inicial
pygame.init()
WIDTH, HEIGHT = 288, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Imágenes
IMAGENES, HITMASKS = {}, {}

bird = pygame.image.load(os.path.join("assets", "bird.png"))
bg = pygame.image.load(os.path.join("assets", "bg.png"))
pipe_image = pygame.image.load(os.path.join("assets", "pipe.png"))
pipe_image = pygame.transform.scale(pipe_image, (52, 512))
ground = pygame.image.load(os.path.join("assets", "base.png"))
ground = pygame.transform.scale(ground, (WIDTH, 100))

# Funciones
def create_pipe(x_pos, pipe_gap):
    pipe_height = random.randint(200, HEIGHT - pipe_gap - 100)
    pipe_offset = pipe_gap
    return [x_pos, pipe_height, pipe_height + pipe_offset]

# Pipes
pipes = []
pipe_gap = 200
for i in range(3):
    pipes.append(create_pipe(WIDTH + i * pipe_gap, pipe_gap))

def move_pipes(pipes):
    for pipe in pipes:
        pipe[0] -= 5


def collision(pipes, bird_collision_rect, ground_collision_rect):
    for pipe in pipes:
        upper_pipe_rect = pygame.Rect(pipe[0], 0, 52, pipe[1])
        lower_pipe_rect = pygame.Rect(pipe[0], pipe[2], 52, HEIGHT - pipe[2])

        # Solo verifica las tuberías que están en la pantalla
        if pipe[0] < WIDTH and pipe[0] + 52 > 0:
            if bird_collision_rect.colliderect(upper_pipe_rect) or bird_collision_rect.colliderect(lower_pipe_rect):
                return True
    if bird_collision_rect.top < 0 or bird_collision_rect.colliderect(ground_collision_rect):
        return True
    return False


def reset_game():
    global bird_rect, bird_movement, pipes, score

    pipes.clear()
    for i in range(3):
        pipes.append(create_pipe(WIDTH + i * pipe_gap, pipe_gap))
    bird_rect = bird.get_rect(center=(50, HEIGHT // 2))
    bird_movement = 0
    score = 0
    return bird_rect

def draw_score(score):
    display_score = score // 10
    score_digits = [int(x) for x in str(display_score)]
    total_width = 0

    for digit in score_digits:
        total_width += IMAGENES["numbers"][digit].get_width()

    x_offset = (WIDTH - total_width) // 2

    for digit in score_digits:
        WIN.blit(IMAGENES["numbers"][digit], (x_offset, HEIGHT * 0.1))
        x_offset += IMAGENES["numbers"][digit].get_width()


def main():
    global clock

    parser = argparse.ArgumentParser("flappy.py")
    parser.add_argument("--fps", type=int, default=60,
                        help="FPS (default: 60)")
    parser.add_argument("--dump_hitmasks", action="store_true",
                        help="dump hitmasks to file and exit")
    args = parser.parse_args()
    FPS = args.fps

    clock = pygame.time.Clock()

    IMAGENES["numbers"] = (
        pygame.image.load(os.path.join("assets", "0.png")).convert_alpha(),
        pygame.image.load(os.path.join("assets", "1.png")).convert_alpha(),
        pygame.image.load(os.path.join("assets", "2.png")).convert_alpha(),
        pygame.image.load(os.path.join("assets", "3.png")).convert_alpha(),
        pygame.image.load(os.path.join("assets", "4.png")).convert_alpha(),
        pygame.image.load(os.path.join("assets", "5.png")).convert_alpha(),
        pygame.image.load(os.path.join("assets", "6.png")).convert_alpha(),
        pygame.image.load(os.path.join("assets", "7.png")).convert_alpha(),
        pygame.image.load(os.path.join("assets", "8.png")).convert_alpha(),
        pygame.image.load(os.path.join("assets", "9.png")).convert_alpha(),
    )

    IMAGENES["gameover"] = pygame.image.load(
        os.path.join("assets", "gameover.png")).convert_alpha()
    IMAGENES["message"] = pygame.image.load(
        os.path.join("assets", "message.png")).convert_alpha()

    # Main loop
    bird_rect = bird.get_rect(center=(50, HEIGHT // 2))
    gravity = 0.25
    bird_movement = 0
    game_state = "welcome"
    score = 0

    while True:
        game_over = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_movement = 0
                    bird_movement -= 5
                    if game_state == "welcome":
                        game_state = "playing"
                    elif game_state == "gameover":
                        bird_rect = reset_game()
                        bird_movement = 0
                        game_state = "welcome"
                        score = 0

        if game_state == "playing":
            # Incrementa la puntuación
            score += 1

            # Ajusta la velocidad de las tuberías en función de la puntuación
            pipe_speed = min(5 + score // 1000, 15)

            # Ajusta el espacio entre tuberías en función de la puntuación
            adjusted_pipe_gap = max(pipe_gap - score // 1500, 100)

            # Movimiento del pájaro
            bird_movement += gravity
            bird_rect.centery += bird_movement
            bird_collision_rect = pygame.Rect(
                bird_rect.x + bird_rect.width * 0.1,
                bird_rect.y + bird_rect.height * 0.1,
                bird_rect.width * 0.8,
                bird_rect.height * 0.8,
            )

            bird_collision_rect = pygame.Rect(
                bird_rect.x + bird_rect.width * 0.1,
                bird_rect.y + bird_rect.height * 0.1,
                bird_rect.width * 0.8,
                bird_rect.height * 0.8,
            )

            ground_collision_rect = pygame.Rect(0, HEIGHT - ground.get_height(), WIDTH, ground.get_height())
            # Mover tuberías y verificar colisiones
            for pipe in pipes:
                pipe[0] -= pipe_speed
                upper_pipe_rect = pygame.Rect(pipe[0], 0, 52, pipe[1])
                lower_pipe_rect = pygame.Rect(
                    pipe[0], pipe[2], 52, HEIGHT - pipe[2])

                if collision(pipes, bird_collision_rect, ground_collision_rect):
                    game_over = True
                    game_state = "gameover"
            
            # Increase the score
            for pipe in pipes:
                if pipe[0] + pipe_image.get_width() / 2 < bird_rect.centerx < pipe[0] + pipe_image.get_width() / 2 + 5:
                    score += 1

            # Eliminar tuberías que estén fuera de la pantalla
            if pipes[0][0] < -pipe_image.get_width():
                pipes.pop(0)

            # Crear nuevas tuberías
            if pipes[-1][0] < WIDTH - adjusted_pipe_gap:
                pipes.append(create_pipe(WIDTH, adjusted_pipe_gap))

            # Crear nuevas tuberías
            if pipes[-1][0] < WIDTH - pipe_gap:
                pipes.append(create_pipe(WIDTH))

        # Dibujar elementos
        WIN.blit(bg, (0, 0))

        if game_state == "welcome":
            WIN.blit(IMAGENES["message"], (WIDTH // 2 - IMAGENES["message"].get_width() // 2, HEIGHT // 2 - IMAGENES["message"].get_height() // 2))
        elif game_state == "gameover":
            WIN.blit(IMAGENES["gameover"], (WIDTH // 2 - IMAGENES["gameover"].get_width() // 2, HEIGHT // 2 - IMAGENES["gameover"].get_height() // 2))

        WIN.blit(bird, bird_rect)


        # Dibujar tuberías
        for pipe in pipes:
            # Dibujar tubería superior
            WIN.blit(pygame.transform.flip(pipe_image, False, True),
                    (pipe[0], pipe[1] - pipe_image.get_height()))

            # Dibujar tubería inferior
            WIN.blit(pipe_image, (pipe[0], pipe[2]))
            # Dibujar zonas de colisión de las tuberías (Agregar estas líneas)
            pygame.draw.rect(WIN, (255, 0, 0), (pipe[0], 0, 52, pipe[1]), 2)
            pygame.draw.rect(WIN, (255, 0, 0), (pipe[0], pipe[2], 52, HEIGHT - pipe[2]), 2)

        # Dibujar suelo
        WIN.blit(ground, (0, HEIGHT - ground.get_height()))

        draw_score(score)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
