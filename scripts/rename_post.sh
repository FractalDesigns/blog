#!/usr/bin/env bash
set -euo pipefail

# Find repository root
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Ensure fzf is installed
if ! command -v fzf &>/dev/null; then
    echo "Error: fzf is required for interactive post selection, but it was not found in PATH."
    exit 1
fi

# Collect all .rst posts
posts=$(ls -1 source/posts/*.rst 2>/dev/null | xargs -n 1 basename 2>/dev/null || true)
if [ -z "$posts" ]; then
    echo "No blog posts found in source/posts/."
    exit 0
fi

# Interactive selection using fzf
selected=$(echo "$posts" | fzf --prompt="Select post to rename > " \
    --header="Enter: select | Esc: cancel" \
    --preview="head -n 30 source/posts/{}" \
    --preview-window=right:60%:wrap) || true

if [ -z "${selected:-}" ]; then
    echo "No post selected. Aborted."
    exit 0
fi

echo "Selected post: $selected"
read -r -p "Enter new post title: " new_title

if [ -z "${new_title// }" ]; then
    echo "Error: Post title cannot be empty. Aborted."
    exit 1
fi

python3 scripts/rename_post.py "$selected" "$new_title"
