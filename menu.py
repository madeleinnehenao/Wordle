import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (70, 70, 80)
FONT = pygame.font.Font(None, 36)

# Set up the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle-like Game Menu")

# Function to display text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Function to create buttons
def draw_button(text, x, y, width, height, color, game_mode_text):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, FONT, BLACK, x + 10, y + 10)
    draw_text(game_mode_text, FONT, BLACK, x + 10, y + 30)

# Main menu loop
def main_menu():
    while True:
        screen.fill(WHITE)
        
        draw_text("Wordle-like Game", FONT, BLACK, 280, 50)
        
        # Draw buttons for word lengths
        draw_button("4-Letter Wordle", 300, 150, 200, 50, GREY, "")
        draw_button("5-Letter Wordle", 300, 225, 200, 50, GREY, "")
        draw_button("6-Letter Wordle", 300, 300, 200, 50, GREY, "")
        draw_button("7-Letter Wordle", 300, 375, 200, 50, GREY, "")
        draw_button("8-Letter Wordle", 300, 450, 200, 50, GREY, "")
        
        # Update the display
        pygame.display.update()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 500:
                    if 150 <= mouse_pos[1] <= 200:
                        # Start 4-letter wordle game
                        print("Starting 4-letter wordle game")
                        # Add your code here to start the game with 4-letter words
                    elif 225 <= mouse_pos[1] <= 275:
                        # Start 5-letter wordle game
                        print("Starting 5-letter wordle game")
                        # Add your code here to start the game with 5-letter words
                    elif 300 <= mouse_pos[1] <= 350:
                        # Start 6-letter wordle game
                        print("Starting 6-letter wordle game")
                        # Add your code here to start the game with 6-letter words
                    elif 375 <= mouse_pos[1] <= 425:
                        # Start 7-letter wordle game
                        print("Starting 7-letter wordle game")
                        # Add your code here to start the game with 7-letter words
                    elif 450 <= mouse_pos[1] <= 500:
                        # Start 8-letter wordle game
                        print("Starting 8-letter wordle game")
                        # Add your code here to start the game with 8-letter words

# Run the main menu loop
if __name__ == "__main__":
    main_menu()