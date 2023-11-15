import sys
import random
import pygame
from Datos import *

class WordleGame:
    def __init__(self):
        # Initialize game attributes
        self.dict_guessing = self.load_dict()
        self.dict_answers = self.load_dict()
        self.answer = ''
        self.input = ''
        self.guesses = []
        self.unguessed = ''
        self.game_over = False
        self.word_length = 5
        # Class data to read the text files
        self.data_4 = Data4()
        self.data_5 = Data5()
        self.data_6 = Data6()
        self.data_7 = Data7()
        self.data_8 = Data8()

        # Pygame initialization
        pygame.init()
        pygame.display.set_caption("Wordle")

        # Define colors
        self.GREY = (70, 70, 80)
        self.GREEN = (6, 214, 160)
        self.YELLOW = (255, 209, 102)
        
        # Font setup
        self.SQ_SIZE = 50  # Change this as needed
        self.FONT = pygame.font.SysFont("Arial", self.SQ_SIZE)
        self.FONT_SMALL = pygame.font.SysFont("Arial", self.SQ_SIZE // 2)
        
        # Screen setup
        self.WIDTH = 600
        self.HEIGHT = 700
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def load_dict(self, size = 4) -> set:
        """
        Esta función lee las palabras válidas para 
        cada uno de los tipos de dificultades. Se leen de los 
        archivos palabras_validas. 

        Args:
            size (int): Tamaño de las palabras a utilizar según el tipo de
        dificultad

        Returns:
            set: Hace un retorno de la data almacenada como un set. Esta se lee desde
        el módulo de Datos
        """
        if size == 4:
            return self.data_4.words4()
        if size == 5:
            return self.data_5.words5()
        if size == 6:
            return self.data_6.words6()
        if size == 7:
            return self.data_7.words7()
        return self.data_8.words8()

    def generate_random_word(self, length) -> str:
        """
        Generates a random word of a specified length from the loaded dictionaries.

        Args:
            size (int): Tamaño de las palabras a utilizar según el tipo de
        dificultad

        Returns:
            str: A random word from the loaded dictionaries with the specified length.
                 Returns None if no word of the given length is found.
        """
        valid_words = self.load_dict(length)
        if valid_words:
            return random.choice(valid_words)
        return None

    def determine_unguessed_letters(self) -> str :
        """
        Determines the unguessed letters based on the guesses made by the player.
        Args:
            None

        Returns:
            str: a string containing the letters that have not been guessed yet.
        """
        guessed_letters = ''.join(self.guesses)
        unguessed_letters = ''
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÑ"
        for letter in alphabet:
            if letter not in guessed_letters:
                unguessed_letters += letter
        return unguessed_letters


    def determine_color(self, guess, j) -> tuple:
        """
        Determines the color for the squares based on the guess made by the player.

        Args:
        guess (str): The guessed word.
        j (int): The index of the character in the guessed word.

        Returns:
        tuple: Returns the color code as a tuple representing RGB values.
        """
        # Get the letter from the guessed word at position j
        letter = guess[j]

        # Check if the guessed letter matches the corresponding letter in the answer
        if letter == self.answer[j]:
            # If it's a correct letter at the correct position, return GREEN
            return self.GREEN
        # If the guessed letter is in the answer but not in the right position
        elif letter in self.answer:
            # Count how many times the guessed letter appears in the answer
            n_target = self.answer.count(letter)
            n_correct = 0  # Counter for correctly placed guessed letters in the answer
            n_ocurrence = 0  # Counter for guessed letters that appear in the answer

            # Loop through the answer to check guessed letters
            for i in range(5):
                # If the guessed letter matches a letter in the answer
                if guess[i] == letter:
                    if i <= j:
                        # If the guessed letter is in a position less than or equal to the current position, increment occurrence
                        n_ocurrence += 1
                    # If the guessed letter is at the same position as in the answer, increment the correct counter
                    if letter == self.answer[i]:
                        n_correct += 1

            # If there are remaining occurrences of the guessed letter not counted as correct or occurrences, return YELLOW
            if n_target - n_correct - n_ocurrence >= 0:
                return self.YELLOW

        # If the guessed letter is not in the answer or in the wrong position, return GREY
        return self.GREY
    

    def set_word_length(self, length):
        """
        Sets the word length for the game.

        Args:
            length (int): The length of the word to be guessed.

        Returns:
            None
        """
        self.word_length = length
        # Reset input field when word length changes
        self.input = ''  


    def reset_game(self):
        """
        Resets the game attributes for a new game.

        Args:
            None

        Returns:
            None
        """
        self.answer = self.generate_random_word(self.word_length)
        self.input = ''
        self.guesses = []
        self.unguessed = self.determine_unguessed_letters()
        self.game_over = False


    def update_game(self):
        """
        Updates the game logic based on user input and events.

        Handles key events for backspace, entering guesses, restarting the game,
        and accepting text input within the specified word length.

        Quits the game if the user closes the window or presses Escape.

        Returns:
            None
        """
        for event in pygame.event.get():
            # Quit game event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard event handling
            elif event.type == pygame.KEYDOWN:
                # Exit game on Escape key
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Backspace to correct input
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.input) > 0:
                        self.input = self.input[:-1]

                # Submitting a guess on Return key press
                elif event.key == pygame.K_RETURN:
                    if len(self.input) == self.word_length and self.input in self.dict_guessing:
                        self.guesses.append(self.input)
                        self.unguessed = self.determine_unguessed_letters()
                        self.game_over = True if self.input == self.answer else False
                        self.input = ""

                # Restart game on Space key press
                elif event.key == pygame.K_SPACE:
                    self.reset_game()

                # Accept text input if conditions are met for the current word length
                elif len(self.input) < self.word_length and not self.game_over:
                    self.input += event.unicode.upper()
    

    def draw_elements(self):
        """
        Draws the game elements including squares and letters on the screen.

        Args:
            None

        Returns:
            None
        """
        # Constants for grid layout
        MARGIN = 10
        T_MARGIN, B_MARGIN, LR_MARGIN = 100, 100, 100

        # Calculate word length and number of guesses
        word_length = len(self.answer)
        num_guesses = 5

        # Calculate square size based on word length
        SQ_SIZE = (self.WIDTH - 4 * MARGIN - 2 * LR_MARGIN) // word_length

        # Loop through guesses to draw the game elements
        for i in range(num_guesses + 1):  # +1 for the input row
            y = T_MARGIN + i * (SQ_SIZE + MARGIN)
            for j in range(word_length):
                x = LR_MARGIN + j * (SQ_SIZE + MARGIN)
                
                # Draw Squares
                square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(self.screen, self.GREY, square, width=2, border_radius=3)

                # Draw guessed letters
                if i < num_guesses:
                    color = self.determine_color(self.guesses[i], j)
                    pygame.draw.rect(self.screen, color, square, border_radius=3)
                    letter = self.FONT.render(self.guesses[i][j], False, (255, 255, 255))
                    surface = letter.get_rect(center=(x + SQ_SIZE // 2, y + SQ_SIZE // 2))
                    self.screen.blit(letter, surface)
                # Draw input row
                elif i == num_guesses:
                    if j < len(self.input):
                        letter = self.FONT.render(self.input[j], False, self.GREY)
                        surface = letter.get_rect(center=(x + SQ_SIZE // 2, y + SQ_SIZE // 2))
                        self.screen.blit(letter, surface)

        # Draw the correct answer if the game is over
        if self.game_over:
            letters = self.FONT.render(self.answer, False, self.GREY)
            surface = letters.get_rect(center=(self.WIDTH // 2, self.HEIGHT - B_MARGIN // 2 - MARGIN))
            self.screen.blit(letters, surface)


def run_game(self):
    # Main game loop to manage game states (intro, main game, etc.)
    clock = pygame.time.Clock()
    
    while True:
        # Update game logic
        self.update_game()

        # Draw game elements
        self.draw_elements()

        # Update display
        pygame.display.flip()

        # Set frame rate
        clock.tick(60)  # Adjust the frame rate as needed (60 FPS in this case)

# Start the game
if __name__ == "__main__":
    wordle_game = WordleGame()
    wordle_game.run_game()