import pygame
import sys
from Wordle4 import *
from Wordle5 import *
from Wordle6 import *
from Wordle7 import *
from Wordle8 import *
from Datos import *

# Constantes para el wordle 4
data_words_4 = Data4()
# Constantes para los diccionarios
DICT_GUESSING_4 = data_words_4.words4()
DICT_ANSWERS_4 = data_words_4.words4()
# Initialize Wordle5 instance
wordle_4 = Wordle4(600, 700, 100, 100, 100, DICT_GUESSING_4, DICT_ANSWERS_4)

# Constantes para el wordle 5
data_words_5 = Data5()
# Constantes para los diccionarios
DICT_GUESSING_5 = data_words_5.words5()
DICT_ANSWERS_5 = data_words_5.words5()
# Initialize Wordle5 instance
wordle_5 = Wordle5(600, 700, 100, 100, 100, DICT_GUESSING_5, DICT_ANSWERS_5)

# Constantes para el wordle 6
data_words_6 = Data6()
# Constantes para los diccionarios
DICT_GUESSING_6 = data_words_6.words6()
DICT_ANSWERS_6 = data_words_6.words6()
# Initialize Wordle5 instance
wordle_6 = Wordle6(600, 700, 100, 100, 100, DICT_GUESSING_6, DICT_ANSWERS_6)

# Constantes para el wordle 7
data_words_7 = Data7()
# Constantes para los diccionarios
DICT_GUESSING_7 = data_words_7.words7()
DICT_ANSWERS_7 = data_words_7.words7()
# Initialize Wordle5 instance
wordle_7 = Wordle7(600, 700, 100, 100, 100, DICT_GUESSING_7, DICT_ANSWERS_7)

# Constantes para el wordle 8
data_words_8 = Data8()
# Constantes para los diccionarios
DICT_GUESSING_8 = data_words_8.words8()
DICT_ANSWERS_8 = data_words_8.words8()
# Initialize Wordle5 instance
wordle_8 = Wordle8(600, 700, 100, 100, 100, DICT_GUESSING_8, DICT_ANSWERS_8)



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
        
        draw_text("Wordle-like Game", FONT, BLACK, 200, 50)
        
        # Draw buttons for word lengths
        draw_button("4-Letter Wordle", 200, 150, 200, 50, GREY, "")
        draw_button("5-Letter Wordle", 200, 225, 200, 50, GREY, "")
        draw_button("6-Letter Wordle", 200, 300, 200, 50, GREY, "")
        draw_button("7-Letter Wordle", 200, 375, 200, 50, GREY, "")
        draw_button("8-Letter Wordle", 200, 450, 200, 50, GREY, "")
        
        # Update the display
        pygame.display.update()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 200 <= mouse_pos[0] <= 400:
                    if 150 <= mouse_pos[1] <= 200:
                        wordle_4.run_game()
                        wordle_4.animating = True
                    elif 225 <= mouse_pos[1] <= 275:
                        wordle_5.run_game()
                        wordle_5.animating = True
                    elif 300 <= mouse_pos[1] <= 350:
                        wordle_6.run_game()
                        wordle_6.animating = True
                    elif 375 <= mouse_pos[1] <= 425:
                        wordle_7.run_game()
                        wordle_7.animating = True
                    elif 450 <= mouse_pos[1] <= 500:
                        # Start 8-letter wordle game
                        wordle_8.run_game()
                        wordle_8.animating = True
                        # Add your code here to start the game with 8-letter words

# Run the main menu loop
if __name__ == "__main__":
    main_menu()