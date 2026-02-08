import pygame
from . import config

# --- BASIC COMPONENTS (Keep these as they were) ---

class Button:
    def __init__(self, x, y, width, height, text_key, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_key = text_key
        self.action = action
        self.color = config.BLUE
        self.hover_color = config.GREEN
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.text_surf = None
        self.text_rect = None
        self.update_text()

    def update_text(self):
        text = config.get_text(self.text_key)
        self.text_surf = self.font.render(text, True, config.WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, config.WHITE, self.rect, 2, border_radius=12)
        if self.text_surf:
            screen.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

class TextLabel:
    def __init__(self, x, y, text_key, font_size=20, color=config.BLACK, anchor="topleft"):
        self.x = x
        self.y = y
        self.text_key = text_key
        self.color = color
        self.anchor = anchor
        self.font = pygame.font.SysFont('Arial', font_size, bold=False)
        self.image = None
        self.rect = None
        self.update_text()

    def update_text(self):
        text = config.get_text(self.text_key)
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(**{self.anchor: (self.x, self.y)})

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)

# --- NEW: SCENE MANAGERS ---

class MainMenu:
    def __init__(self, start_cb, lang_cb, exit_cb):
        """
        cb = callback (the function to run when button is clicked)
        """
        center_x = config.SCREEN_WIDTH // 2 - 100
        
        self.title = TextLabel(config.SCREEN_WIDTH // 2, 150, 'title', font_size=60, anchor="center")
        self.author = TextLabel(config.SCREEN_WIDTH - 10, config.SCREEN_HEIGHT - 10, 'author', font_size=16, anchor="bottomright")
        
        self.buttons = [
            Button(center_x, 250, 200, 50, 'start', start_cb),
            Button(center_x, 320, 200, 50, 'Lang', lang_cb),
            Button(center_x, 390, 200, 50, 'exit', exit_cb)
        ]

    def update_language(self):
        self.title.update_text()
        self.author.update_text()
        for btn in self.buttons:
            btn.update_text()

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, screen):
        self.title.draw(screen)
        self.author.draw(screen)
        for btn in self.buttons:
            btn.draw(screen)


class WinScreen:
    def __init__(self, restart_cb, menu_cb, exit_cb):
        self.title = TextLabel(config.SCREEN_WIDTH // 2, 250, 'win', font_size=80, color=config.GREEN, anchor="center")
        
        # Win buttons are arranged horizontally
        bx = config.SCREEN_WIDTH // 2
        self.buttons = [
            Button(bx - 220, 400, 130, 50, 'restart', restart_cb),
            Button(bx - 70, 400, 140, 50, 'main_menu', menu_cb),
            Button(bx + 90, 400, 130, 50, 'exit', exit_cb)
        ]
        
        # Create a transparent overlay once
        self.overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

    def update_language(self):
        self.title.update_text()
        for btn in self.buttons:
            btn.update_text()

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, screen):
        # Draw overlay first
        screen.blit(self.overlay, (0, 0))
        self.title.draw(screen)
        for btn in self.buttons:
            btn.draw(screen)