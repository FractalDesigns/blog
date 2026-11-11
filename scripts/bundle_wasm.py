#!/usr/bin/env python3
"""Builds the egui Rust crate and bundles the WebAssembly binary into an inlined JS module.

This allows the WebAssembly app to run:
1. Directly from disk over `file://` protocol (without needing a local HTTP server)
2. On any static hosting provider like GitHub Pages
"""

import subprocess
import sys
import os
import base64

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    egui_dir = os.path.join(root_dir, "egui_demo")
    out_dir = os.path.join(root_dir, "source", "_static", "wasm")
    os.makedirs(out_dir, exist_ok=True)

    print("→ Compiling egui Rust application to wasm32-unknown-unknown...")
    env = os.environ.copy()
    home = os.path.expanduser("~")
    cargo_bin = os.path.join(home, ".cargo", "bin")
    env["PATH"] = f"{cargo_bin}:{env.get('PATH', '')}"

    subprocess.run(
        ["cargo", "build", "--manifest-path", os.path.join(egui_dir, "Cargo.toml"), "--target", "wasm32-unknown-unknown", "--release"],
        cwd=root_dir,
        env=env,
        check=True
    )

    wasm_input = os.path.join(egui_dir, "target", "wasm32-unknown-unknown", "release", "egui_demo.wasm")
    if not os.path.exists(wasm_input):
        print(f"Error: {wasm_input} not found", file=sys.stderr)
        sys.exit(1)

    print("→ Generating wasm-bindgen bindings (no-modules target for file:// & static web compatibility)...")
    subprocess.run(
        ["wasm-bindgen", "--target", "no-modules", "--out-dir", out_dir, wasm_input, "--no-typescript"],
        env=env,
        check=True
    )

    wasm_bg = os.path.join(out_dir, "egui_demo_bg.wasm")
    print(f"→ Inlining WebAssembly bytes into JS bundle for CORS-free local execution...")
    with open(wasm_bg, "rb") as f:
        wasm_bytes = f.read()

    b64_wasm = base64.b64encode(wasm_bytes).decode("ascii")
    data_js = os.path.join(out_dir, "egui_wasm_data.js")
    with open(data_js, "w", encoding="utf-8") as f:
        f.write('// Auto-generated WebAssembly binary bundle\n')
        f.write(f'window.__EGUI_WASM_BASE64 = "{b64_wasm}";\n')

    print(f"✓ Successfully built and bundled:")
    print(f"  • {os.path.relpath(os.path.join(out_dir, 'egui_demo.js'), root_dir)}")
    print(f"  • {os.path.relpath(data_js, root_dir)}")
    print(f"  • {os.path.relpath(wasm_bg, root_dir)}")

if __name__ == "__main__":
    main()
