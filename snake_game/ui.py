"""Tkinter interface for the Snake game."""

from __future__ import annotations

import tkinter as tk

from .model import Direction, GameStatus, SnakeGame

CELL_SIZE = 24
BOARD_WIDTH = 20
BOARD_HEIGHT = 20
START_DELAY_MS = 150
MIN_DELAY_MS = 65

BACKGROUND = "#101820"
GRID = "#1d2b34"
SNAKE = "#55c57a"
SNAKE_HEAD = "#9be15d"
FOOD = "#ff5a5f"
TEXT = "#f4f7f5"


class SnakeApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.game = SnakeGame(BOARD_WIDTH, BOARD_HEIGHT)
        self.root.title("贪吃蛇")
        self.root.resizable(False, False)

        self.score_label = tk.Label(
            root,
            bg=BACKGROUND,
            fg=TEXT,
            font=("Arial", 14, "bold"),
            padx=10,
            pady=8,
        )
        self.score_label.pack(fill="x")

        self.canvas = tk.Canvas(
            root,
            width=BOARD_WIDTH * CELL_SIZE,
            height=BOARD_HEIGHT * CELL_SIZE,
            bg=BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.help_label = tk.Label(
            root,
            text="方向键 / WASD 移动  ·  空格 开始/暂停  ·  R 重新开始",
            bg=BACKGROUND,
            fg="#a8b4bb",
            font=("Arial", 10),
            padx=10,
            pady=8,
        )
        self.help_label.pack(fill="x")

        self.root.configure(bg=BACKGROUND)
        self.root.bind("<Key>", self._on_key)
        self.root.focus_force()
        self._draw()
        self.root.after(START_DELAY_MS, self._tick)

    @property
    def delay_ms(self) -> int:
        return max(MIN_DELAY_MS, START_DELAY_MS - self.game.score * 5)

    def _on_key(self, event: tk.Event) -> None:
        key = event.keysym.lower()
        directions = {
            "up": Direction.UP,
            "w": Direction.UP,
            "down": Direction.DOWN,
            "s": Direction.DOWN,
            "left": Direction.LEFT,
            "a": Direction.LEFT,
            "right": Direction.RIGHT,
            "d": Direction.RIGHT,
        }
        if key in directions:
            self.game.change_direction(directions[key])
        elif key == "space":
            self.game.start_or_toggle_pause()
        elif key == "r":
            self.game.reset()
        self._draw()

    def _tick(self) -> None:
        self.game.step()
        self._draw()
        self.root.after(self.delay_ms, self._tick)

    def _draw(self) -> None:
        self.canvas.delete("all")
        self._draw_grid()

        if self.game.food is not None:
            self._draw_cell(self.game.food, FOOD, inset=4, oval=True)

        for index, segment in reversed(list(enumerate(self.game.snake))):
            color = SNAKE_HEAD if index == 0 else SNAKE
            self._draw_cell(segment, color, inset=2)

        self.score_label.configure(text=f"得分：{self.game.score}")
        messages = {
            GameStatus.READY: "按空格开始",
            GameStatus.PAUSED: "已暂停",
            GameStatus.GAME_OVER: "游戏结束 · 按 R 重新开始",
            GameStatus.WON: "你赢了！· 按 R 重新开始",
        }
        if self.game.status in messages:
            self._draw_overlay(messages[self.game.status])

    def _draw_grid(self) -> None:
        width = BOARD_WIDTH * CELL_SIZE
        height = BOARD_HEIGHT * CELL_SIZE
        for x in range(0, width + 1, CELL_SIZE):
            self.canvas.create_line(x, 0, x, height, fill=GRID)
        for y in range(0, height + 1, CELL_SIZE):
            self.canvas.create_line(0, y, width, y, fill=GRID)

    def _draw_cell(
        self, point: tuple[int, int], color: str, *, inset: int, oval: bool = False
    ) -> None:
        x, y = point
        bounds = (
            x * CELL_SIZE + inset,
            y * CELL_SIZE + inset,
            (x + 1) * CELL_SIZE - inset,
            (y + 1) * CELL_SIZE - inset,
        )
        if oval:
            self.canvas.create_oval(*bounds, fill=color, outline="")
        else:
            self.canvas.create_rectangle(*bounds, fill=color, outline="")

    def _draw_overlay(self, message: str) -> None:
        center_x = BOARD_WIDTH * CELL_SIZE / 2
        center_y = BOARD_HEIGHT * CELL_SIZE / 2
        self.canvas.create_rectangle(
            30,
            center_y - 40,
            BOARD_WIDTH * CELL_SIZE - 30,
            center_y + 40,
            fill=BACKGROUND,
            outline=SNAKE,
            width=2,
        )
        self.canvas.create_text(
            center_x,
            center_y,
            text=message,
            fill=TEXT,
            font=("Arial", 16, "bold"),
        )


def main() -> None:
    root = tk.Tk()
    SnakeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

