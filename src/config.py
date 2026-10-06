"""Параметры запуска эмулятора."""

import argparse
from dataclasses import dataclass

@dataclass
class Configuration:
    """Хранит пути к VFS и стартовому скрипту."""

    vfs_path: str = ""
    startup_script: str = ""

    def dump(self):
        """Возвращает настройки в формате ключ-значение."""
        return (
            f"vfs_path={self.vfs_path}\n"
            f"startup_script={self.startup_script}"
        )

def parse_arguments(arguments=None):
    """Читает параметры командной строки."""
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки ОС. Вариант 7."
    )
    parser.add_argument(
        "--vfs",
        default="",
        help="Путь к ZIP-архиву виртуальной файловой системы.",
    )
    parser.add_argument(
        "--script",
        default="",
        help="Путь к стартовому скрипту эмулятора.",
    )
    options = parser.parse_args(arguments)
    return Configuration(
        vfs_path=options.vfs,
        startup_script=options.script,
    )


