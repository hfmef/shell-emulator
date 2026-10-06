#!/bin/zsh

echo "=== VFS по умолчанию ==="
./run.sh --script scripts/stage3.txt

echo "=== Минимальная VFS ==="
./run.sh --vfs vfs_samples/minimal.zip

echo "=== VFS с несколькими файлами ==="
./run.sh --vfs vfs_samples/files.zip

echo "=== VFS с тремя уровнями ==="
./run.sh --vfs vfs_samples/deep.zip