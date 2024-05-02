import pygame
import sys
from settings import *
from cards import Card
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.cards = []
        self.player_score = 0  # Initialize score
        self.computer_score = 0
        self.computer_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # List of computer's cards (hidden)
        self.current_turn = "Player 1"  # Whose turn it is
        self.diamond_deck = []  # List to store diamond cards
        self.load_diamonds()  # Load diamond cards (function below)
        width_value = 100
        height_value = 100
        width = 200
        height = 600
        self.selected_diamond_image = pygame.image.load("images/Diamonds/2D.png")  # Initialize with a default image
        self.computer = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

        for suit in ['Clubs']:
            for card_value in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                image_path = f"images/{suit}/{card_value}{suit[0]}.png"
                position = (width + width_value, height)
                width_value += 100
                card = Card(image_path, position, suit)
                self.cards.append(card)
            width = 300
            width_value = 100
            height += height_value

    def load_diamonds(self):
        """Loads diamond cards from a separate deck."""
        self.diamond_deck = [
            ['2', 2, "images/Diamonds/2D.png"], ['3', 3, "images/Diamonds/3D.png"],
            ['4', 4, "images/Diamonds/4D.png"], ['5', 5, "images/Diamonds/5D.png"],
            ['6', 6, "images/Diamonds/6D.png"], ['7', 7, "images/Diamonds/7D.png"],
            ['8', 8, "images/Diamonds/8D.png"], ['9', 9, "images/Diamonds/9D.png"],
            ['T', 10, "images/Diamonds/TD.png"], ['J', 11, "images/Diamonds/JD.png"],
            ['Q', 12, "images/Diamonds/QD.png"], ['K', 13, "images/Diamonds/KD.png"],
            ['A', 14, "images/Diamonds/AD.png"]
        ]

    def diamond(self):
        """Returns a random diamond card."""
        if self.diamond_deck:
            diamond_card = random.choice(self.diamond_deck)
            self.diamond_deck.remove(diamond_card)
            return diamond_card
        else:
            return None  # No diamonds left

    def computers_choice(self):
        """Returns the value of the computer's chosen card and removes it from their deck."""
        if self.computer_cards:
            chosen_value = random.choice(self.computer_cards)
            self.computer_cards.remove(chosen_value)
            return chosen_value
        else:
            return None

    def display_selected_card(self, selected_image):
        selected_card_width = 100
        selected_card_height = 150
        x = (WIDTH - selected_card_width) // 2
        y = (HEIGHT - selected_card_height) // 2
        self.screen.blit(pygame.transform.scale(selected_image, (selected_card_width, selected_card_height)), (x, y))

    def run(self):
        self.load_diamonds()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.current_turn == "Player 1":
                    mouse_pos = pygame.mouse.get_pos()

                    for card in self.cards:
                        if card.rect.collidepoint(mouse_pos):
                            self.cards.remove(card)
                            computer_choice = self.computers_choice()

                            if computer_choice is not None:
                                # Award points based on chosen cards and diamond value
                                diamond_card = self.diamond()
                                if diamond_card is not None:
                                    diamond_value = diamond_card[1]
                                    diamond_display = diamond_card[2]
                                    self.selected_diamond_image = pygame.image.load(diamond_display)
                                    self.display_selected_card(self.selected_diamond_image)

                                    # Continue with player and computer turns
                                    if card.get_value() > computer_choice:
                                        self.player_score += diamond_value
                                    elif card.get_value() < computer_choice:
                                        self.computer_score += diamond_value
                                    else:
                                        self.player_score += diamond_value / 2
                                        self.computer_score += diamond_value / 2
                                        # Display computer's bid image
                                    computer_bid_image = pygame.image.load(f"images/Heart/{self.computer[computer_choice]}H.png")
                                    self.screen.blit(pygame.transform.scale(computer_bid_image, (100, 150)), (WIDTH // 2 - 50, HEIGHT // 2 - 75))

                                else:
                                    # No diamonds left, no turn change
                                    pass
                            else:
                                # Computer has no cards left, player 1 keeps their turn
                                pass
                            break  # Only remove one card per click

            self.screen.fill(BG_COLOR)

            # Draw player one's cards
            for card in self.cards:
                self.screen.blit(card.image, card.rect)

            # Display diamond card if it has been drawn and the game is not over
            if self.selected_diamond_image and (self.cards or self.computer_cards):
                self.screen.blit(pygame.transform.scale(self.selected_diamond_image, (100, 150)), (WIDTH // 2 - 50, HEIGHT // 2 - 75))

            # Display score and current turn
            self.display_score(self.current_turn)

            pygame.display.flip()

            # Check if all cards are played
            if not self.cards and not self.computer_cards:
                # Game over, determine winner
                if self.player_score > self.computer_score:
                    winner_text = "Player 1 wins!"
                elif self.player_score < self.computer_score:
                    winner_text = "Computer wins!"
                else:
                    winner_text = "It's a tie!"

                # Display winner text
                font = pygame.font.Font(None, 50)
                winner_text_surface = font.render(winner_text, True, (255, 255, 255))
                winner_text_rect = winner_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                self.screen.blit(winner_text_surface, winner_text_rect)

                pygame.display.flip()
                            
            
    def display_score(self, current_turn):
        # Define score rectangle properties (adjust as needed)
        score_rect_x = 100
        score_rect_y = 100
        score_rect_width = WIDTH - 1625
        score_rect_height = 80

        # Create the score rectangle
        score_rect = pygame.Rect(score_rect_x, score_rect_y, score_rect_width, score_rect_height)

        pygame.draw.rect(self.screen, (255, 255, 255), score_rect)  # White rectangle

        # Define font and text color
        font = pygame.font.Font(None, 24)  # Adjust font size as needed
        text_color = (0, 0, 0)  # Black text

        # Create text surfaces for heading, score and player labels
        heading_text = font.render("Scoreboard", True, text_color)
        score_text = font.render(f"Player 1: {self.player_score}", True, text_color)
        turn_text = font.render(f"Computer: {self.computer_score}", True, text_color)

        # Calculate text position within the rectangle
        INCREASED_OFFSET = 15  # Adjust spacing as needed
        heading_text_rect = heading_text.get_rect(center=(score_rect.centerx, score_rect.top + INCREASED_OFFSET))
        score_text_rect = score_text.get_rect(centerx=score_rect.centerx, y=score_rect.centery - score_text.get_height() // 2)
        turn_text_rect = turn_text.get_rect(centerx=score_rect.centerx, y=score_rect.bottom - turn_text.get_height() - INCREASED_OFFSET)

        # Blit the text surfaces onto the screen
        self.screen.blit(heading_text, heading_text_rect)
        self.screen.blit(score_text, score_text_rect)
        self.screen.blit(turn_text, turn_text_rect)

if __name__ == '__main__':
    game = Game()
    game.run()