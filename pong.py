import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pong game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

BALL_SIZE = 10

player1_x, player1_y = 10, HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_x, player2_y = WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2

ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 4, 4

player1_dy = 0
player2_dy = 0

player1_score = 0
player2_score = 0

font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()

def reset_game():
    global player1_score, player2_score, ball_x, ball_y, ball_dx, ball_dy
    player1_score = 0
    player2_score = 0
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = 4, 4

def show_win_screen(winner):
    screen.fill(BLACK)
    win_text = font.render(f"{winner} Wins!", True, WHITE)
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 100))

    button_text = button_font.render("Start Over", True, WHITE)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    pygame.draw.rect(screen, WHITE, button_rect.inflate(20, 10), 2)  
    screen.blit(button_text, button_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos): 
                    reset_game()
                    waiting = False

def main():
    global player1_dy, player2_dy, player1_y, player2_y, ball_x, ball_y, ball_dx, ball_dy, player1_score, player2_score

    running = True
    while running:
        screen.fill(BLACK) 

        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  
                    player1_dy = -6
                elif event.key == pygame.K_s: 
                    player1_dy = 6
                elif event.key == pygame.K_UP: 
                    player2_dy = -6
                elif event.key == pygame.K_DOWN: 
                    player2_dy = 6
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):  
                    player1_dy = 0
                elif event.key in (pygame.K_UP, pygame.K_DOWN): 
                    player2_dy = 0

        player1_y += player1_dy
        player2_y += player2_dy

        player1_y = max(0, min(HEIGHT - PADDLE_HEIGHT, player1_y))
        player2_y = max(0, min(HEIGHT - PADDLE_HEIGHT, player2_y))

        ball_x += ball_dx
        ball_y += ball_dy

        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_dy *= -1

        if (ball_x <= player1_x + PADDLE_WIDTH and player1_y <= ball_y <= player1_y + PADDLE_HEIGHT) or \
           (ball_x >= player2_x - PADDLE_WIDTH and player2_y <= ball_y <= player2_y + PADDLE_HEIGHT):
            ball_dx *= -1

        if ball_x < 0: 
            player2_score += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx *= -1
        elif ball_x > WIDTH: 
            player1_score += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx *= -1

        if player1_score == 10:
            show_win_screen("Player 1")
        elif player2_score == 10:
            show_win_screen("Player 2")

        pygame.draw.rect(screen, WHITE, (player1_x, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, WHITE, (player2_x, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

        player1_text = font.render(str(player1_score), True, WHITE)
        player2_text = font.render(str(player2_score), True, WHITE)
        screen.blit(player1_text, (WIDTH // 2 - 100, 20))  
        screen.blit(player2_text, (WIDTH // 2 + 50, 20))  

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
