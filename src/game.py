import pygame
import os   
import random
from . import config

# -- 1. CARD CLASS/ClASE CARTA ---
class Card:
    def __init__(self, x, y, width, height, pair_id, kind): 
        """
        kind: 'symbol'(image) or 'text'(string)/símbolo (imagen) o texto (cadena)
        pair_id: 0-9 (index in COMPONENT_NAMES)/índice en COMPONENT_NAMES
        """
        self.rect = pygame.Rect(x, y, width, height) # Position and size/Posición y tamaño
        self.pair_id = pair_id # Which pair it belongs to/ a qué par pertenece
        self.kind = kind  # 'symbol' or 'text' to determine what to display/para determinar qué mostrar
        self.flipped = False # Whether the card is currently flipped/si la carta está volteada
        self.matched = False # Whether the card has been matched/si la carta ha sido emparejada
        self.surface = self._create_surface(width, height) # Pre-render the card face/Pre-renderizar la cara de la carta

    def _create_surface(self, width, height):
        """
        Create the card surface based on its kind./Crear la superficie de la carta según su tipo.
        """
        surf = pygame.Surface((width, height)) # Start with a blank surface/Comenzar con una superficie en blanco
        surf.fill(config.WHITE) # Card background color/Color de fondo de la carta
        pygame.draw.rect(surf, config.BLACK, (0, 0, width, height), 3) # Card border/Dibujo del borde de la carta

        # A) Text card / Carta de texto
        if self.kind == 'text': 
            name = config.get_component_name(self.pair_id)# Get the name based on current language/Obtener el nombre según el idioma actual
            font_size = 18 if len(name) <= 8 else 15 # Dynamic font size based on text length/Tamaño de fuente dinámico según la longitud del texto
            font = pygame.font.SysFont('Arial', font_size, bold=True) # Use a bold font for better readability/Usar una fuente en negrita para mejor legibilidad
            text_surf = font.render(name, True, config.BLACK) # Render the text/Renderizar el texto
            text_rect = text_surf.get_rect(center=(width//2, height//2)) # Center the text/Centrar el texto
            surf.blit(text_surf, text_rect)# Draw the text onto the card/Dibujar el texto en la carta

        # B) Symbol card / Carta de símbolo
        elif self.kind == 'symbol':
            filename = f"symbol_{self.pair_id}.png"# Image file name based on pair_id/Nombre del archivo de imagen basado en pair_id
            relative_path = os.path.join(config.ASSETS_DIR, filename) # Relative path to the image/Ruta relativa a la imagen
            full_path = config.get_path(relative_path) # Get the full path to the image/Obtener la ruta completa a la imagen

            if os.path.exists(full_path): # Check if the image file exists/Verificar si el archivo de imagen existe
                img = pygame.image.load(full_path).convert_alpha() # Load the image with transparency/Cargar la imagen con transparencia
                # Smoothscale looks better for resizing/Smoothscale se ve mejor para redimensionar
                img = pygame.transform.smoothscale(img, (width - 20, height - 20))
                img_rect = img.get_rect(center=(width//2, height//2)) # Center the image/Centrar la imagen
                surf.blit(img, img_rect) # Draw the image onto the card/Dibujar la imagen en la carta
            else:
                # Fallback if image is missing/Alternativa si falta la imagen
                font = pygame.font.SysFont('Arial', 20, bold=True)
                text_surf = font.render("Image Missing", True, config.RED)
                text_rect = text_surf.get_rect(center=(width//2, height//2))
                surf.blit(text_surf, text_rect) 

        return surf # Return the pre-rendered card surface/Devolver la superficie de la carta pre-renderizada
       
    def draw(self, screen): # Draw the card on the screen/Dibujar la carta en la pantalla
        if self.flipped or self.matched: # If the card is flipped or matched, show its face/Si la carta está volteada o emparejada, mostrar su cara
            screen.blit(self.surface, self.rect)
        else:
            # Draw the back of the card/Dibujar el reverso de la carta
            pygame.draw.rect(screen, config.INDIGO, self.rect) # Card back color/Color del reverso de la carta
            pygame.draw.rect(screen, config.BLACK, self.rect, 2) # Card back border/Borde del reverso de la carta
        
       

# -- 2. GAME CLASS/CLASE JUEGO ---
class MemoryGame:
    def __init__(self): # Initialize game state/Inicializar el estado del juego
        self.cards = [] # List to hold all the cards/Lista para contener todas las cartas
        self.flipped = [] # Currently flipped cards/Cartas actualmente volteadas
        self.pairs_found = 0 # Number of pairs found/Número de pares encontrados
        self.block_input = False # Whether to block input during mismatch delay/Si bloquear la entrada durante el retraso de no coincidencia
        self.last_mismatch_time = 0 # Time when the last mismatch occurred/Hora en que ocurrió la última no coincidencia

        self.score_font = pygame.font.SysFont('Arial', 24, bold=True) # Font for score display/Fuente para la visualización de la puntuación
        
        self.generate_grid() # Generate the grid of cards/Generar la cuadrícula de cartas
    
    def generate_grid(self):
        """
        Generate the grid of cards/Generar la cuadrícula de cartas
        """
        # 1. Calculate Card Size/Calcular el tamaño de la carta
        top_margin = 60 
        
        # Calculate available width/Calcular el ancho disponible
        total_h_gap = (config.GRID_COLS + 1) * config.CARD_GAP # Total horizontal gap including margins/Gap horizontal total incluyendo márgenes
        available_width = config.SCREEN_WIDTH - total_h_gap # Width left for cards/Ancho restante para las cartas
        card_width = available_width // config.GRID_COLS # Width of each card/Ancho de cada carta

        # Calculate available height/Calcular el alto disponible
        total_v_gap = (config.GRID_ROWS + 1) * config.CARD_GAP # Total vertical gap including margins/Gap vertical total incluyendo márgenes
        available_height = (config.SCREEN_HEIGHT - top_margin) - total_v_gap # Height left for cards/Alto restante para las cartas
        card_height = available_height // config.GRID_ROWS # Height of each card/Alto de cada carta

        # 2. Create the Card Pairs/Crear los pares de cartas
        temp_cards = [] # Temporary list to hold cards before shuffling/Lista temporal para contener las cartas antes de mezclar
        for i in range(10): 
            card_a = Card(0, 0, card_width, card_height, i, 'symbol') # Symbol card for this pair/Carta de símbolo para este par
            card_b = Card(0, 0, card_width, card_height, i, 'text')  # Text card for this pair/Carta de texto para este par
            temp_cards.append(card_a) # Add symbol card to temp list/Agregar carta de símbolo a la lista temporal
            temp_cards.append(card_b) # Add text card to temp list/Agregar carta de texto a la lista temporal
        
        random.shuffle(temp_cards) # Shuffle the cards to randomize their positions/Mezclar las cartas para aleatorizar sus posiciones

        # 3. Position Cards on the Grid
        grid_pixel_w = config.GRID_COLS * card_width + (config.GRID_COLS - 1) * config.CARD_GAP # Total width of the grid in pixels/Ancho total de la cuadrícula en píxeles
        grid_pixel_h = config.GRID_ROWS * card_height + (config.GRID_ROWS - 1) * config.CARD_GAP # Total height of the grid in pixels/Alto total de la cuadrícula en píxeles
        
        start_x = (config.SCREEN_WIDTH - grid_pixel_w) // 2 # Center the grid horizontally/Centrar la cuadrícula horizontalmente
        start_y = top_margin + ((config.SCREEN_HEIGHT - top_margin - grid_pixel_h) // 2) # Center the grid vertically within the available space/Centrar la cuadrícula verticalmente dentro del espacio disponible

        for index, card in enumerate(temp_cards): # Position each card based on its index/Posicionar cada carta según su índice
            row = index // config.GRID_COLS # Calculate row based on index/Calcular la fila según el índice
            col = index % config.GRID_COLS # Calculate column based on index/Calcular la columna según el índice
            
            card.rect.x = start_x + col * (card_width + config.CARD_GAP) # Set the x position of the card/Establecer la posición x de la carta
            card.rect.y = start_y + row * (card_height + config.CARD_GAP) # Set the y position of the card/Establecer la posición y de la carta
            self.cards.append(card) # Add the card to the game's card list/Agregar la carta a la lista de cartas del juego

    def handle_click(self, pos):
        """Handle card flipping logic
        /Manejar la lógica de volteo de cartas
        """
        if self.block_input: # If we're currently blocking input due to a mismatch, ignore clicks/Si actualmente estamos bloqueando la entrada debido a una no coincidencia, ignorar los clics
            return
        
        for card in self.cards: # Check if the click is on a card and if it's not already flipped or matched/Verificar si el clic está en una carta y si no está ya volteada o emparejada
        
            if card.rect.collidepoint(pos) and not card.flipped and not card.matched: # If the card was clicked and is not already flipped or matched/Si se hizo clic en la carta y no está ya volteada o emparejada
                card.flipped = True # Flip the card/Voltear la carta
                self.flipped.append(card) # Add it to the list of currently flipped cards/Agregarlo a la lista de cartas actualmente volteadas
                if len(self.flipped) == 2: # If two cards are flipped, check for a match/Si se voltearon dos cartas, verificar si coinciden
                    self.check_match()
                break # Only allow flipping one card per click/Solo permitir voltear una carta por clic
        
    def check_match(self): # Check if the two flipped cards are a match/Verificar si las dos cartas volteadas son un par
        card1, card2 = self.flipped # Get the two flipped cards/Obtener las dos cartas volteadas
        if card1.pair_id == card2.pair_id: # If the pair IDs match, it's a correct match/Si los IDs de par coinciden, es un par correcto
            card1.matched = True # Mark the first card as matched/Marcar la primera carta como emparejada
            card2.matched = True # Mark the second card as matched/Marcar la segunda carta como emparejada
            self.pairs_found += 1 # Increment the pairs found count/Incrementar el conteo de pares encontrados
            self.flipped.clear() # Clear the flipped list for the next turn/Limpiar la lista de volteadas para el siguiente turno
        else:
            self.block_input = True # Block input until we flip the cards back/ Bloquear la entrada hasta que volvamos a voltear las cartas
            self.last_mismatch_time = pygame.time.get_ticks() # Record the time of the mismatch/Registrar la hora de la no coincidencia
        
    def update(self):
        if self.block_input: # If we're blocking input due to a mismatch, check if enough time has passed to flip the cards back/Si estamos bloqueando la entrada debido a una no coincidencia, verificar si ha pasado suficiente tiempo para volver a voltear las cartas
            current_time = pygame.time.get_ticks()
            if current_time - self.last_mismatch_time > 1000: 
                # 1 second delay/Retraso de 1 segundo
                for card in self.flipped: # Flip the cards back over/Volver a voltear las cartas
                    card.flipped = False # Unflip the card/Desvoltear la carta
                self.flipped.clear() # Clear the flipped list for the next turn/Limpiar la lista de volteadas para el siguiente turno
                self.block_input = False # Unblock input/Desbloquear la entrada

    def draw(self, screen): # Draw all the cards and the score on the screen/Dibujar todas las cartas y la puntuación en la pantalla
        for card in self.cards: 
            card.draw(screen)

        total_pairs = config.TOTAL_PAIRS # Total pairs in the game/Total de pares en el juego
        label_text = config.get_text('pairs') # Get the label text based on the current language/Obtener el texto de la etiqueta según el idioma actual
        score_str = f"{label_text} {self.pairs_found}/{total_pairs}" # Create the score string with the number of pairs found/Crear la cadena de puntuación con el número de pares encontrados

        score_surf = self.score_font.render(score_str, True, config.BLACK) # Render the score text/Renderizar el texto de la puntuación
        
        text_rect = score_surf.get_rect(midtop=(config.SCREEN_WIDTH//2, 10)) # Position the score at the top center/Posicionar la puntuación en la parte superior central
        screen.blit(score_surf, text_rect) # Draw the score on the screen/Dibujar la puntuación en la pantalla