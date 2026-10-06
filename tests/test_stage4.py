import unittest

from src.vfs import VirtualFileSystem

class TestStage4(unittest.TestCase):
    """Тесты команд чтения VFS для этапа 4."""

    def setUp(self):
        """Создаёт тестовую VFS."""
        self.vfs = VirtualFileSystem()

        self.vfs.directories.update(
            {
                "/docs",
                "/docs/projects",
                "/docs/projects/python",
            }
        )

        self.vfs.files.update(
            {
                "/hello.txt": b"Hello",
                "/docs/readme.txt": b"Readme",
                "/docs/projects/task.txt": b"Task",
                "/docs/projects/python/main.py": b"print('Hello')",
            }
        )

    def test_ls_root(self):
        """Проверяет ls в корневом каталоге."""
        result = self.vfs.list_dir("/")

        self.assertIn("docs/", result)
        self.assertIn("hello.txt", result)

    def test_ls_nested_directory(self):
        """Проверяет ls во вложенном каталоге."""
        result = self.vfs.list_dir("/docs")

        self.assertIn("projects/", result)
        self.assertIn("readme.txt", result)

    def test_cd(self):
        """Проверяет переход в каталог."""
        self.vfs.change_dir("/docs")

        self.assertEqual(
            self.vfs.get_current_dir(),
            "/docs",
        )

    def test_relative_cd(self):
        """Проверяет относительный переход."""
        self.vfs.change_dir("/docs")
        self.vfs.change_dir("projects")

        self.assertEqual(
            self.vfs.get_current_dir(),
            "/docs/projects",
        )

    def test_cd_parent(self):
        """Проверяет переход через две точки."""
        self.vfs.change_dir("/docs/projects")
        self.vfs.change_dir("..")

        self.assertEqual(
            self.vfs.get_current_dir(),
            "/docs",
        )

    def test_deep_directory(self):
        """Проверяет три уровня вложенности."""
        self.vfs.change_dir(
            "/docs/projects/python"
        )

        result = self.vfs.list_dir(".")

        self.assertIn(
            "main.py",
            result,
        )

    def test_missing_directory(self):
        """Проверяет ошибку отсутствующего каталога."""
        with self.assertRaises(ValueError):
            self.vfs.change_dir(
                "/missing"
            )

if __name__ == "__main__":
    unittest.main()