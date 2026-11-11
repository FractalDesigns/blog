#!/usr/bin/env python3
import sys
import os
import re
import subprocess
import unicodedata

def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text or "untitled"

def main():
    if len(sys.argv) < 3:
        print("Usage: rename_post.py <old_filename> <new_title>", file=sys.stderr)
        sys.exit(1)

    old_filename = sys.argv[1].strip()
    new_title = sys.argv[2].strip()

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    posts_dir = os.path.join(root_dir, "source", "posts")
    old_path = os.path.join(posts_dir, old_filename)

    if not os.path.exists(old_path):
        print(f"Error: {old_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    # Preserve date prefix if present (e.g. 2026-11-06-)
    match = re.match(r"^(\d{4}-\d{2}-\d{2})-(.*)\.rst$", old_filename)
    new_slug = slugify(new_title)
    if match:
        date_prefix = match.group(1)
        new_filename = f"{date_prefix}-{new_slug}.rst"
    else:
        new_filename = f"{new_slug}.rst"

    new_path = os.path.join(posts_dir, new_filename)

    if new_path != old_path and os.path.exists(new_path):
        print(f"Error: Target file {new_filename} already exists.", file=sys.stderr)
        sys.exit(1)

    # Read old file and update title heading (first line + matching underline)
    with open(old_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    replaced = False
    for i in range(len(lines) - 1):
        line = lines[i].strip()
        next_line = lines[i+1].strip()
        if line and next_line and set(next_line) == {'='} and len(next_line) >= 3:
            lines[i] = new_title
            lines[i+1] = "=" * max(len(new_title), 4)
            replaced = True
            break

    if not replaced:
        underline = "=" * max(len(new_title), 4)
        new_content = f"{new_title}\n{underline}\n\n" + content
    else:
        new_content = "\n".join(lines) + "\n"

    # Write new file
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    # If filename changed, remove old source and old compiled HTML
    if new_path != old_path:
        os.remove(old_path)
        old_base = old_filename.removesuffix(".rst")
        old_html = os.path.join(root_dir, "posts", f"{old_base}.html")
        if os.path.exists(old_html):
            os.remove(old_html)
        old_src_txt = os.path.join(root_dir, "_sources", "posts", f"{old_filename}.txt")
        if os.path.exists(old_src_txt):
            os.remove(old_src_txt)

    print(f"✓ Renamed post to: {new_filename} ('{new_title}')")

    # Clean any orphaned posts in posts/
    posts_html_dir = os.path.join(root_dir, "posts")
    if os.path.isdir(posts_html_dir):
        for fname in os.listdir(posts_html_dir):
            if fname.endswith(".html"):
                base_name = fname.removesuffix(".html")
                if not os.path.exists(os.path.join(posts_dir, f"{base_name}.rst")):
                    try:
                        os.remove(os.path.join(posts_html_dir, fname))
                    except OSError:
                        pass

    # Rebuild blog
    print("→ Rebuilding blog...")
    env = os.environ.copy()
    env["PATH"] = f"/home/linuxbrew/.linuxbrew/bin:{os.path.expanduser('~')}/.cargo/bin:{env.get('PATH', '')}"
    subprocess.run(["sphinx-build", "-a", "-E", "-b", "html", "source/", "."], cwd=root_dir, env=env, check=True)
    with open(os.path.join(root_dir, ".nojekyll"), "w") as f:
        pass
    print("✓ Blog successfully rebuilt with updated title and navigation.")

if __name__ == "__main__":
    main()
