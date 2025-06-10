import pandas as pd
from bar_chars_single import write_ccu_bar_char
from threading import Thread
from playwright.sync_api import sync_playwright
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_dir)
from ccu_autopilot import AutoPilot
df = pd.read_csv('all_ccu.csv', header=None)
df = df.fillna(" ")

ccu_list = df.values.tolist()

ccu_dict_arr = []

def build_para(list_of_rows):
  output = ""
  for line in list_of_rows:
    output += f"{line}\n"
  return output

for ccu in ccu_list:
  ccu_dict_arr.append({
    "ip_addr": ccu[0],
     "para": build_para(ccu[1:])
  })

def test_target(para, ip_addr):
  with sync_playwright() as p:
    browser = p.chromium.launch(slow_mo=100)
    context = browser.new_context(
      http_credentials={"username": 'admin', "password": 'hdcu5500'},
      viewport={"height": 1080, "width": 1920}
    )
    page = context.new_page()
    page.goto(f"http://{ip_addr}")

    ap = AutoPilot(page)
    ap.open_osd()
    ap.return_to_main_menu()
    ap.bar_char_initialize()
    ap.bar_char_type_paragraph(para)

threads = []

for thing in ccu_dict_arr:
  threads.append(Thread(target=test_target, args=(thing["para"], thing["ip_addr"])))

for thread in threads:
  thread.start()

for thread in threads:
  thread.join() 