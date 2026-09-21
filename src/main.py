"""Графический прототип эмулятора оболочки ОС."""

import getpass
import socket
import tkinter as tk
from tkinter import scrolledtext


WINDOW_WIDTH = 700
WINDOW_HEIGHT = 450
PADDING = 12


def get_window_title():
    """Возвращает заголовок окна с данными текущей ОС."""
    username = getpass.getuser()
    hostname = socket.gethostname()
    return f"Эмулятор - [{username}@{hostname}]"


def parse_input(user_input):
    """Разделяет введённую строку на команду и аргументы."""
    parts = user_input.strip().split()

    if not parts:
        return "", []

    return parts[0], parts[1:]


class EmulatorWindow:
    """Создаёт и обслуживает окно эмулятора."""

    def __init__(self, root):
        """Настраивает главное окно приложения."""
        self.root = root
        self.root.title(get_window_title())
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.create_widgets()

    def create_widgets(self):
        """Создаёт элементы графического интерфейса."""
        frame = tk.Frame(self.root, padx=PADDING, pady=PADDING)
        frame.pack(fill=tk.BOTH, expand=True)

        label = tk.Label(frame, text="Введите команду:")
        label.pack(anchor=tk.W)

        self.command_entry = tk.Entry(frame)
        self.command_entry.pack(fill=tk.X, pady=(0, PADDING))
        self.command_entry.bind("<Return>", self.on_enter)

        run_button = tk.Button(
            frame,
            text="Выполнить",
            command=self.execute_command,
        )
        run_button.pack(anchor=tk.W, pady=(0, PADDING))

        self.output = scrolledtext.ScrolledText(
            frame,
            height=18,
            state=tk.DISABLED,
        )
        self.output.pack(fill=tk.BOTH, expand=True)
        self.command_entry.focus()

    def add_output(self, message):
        """Добавляет сообщение в область вывода."""
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, f"{message}\n")
        self.output.configure(state=tk.DISABLED)
        self.output.see(tk.END)

    def execute_command(self):
        """Разбирает и выполняет введённую команду."""
        user_input = self.command_entry.get()
        command, arguments = parse_input(user_input)

        if not command:
            return

        self.add_output(f"> {user_input}")
        self.command_entry.delete(0, tk.END)

        if command == "exit":
            self.root.destroy()
            return

        if command in {"ls", "cd"}:
            self.run_stub(command, arguments)
            return

        self.add_output(f"Ошибка: неизвестная команда '{command}'.")

    def run_stub(self, command, arguments):
        """Выводит результат работы команды-заглушки."""
        if command == "cd" and len(arguments) > 1:
            self.add_output("Ошибка: команда cd принимает не более одного аргумента.")
            return

        arguments_text = " ".join(arguments) or "нет"
        self.add_output(
            f"Команда-заглушка: {command}; аргументы: {arguments_text}."
        )

    def on_enter(self, event):
        """Запускает команду после нажатия Enter."""
        self.execute_command()
        return "break"


def main():
    """Запускает приложение."""
    root = tk.Tk()
    EmulatorWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()