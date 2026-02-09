import pygame
from . import config

# --- UI COMPONENTS/COMPONENTES DE INTERFAZ ---

class Button: # Main menu buttons and win screen buttons/Botones del menú principal y de la pantalla de victoria
    def __init__(self, x, y, width, height, text_key, action):
        self.rect = pygame.Rect(x, y, width, height) # The button's rectangle area/El área rectangular del botón
        self.text_key = text_key # The key to look up the button's text in the current language/La clave para buscar el texto del botón en el idioma actual
        self.action = action # The function to call when the button is clicked/La función a llamar cuando se hace clic en el botón
        self.color = config.BLUE # Default button color/Color predeterminado del botón
        self.hover_color = config.GREEN # Color when hovered/Color al pasar el mouse por encima
        self.font = pygame.font.SysFont('Arial', 24, bold=True) # Font for button text/Fuente para el texto del botón
        self.text_surf = None # Surface for the button text/Superficie para el texto del botón
        self.text_rect = None # Rectangle for centering the text/Rectángulo para centrar el texto
        self.update_text() # Initialize the text surface and rectangle/Inicializar la superficie y el rectángulo del texto

    def update_text(self): # Update the text surface and rectangle based on the current language/Actualizar la superficie y el rectángulo del texto según el idioma actual
        text = config.get_text(self.text_key) # Get the button text based on the current language/Obtener el texto del botón según el idioma actual
        self.text_surf = self.font.render(text, True, config.WHITE) # Render the text surface/Renderizar la superficie del texto
        self.text_rect = self.text_surf.get_rect(center=self.rect.center) # Center the text rectangle/Centrar el rectángulo del texto

    def draw(self, screen): # Draw the button on the screen/Dibujar el botón en la pantalla
        mouse_pos = pygame.mouse.get_pos() # Get the current mouse position/Obtener la posición actual del mouse
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color # Change color if hovered/Cambiar el color si se pasa el mouse por encima
        pygame.draw.rect(screen, color, self.rect, border_radius=12) # Draw the button rectangle/Dibujar el rectángulo del botón
        pygame.draw.rect(screen, config.WHITE, self.rect, 2, border_radius=12) # Draw the button border/Dibujar el borde del botón
        if self.text_surf: # Draw the button text/Dibujar el texto del botón
            screen.blit(self.text_surf, self.text_rect) # Draw the text surface on the button/Dibujar la superficie del texto en el botón

    def handle_event(self, event): # Handle mouse click events to trigger the button action/ Manejar eventos de clic del mouse para activar la acción del botón
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button click/ Clic del botón izquierdo del mouse
            if self.rect.collidepoint(event.pos): # Check if the click is within the button area/ Verificar si el clic está dentro del área del botón
                self.action()

class TextLabel: # For displaying static text like the title and win message/Para mostrar texto estático como el título y el mensaje de victoria
    def __init__(self, x, y, text_key, font_size=20, color=config.BLACK, anchor="topleft"):
        self.x = x # X position of the text/Posición X del texto
        self.y = y # Y position of the text/Posición Y del texto
        self.text_key = text_key # The key to look up the text in the current language/La clave para buscar el texto en el idioma actual
        self.color = color # Text color/Color del texto
        self.anchor = anchor # Anchor point for positioning the text/ Punto de anclaje para posicionar el texto (e.g., "center", "topleft")
        self.font = pygame.font.SysFont('Arial', font_size, bold=False) # Font for the text/Fuente para el texto
        self.image = None # Surface for the rendered text/Superficie para el texto renderizado
        self.rect = None # Rectangle for positioning the text/Rectángulo para posicionar el texto
        self.update_text() # Initialize the text surface and rectangle/Inicializar la superficie y el rectángulo del texto

    def update_text(self): # Update the text surface and rectangle based on the current language/Actualizar la superficie y el rectángulo del texto según el idioma actual
        text = config.get_text(self.text_key) # Get the text based on the current language/Obtener el texto según el idioma actual
        self.image = self.font.render(text, True, self.color) # Render the text surface/Renderizar la superficie del texto
        self.rect = self.image.get_rect(**{self.anchor: (self.x, self.y)}) # Position the text rectangle based on the anchor/Posicionar el rectángulo del texto según el ancla

    def draw(self, screen): # Draw the text on the screen/Dibujar el texto en la pantalla
        if self.image:
            screen.blit(self.image, self.rect) # Draw the text surface on the screen/Dibujar la superficie del texto en la pantalla


