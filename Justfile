export PATH := env_var('HOME') + "/.cargo/bin:" + env_var('PATH')

# Build HTML blog
build:
    sphinx-build -b html source/ build/

# Build the Rust egui WebAssembly app into source/_static/wasm/
build-wasm:
    python3 scripts/bundle_wasm.py

# Build both WebAssembly and Sphinx blog
build-all: build-wasm build

# Deploy to GitHub Pages via gh-pages branch (bypasses GitHub Actions)
deploy: build-all
    python3 scripts/deploy_gh_pages.py

# Run local web server to preview blog and test WASM in browser
serve:
    python3 -m http.server 8000 --directory build/

# Create a new blog post: just new My Post Title
new +title:
    python3 scripts/new_post.py {{title}}



