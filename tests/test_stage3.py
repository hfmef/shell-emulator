import os
import tempfile
import unittest
import zipfile

from src.vfs import VirtualFileSystem

class TestStage3(unittest.TestCase):
    """Тесты виртуальной файловой системы этапа 3."""

    def test_default_vfs(self):
        vfs = VirtualFileSystem()

        self.assertTrue(vfs.is_dir("/"))
        self.assertTrue(vfs.is_file("/readme.txt"))

    def test_zip_vfs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "test.zip")

            with zipfile.ZipFile(zip_path, "w") as archive:
                archive.writestr("hello.txt", "Hello!")
                archive.writestr(
                    "level1/level2/level3/file.txt",
                    "Deep file"
                )

            vfs = VirtualFileSystem(zip_path)

            self.assertTrue(vfs.is_file("/hello.txt"))
            self.assertTrue(vfs.is_dir("/level1"))
            self.assertTrue(vfs.is_dir("/level1/level2"))
            self.assertTrue(vfs.is_dir("/level1/level2/level3"))
            self.assertTrue(
                vfs.is_file("/level1/level2/level3/file.txt")
            )

    def test_missing_zip(self):
        with self.assertRaises(ValueError):
            VirtualFileSystem("missing_vfs.zip")

    def test_invalid_zip(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(b"This is not a ZIP file")
            file.flush()

            with self.assertRaises(ValueError):
                VirtualFileSystem(file.name)

if __name__ == "__main__":
    unittest.main()