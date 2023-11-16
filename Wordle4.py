import random
import pygame

class Wordle4:
    """
    Clase para generar un juego de Wordle con 4 Letras. 
    """
    def __init__(self, width, height, t_margin, b_margin, lr_margin, dict_guessing, dict_answers):
        """
        Inicializa una instancia de Wordle4.

        Args:
            width (int): Ancho de la ventana del juego.
            height (int): Alto de la ventana del juego.
            t_margin (int): Margen superior.
            b_margin (int): Margen inferior.
            lr_margin (int): Márgenes izquierdo y derecho.
            dict_guessing (set): Conjunto de palabras para adivinar.
            dict_answers (set): Conjunto de palabras de respuesta.
        """
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
        self.sq_size = (self.width - 4 * self.margin - 2 * self.lr_margin) // 5
        self.input_text = ''
        # Se utiliza para almacenar los intentos que el jugador realiza durante
        # el juego para adivinar la palabra objetivo.
        self.guesses = []
        # Se utiliza para almacenar las letras que no han sido usadas
        self.unguessed = self.alphabet[:]
        self.game_over = False
        self.game_lost = False
        #Contadores de aciertos y fallas
        self.aciertos=0
        self.fallos=0

        # Inicializa el pygame.
        pygame.font.init()
        pygame.display.set_caption("Wordle")
        self.font = pygame.font.SysFont("free sans bold", self.sq_size)
        self.font_small = pygame.font.SysFont("free sans bold", self.sq_size // 3)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.animating = True


    def close_game(self):
        """
        Function to close the game.
        """
        self.animating = False

    def draw_close_button(self):
        """
        Draws a button to close the game in the upper left corner.
        """
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(10, 10, 55, 25), border_radius = 3 )
        close_text = self.font_small.render("Close", True, (255, 255, 255))
        self.screen.blit(close_text, (15, 15))

    def draw_aciertos(self) -> None:
        """
        Dibuja un recuadro al fondo de la pantalla con la cantidad de aciertos.
        """

        pygame.draw.rect(self.screen, (6, 214, 160), pygame.Rect(160, 670, 120, 30),
                         border_radius= 3)
        fallos_text = self.font_small.render(f"Aciertos: {self.aciertos}", True, (255, 255, 255))
        self.screen.blit(fallos_text, (180, 675))


    def draw_fallos(self) -> None:
        """
        Dibuja un recuadro al fondo de la pantalla con la cantidad de fallos.
        """

        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(300, 670, 120, 30),
                         border_radius=3)
        fallos_text = self.font_small.render(f"Fallos: {self.fallos}", True, (255, 255, 255))
        self.screen.blit(fallos_text, (320, 675))

    def determine_unguessed_letters(self) -> None:
        """
        Determina las letras no adivinadas y actualiza la lista 'unguessed'.

        Esta función se utiliza para actualizar la lista 'unguessed', que contiene
        las letras del alfabeto que aún no han sido adivinadas por el jugador.
        
        Args:
        None

        Returns:
        None
        """
        guessed_letters = ''.join(self.guesses)
        self.unguessed = ''
        for letter in self.alphabet:
            if letter not in guessed_letters:
                self.unguessed += letter


    def determine_color(self, guess:str, j:int) -> tuple:
        """
        Determina el color del cuadrado según la letra adivinada.

        Esta función determina el color del cuadrado en función de la letra adivinada
        y su posición con respecto a la respuesta correcta.

        Args:
            guess (str): La suposición actual del jugador (cadena de letras).
            j (int): Índice de la letra actual en la suposición.

        Returns:
            tuple: Tupla que representa el color RGB del cuadrado.
        """
        letter = guess[j]

        # Si la letra en la suposición coincide con la respuesta en la misma posición, devuelve VERDE
        if letter == self.answer[j]:
            return (6, 214, 160)  # Verde (6, 214, 160)

        # Si la letra está en la respuesta, pero no en la misma posición, comprueba la ocurrencia
        elif letter in self.answer:
            # Determina cuántas veces aparece la letra adivinada en toda la respuesta. n_target guarda este recuento.
            n_target = self.answer.count(letter)
            # cantidad de ocurrencias correctas 
            n_correct = 0
            # cantidad de ocurrencias de la letra en posiciones anteriores a j.
            n_ocurrence = 0

            # Itera para contar las ocurrencias y letras correctas en diferentes posiciones
            for i in range(4):
                if guess[i] == letter:
                    # Esto es importante para contar las ocurrencias que ya se han mostrado
                    #  al jugador en iteraciones anteriores.
                    if i <= j:
                        n_ocurrence += 1
                    # Comprueba si la letra adivinada (letter) en la posición i
                    #  coincide con la letra correspondiente en la respuesta
                    if letter == self.answer[i]:
                        n_correct += 1
            
            # Si las ocurrencias totales - ocurrencias correctas - ocurrencias ya mostradas son >= 0, devuelve AMARILLO
            if n_target - n_correct - n_ocurrence >= 0:
                return (255, 209, 102)  # Amarillo (255, 209, 102)

        # Si no coincide con ninguna condición anterior, devuelve GRIS
        return (70, 70, 80)  # Gris (70, 70, 80)
    

    def show_modal_message(self, message:str,
                           width:int, height:int,
                           color:tuple) -> None:
        """
        Muestra un mensaje modal en la pantalla del juego.

        Esta función crea un mensaje modal con un mensaje dado y lo muestra en el centro de la pantalla.

        Args:
            message (str): El mensaje que se mostrará en el modal.
            width (int): Ancho del mensaje modal.
            height (int): Alto del mensaje modal.
            color (tuple): Color de fondo para el modal (formato RGB).

        Returns:
            None
        """
        modal_font = pygame.font.SysFont("Arial", 20)
        modal_width = width
        modal_height = height

        modal_surface = pygame.Surface((modal_width, modal_height))
        modal_surface.fill(color)  # Color de fondo para el modal

        text = modal_font.render(message, True, (0, 0, 0))  # Color del texto: negro
        text_rect = text.get_rect(center=(modal_width // 2, modal_height // 2))

        modal_surface.blit(text, text_rect)

        modal_x = (self.width - modal_width) // 2
        modal_y = (self.height - modal_height) // 2

        self.screen.blit(modal_surface, (modal_x, modal_y))
        pygame.display.flip()

    
    def run_game(self):
        """
        Ejecuta el ciclo principal del juego Wordle.

        Este método controla la lógica principal del juego Wordle, gestionando la pantalla,
        la interacción del usuario y las actualizaciones de los elementos visuales.

        Returns:
            None
        """
        while self.animating:
            self.screen.fill("white")
            self.draw_close_button()  # Dibuja el botón de cierre
            self.draw_aciertos()
            self.draw_fallos()

            # Dibuja las letras no adivinadas en la parte superior de la pantalla
            letters = self.font_small.render(self.unguessed, False, (70, 70, 80))
            surface = letters.get_rect(center=(self.width // 2, self.t_margin // 2))
            self.screen.blit(letters, surface)

            # Dibuja la matriz de adivinanzas y letras ingresadas por el usuario
            y = self.t_margin
            for i in range(6):
                x = self.lr_margin
                for j in range(4):
                    square = pygame.Rect(x, y, self.sq_size, self.sq_size)
                    pygame.draw.rect(self.screen, (70, 70, 80), square, width=2, border_radius=3)

                    # Dibuja las letras adivinadas en la matriz
                    if i < len(self.guesses):
                        color = self.determine_color(self.guesses[i], j)
                        pygame.draw.rect(self.screen, color, square, border_radius=3)
                        letter = self.font.render(self.guesses[i][j], False, (255, 255, 255))
                        surface = letter.get_rect(center=(x + self.sq_size // 2, y + self.sq_size // 2))
                        self.screen.blit(letter, surface)

                    # Dibuja las letras ingresadas por el usuario
                    if i == len(self.guesses) and j < len(self.input_text):
                        letter = self.font.render(self.input_text[j], False, (70, 70, 80))
                        surface = letter.get_rect(center=(x + self.sq_size // 2, y + self.sq_size // 2))
                        self.screen.blit(letter, surface)

                    x += self.sq_size + self.margin + 20
                y += self.sq_size + self.margin - 5

            # Muestra la respuesta correcta si el juego termina sin éxito
            if len(self.guesses) == 6 and self.guesses[5] != self.answer:
                self.game_over = True
                letters = self.font.render(self.answer, False, (70, 70, 80))
                surface = letters.get_rect(center=(self.width // 2, self.height - self.b_margin // 2 - self.margin))
                self.screen.blit(letters, surface)

            # Si el jugador no adivina la palabra en sus intentos, se suman los fallos
            if len(self.guesses)==6 and self.guesses[5] != self.answer and not self.game_lost:
                self.fallos+=1
                self.game_lost = True

            pygame.display.flip()

            # Gestiona la interacción del usuario
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.animating = False
                elif event.type == pygame.KEYDOWN:
                    
                    # Si le da click en Escape se termina el juego
                    if event.key == pygame.K_ESCAPE:
                        self.animating = False

                    # Elimina la última letra ingresada
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.input_text) > 0:
                            self.input_text = self.input_text[ : len(self.input_text) - 1]

                    # Verifica la adivinanza al presionar Enter
                    elif event.key == pygame.K_RETURN:
                        if len(self.input_text) == 4:
                            if self.input_text in self.dict_guessing:
                                # Agrega la adivinanza, actualiza letras no adivinadas y verifica si es la respuesta
                                self.guesses.append(self.input_text)
                                self.determine_unguessed_letters()
                                self.game_over = True if self.input_text == self.answer else False
                                if self.game_over:
                                    # Muestra un mensaje modal si se gana el juego
                                    self.show_modal_message("¡Excelente, has ganado! Presiona espacio para reiniciar",
                                                            425, 150,
                                                            (170, 235, 160))
                                    # En cuanto gane aumento el contador de victorias
                                    self.aciertos += 1
                                    pygame.time.delay(1500)  # Muestra el mensaje de victoria durante 1.5 segundos
                                    self.game_over = False  # Reinicia el estado de fin del juego
                                self.input_text = ""
                            else:
                                # Muestra el mensaje modal si la palabra no está en el conjunto de palabras
                                self.show_modal_message('La palabra no es válida',
                                                        300, 100,
                                                       (207, 205, 182))
                                pygame.time.delay(1000)  # Muestra el mensaje de palabra no válida durante 1 segundo
                                  
                    # Reinicia el juego al presionar espacio
                    elif event.key == pygame.K_SPACE:
                        self.game_over = False
                        self.guesses = []
                        self.unguessed = self.alphabet
                        self.input_text = ''
                        self.answer = random.choice(list(self.dict_answers))
                        self.game_lost = False

                    # Agrega letras ingresadas por el usuario si no se ha alcanzado el límite
                    elif len(self.input_text) < 4 and not self.game_over:
                        self.input_text += event.unicode.upper()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Verifica si se hizo clic con el botón izquierdo del ratón
                        if pygame.Rect(10, 10, 50, 30).collidepoint(event.pos):
                            self.close_game()  # Cierra el juego al hacer clic en el botón