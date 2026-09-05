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


def compute_fan(n: int):
    """Return per-image {rot, x, z} resting offsets so images fan out from
    center. No image's resting position is dead-center — only the
    'active' class (applied via JS on click) pulls a photo to center,
    so every photo always has a reachable, distinct resting spot to
    click back to."""
    fan = []
    for i in range(n):
        side = 1 if i % 2 == 0 else -1
        magnitude = i // 2 + 1
        rot = side * 6 * magnitude
        x = side * 16 * magnitude
        fan.append({"rot": rot, "x": x, "z": n - i})
    return fan


def build() -> None:
    resume_data = load_json(DATA_FILE)
    biography_data = load_json(BIOGRAPHY_FILE) if BIOGRAPHY_FILE.exists() else {}

    chapters = biography_data.get("chapters", [])
    for ch in chapters:
        images = ch.get("images") or ([ch["image"]] if ch.get("image") else [])
        ch["images"] = images
        ch["fan"] = compute_fan(len(images))

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    env.globals["zip"] = zip
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Biography homepage
    index_template = env.get_template("index.html.j2")
    index_html = index_template.render(
        basics=resume_data.get("basics", {}),
        intro=biography_data.get("intro"),
        chapters=chapters,
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
