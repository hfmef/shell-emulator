import unittest

from src.vfs import VirtualFileSystem

class TestStage5(unittest.TestCase):
    """Тесты изменения виртуальной файловой системы."""

    def setUp(self):
        """Создаёт чистую VFS перед каждым тестом."""
        self.vfs = VirtualFileSystem()

    def test_mkdir(self):
        """Проверяет создание каталога."""
        self.vfs.make_dir("/test")

        self.assertTrue(
            self.vfs.is_dir("/test")
        )

    def test_mkdir_relative(self):
        """Проверяет создание каталога относительным путём."""
        self.vfs.make_dir("/docs")
        self.vfs.change_dir("/docs")
        self.vfs.make_dir("projects")

        self.assertTrue(
            self.vfs.is_dir("/docs/projects")
        )

    def test_mkdir_existing(self):
        """Нельзя создать уже существующий каталог."""
        self.vfs.make_dir("/test")

        with self.assertRaises(ValueError):
            self.vfs.make_dir("/test")

    def test_mkdir_missing_parent(self):
        """Нельзя создать каталог внутри отсутствующего."""
        with self.assertRaises(ValueError):
            self.vfs.make_dir(
                "/missing/test"
            )

    def test_rmdir(self):
        """Проверяет удаление пустого каталога."""
        self.vfs.make_dir("/test")
        self.vfs.remove_dir("/test")

        self.assertFalse(
            self.vfs.is_dir("/test")
        )

    def test_rmdir_missing(self):
        """Нельзя удалить отсутствующий каталог."""
        with self.assertRaises(ValueError):
            self.vfs.remove_dir(
                "/missing"
            )

    def test_rmdir_non_empty(self):
        """Нельзя удалить непустой каталог."""
        self.vfs.make_dir("/parent")
        self.vfs.make_dir("/parent/child")

        with self.assertRaises(ValueError):
            self.vfs.remove_dir(
                "/parent"
            )

    def test_rmdir_root(self):
        """Нельзя удалить корневой каталог."""
        with self.assertRaises(ValueError):
            self.vfs.remove_dir("/")

    def test_rmdir_current_directory(self):
        """Нельзя удалить текущий каталог."""
        self.vfs.make_dir("/test")
        self.vfs.change_dir("/test")

        with self.assertRaises(ValueError):
            self.vfs.remove_dir("/test")

if __name__ == "__main__":
    unittest.main()