import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.init import CARS, FEATURES, filter_cars

import pygame

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (220, 220, 220)

FONT_TITLE = pygame.font.Font(None, 48)
FONT_QUESTION = pygame.font.Font(None, 36)
FONT_OPTION = pygame.font.Font(None, 32)
FONT_RESULT = pygame.font.Font(None, 40)

BUTTON_WIDTH = 350
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

class CarGuessingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Car Guessing Game")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.candidate_cars = CARS.copy()
        self.feature_index = 0
        self.selected_answers = {}
        self.finished = False
        self.result = None

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
        self.candidate_cars = filter_cars(self.candidate_cars, feature, value)
        self.feature_index += 1
        if self.feature_index >= len(FEATURES) or len(self.candidate_cars) <= 1:
            self.finished = True
            if len(self.candidate_cars) == 1:
                self.result = f"Your car is: {self.candidate_cars[0]['name']}"
            elif len(self.candidate_cars) > 1:
                names = ', '.join(car['name'] for car in self.candidate_cars)
                self.result = f"Possible cars: {names}"
            else:
                self.result = "No matching car found."

    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)
            self.draw_text("Car Guessing Game", FONT_TITLE, BLACK, WINDOW_WIDTH//2, 50)

            if not self.finished:
                feature, options = self.get_current_feature()
                self.draw_text(f"Select {feature.title()}:", FONT_QUESTION, BLACK, WINDOW_WIDTH//2, 140)
                button_rects = []
                for i, option in enumerate(options):
                    x = WINDOW_WIDTH//2 - BUTTON_WIDTH//2
                    y = 200 + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
                    rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
                    pygame.draw.rect(self.screen, GRAY, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 2)
                    label = str(option)
                    self.draw_text(label, FONT_OPTION, BLACK, rect.centerx, rect.centery)
                    button_rects.append((rect, option))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for rect, value in button_rects:
                            if rect.collidepoint(mouse_pos):
                                self.handle_option_click(value)
                                break
            else:
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
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

def main():
    game = CarGuessingGame()
    game.run()

if __name__ == "__main__":
    main() 