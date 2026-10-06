import io
import posixpath
import zipfile

class VirtualFileSystem:
    """Виртуальная файловая система, работающая только в памяти."""

    def __init__(self, zip_path=None):
        self.files = {}
        self.directories = {"/"}
        self.current_dir = "/"

        if zip_path:
            self.load_zip(zip_path)
        else:
            self.create_default()

    def create_default(self):
        """Создать VFS по умолчанию."""
        self.files = {
            "/readme.txt": b"Default virtual file system\n"
        }
        self.directories = {"/"}
        self.current_dir = "/"

    def load_zip(self, zip_path):
        """Загрузить ZIP-архив в память без распаковки на диск."""
        self.files = {}
        self.directories = {"/"}
        self.current_dir = "/"

        try:
            with open(zip_path, "rb") as source:
                zip_data = source.read()

            with zipfile.ZipFile(io.BytesIO(zip_data), "r") as archive:
                for info in archive.infolist():
                    path = self._normalize("/" + info.filename)

                    if info.is_dir():
                        self._add_directory(path)
                    else:
                        self.files[path] = archive.read(info.filename)
                        self._add_parent_directories(path)

        except FileNotFoundError as error:
            raise ValueError(
                f"VFS file not found: {zip_path}"
            ) from error

        except zipfile.BadZipFile as error:
            raise ValueError(
                f"Invalid VFS ZIP file: {zip_path}"
            ) from error

    def _normalize(self, path):
        """Привести виртуальный путь к стандартному виду."""
        if not path.startswith("/"):
            path = posixpath.join(
                self.current_dir,
                path,
            )

        path = posixpath.normpath(path)

        if not path.startswith("/"):
            path = "/" + path

        return path

    def _add_directory(self, path):
        """Добавить каталог и его родительские каталоги."""
        path = self._normalize(path)

        while path != "/":
            self.directories.add(path)
            path = posixpath.dirname(path)

        self.directories.add("/")

    def _add_parent_directories(self, path):
        """Добавить каталоги, необходимые для файла."""
        parent = posixpath.dirname(path)
        self._add_directory(parent)

    def exists(self, path):
        """Проверить существование файла или каталога."""
        path = self._normalize(path)

        return (
            path in self.files
            or path in self.directories
        )

    def is_file(self, path):
        """Проверить, является ли путь файлом."""
        return self._normalize(path) in self.files

    def is_dir(self, path):
        """Проверить, является ли путь каталогом."""
        return self._normalize(path) in self.directories

    def list_dir(self, path="."):
        """Возвращает содержимое виртуального каталога."""
        path = self._normalize(path)

        if path not in self.directories:
            raise ValueError(
                f"каталог не найден: {path}"
            )

        entries = set()

        for directory in self.directories:
            if directory == path:
                continue

            parent = posixpath.dirname(directory)

            if parent == path:
                entries.add(
                    posixpath.basename(directory) + "/"
                )

        for file_path in self.files:
            parent = posixpath.dirname(file_path)

            if parent == path:
                entries.add(
                    posixpath.basename(file_path)
                )

        return sorted(entries)

    def change_dir(self, path="/"):
        """Изменяет текущий каталог VFS."""
        if not path:
            path = "/"

        target = self._normalize(path)

        if target not in self.directories:
            raise ValueError(
                f"каталог не найден: {target}"
            )

        self.current_dir = target


    def get_current_dir(self):
        """Возвращает текущий каталог VFS."""
        return self.current_dir

    def make_dir(self, path):
        """Создаёт новый каталог в VFS."""
        if not path:
            raise ValueError(
                "не указано имя каталога."
            )

        target = self._normalize(path)

        if self.exists(target):
            raise ValueError(
                f"файл или каталог уже существует: {target}"
            )

        parent = posixpath.dirname(target)

        if parent not in self.directories:
            raise ValueError(
                f"родительский каталог не найден: {parent}"
            )

        self.directories.add(target)

    def remove_dir(self, path):
        """Удаляет пустой каталог из VFS."""
        if not path:
            raise ValueError(
                "не указано имя каталога."
            )

        target = self._normalize(path)

        if target == "/":
            raise ValueError(
                "нельзя удалить корневой каталог."
            )

        if target not in self.directories:
            raise ValueError(
                f"каталог не найден: {target}"
            )

        prefix = target + "/"

        for directory in self.directories:
            if (
                directory != target
                and directory.startswith(prefix)
            ):
                raise ValueError(
                    f"каталог не пуст: {target}"
                )

        for file_path in self.files:
            if file_path.startswith(prefix):
                raise ValueError(
                    f"каталог не пуст: {target}"
                )

        if self.current_dir == target:
            raise ValueError(
                "нельзя удалить текущий каталог."
            )

        self.directories.remove(target) 