import random
import pygame

def load_dict(file_name):
    file = open(file_name)
    words = file.readlines()
    file.close()
    return [word[:5].upper() for word in words]

DICT_GUESSING = load_dict("dict_all.txt")
DICT_ANSWERS = load_dict("dict_eng.txt")
ANSWER = random.choice(DICT_ANSWERS)

WIDTH = 600
HEIGHT = 700

MARGIN = 10
T_MARGIN, B_MARGIN, LR_MARGIN  = 100, 100, 100

INPUT = ''
GUESSES = []
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÑ"
UNGUESSED = ALPHABET
GAME_OVER = False   

GREY = (70, 70, 80)
GREEN = (6, 214, 160)
YELLOW = (255, 209, 102)

pygame.init()
pygame.font.init()
pygame.display.set_caption("Wordle")
"""
Size of a individual square, it takes into account
the margins between squares and the margins left and right.
It's divided by 5 because by default wordle is 5 letters
"""
SQ_SIZE = (WIDTH - 4*MARGIN - 2*LR_MARGIN) // 5

FONT = pygame.font.SysFont("free sans bold", SQ_SIZE)
FONT_SMALL = pygame.font.SysFont("free sans bold", SQ_SIZE//2)

def determine_unguessed_letters(guesses):
    guessed_letters = ''.join(guesses)
    unguessed_letters = ''
    for letter in ALPHABET:
        if letter not in guessed_letters:
            unguessed_letters = unguessed_letters + letter
    return unguessed_letters

def determine_color(guess, j):
    letter = guess[j]
    if letter == ANSWER[j]:
        return GREEN
    elif letter in ANSWER:
        """
        Count how often the letter we are working with appears
        in the answer
        """
        n_target = ANSWER.count(letter)
        # Count how often that letter was in the correct position
        n_correct = 0
        # Highligthed already 
        n_ocurrence = 0
        for i in range(5):
            if guess[i] == letter:
                if i <= j:
                    n_ocurrence += 1
                if letter == ANSWER[i]:
                    n_correct += 1
        if n_target - n_correct - n_ocurrence >= 0:
            return YELLOW
    return GREY

# Create Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Animation loop
ANIMATING = True

while ANIMATING:

    # background
    screen.fill("white")
    # Draw unguessed letters, the top thingis
    letters = FONT_SMALL.render(UNGUESSED, False, GREY)
    surface = letters.get_rect(center = (WIDTH//2,
                                        T_MARGIN//2))
    screen.blit(letters, surface)
    # Draw guesses
    y =  T_MARGIN
    # Size matrix
    # Number of guesses
    for i in range(6): 
        x = LR_MARGIN
        # Size of word
        for j in range(5):
              
            # Draw Squares
            square = pygame.Rect( x, y, SQ_SIZE, SQ_SIZE )
            pygame.draw.rect(screen, GREY, square, width=2,
                             border_radius= 3)

            # Letters/words that have already been guessed
            if i < len(GUESSES):
                color = determine_color(GUESSES[i], j)
                pygame.draw.rect(screen, color, square, border_radius= 3)
                letter = FONT.render(GUESSES[i][j], False, (255,255,255))
                surface = letter.get_rect(center = (x + SQ_SIZE//2,
                                                    y + SQ_SIZE//2))
                screen.blit(letter, surface)
            # User text input (next guess)
            if i == len(GUESSES) and j < len(INPUT):
                # Colors of the letter to be typed
                letter = FONT.render(INPUT[j], False, GREY)
                surface = letter.get_rect(center = (x + SQ_SIZE//2,
                                                    y + SQ_SIZE//2))
                screen.blit(letter, surface)

            x += SQ_SIZE + MARGIN
        y += SQ_SIZE + MARGIN
    # Show the correct anser after a game over
    if len(GUESSES) == 6 and GUESSES[5] != ANSWER:
        GAME_OVER = True
        letters = FONT.render(ANSWER, False, GREY)
        surface = letters.get_rect(center = (WIDTH//2,
                                            HEIGHT - B_MARGIN//2 - MARGIN))
        screen.blit(letters, surface)

    # update the screen
    pygame.display.flip()
    # Track user interaction 
    for event in pygame.event.get():

        # Closign the window
        if event.type == pygame.QUIT:
            ANIMATING = False
        # User presses key
        elif event.type == pygame.KEYDOWN: 
             # Close game
            if event.key == pygame.K_ESCAPE:
                ANIMATING = False
            # Backspace to correct user input
            if event.key == pygame.K_BACKSPACE:
                if len(INPUT) > 0:
                    INPUT = INPUT[: len(INPUT) - 1]
            # Press return key to submit a guess
            elif event.key == pygame.K_RETURN:
                # Only if is a valid 5 letter word
                # TODO: Esto es importante porque acá se hace la 
                # búsqueda para que sea una palabra válida
                if len(INPUT) == 5 and INPUT in DICT_GUESSING:
                    GUESSES.append(INPUT)
                    UNGUESSED = determine_unguessed_letters(GUESSES)
                    GAME_OVER = True if INPUT == ANSWER else False
                    INPUT = ""

            # Spacebar to restart
            elif event.key == pygame.K_SPACE:
                GAME_OVER = False
                GUESSES = []
                UNGUESSED = ALPHABET
                INPUT = ''
                ANSWER = random.choice(DICT_ANSWERS)
            # Regular text input
            elif len(INPUT) < 5 and not GAME_OVER:
                INPUT = INPUT + event.unicode.upper()