#!/bin/zsh
cd -- "$(dirname -- "$0")/.." || exit 1
./run.sh --vfs example.zip --script scripts/missing.txt