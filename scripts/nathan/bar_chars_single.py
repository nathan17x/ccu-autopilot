from playwright.sync_api import sync_playwright
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_dir)
from ccu_autopilot import AutoPilot

IP_ADDR = "10.49.6.23"
USER = "admin"
PW = "hdcu5500"

with sync_playwright() as p:
  browser = p.chromium.launch(slow_mo=100, headless=False)
  context = browser.new_context(
    http_credentials={"username": USER, "password": PW},
    viewport={"height": 1080, "width": 1920}
  )
  page = context.new_page()
  page.goto(f"http://{IP_ADDR}")

  ap = AutoPilot(page)

  ap.open_osd()

  page.wait_for_timeout(1000)


