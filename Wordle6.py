import random
import pygame
from Datos import Data6

data_words = Data6()

class Wordle6:
    def __init__(self, width, height, t_margin, b_margin, lr_margin, dict_guessing, dict_answers):
        self.width = width
        self.height = height
        self.t_margin = t_margin
        self.b_margin = b_margin
        self.lr_margin = lr_margin
        self.dict_guessing = dict_guessing
        self.dict_answers = dict_answers
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÑ"
        self.answer = random.choice(list(self.dict_answers))
        self.margin = 15
        self.sq_size = (self.width - 4 * self.margin - 2 * self.lr_margin) // 6
        self.input_text = ''
        self.guesses = []
        self.unguessed = self.alphabet[:]
        self.game_over = False

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Wordle")
        self.font = pygame.font.SysFont("free sans bold", self.sq_size)
        self.font_small = pygame.font.SysFont("free sans bold", self.sq_size // 2)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.animating = True



    def determine_unguessed_letters(self):
        guessed_letters = ''.join(self.guesses)
        self.unguessed = ''
        for letter in self.alphabet:
            if letter not in guessed_letters:
                self.unguessed += letter

    def determine_color(self, guess, j):
        letter = guess[j]
        if letter == self.answer[j]:
            return (6, 214, 160)  # GREEN
        elif letter in self.answer:
            n_target = self.answer.count(letter)
            n_correct = 0
            n_ocurrence = 0
            for i in range(6):
                if guess[i] == letter:
                    if i <= j:
                        n_ocurrence += 1
                    if letter == self.answer[i]:
                        n_correct += 1
            if n_target - n_correct - n_ocurrence >= 0:
                return (255, 209, 102)  # YELLOW
        return (70, 70, 80)  # GREY
    
    def show_modal_message(self, message):
        modal_font = pygame.font.SysFont("Arial", 20)
        modal_width = 300
        modal_height = 150

        modal_surface = pygame.Surface((modal_width, modal_height))
        modal_surface.fill((167, 204, 177))  # Background color for the modal

        text = modal_font.render(message, True, (0, 0, 0))  # Text color: black
        text_rect = text.get_rect(center=(modal_width // 2, modal_height // 2))

        modal_surface.blit(text, text_rect)

        modal_x = (self.width - modal_width) // 2
        modal_y = (self.height - modal_height) // 2

        self.screen.blit(modal_surface, (modal_x, modal_y))
        pygame.display.flip()

    
    def draw_bottom_message(self, message):
        bottom_message_font = pygame.font.SysFont("Arial", 20)
        bottom_message_width = 300
        bottom_message_height = 100

        bottom_message_surface = pygame.Surface((bottom_message_width, bottom_message_height))
        bottom_message_surface.fill((207, 205, 182))  # Background color for the modal

        text = bottom_message_font.render(message, True, (0, 0, 0))  # Text color: black
        text_rect = text.get_rect(center=(bottom_message_width // 2, bottom_message_height // 2))

        bottom_message_surface.blit(text, text_rect)

        bottom_message_x = (self.width - bottom_message_width) // 2
        bottom_message_y = (self.height - bottom_message_height) // 2

        self.screen.blit(bottom_message_surface, (bottom_message_x, bottom_message_y))
        pygame.display.flip()



    def run_game(self):
        while self.animating:
            self.screen.fill("white")

            # Draw unguessed letters
            letters = self.font_small.render(self.unguessed, False, (70, 70, 80))
            surface = letters.get_rect(center=(self.width // 2, self.t_margin // 2))
            self.screen.blit(letters, surface)

            y = self.t_margin
            for i in range(6):
                x = self.lr_margin
                for j in range(6):
                    square = pygame.Rect(x, y, self.sq_size, self.sq_size)
                    pygame.draw.rect(self.screen, (70, 70, 80), square, width=2, border_radius=3)

                    if i < len(self.guesses):
                        color = self.determine_color(self.guesses[i], j)
                        pygame.draw.rect(self.screen, color, square, border_radius=3)
                        letter = self.font.render(self.guesses[i][j], False, (255, 255, 255))
                        surface = letter.get_rect(center=(x + self.sq_size // 2, y + self.sq_size // 2))
                        self.screen.blit(letter, surface)

                    if i == len(self.guesses) and j < len(self.input_text):
                        letter = self.font.render(self.input_text[j], False, (70, 70, 80))
                        surface = letter.get_rect(center=(x + self.sq_size // 2, y + self.sq_size // 2))
                        self.screen.blit(letter, surface)

                    x += self.sq_size + self.margin 
                y += self.sq_size + self.margin + 10

            if len(self.guesses) == 6 and self.guesses[6] != self.answer:
                self.game_over = True
                letters = self.font.render(self.answer, False, (70, 70, 80))
                surface = letters.get_rect(center=(self.width // 2, self.height - self.b_margin // 2 - self.margin))
                self.screen.blit(letters, surface)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.animating = False
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        self.animating = False

                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.input_text) > 0:
                            self.input_text = self.input_text[ : len(self.input_text) - 1]

                    elif event.key == pygame.K_RETURN:
                        if len(self.input_text) == 6:
                            if self.input_text in self.dict_guessing:
                                self.guesses.append(self.input_text)
                                self.determine_unguessed_letters()
                                self.game_over = True if self.input_text == self.answer else False
                                if self.game_over:
                                    self.show_modal_message("Great, you win!. Press space to restart")
                                    pygame.time.delay(2000)  # Display the winning message for 2 seconds
                                    self.game_over = False  # Reset the game-over state
                                self.input_text = ""
                            else:
                                self.draw_bottom_message('The word is not valid')
                                pygame.time.delay(1000)  # Display the winning message for 2 seconds
                        
                                    
                    
                    elif event.key == pygame.K_SPACE:
                        self.game_over = False
                        self.guesses = []
                        self.unguessed = self.alphabet
                        self.input_text = ''
                        self.answer = random.choice(list(self.dict_answers))

                    elif len(self.input_text) < 6 and not self.game_over:
                        self.input_text += event.unicode.upper()
                    
        pygame.quit()


# Constants
DICT_GUESSING = data_words.words6()
DICT_ANSWERS = data_words.words6()


# Initialize Wordle5 instance
wordle = Wordle6(600, 700, 80, 80, 80, DICT_GUESSING, DICT_ANSWERS)
print(wordle.answer)
wordle.run_game()
