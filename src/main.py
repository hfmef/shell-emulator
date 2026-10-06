"""Графический эмулятор оболочки. Этап 5: операции с VFS."""

import getpass
import socket
import time
import tkinter as tk
from tkinter import scrolledtext

from config import parse_arguments
from startup import read_startup_script
from vfs import VirtualFileSystem

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 450
PADDING = 12
OUTPUT_HEIGHT = 18
MAX_CD_ARGUMENTS = 1

def get_window_title():
    """Формирует заголовок из реальных данных ОС."""
    username = getpass.getuser()
    hostname = socket.gethostname()
    return f"Эмулятор - [{username}@{hostname}]"

def parse_input(user_input):
    """Разделяет строку на команду и аргументы по пробелам."""
    parts = user_input.strip().split()

    if not parts:
        return "", []

    return parts[0], parts[1:]

class EmulatorWindow:
    """Создаёт окно и обрабатывает команды пользователя."""

    def __init__(self, root, configuration):
        """Настраивает окно, VFS и выполнение скрипта."""
        self.root = root
        self.configuration = configuration
        self.closed = False
        self.start_time = time.monotonic()

        self.root.title(get_window_title())
        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.create_widgets()

        self.add_output("Параметры запуска:")
        self.add_output(
            self.configuration.dump()
        )

        if not self.initialize_vfs():
            return

        self.root.after_idle(
            self.run_startup_script
        )

    def create_widgets(self):
        """Создаёт поле ввода, кнопку и область вывода."""
        frame = tk.Frame(
            self.root,
            padx=PADDING,
            pady=PADDING,
        )
        frame.pack(
            fill=tk.BOTH,
            expand=True,
        )

        label = tk.Label(
            frame,
            text="Введите команду:",
        )
        label.pack(anchor=tk.W)

        self.command_entry = tk.Entry(frame)
        self.command_entry.pack(
            fill=tk.X,
            pady=(0, PADDING),
        )
        self.command_entry.bind(
            "<Return>",
            self.on_enter,
        )

        run_button = tk.Button(
            frame,
            text="Выполнить",
            command=self.execute_command,
        )
        run_button.pack(
            anchor=tk.W,
            pady=(0, PADDING),
        )

        self.output = scrolledtext.ScrolledText(
            frame,
            height=OUTPUT_HEIGHT,
            state=tk.DISABLED,
        )
        self.output.pack(
            fill=tk.BOTH,
            expand=True,
        )

        self.command_entry.focus()

    def initialize_vfs(self):
        """Загружает VFS или создаёт VFS по умолчанию."""
        try:
            self.vfs = VirtualFileSystem(
                self.configuration.vfs_path
            )
        except ValueError as error:
            self.add_output(
                f"Ошибка загрузки VFS: {error}"
            )
            return False

        if self.configuration.vfs_path:
            self.add_output(
                "VFS успешно загружена в память."
            )
        else:
            self.add_output(
                "Путь к VFS не указан. "
                "Создана VFS по умолчанию в памяти."
            )

        return True

    def add_output(self, message):
        """Добавляет сообщение и прокручивает вывод вниз."""
        self.output.configure(
            state=tk.NORMAL
        )
        self.output.insert(
            tk.END,
            f"{message}\n",
        )
        self.output.configure(
            state=tk.DISABLED
        )
        self.output.see(tk.END)

    def execute_command(self):
        """Передаёт введённую строку на выполнение."""
        user_input = self.command_entry.get()
        self.command_entry.delete(
            0,
            tk.END,
        )
        self.execute_line(user_input)

    def execute_line(
        self,
        user_input,
        line_number=None,
    ):
        """Выполняет строку и показывает ошибки."""
        command, arguments = parse_input(user_input
        )

        if not command:
            return

        self.add_output(
            f"> {user_input}"
        )

        try:
            self.dispatch_command(
                command,
                arguments,
            )
        except ValueError as error:
            location = ""

            if line_number is not None:
                location = (
                    f" в строке {line_number} "
                    "стартового скрипта"
                )

            self.add_output(
                f"Ошибка{location}: {error}"
            )

    def dispatch_command(
        self,
        command,
        arguments,
    ):
        """Выбирает обработчик команды."""
        if command == "exit":
            self.require_no_arguments(
                command,
                arguments,
            )
            self.closed = True
            self.root.destroy()

        elif command == "conf-dump":
            self.require_no_arguments(
                command,
                arguments,
            )
            self.add_output(
                self.configuration.dump()
            )

        elif command == "ls":
            self.command_ls(arguments)

        elif command == "cd":
            self.command_cd(arguments)

        elif command == "echo":
            self.command_echo(arguments)

        elif command == "whoami":
            self.command_whoami(arguments)

        elif command == "uptime":
            self.command_uptime(arguments)

        elif command == "mkdir":
            self.command_mkdir(arguments)

        elif command == "rmdir":
            self.command_rmdir(arguments)

        else:
            raise ValueError(
                f"неизвестная команда '{command}'."
            )

    def require_no_arguments(
        self,
        command,
        arguments,
    ):
        """Отклоняет аргументы у команд без аргументов."""
        if arguments:
            raise ValueError(
                f"команда {command} "
                "не принимает аргументы."
            )

    def require_one_argument(
        self,
        command,
        arguments,
    ):
        """Проверяет наличие ровно одного аргумента."""
        if len(arguments) != 1:
            raise ValueError(
                f"команда {command} "
                "принимает ровно один аргумент."
            )

    def command_ls(self, arguments):
        """Показывает содержимое каталога VFS."""
        if len(arguments) > 1:
            raise ValueError(
                "команда ls принимает "
                "не более одного аргумента."
            )

        path = (
            arguments[0]
            if arguments
            else "."
        )

        entries = self.vfs.list_dir(path)

        if entries:
            self.add_output(
                "  ".join(entries)
            )

    def command_cd(self, arguments):
        """Изменяет текущий каталог VFS."""
        if len(arguments) > MAX_CD_ARGUMENTS:
            raise ValueError(
                "команда cd принимает "
                "не более одного аргумента."
            )

        path = (
            arguments[0]
            if arguments
            else "/"
        )

        self.vfs.change_dir(path)

    def command_echo(self, arguments):
        """Выводит переданные аргументы."""
        self.add_output(
            " ".join(arguments)
        )

    def command_whoami(self, arguments):
        """Показывает имя текущего пользователя."""
        self.require_no_arguments(
            "whoami",
            arguments,
        )

        self.add_output(
            getpass.getuser()
        )

    def command_uptime(self, arguments):
        """Показывает время работы эмулятора."""
        self.require_no_arguments(
            "uptime",
            arguments,
        )

        seconds = int(
            time.monotonic()
            - self.start_time
        )

        self.add_output(
            f"Эмулятор работает {seconds} сек."
        )

    def command_mkdir(self, arguments):
        """Создаёт каталог в виртуальной файловой системе."""
        self.require_one_argument(
            "mkdir",
            arguments,
        )

        self.vfs.make_dir(
            arguments[0]
        )

    def command_rmdir(self, arguments):
        """Удаляет пустой каталог из виртуальной файловой системы."""
        self.require_one_argument(
            "rmdir",
            arguments,
        )

        self.vfs.remove_dir(
            arguments[0]
        )

    def run_startup_script(self):
        """Выполняет стартовый скрипт."""
        path = self.configuration.startup_script

        if not path:
            return

        try:
            commands = read_startup_script(
                path
            )
        except ValueError as error:
            self.add_output(
                f"Ошибка: {error}"
            )
            return

        self.add_output(
            f"Стартовый скрипт: {path}"
        )

        for line_number, command in commands:
            self.execute_line(
                command,
                line_number,
            )

            if self.closed:
                return

        self.add_output(
            "Выполнение стартового скрипта "
            "завершено."
        )

    def on_enter(self, event):
        """Обрабатывает Enter в поле ввода."""
        self.execute_command()
        return "break"

def main():
    """Читает настройки и запускает приложение."""
    configuration = parse_arguments()

    root = tk.Tk()

    EmulatorWindow(
        root,
        configuration,
    )

    root.mainloop()

if __name__ == "__main__":
    main()


