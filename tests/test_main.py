"""Тесты разбора команд."""

import sys
import unittest
from pathlib import Path


SOURCE_DIRECTORY = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_DIRECTORY))

from main import parse_input


class ParseInputTests(unittest.TestCase):
    """Проверяет функцию разбора команд."""

    def test_empty_input(self):
        """Пустая строка даёт пустые значения."""
        self.assertEqual(parse_input("   "), ("", []))

    def test_command_without_arguments(self):
        """Команда без аргументов разбирается правильно."""
        self.assertEqual(parse_input("ls"), ("ls", []))

    def test_command_with_arguments(self):
        """Команда и аргументы разделяются пробелами."""
        actual = parse_input("cd Documents Projects")
        expected = ("cd", ["Documents", "Projects"])
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()