class MainMenu: # The main menu screen with title and buttons/La pantalla del menú principal con título y botones
    def __init__(self, start_cb, lang_cb, exit_cb):
        """
        start_cb: callback function to start the game/función de callback para iniciar el juego
        lang_cb: callback function to change the language/función de callback para cambiar el idioma
        exit_cb: callback function to exit the game/función de callback para salir del juego
        """
        center_x = config.SCREEN_WIDTH // 2 - 100 # Center the buttons horizontally/Centrar los botones horizontalmente
        
        self.title = TextLabel(config.SCREEN_WIDTH // 2, 150, 'title', font_size=60, anchor="center") # Title text label/Etiqueta de texto del título
        self.author = TextLabel(config.SCREEN_WIDTH - 10, config.SCREEN_HEIGHT - 10, 'author', font_size=16, anchor="bottomright") # Author credit in the bottom right corner/Crédito del autor en la esquina inferior derecha
        
        self.buttons = [
            Button(center_x, 250, 200, 50, 'start', start_cb), # Start Game button/Botón de iniciar juego
            Button(center_x, 320, 200, 50, 'Lang', lang_cb), # Language toggle button/Botón de cambio de idioma
            Button(center_x, 390, 200, 50, 'exit', exit_cb) # Exit button/Botón de salir
        ]

    def update_language(self): # Update the text for the title, author, and buttons when the language changes/Actualizar el texto del título, autor y botones cuando cambia el idioma
        self.title.update_text() #  Update the title text/Actualizar el texto del título
        self.author.update_text() # Update the author text/Actualizar el texto del autor
        for btn in self.buttons: # Update the button text/Actualizar el texto del botón
            btn.update_text() #

    def handle_event(self, event): # Handle events for the buttons/ Manejar eventos para los botones
        for btn in self.buttons: #  Check each button to see if it was clicked/Verificar cada botón para ver si fue clickeado
            btn.handle_event(event)

    def draw(self, screen): # Draw the title, author, and buttons on the screen/Dibujar el título, autor y botones en la pantalla
        self.title.draw(screen) # Draw the title/Dibujar el título
        self.author.draw(screen) # Draw the author credit/Dibujar el crédito del autor
        for btn in self.buttons: # Draw each button/Dibujar cada botón
            btn.draw(screen)


class WinScreen: # The screen that appears when the player wins, with a message and buttons to restart, go to menu, or exit/La pantalla que aparece cuando el jugador gana, con un mensaje y botones para reiniciar, ir al menú o salir
    def __init__(self, restart_cb, menu_cb, exit_cb):
        self.title = TextLabel(config.SCREEN_WIDTH // 2, 250, 'win', font_size=80, color=config.GREEN, anchor="center") # Win message text label/Etiqueta de texto del mensaje de victoria
        
        # Win buttons are arranged horizontally
        bx = config.SCREEN_WIDTH // 2 # Center X for the buttons/Centro X para los botones
        self.buttons = [
            Button(bx - 220, 400, 130, 50, 'restart', restart_cb), # Restart button/Botón de reiniciar
            Button(bx - 70, 400, 140, 50, 'main_menu', menu_cb), # Main Menu button/Botón de menú principal
            Button(bx + 90, 400, 130, 50, 'exit', exit_cb) # Exit button/Botón de salir
        ]
        
        # Create a transparent overlay once
        self.overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA) # Crear una superposición transparente una vez
        self.overlay.fill((0, 0, 0, 180)) # Fill with semi-transparent black/Rellenar con

    def update_language(self): # Update the text for the win message and buttons when the language changes/Actualizar el texto del mensaje de victoria y los botones cuando cambia el idioma
        self.title.update_text() # Update the win message text/Actualizar el texto del mensaje de victoria
        for btn in self.buttons: # Update the button text/Actualizar el texto del botón
            btn.update_text()

    def handle_event(self, event): # Handle events for the buttons/ Manejar eventos para los botones
        for btn in self.buttons: # Check each button to see if it was clicked/Verificar cada botón para ver si fue clickeado
            btn.handle_event(event)

    def draw(self, screen): # Draw the win message and buttons on the screen/Dibujar el mensaje de victoria y los botones en la pantalla
        # Draw overlay first
        screen.blit(self.overlay, (0, 0)) # Draw the semi-transparent overlay/Dibujar la superposición semitransparente
        self.title.draw(screen) # Draw the win message/Dibujar el mensaje de victoria
        for btn in self.buttons: #  Draw each button/Dibujar cada botón
            btn.draw(screen)