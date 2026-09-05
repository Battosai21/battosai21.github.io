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
BIOGRAPHY_FILE = ROOT / "data" / "biography.json"
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"
ASSETS_DIR = ROOT / "assets"


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build() -> None:
    resume_data = load_json(DATA_FILE)
    biography_data = load_json(BIOGRAPHY_FILE) if BIOGRAPHY_FILE.exists() else {}

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Biography homepage
    index_template = env.get_template("index.html.j2")
    index_html = index_template.render(
        basics=resume_data.get("basics", {}),
        intro=biography_data.get("intro"),
        chapters=biography_data.get("chapters", []),
    )
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    # Resume page
    resume_template = env.get_template("resume.html.j2")
    resume_html = resume_template.render(**resume_data)
    (OUTPUT_DIR / "resume.html").write_text(resume_html, encoding="utf-8")

    if ASSETS_DIR.exists():
        dest = OUTPUT_DIR / "assets"
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(ASSETS_DIR, dest)

    print(f"Built index.html and resume.html in {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
