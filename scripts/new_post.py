#!/usr/bin/env python3
import sys
import os
import re
import unicodedata
from datetime import datetime

def slugify(text: str) -> str:
    # Normalize accented characters (e.g., é -> e)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text or "untitled"

def main():
    if len(sys.argv) > 1:
        title = " ".join(sys.argv[1:]).strip()
    else:
        title = input("Enter post title: ").strip()

    if not title:
        print("Error: Post title cannot be empty.")
        sys.exit(1)

    now = datetime.now()
    date_prefix = now.strftime("%Y-%m-%d")
    date_display = now.strftime("%B %d, %Y")
    slug = slugify(title)

    filename = f"{date_prefix}-{slug}.rst"
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    posts_dir = os.path.join(project_root, "source", "posts")
    os.makedirs(posts_dir, exist_ok=True)
    file_path = os.path.join(posts_dir, filename)
    rel_path = os.path.relpath(file_path, project_root)

    if os.path.exists(file_path):
        print(f"Error: File already exists at {rel_path}")
        sys.exit(1)

    underline = "=" * max(len(title), 4)
    content = f"""{title}
{underline}

:date: {date_display}
:author: Achraf Elafrit

Write your content here...
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ Created new blog post: {rel_path}")
    print(f"  → Ready for you to edit in {rel_path}")

if __name__ == "__main__":
    main()
