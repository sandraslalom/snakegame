#!/usr/bin/env python3
"""
Sprites module for Snake Game - Contains classes for game objects
"""
import pygame
from enum import Enum
from typing import List, Dict, Tuple, Optional, Any, Callable as PyCallable


class Apple(pygame.sprite.Sprite):
    """Apple sprite that the snake tries to eat"""
    
    # Class constants
    _DEFAULT_COLOR = (255, 0, 0)  # Red
    _DEFAULT_SIZE = (10, 10)
    
    def __init__(self, color: Optional[Tuple[int, int, int]] = None, 
                 size: Optional[Tuple[int, int]] = None, 
                 position: Optional[List[int]] = None):
        """
        Initialize an apple sprite
        
        Args:
            color: RGB color tuple, defaults to red
            size: (width, height) tuple, defaults to (10, 10)
            position: [x, y] position list
        
        Raises:
            ValueError: If position is None
        """
        super().__init__()
        
        # Parameter validation
        if color is None:
            color = self._DEFAULT_COLOR
        if size is None:
            size = self._DEFAULT_SIZE
        if position is None:
            raise ValueError('Invalid position: position cannot be None')
        
        # Initialize sprite properties
        self.color = color
        self.size = size
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position


class Snake(pygame.sprite.Sprite):
    """Snake sprite controlled by the player"""
    
    # Class constants
    _DEFAULT_COLOR = (0, 255, 0)  # Green
    _DEFAULT_SIZE = (10, 10)  # 10px X 10px
    _DEFAULT_POSITION = [30, 30]  # Space given to tail of length 2
    
    class SnakeMove(Enum):
        """Enum for snake movement directions"""
        UP = '1Y'
        DOWN = '-1Y'
        RIGHT = '1X'
        LEFT = '-1X'
        
        @classmethod
        def is_valid_direction(cls, direction) -> bool:
            """Check if a direction is valid"""
            return direction in [cls.UP, cls.DOWN, cls.RIGHT, cls.LEFT]
    
    class _SnakeTail(pygame.sprite.Sprite):
        """Private class representing the snake's tail"""
        
        def __init__(self):
            """Initialize an empty tail"""
            super().__init__()
            self.tiles: List[Dict[str, Any]] = []
        
        def add_tile(self, color: Tuple[int, int, int], size: Tuple[int, int], position: List[int]):
            """
            Add a new tile to the tail
            
            Args:
                color: RGB color tuple
                size: (width, height) tuple
                position: [x, y] position list
            """
            tile = pygame.Surface(size)
            tile.fill(color)
            rect = tile.get_rect()
            rect.topleft = position
            
            self.tiles.append({'image': tile, 'rect': rect})
    
    class _SnakeHead(pygame.sprite.Sprite):
        """Private class representing the snake's head"""
        
        def __init__(self, color: Tuple[int, int, int], size: Tuple[int, int], position: List[int]):
            """
            Initialize the snake's head
            
            Args:
                color: RGB color tuple
                size: (width, height) tuple
                position: [x, y] position list
            """
            super().__init__()
            self.image = pygame.Surface(size)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.topleft = position
    
    def __init__(self, color: Optional[Tuple[int, int, int]] = None, 
                 size: Optional[Tuple[int, int]] = None, 
                 position: Optional[List[int]] = None):
        """
        Initialize a snake sprite
        
        Args:
            color: RGB color tuple, defaults to green
            size: (width, height) tuple, defaults to (10, 10)
            position: [x, y] position list, defaults to [30, 30]
            
        Raises:
            ValueError: If width and height are not equal
        """
        super().__init__()
        
        # Parameter validation
        if color is None:
            color = self._DEFAULT_COLOR
        if size is None:
            size = self._DEFAULT_SIZE
        if size[0] != size[1]:
            raise ValueError('Invalid tile size. Width and height must be equal.')
        if position is None:
            position = self._DEFAULT_POSITION.copy()
        
        # Initialize snake properties
        self.color = color
        self.size = size
        self.head = self._SnakeHead(color, size, position)
        self.tail = self._SnakeTail()
        
        # Create initial tail segments
        tailposition = [(position[0] - size[0]), position[1]]
        self.tail.add_tile(color, size, tailposition)
        tailposition = [(position[0] - 2*size[0]), position[1]]
        self.tail.add_tile(color, size, tailposition)
    
    def move(self, direction: SnakeMove, frame_width: int, frame_height: int) -> bool:
        """
        Move the snake in the specified direction
        
        Args:
            direction: Direction to move (from SnakeMove enum)
            frame_width: Width of the game frame
            frame_height: Height of the game frame
            
        Returns:
            bool: True if move was successful, False if snake collided with itself
            
        Raises:
            ValueError: If direction is invalid
        """
        # Parameter validation
        if not self.SnakeMove.is_valid_direction(direction):
            raise ValueError('Invalid movement direction')
        
        # Calculate new head position
        stepsize = self.size[0]  # Use size directly since width and height are equal
        newheadposition = list(self.head.rect.topleft)
        
        if direction == self.SnakeMove.UP:
            newheadposition[1] = (newheadposition[1] - stepsize) % frame_height
        elif direction == self.SnakeMove.DOWN:
            newheadposition[1] = (newheadposition[1] + stepsize) % frame_height
        elif direction == self.SnakeMove.RIGHT:
            newheadposition[0] = (newheadposition[0] + stepsize) % frame_width
        elif direction == self.SnakeMove.LEFT:
            newheadposition[0] = (newheadposition[0] - stepsize) % frame_width
        
        # Check for collision with self
        if self.occupies_position(newheadposition):
            return False
        
        # Move head to new position
        newtileposition = self.head.rect.topleft
        self.head.rect.topleft = newheadposition
        
        # Move tail segments
        for tile in self.tail.tiles:
            prevtileposition = tile['rect'].topleft
            tile['rect'].topleft = newtileposition
            newtileposition = prevtileposition
        
        return True
    
    def occupies_position(self, position: List[int]) -> bool:
        """
        Check if the snake occupies a given position
        
        Args:
            position: [x, y] position to check
            
        Returns:
            bool: True if position is occupied by snake, False otherwise
        """
        # Parameter validation
        if position[0] is None or position[1] is None:
            return True
        
        # Check head position
        if self.head.rect.topleft[0] == position[0] and self.head.rect.topleft[1] == position[1]:
            return True
        
        # Check tail positions
        for tile in self.tail.tiles:
            if (tile['rect'].topleft[0] == position[0] and 
                tile['rect'].topleft[1] == position[1]):
                return True
        
        return False
    
    def lengthen_tail(self, number: int, current_direction: SnakeMove):
        """
        Add segments to the snake's tail
        
        Args:
            number: Number of segments to add
            current_direction: Current movement direction
            
        Raises:
            ValueError: If direction is invalid
        """
        # Parameter validation
        if number is None:
            number = 1
        if not self.SnakeMove.is_valid_direction(current_direction):
            raise ValueError('Invalid movement direction')
        
        size = self.size[0]
        color = self.color
        
        # Add new tail segments
        for count in range(number):
            lastindex = len(self.tail.tiles) - 1
            X = self.tail.tiles[lastindex]['rect'].topleft[0]
            Y = self.tail.tiles[lastindex]['rect'].topleft[1]
            
            # Determine position of new tile based on direction
            if current_direction == self.SnakeMove.UP:
                Y = Y - size + (count * size)
            elif current_direction == self.SnakeMove.DOWN:
                Y = Y + size + (count * size)
            elif current_direction == self.SnakeMove.RIGHT:
                X = X - size + (count * size)
            elif current_direction == self.SnakeMove.LEFT:
                X = X + size + (count * size)
            
            self.tail.add_tile(color, self.size, [X, Y])
