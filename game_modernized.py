#!/usr/bin/env python3
"""
Snake Game - A classic snake game implementation using Pygame
"""
import sys
import random
import pygame
<<<<<<< HEAD
from sprites import Snake, Apple
=======
from archive.sprites import Snake, Apple
>>>>>>> a28fd46 (updates after modernization)


class SnakeGame:
    """Main game class that handles the game loop and game state"""
    
    # Game constants
    DEFAULT_SCREEN_SIZE = (640, 480)
    DEFAULT_UPDATE_SPEED = 100
    BACKGROUND_COLOR = (0, 0, 0)  # Black
    
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        self.screen = pygame.display.set_mode(self.DEFAULT_SCREEN_SIZE)
        pygame.display.set_caption('Snake')
        
        # Game state
        self.is_running = True
        self.is_game_over = False
        self.is_paused = False
        self.score = 0
        self.direction = Snake.SnakeMove.RIGHT
        
        # Initialize game objects
        self.snake = Snake(None, None, None)
        self.apple = None
        self.create_apple()
        
        # Timing control
        self.clock = pygame.time.Clock()
        self.update_time = pygame.time.get_ticks() + self.DEFAULT_UPDATE_SPEED
    
    def create_apple(self):
        """Create a new apple at a random position not occupied by the snake"""
        hlimit = (self.DEFAULT_SCREEN_SIZE[0] // Apple._DEFAULT_SIZE[0]) - 1
        vlimit = (self.DEFAULT_SCREEN_SIZE[1] // Apple._DEFAULT_SIZE[1]) - 1
        
        position = [None, None]
        while self.snake.occupies_position(position) or position[0] is None:
            position[0] = random.randint(0, hlimit) * Apple._DEFAULT_SIZE[0]
            position[1] = random.randint(0, vlimit) * Apple._DEFAULT_SIZE[1]
        
        self.apple = Apple(None, None, position)
    
    def handle_events(self):
        """Process user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                elif event.key == pygame.K_p:
                    self.is_paused = not self.is_paused
                elif event.key == pygame.K_r and self.is_game_over:
                    self.reset_game()
                
                # Direction controls (only when not paused and game not over)
                if not self.is_paused and not self.is_game_over:
                    if event.key == pygame.K_UP and self.direction != Snake.SnakeMove.DOWN:
                        self.direction = Snake.SnakeMove.UP
                    elif event.key == pygame.K_DOWN and self.direction != Snake.SnakeMove.UP:
                        self.direction = Snake.SnakeMove.DOWN
                    elif event.key == pygame.K_RIGHT and self.direction != Snake.SnakeMove.LEFT:
                        self.direction = Snake.SnakeMove.RIGHT
                    elif event.key == pygame.K_LEFT and self.direction != Snake.SnakeMove.RIGHT:
                        self.direction = Snake.SnakeMove.LEFT
    
    def update(self):
        """Update game state"""
        if self.is_paused or self.is_game_over:
            return
            
        current_time = pygame.time.get_ticks()
        
        if current_time >= self.update_time:
            # Move snake
            moved = self.snake.move(self.direction, self.DEFAULT_SCREEN_SIZE[0], self.DEFAULT_SCREEN_SIZE[1])
            if not moved:
                self.is_game_over = True
            
            # Check if snake ate the apple
            if self.snake.occupies_position(self.apple.rect.topleft):
                self.create_apple()
                self.snake.lengthen_tail(1, self.direction)
                self.score += 1
                pygame.display.set_caption(f'Snake: {self.score}')
            
            # Update next update time
            self.update_time = current_time + self.DEFAULT_UPDATE_SPEED
    
    def render(self):
        """Render the game state to the screen"""
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # Render game objects
        self.render_apple()
        self.render_snake()
        
        # Render game over message if game is over
        if self.is_game_over:
            self.render_game_over()
        
        # Render pause message if game is paused
        if self.is_paused and not self.is_game_over:
            self.render_pause_message()
            
        pygame.display.update()
    
    def render_snake(self):
        """Render the snake on the screen"""
        self.screen.blit(self.snake.head.image, self.snake.head.rect)
        for tile in self.snake.tail.tiles:
            self.screen.blit(tile['image'], tile['rect'])
    
    def render_apple(self):
        """Render the apple on the screen"""
        self.screen.blit(self.apple.image, self.apple.rect)
    
    def render_game_over(self):
        """Render game over message"""
        font = pygame.font.SysFont('Arial', 30)
        game_over_text = font.render(f'GAME OVER - Score: {self.score}', True, (255, 255, 255))
        restart_text = font.render('Press R to restart', True, (255, 255, 255))
        
        text_rect = game_over_text.get_rect(center=(self.DEFAULT_SCREEN_SIZE[0] // 2, 
                                                   self.DEFAULT_SCREEN_SIZE[1] // 2 - 20))
        restart_rect = restart_text.get_rect(center=(self.DEFAULT_SCREEN_SIZE[0] // 2, 
                                                    self.DEFAULT_SCREEN_SIZE[1] // 2 + 20))
        
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.set_caption(f'Snake: {self.score} - GAME OVER')
    
    def render_pause_message(self):
        """Render pause message"""
        font = pygame.font.SysFont('Arial', 30)
        pause_text = font.render('PAUSED - Press P to resume', True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(self.DEFAULT_SCREEN_SIZE[0] // 2, 
                                               self.DEFAULT_SCREEN_SIZE[1] // 2))
        self.screen.blit(pause_text, text_rect)
    
    def reset_game(self):
        """Reset the game state to start a new game"""
        self.is_game_over = False
        self.score = 0
        self.direction = Snake.SnakeMove.RIGHT
        self.snake = Snake(None, None, None)
        self.create_apple()
        pygame.display.set_caption('Snake')
    
    def run(self):
        """Main game loop"""
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Cap at 60 FPS
        
        pygame.quit()
        return self.score


def main():
    """Main entry point for the game"""
    game = SnakeGame()
    final_score = game.run()
    print(f"Final score: {final_score}")
    return 0


if __name__ == "__main__":
<<<<<<< HEAD
    sys.exit(main())
=======
    sys.exit(main())
>>>>>>> a28fd46 (updates after modernization)
