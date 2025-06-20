from threading import Thread
from playwright.sync_api import sync_playwright
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_dir)
from ccu_autopilot import AutoPilot

ip_addresses = [
    '172.26.1.121',
    '172.26.1.124',
    '172.26.1.125',
    '172.26.1.126',
    '172.26.1.127',
    '172.26.1.134',
    '172.26.1.136',
    '172.26.1.137',
    '172.26.1.138'
]
def thread_target(ip_addr):
    with sync_playwright() as p:
        browser = p.chromium.launch(slow_mo=100, headless=False)
        context = browser.new_context(
        http_credentials={"username": 'admin', "password": 'hdcu5500'},
        viewport={"height": 1080, "width": 1920}
        )
        page = context.new_page()
        page.goto(f"http://{ip_addr}")

        ap = AutoPilot(page)
        ap.open_osd()
        ap.return_to_main_menu()
        ap.verticle_scroll_to('MAINTENANCE')
        ap.find_page_by_text('M10')
        ap.verticle_scroll_to('GMCS')
        ap.down()
        ap.enter()
    
threads = []

for address in ip_addresses:
  threads.append(Thread(target=thread_target(address)))

for thread in threads:
  thread.start()

for thread in threads:
  thread.join() 

