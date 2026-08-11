"""Game rules for Snake, kept independent from the graphical interface."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Protocol

Point = tuple[int, int]


class ChoiceSource(Protocol):
    def choice(self, sequence: list[Point]) -> Point: ...


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def opposite(self) -> "Direction":
        dx, dy = self.value
        return Direction((-dx, -dy))


class GameStatus(Enum):
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    WON = "won"


@dataclass
class SnakeGame:
    """Mutable state and rules for a grid-based Snake game."""

    width: int = 20
    height: int = 20
    rng: ChoiceSource = field(default_factory=random.Random, repr=False)
    snake: list[Point] = field(init=False)
    food: Point | None = field(init=False)
    direction: Direction = field(init=False)
    pending_direction: Direction = field(init=False)
    score: int = field(init=False)
    status: GameStatus = field(init=False)

    def __post_init__(self) -> None:
        if self.width < 4 or self.height < 1:
            raise ValueError("The board must be at least 4 cells wide and 1 cell high")
        self.reset()

    def reset(self) -> None:
        """Restore the initial centered snake and place fresh food."""
        center_x = self.width // 2
        center_y = self.height // 2
        self.snake = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.direction = Direction.RIGHT
        self.pending_direction = Direction.RIGHT
        self.score = 0
        self.status = GameStatus.READY
        self.food = self._place_food()

    def start_or_toggle_pause(self) -> None:
        if self.status is GameStatus.READY:
            self.status = GameStatus.RUNNING
        elif self.status is GameStatus.RUNNING:
            self.status = GameStatus.PAUSED
        elif self.status is GameStatus.PAUSED:
            self.status = GameStatus.RUNNING

    def change_direction(self, direction: Direction) -> bool:
        """Queue one safe turn for the next step.

        Comparing with the current movement direction also prevents two rapid key
        presses from reversing the snake before the next game tick.
        """
        if direction is self.direction.opposite:
            return False
        self.pending_direction = direction
        return True

    def step(self) -> bool:
        """Advance one cell and return whether the board changed."""
        if self.status is not GameStatus.RUNNING:
            return False

        self.direction = self.pending_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        eating = new_head == self.food

        if self._hits_wall(new_head) or self._hits_self(new_head, eating):
            self.status = GameStatus.GAME_OVER
            return False

        self.snake.insert(0, new_head)
        if eating:
            self.score += 1
            self.food = self._place_food()
            if self.food is None:
                self.status = GameStatus.WON
        else:
            self.snake.pop()
        return True

    def _hits_wall(self, point: Point) -> bool:
        x, y = point
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def _hits_self(self, point: Point, eating: bool) -> bool:
        # The tail vacates its cell on a normal step, so entering it is legal.
        occupied = self.snake if eating else self.snake[:-1]
        return point in occupied

    def _place_food(self) -> Point | None:
        occupied = set(self.snake)
        available = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in occupied
        ]
        return self.rng.choice(available) if available else None

