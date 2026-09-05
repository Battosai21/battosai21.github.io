#!/usr/bin/env python3
"""
Build script for the portfolio site.

Reads structured data from data/resume.json and renders it through the
Jinja2 template in templates/index.html.j2 into output/index.html.

Usage:
    python build.py
"""
import json
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "resume.json"
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"
ASSETS_DIR = ROOT / "assets"


def load_data() -> dict:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build() -> None:
    data = load_data()

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("index.html.j2")

    html = template.render(**data)

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / "index.html"
    output_file.write_text(html, encoding="utf-8")

    if ASSETS_DIR.exists():
        dest = OUTPUT_DIR / "assets"
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(ASSETS_DIR, dest)

    print(f"Built {output_file} from {DATA_FILE}")


if __name__ == "__main__":
    build()
