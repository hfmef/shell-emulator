"""Проверки конфигурации и стартового скрипта."""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

SOURCE_DIRECTORY = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_DIRECTORY))

from config import Configuration, parse_arguments
from startup import read_startup_script

class ConfigurationTests(unittest.TestCase):
    """Проверяет параметры запуска."""

    def test_default_parameters(self):
        """Без параметров пути остаются пустыми."""
        configuration = parse_arguments([])
        self.assertEqual(configuration.vfs_path, "")
        self.assertEqual(configuration.startup_script, "")

    def test_explicit_parameters(self):
        """Оба переданных пути сохраняются."""
        configuration = parse_arguments([
            "--vfs", "my files/example.zip",
            "--script", "scripts/stage2.txt",
        ])
        self.assertEqual(
            configuration.vfs_path, "my files/example.zip"
        )
        self.assertEqual(
            configuration.startup_script, "scripts/stage2.txt"
        )

    def test_configuration_dump(self):
        """Настройки выводятся в формате ключ=значение."""
        configuration = Configuration("example.zip", "start.txt")
        self.assertEqual(
            configuration.dump(),
            "vfs_path=example.zip\nstartup_script=start.txt",
        )

    def test_unknown_parameter(self):
        """Неизвестный параметр вызывает ошибку запуска."""
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                parse_arguments(["--unknown"])
        self.assertEqual(error.exception.code, 2)

    def test_missing_parameter_value(self):
        """Параметр без значения вызывает ошибку."""
        for option in ("--vfs", "--script"):
            with self.subTest(option=option):
                with redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as error:
                        parse_arguments([option])
                self.assertEqual(error.exception.code, 2)

class StartupScriptTests(unittest.TestCase):
    """Проверяет чтение команд из файла."""

    def setUp(self):
        """Создаёт временную папку для каждого теста."""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "startup.txt"

    def test_comments_and_line_numbers(self):
        """Комментарии пропускаются, номера строк сохраняются."""
        self.path.write_text(
            "# Комментарий\n\nls # список\n  cd Documents  \n",
            encoding="utf-8",
        )
        self.assertEqual(
            read_startup_script(self.path),
            [(3, "ls"), (4, "cd Documents")],
        )

    def test_empty_script(self):
        """Пустой файл не содержит команд."""
        self.path.write_text("", encoding="utf-8")
        self.assertEqual(read_startup_script(self.path), [])

    def test_utf8_bom(self):
        """Метка BOM в начале файла не мешает чтению."""
        self.path.write_text("conf-dump\n", encoding="utf-8-sig")
        self.assertEqual(
            read_startup_script(self.path),
            [(1, "conf-dump")],
        )

    def test_missing_file(self):
        """Отсутствующий файл вызывает понятную ошибку."""
        with self.assertRaisesRegex(
            ValueError, "Не удалось прочитать"
        ):
            read_startup_script(self.path)

    def test_invalid_encoding(self):
        """Файл с неправильной кодировкой вызывает ошибку."""
        self.path.write_bytes(b"\xff\xfe")
        with self.assertRaisesRegex(
            ValueError, "Не удалось прочитать"
        ):
            read_startup_script(self.path)

if __name__ == "__main__":
    unittest.main()