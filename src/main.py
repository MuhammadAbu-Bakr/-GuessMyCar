import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.init import CARS, FEATURES, CarProlog

import pygame


pygame.init()

\
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (220, 220, 220)

FONT_TITLE = pygame.font.Font(None, 48)
FONT_QUESTION = pygame.font.Font(None, 32)
FONT_OPTION = pygame.font.Font(None, 28)
FONT_RESULT = pygame.font.Font(None, 40)
FONT_MENU = pygame.font.Font(None, 44)
FONT_SMALL = pygame.font.Font(None, 24)
FONT_TIMER = pygame.font.Font(None, 32)

BUTTON_WIDTH = 350
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

MENU_OPTIONS = ["Start", "Settings", "About", "Quit"]

CAR_LINE_HEIGHT = 26
ABOUT_LINE_HEIGHT = 32
ABOUT_TOP = 60
ABOUT_START_Y = 120
CAR_LIST_HEIGHT = 200
CAR_LIST_MARGIN = 20

class CarGuessingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Car Guessing Game")
        self.clock = pygame.time.Clock()
        self.state = "menu"  
        self.about_scroll = 0
        self.about_dragging = False
        self.about_drag_start_y = 0
        self.about_scroll_start = 0
        self.timer_start = None
        self.timer_end = None
        self.car_prolog = CarProlog()
        self.reset_game()

    def reset_game(self):
        self.feature_index = 0
        self.selected_answers = {}
        self.finished = False
        self.result = None
        self.timer_start = None
        self.timer_end = None
        self.car_prolog.reset()
        self.candidate_cars = CARS.copy()  # For About section only

    def draw_text(self, text, font, color, x, y, center=True):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
        self.screen.blit(surf, rect)
        return rect

    def get_current_feature(self):
        if self.feature_index < len(FEATURES):
            return FEATURES[self.feature_index]
        return None

    def handle_option_click(self, value):
        feature, _ = FEATURES[self.feature_index]
        self.selected_answers[feature] = value
        self.car_prolog.assert_selection(feature, value)
        self.feature_index += 1
        matches = self.car_prolog.get_matches()
        if self.feature_index >= len(FEATURES) or len(matches) <= 1:
            self.finished = True
            self.timer_end = time.time()
            if len(matches) == 1:
                self.result = f"Your car is: {matches[0]}"
            elif len(matches) > 1:
                names = ', '.join(matches)
                self.result = f"Possible cars: {names}"
            else:
                self.result = "No matching car found."

    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)
            if self.state == "menu":
                self.draw_text("Car Guessing Game", FONT_TITLE, BLACK, WINDOW_WIDTH//2, 80)
                button_rects = []
                for i, option in enumerate(MENU_OPTIONS):
                    x = WINDOW_WIDTH//2 - BUTTON_WIDTH//2
                    y = 200 + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
                    rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
                    color = BLUE if option == "Start" else GRAY
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 2)
                    self.draw_text(option, FONT_MENU, BLACK, rect.centerx, rect.centery)
                    button_rects.append((rect, option))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for rect, option in button_rects:
                            if rect.collidepoint(mouse_pos):
                                if option == "Start":
                                    self.reset_game()
                                    self.state = "game"
                                    self.timer_start = time.time()
                                elif option == "Settings":
                                    self.state = "settings"
                                elif option == "About":
                                    self.state = "about"
                                    self.about_scroll = 0
                                elif option == "Quit":
                                    running = False
            elif self.state == "settings":
                self.draw_text("Settings", FONT_TITLE, BLACK, WINDOW_WIDTH//2, 80)
                self.draw_text("(Settings coming soon)", FONT_QUESTION, BLACK, WINDOW_WIDTH//2, 200)
                back_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 120, 200, 50)
                pygame.draw.rect(self.screen, GRAY, back_rect)
                pygame.draw.rect(self.screen, BLACK, back_rect, 2)
                self.draw_text("Back", FONT_OPTION, BLACK, back_rect.centerx, back_rect.centery)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if back_rect.collidepoint(event.pos):
                            self.state = "menu"
            elif self.state == "about":
                self.draw_text("About", FONT_TITLE, BLACK, WINDOW_WIDTH//2, ABOUT_TOP)
                about_lines = [
                    "Car Guessing Game",
                    "Inspired by Akinator, built with Pygame.",
                    "Data: Popular cars in Pakistan.",
                    "@Muhammad AbuBakr",
                    "Cars the agent can guess:",
                    "Developer:",
                    "- Your very own trusty Computer Scientist Muhammad AbuBakr",
                    "GitHub profile:",
                    "- https://github.com/MuhammadAbu-Bakr",
                ]
                
                for i, line in enumerate(about_lines):
                    self.draw_text(line, FONT_QUESTION if i < 5 else FONT_SMALL, BLACK, WINDOW_WIDTH//2, ABOUT_START_Y + i*ABOUT_LINE_HEIGHT)
                # Calculate where the car list should start
                car_list_y = ABOUT_START_Y + len(about_lines)*ABOUT_LINE_HEIGHT + CAR_LIST_MARGIN
                car_names = CARS
                total_height = len(car_names) * CAR_LINE_HEIGHT
                max_scroll = max(0, total_height - CAR_LIST_HEIGHT)
                scroll_y = int(self.about_scroll)
                # Draw a white rectangle as the scroll area background
                pygame.draw.rect(self.screen, WHITE, (0, car_list_y, WINDOW_WIDTH, CAR_LIST_HEIGHT))
                for i, name in enumerate(car_names):
                    y = car_list_y + i * CAR_LINE_HEIGHT - scroll_y
                    if car_list_y - CAR_LINE_HEIGHT < y < car_list_y + CAR_LIST_HEIGHT:
                        self.draw_text(f"{i+1}. {name}", FONT_SMALL, BLACK, WINDOW_WIDTH//2, y)
                # Back button (top right)
                back_rect = pygame.Rect(WINDOW_WIDTH - 130, 20, 100, 40)
                pygame.draw.rect(self.screen, GRAY, back_rect)
                pygame.draw.rect(self.screen, BLACK, back_rect, 2)
                self.draw_text("Back", FONT_OPTION, BLACK, back_rect.centerx, back_rect.centery)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if back_rect.collidepoint(event.pos):
                            self.state = "menu"
                        elif car_list_y < event.pos[1] < car_list_y + CAR_LIST_HEIGHT:
                            self.about_dragging = True
                            self.about_drag_start_y = event.pos[1]
                            self.about_scroll_start = self.about_scroll
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.about_dragging = False
                    elif event.type == pygame.MOUSEMOTION:
                        if self.about_dragging:
                            dy = event.pos[1] - self.about_drag_start_y
                            self.about_scroll = min(max(self.about_scroll_start - dy, 0), max_scroll)
                    elif event.type == pygame.MOUSEWHEEL:
                        self.about_scroll -= event.y * 30
                        self.about_scroll = min(max(self.about_scroll, 0), max_scroll)
            elif self.state == "game":
                self.draw_text("Car Guessing Game", FONT_TITLE, BLACK, WINDOW_WIDTH//2, 50)
                # Draw timer at top right
                if self.timer_start is not None and not self.finished:
                    elapsed = time.time() - self.timer_start
                    self.draw_text(f"Time: {elapsed:.1f}s", FONT_TIMER, BLUE, WINDOW_WIDTH - 120, 40)
                if not self.finished:
                    feature, options = self.get_current_feature()
                    self.draw_text(f"Select {feature.title()}:", FONT_QUESTION, BLACK, WINDOW_WIDTH//2, 140)
                    # --- Option scrolling logic ---
                    option_area_top = 200
                    option_area_height = WINDOW_HEIGHT - option_area_top - 120
                    option_btn_height = BUTTON_HEIGHT
                    option_btn_margin = BUTTON_MARGIN
                    visible_btns = max(1, option_area_height // (option_btn_height + option_btn_margin))
                    total_btns = len(options)
                    # Scrolling state
                    if not hasattr(self, 'option_scroll'):
                        self.option_scroll = 0
                        self.option_dragging = False
                        self.option_drag_start_y = 0
                        self.option_scroll_start = 0
                    max_scroll = max(0, total_btns - visible_btns)
                    start_idx = int(self.option_scroll)
                    end_idx = min(start_idx + visible_btns, total_btns)
                    button_rects = []
                    for i, option in enumerate(options[start_idx:end_idx]):
                        x = WINDOW_WIDTH//2 - BUTTON_WIDTH//2
                        y = option_area_top + i * (option_btn_height + option_btn_margin)
                        rect = pygame.Rect(x, y, BUTTON_WIDTH, option_btn_height)
                        pygame.draw.rect(self.screen, GRAY, rect)
                        pygame.draw.rect(self.screen, BLACK, rect, 2)
                        label = str(option)
                        self.draw_text(label, FONT_OPTION, BLACK, rect.centerx, rect.centery)
                        button_rects.append((rect, option))
                    # Scrollbar
                    if total_btns > visible_btns:
                        bar_height = int(option_area_height * visible_btns / total_btns)
                        bar_y = option_area_top + int(option_area_height * start_idx / total_btns)
                        bar_rect = pygame.Rect(WINDOW_WIDTH - 40, bar_y, 20, bar_height)
                        pygame.draw.rect(self.screen, GRAY, bar_rect)
                        pygame.draw.rect(self.screen, BLACK, bar_rect, 2)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if total_btns > visible_btns and WINDOW_WIDTH - 40 <= mouse_pos[0] <= WINDOW_WIDTH - 20 and option_area_top <= mouse_pos[1] <= option_area_top + option_area_height:
                                self.option_dragging = True
                                self.option_drag_start_y = mouse_pos[1]
                                self.option_scroll_start = self.option_scroll
                            else:
                                for rect, value in button_rects:
                                    if rect.collidepoint(mouse_pos):
                                        self.handle_option_click(value)
                                        self.option_scroll = 0
                                        break
                        elif event.type == pygame.MOUSEBUTTONUP:
                            self.option_dragging = False
                        elif event.type == pygame.MOUSEMOTION:
                            if getattr(self, 'option_dragging', False):
                                dy = event.pos[1] - self.option_drag_start_y
                                scroll_amt = int(dy / (option_btn_height + option_btn_margin))
                                self.option_scroll = min(max(self.option_scroll_start + scroll_amt, 0), max_scroll)
                        elif event.type == pygame.MOUSEWHEEL:
                            self.option_scroll -= event.y
                            self.option_scroll = min(max(self.option_scroll, 0), max_scroll)
                else:
                    # Show timer with result
                    if self.timer_start is not None and self.timer_end is not None:
                        elapsed = self.timer_end - self.timer_start
                        self.draw_text(f"Time: {elapsed:.1f}s", FONT_TIMER, BLUE, WINDOW_WIDTH - 120, 40)
                    self.draw_text(self.result, FONT_RESULT, BLUE, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
                    # Restart button
                    restart_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 80, 200, 50)
                    pygame.draw.rect(self.screen, GREEN, restart_rect)
                    pygame.draw.rect(self.screen, BLACK, restart_rect, 2)
                    self.draw_text("Restart", FONT_OPTION, BLACK, restart_rect.centerx, restart_rect.centery)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if restart_rect.collidepoint(event.pos):
                                self.reset_game()
                                self.state = "menu"
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

def main():
    game = CarGuessingGame()
    game.run()

if __name__ == "__main__":
    main() 