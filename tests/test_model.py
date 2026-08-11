import random
import unittest

from snake_game import Direction, GameStatus, SnakeGame


class SnakeGameTests(unittest.TestCase):
    def make_game(self, width: int = 8, height: int = 6) -> SnakeGame:
        return SnakeGame(width, height, rng=random.Random(7))

    def test_initial_state(self) -> None:
        game = self.make_game()

        self.assertEqual(GameStatus.READY, game.status)
        self.assertEqual(Direction.RIGHT, game.direction)
        self.assertEqual(3, len(game.snake))
        self.assertNotIn(game.food, game.snake)
        self.assertEqual(0, game.score)

    def test_board_must_fit_initial_snake(self) -> None:
        with self.assertRaises(ValueError):
            SnakeGame(3, 3)
        with self.assertRaises(ValueError):
            SnakeGame(4, 0)

    def test_step_only_moves_while_running(self) -> None:
        game = self.make_game()
        original = list(game.snake)

        self.assertFalse(game.step())
        self.assertEqual(original, game.snake)
        game.start_or_toggle_pause()
        self.assertTrue(game.step())
        self.assertNotEqual(original, game.snake)

    def test_pause_and_resume(self) -> None:
        game = self.make_game()

        game.start_or_toggle_pause()
        self.assertEqual(GameStatus.RUNNING, game.status)
        game.start_or_toggle_pause()
        self.assertEqual(GameStatus.PAUSED, game.status)
        game.start_or_toggle_pause()
        self.assertEqual(GameStatus.RUNNING, game.status)

    def test_rejects_reverse_direction(self) -> None:
        game = self.make_game()

        self.assertFalse(game.change_direction(Direction.LEFT))
        self.assertEqual(Direction.RIGHT, game.pending_direction)
        self.assertTrue(game.change_direction(Direction.UP))
        self.assertFalse(game.change_direction(Direction.LEFT))
        self.assertEqual(Direction.UP, game.pending_direction)

    def test_turn_is_applied_on_next_step(self) -> None:
        game = self.make_game()
        game.start_or_toggle_pause()
        old_head = game.snake[0]

        game.change_direction(Direction.UP)
        game.step()

        self.assertEqual((old_head[0], old_head[1] - 1), game.snake[0])
        self.assertEqual(Direction.UP, game.direction)

    def test_eating_grows_snake_and_scores(self) -> None:
        game = self.make_game()
        game.start_or_toggle_pause()
        head_x, head_y = game.snake[0]
        game.food = (head_x + 1, head_y)
        old_length = len(game.snake)

        self.assertTrue(game.step())

        self.assertEqual(old_length + 1, len(game.snake))
        self.assertEqual(1, game.score)
        self.assertNotIn(game.food, game.snake)

    def test_wall_collision_ends_game(self) -> None:
        game = self.make_game()
        game.snake = [(game.width - 1, 2), (game.width - 2, 2), (game.width - 3, 2)]
        game.start_or_toggle_pause()

        self.assertFalse(game.step())
        self.assertEqual(GameStatus.GAME_OVER, game.status)

    def test_self_collision_ends_game(self) -> None:
        game = self.make_game()
        game.snake = [(3, 2), (3, 1), (2, 1), (2, 2), (2, 3), (3, 3)]
        game.direction = Direction.UP
        game.pending_direction = Direction.LEFT
        game.status = GameStatus.RUNNING

        self.assertFalse(game.step())
        self.assertEqual(GameStatus.GAME_OVER, game.status)

    def test_can_move_into_vacating_tail_cell(self) -> None:
        game = self.make_game()
        game.snake = [(3, 2), (3, 1), (2, 1), (2, 2)]
        game.direction = Direction.UP
        game.pending_direction = Direction.LEFT
        game.food = (7, 5)
        game.status = GameStatus.RUNNING

        self.assertTrue(game.step())
        self.assertEqual((2, 2), game.snake[0])
        self.assertEqual(GameStatus.RUNNING, game.status)

    def test_food_is_placed_on_only_available_cell(self) -> None:
        game = SnakeGame(4, 1, rng=random.Random(2))
        game.snake = [(2, 0), (1, 0), (0, 0)]

        self.assertEqual((3, 0), game._place_food())

    def test_filling_board_wins_game(self) -> None:
        game = SnakeGame(4, 1, rng=random.Random(2))
        game.snake = [(2, 0), (1, 0), (0, 0)]
        game.food = (3, 0)
        game.status = GameStatus.RUNNING

        self.assertTrue(game.step())
        self.assertEqual(GameStatus.WON, game.status)
        self.assertIsNone(game.food)
        self.assertEqual(1, game.score)

    def test_reset_restores_new_game(self) -> None:
        game = self.make_game()
        game.status = GameStatus.GAME_OVER
        game.score = 9
        game.snake = [(0, 0)]

        game.reset()

        self.assertEqual(GameStatus.READY, game.status)
        self.assertEqual(0, game.score)
        self.assertEqual(3, len(game.snake))


if __name__ == "__main__":
    unittest.main()
