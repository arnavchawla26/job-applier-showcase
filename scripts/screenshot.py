"""Render assets/demo_tracker.html to assets/tracker.png with headless Chromium (Playwright).

Usage:  python3 -I scripts/screenshot.py          (needs `pip install playwright && playwright install chromium`)
The page is a static copy of the app's Tracker page with demo rows; nothing personal is rendered.
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=2)
    page.goto((ROOT / "assets" / "demo_tracker.html").as_uri())
    page.screenshot(path=str(ROOT / "assets" / "tracker.png"), full_page=True)
    browser.close()
print("wrote", ROOT / "assets" / "tracker.png")
