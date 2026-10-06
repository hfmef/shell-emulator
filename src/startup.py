"""Чтение стартового скрипта эмулятора."""

from pathlib import Path

def read_startup_script(path):
    """Читает команды, убирая пустые строки и комментарии."""
    try:
        text = Path(path).read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        raise ValueError(
            f"Не удалось прочитать стартовый скрипт: {error}"
        ) from error

    commands = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        command = line.partition("#")[0].strip()

        if command:
            commands.append((line_number, command))

    return commands


