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
            full_path = config.get_path(relative_path)

            if os.path.exists(full_path):
                img = pygame.image.load(full_path).convert_alpha()
                # Smoothscale looks better for resizing
                img = pygame.transform.smoothscale(img, (width - 20, height - 20))
                img_rect = img.get_rect(center=(width//2, height//2))
                surf.blit(img, img_rect)
            else:
                # Fallback if image is missing
                font = pygame.font.SysFont('Arial', 20, bold=True)
                text_surf = font.render("Image Missing", True, config.RED)
                text_rect = text_surf.get_rect(center=(width//2, height//2))
                surf.blit(text_surf, text_rect) 

        return surf
       
    def draw(self, screen):
        if self.flipped or self.matched:
            screen.blit(self.surface, self.rect)
        else:
            # Draw the back of the card
            pygame.draw.rect(screen, config.BLUE, self.rect)
            pygame.draw.rect(screen, config.WHITE, self.rect, 2)
        
       

# -- 2. GAME CLASS ---
class MemoryGame:
    def __init__(self):
        self.cards = []
        self.flipped = []
        self.pairs_found = 0
        self.block_input = False
        self.last_mismatch_time = 0
        
        # --- FIX: Load the Score Font ONCE here ---
        # This prevents the "laggy loop" issue.
        self.score_font = pygame.font.SysFont('Arial', 24, bold=True)
        
        self.generate_grid()
    
    def generate_grid(self):
        """
        Generate the grid of cards
        """
        # 1. Calculate Card Size
        top_margin = 60 
        
        # Calculate available width
        total_h_gap = (config.GRID_COLS + 1) * config.CARD_GAP
        available_width = config.SCREEN_WIDTH - total_h_gap
        card_width = available_width // config.GRID_COLS

        # Calculate available height
        total_v_gap = (config.GRID_ROWS + 1) * config.CARD_GAP
        available_height = (config.SCREEN_HEIGHT - top_margin) - total_v_gap
        card_height = available_height // config.GRID_ROWS

        # 2. Create the Card Pairs
        temp_cards = []
        for i in range(10): 
            card_a = Card(0, 0, card_width, card_height, i, 'symbol')
            card_b = Card(0, 0, card_width, card_height, i, 'text') 
            temp_cards.append(card_a)
            temp_cards.append(card_b)
        
        random.shuffle(temp_cards) 

        # 3. Position Cards on the Grid
        grid_pixel_w = config.GRID_COLS * card_width + (config.GRID_COLS - 1) * config.CARD_GAP
        grid_pixel_h = config.GRID_ROWS * card_height + (config.GRID_ROWS - 1) * config.CARD_GAP
        
        start_x = (config.SCREEN_WIDTH - grid_pixel_w) // 2
        start_y = top_margin + ((config.SCREEN_HEIGHT - top_margin - grid_pixel_h) // 2)

        for index, card in enumerate(temp_cards):
            row = index // config.GRID_COLS
            col = index % config.GRID_COLS
            
            card.rect.x = start_x + col * (card_width + config.CARD_GAP)
            card.rect.y = start_y + row * (card_height + config.CARD_GAP)
            self.cards.append(card)

    def handle_click(self, pos):
        """Handle card flipping logic"""
        if self.block_input:
            return
        
        for card in self.cards:
            # Added check to ensure we don't click a card that is already in self.flipped
            if card.rect.collidepoint(pos) and not card.flipped and not card.matched:
                card.flipped = True
                self.flipped.append(card)
                if len(self.flipped) == 2:
                    self.check_match()
                break
        
    def check_match(self):
        card1, card2 = self.flipped
        if card1.pair_id == card2.pair_id:
            card1.matched = True
            card2.matched = True
            self.pairs_found += 1
            self.flipped.clear()
        else:
            self.block_input = True
            self.last_mismatch_time = pygame.time.get_ticks()
        
    def update(self):
        if self.block_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_mismatch_time > 1000: 
                # 1 second delay
                for card in self.flipped:
                    card.flipped = False
                self.flipped.clear()
                self.block_input = False

    def draw(self, screen):
        for card in self.cards:
            card.draw(screen)

        total_pairs = len(self.cards) // 2
        label_text = config.get_text('pairs') 
        score_str = f"{label_text} {self.pairs_found}/{total_pairs}"

        # --- FIX: Use the PRE-LOADED font ---
        score_surf = self.score_font.render(score_str, True, config.BLACK)
        
        text_rect = score_surf.get_rect(midtop=(config.SCREEN_WIDTH//2, 10))
        screen.blit(score_surf, text_rect)