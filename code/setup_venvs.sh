#!/usr/bin/env bash
# Creates a .venv inside each chapter directory and installs its requirements.txt
# Usage: bash setup_venvs.sh [chapter1 chapter2 ...]
#   - No args: sets up all chapters
#   - With args: sets up only specified chapters

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

chapters=("chapter1" "chapter2" "chapter3" "chapter4" "chapter5"
          "chapter6" "chapter7" "chapter8" "chapter9" "chapter10"
          "chapter11" "chapter12" "chapter13" "chapter14" "chapter15")

# If specific chapters are given as args, use those instead
if [ $# -gt 0 ]; then
  chapters=("$@")
fi

for chapter in "${chapters[@]}"; do
  dir="$SCRIPT_DIR/$chapter"

  if [ ! -d "$dir" ]; then
    echo "⚠  $chapter: directory not found, skipping"
    continue
  fi

  # Find requirements.txt (top-level or first subdirectory)
  req=""
  if [ -f "$dir/requirements.txt" ]; then
    req="$dir/requirements.txt"
  else
    req=$(find "$dir" -maxdepth 2 -name "requirements.txt" | head -1)
  fi

  if [ -z "$req" ]; then
    echo "⚠  $chapter: no requirements.txt found, skipping"
    continue
  fi

  echo ""
  echo "=== Setting up $chapter ==="

  venv_dir="$dir/.venv"
  if [ -d "$venv_dir" ]; then
    echo "   .venv already exists, skipping creation"
  else
    python -m venv "$venv_dir"
    echo "   Created .venv"
  fi

  # Use python -m pip to avoid .exe execution issues in Git Bash on Windows
  if [ -f "$venv_dir/Scripts/python.exe" ]; then
    python_bin="$venv_dir/Scripts/python.exe"
  else
    python_bin="$venv_dir/bin/python"
  fi

  # Bootstrap pip if it's missing (venv created without it)
  "$python_bin" -m pip --version &>/dev/null || "$python_bin" -m ensurepip

  "$python_bin" -m pip install --upgrade pip -q
  "$python_bin" -m pip install -r "$req"
  echo "   Installed: $req"
done

echo ""
echo "Done. To activate a chapter's environment:"
echo "  Windows:  .\\chapterN\\.venv\\Scripts\\activate"
echo "  macOS/Linux: source chapterN/.venv/bin/activate"
