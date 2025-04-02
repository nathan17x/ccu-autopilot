from playwright.sync_api import sync_playwright
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_dir)
from ccu_autopilot import AutoPilot

IP_ADDR = "10.49.6.23"
USER = "admin"
PW = "hdcu5500"

def create_border_block(para: str):
  para_lines = para.splitlines()
  if len(para_lines) > 14:
    raise Exception("Paragraph inside border cannot be longer than 14 lines")
  horizontal_border = "##################################\n"
  output = ""
  output += horizontal_border
  for line in para_lines:
    if len(line) > 32:
      raise Exception("Line inside border cannot be longer than 32 chars")
    output += f"#{line.ljust(32)}#\n"
  for _ in range(14 - len(para_lines)):
    output += f"{"#".ljust(33)}#\n"
  output += horizontal_border
  return output

para = """test123
GCV Centennial
!!!
"""

with sync_playwright() as p:
  browser = p.chromium.launch(slow_mo=100, headless=True)
  context = browser.new_context(
    http_credentials={"username": USER, "password": PW},
    viewport={"height": 1080, "width": 1920}
  )
  page = context.new_page()
  page.goto(f"http://{IP_ADDR}")

  ap = AutoPilot(page)

  ap.bar_char_initialize()

  ap.bar_char_type_paragraph(create_border_block(para))
  





