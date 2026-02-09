import pygame
import sys
from . import config
from .game import MemoryGame
from .ui import MainMenu, WinScreen

# Global State / Estado global
current_state = "MENU" 
game = None

# Main function to run the game/Función principal para ejecutar el juego
def main():
    pygame.init() # Initialize Pygame/Inicializar Pygame
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT)) # Create the game window/Crear la ventana del juego
    pygame.display.set_caption(config.get_text('title')) # Set the window title based on the current language/Establecer el título de la ventana según el idioma actual
    clock = pygame.time.Clock() # Create a clock to manage the frame rate/Crear un reloj para gestionar la tasa de fotogramas

    # --- ACTION CALLBACKS / FUNCIONES DE RETROALIMENTACIÓN DE ACCIÓN ---
    def start_game(): # Start a new game/Comenzar un nuevo juego
        global current_state, game # Set the current state to "GAME" and create a new game instance/Establecer el estado actual a "JUEGO" y crear una nueva instancia del juego
        game = MemoryGame() # Create a new game instance/Crear una nueva instancia del juego
        current_state = "GAME" # Switch to the game state/Cambiar al estado del juego

    def go_to_menu(): # Return to the main menu/Volver al menú principal
        global current_state # Set the current state back to "MENU"/Establecer el estado actual de nuevo a "MENU"
        current_state = "MENU" # Switch to the menu state/Cambiar al estado del menú

    def exit_game(): # Exit the game/Salir del juego
        pygame.quit()
        sys.exit()

    def toggle_language(): # Toggle the language between English and Spanish/Alternar el idioma entre inglés y español
        # 1. Flip the language config/Cambiar la configuración del idioma
        config.LANGUAGE = 'es' if config.LANGUAGE == 'en' else 'en'
        pygame.display.set_caption(config.get_text('title')) 
        
        # 2. Tell the UI Managers to refresh their text / Decirles a los administradores de UI que actualicen su texto
        menu_screen.update_language()
        win_screen.update_language()

    # --- INITIALIZE SCENES / INICIALIZAR ESCENAS ---
    # We just create the managers and pass them the functions they need to call / Simplemente creamos los administradores y les pasamos las funciones que necesitan llamar
    menu_screen = MainMenu(start_game, toggle_language, exit_game)
    win_screen = WinScreen(start_game, go_to_menu, exit_game)

    # --- GAME LOOP / BUCLE DEL JUEGO ---
    global current_state # We need to modify the global state variable inside the loop/ Necesitamos modificar la variable de estado global dentro del bucle
    running = True # Main loop flag/Bandera del bucle principal
    
    while running:
        # 1. Event Handling / Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # -----------------------------------------------------------------------------------------------------------------------------------------------------------|
            # Insta win Cheat Code, uncomment to enable, for testing purposes. Press W during the game to instantly win.                                                 |
            # Código de truco de victoria instantánea, descomentar para habilitar, para propósitos de prueba. Presiona W durante el juego para ganar instantáneamente.   |
            #                                                                                                                                                            |
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_w and current_state == "GAME":
                #game.pairs_found = config.TOTAL_PAIRS                                                                                                                   |   
            # -----------------------------------------------------------------------------------------------------------------------------------------------------------|
            
            # Delegate events to the correct scene/Delegar eventos a la escena correcta
            if current_state == "MENU": # If we're in the menu, let the menu handle the events/Si estamos en el menú, dejar que el menú maneje los eventos
                menu_screen.handle_event(event)
            
            elif current_state == "GAME": # If we're in the game, we need to handle card clicks as well as delegate to the game/Si estamos en el juego, necesitamos manejar los clics de las cartas además de delegar al juego
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.handle_click(event.pos)

            elif current_state == "WIN": # If we're in the win screen, let it handle the events/Si estamos en la pantalla de victoria, dejar que maneje los eventos
                win_screen.handle_event(event)

        # 2. Update Logic/Lógica de actualización
        if current_state == "GAME":
            game.update() # Update the game state/Actualizar el estado del juego
            if game.pairs_found == 10: # Check for win condition/Verificar la condición de victoria
                current_state = "WIN"

        # 3. Drawing/Dibujar
        screen.fill(config.GRAY) # Clear the screen with a gray background/Limpiar la pantalla con un fondo gris

        if current_state == "MENU": # If we're in the menu, draw the menu/Si estamos en el menú, dibujar el menú
            menu_screen.draw(screen)

        elif current_state == "GAME": # If we're in the game, draw the game/Si estamos en el juego, dibujar el juego
            game.draw(screen)

        elif current_state == "WIN": # If we're in the win screen, draw the game behind the win screen for a nice effect, then draw the win screen/Si estamos en la pantalla de victoria, dibujar el juego detrás de la pantalla de victoria para un efecto agradable, luego dibujar la pantalla de victoria
            game.draw(screen) # Draw game behind the win screen/Dibujar el juego detrás de la pantalla de victoria
            win_screen.draw(screen) # Draw the win screen/Dibujar la pantalla de victoria

        pygame.display.flip() # Update the display/Actualizar la pantalla
        clock.tick(config.FPS) # Cap the frame rate to the configured FPS/ Limitar la tasa de fotogramas a los FPS configurados

    pygame.quit() # Quit Pygame/Salir de Pygame