import pygame
import sys
from . import config
from .game import MemoryGame
from .ui import MainMenu, WinScreen

# Global State
current_state = "MENU" 
game = None

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.get_text('title'))
    clock = pygame.time.Clock()

    # --- ACTION CALLBACKS ---
    def start_game():
        global current_state, game
        game = MemoryGame()
        current_state = "GAME"

    def go_to_menu():
        global current_state
        current_state = "MENU"

    def exit_game():
        pygame.quit()
        sys.exit()

    def toggle_language():
        # 1. Flip the language config
        config.LANGUAGE = 'es' if config.LANGUAGE == 'en' else 'en'
        pygame.display.set_caption(config.get_text('title'))
        
        # 2. Tell the UI Managers to refresh their text
        menu_screen.update_language()
        win_screen.update_language()

    # --- INITIALIZE SCENES ---
    # We just create the managers and pass them the functions they need to call
    menu_screen = MainMenu(start_game, toggle_language, exit_game)
    win_screen = WinScreen(start_game, go_to_menu, exit_game)

    # --- GAME LOOP ---
    global current_state
    running = True
    
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Global Cheat Code, uncomment to enable, for testing purposes.
            # / Códigos de trucos globales, descomentar para habilitar, para propósitos de prueba.
            
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_w and current_state == "GAME":
                #game.pairs_found = config.TOTAL_PAIRS

            # Delegate events to the correct scene
            if current_state == "MENU":
                menu_screen.handle_event(event)
            
            elif current_state == "GAME":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.handle_click(event.pos)

            elif current_state == "WIN":
                win_screen.handle_event(event)

        # 2. Update Logic
        if current_state == "GAME":
            game.update()
            if game.pairs_found == 10:
                current_state = "WIN"

        # 3. Drawing
        screen.fill(config.GRAY)

        if current_state == "MENU":
            menu_screen.draw(screen)

        elif current_state == "GAME":
            game.draw(screen)

        elif current_state == "WIN":
            game.draw(screen) # Draw game behind the win screen
            win_screen.draw(screen)

        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()