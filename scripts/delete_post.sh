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
selected=$(echo "$posts" | fzf --prompt="Select post to delete > " \
    --header="Enter: delete | Esc: cancel" \
    --preview="head -n 30 source/posts/{}" \
    --preview-window=right:60%:wrap) || true

if [ -z "${selected:-}" ]; then
    echo "No post selected. Aborted."
    exit 0
fi

base="${selected%.rst}"

# Delete the post source and its generated files
rm -f "source/posts/${selected}"
rm -f "posts/${base}.html"
rm -f "_sources/posts/${selected}.txt"
echo "✓ Deleted source/posts/${selected}"

# Clean any orphaned posts in posts/
for html in posts/*.html; do
    [ -f "$html" ] || continue
    b=$(basename "$html" .html)
    if [ ! -f "source/posts/${b}.rst" ]; then
        rm -f "$html" "_sources/posts/${b}.rst.txt"
    fi
done

# Rebuild ALL pages (-a -E) so sidebars and navigation links are completely refreshed
echo "→ Updating blog index and sidebars on all pages..."
if command -v sphinx-build &>/dev/null; then
    sphinx-build -a -E -b html source/ .
elif [ -x "/home/linuxbrew/.linuxbrew/bin/sphinx-build" ]; then
    /home/linuxbrew/.linuxbrew/bin/sphinx-build -a -E -b html source/ .
fi
touch .nojekyll
echo "✓ Blog updated successfully. Sidebars refreshed across all pages."
