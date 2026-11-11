export PATH := "/home/linuxbrew/.linuxbrew/bin:" + env_var('HOME') + "/.cargo/bin:" + env_var('PATH')

# Build blog directly into root directory (served by GitHub Pages)
build:
    sphinx-build -b html source/ .
    touch .nojekyll

# Build the Rust egui WebAssembly app into source/_static/wasm/
build-wasm:
    python3 scripts/bundle_wasm.py

# Build both WebAssembly and Sphinx blog
build-all: build-wasm build

# Run local web server to preview blog and test WASM in browser
serve:
    python3 -m http.server 8000 --directory .

# Create a new blog post: just new My Post Title
new +title:
    python3 scripts/new_post.py {{title}}

# Delete a post interactively using fzf
delete-post:
    bash scripts/delete_post.sh

alias delete := delete-post
alias rm-post := delete-post
