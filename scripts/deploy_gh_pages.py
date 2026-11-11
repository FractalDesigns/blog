#!/usr/bin/env python3
"""Deploys the pre-built `build/` directory directly to the `gh-pages` branch.

This bypasses GitHub Actions runners completely, allowing deployment even if
GitHub Actions is locked or disabled on the account.
"""

import subprocess
import sys
import os
import shutil

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    build_dir = os.path.join(root_dir, "build")

    if not os.path.isdir(build_dir):
        print("Error: build/ directory not found. Please run 'just build-all' first.", file=sys.stderr)
        sys.exit(1)

    # Ensure .nojekyll exists
    nojekyll = os.path.join(build_dir, ".nojekyll")
    open(nojekyll, "a").close()

    try:
        remote_url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=root_dir,
            text=True
        ).strip()
    except Exception as e:
        print(f"Error getting remote.origin.url: {e}", file=sys.stderr)
        sys.exit(1)

    git_dir = os.path.join(build_dir, ".git")
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)

    print("→ Initializing static deployment commit from build/...")
    subprocess.run(["git", "init"], cwd=build_dir, check=True)
    subprocess.run(["git", "checkout", "-B", "gh-pages"], cwd=build_dir, check=True)
    subprocess.run(["git", "add", "-A"], cwd=build_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Deploy to GitHub Pages [skip ci]"], cwd=build_dir, check=True)

    print(f"→ Pushing static site directly to {remote_url} (gh-pages branch)...")
    subprocess.run(["git", "push", "-f", remote_url, "gh-pages"], cwd=build_dir, check=True)

    shutil.rmtree(git_dir, ignore_errors=True)
    print("✓ Successfully pushed to gh-pages branch!")
    print("  Make sure your GitHub Repo Settings → Pages is set to:")
    print("  • Source: 'Deploy from a branch'")
    print("  • Branch: 'gh-pages' / '/ (root)'")

if __name__ == "__main__":
    main()
