from threading import Thread
import time
from playwright.sync_api import sync_playwright
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_dir)
from ccu_autopilot import AutoPilot

ccu_camera_pairs = [
  {"ccu_addr": "172.26.1.133", "camera_addr": 33},
]

_ccu_camera_pairs = [
    {"ccu_addr": "172.26.1.111", "camera_addr": 11},
    {"ccu_addr": "172.26.1.112", "camera_addr": 12},
    {"ccu_addr": "172.26.1.113", "camera_addr": 13},
    {"ccu_addr": "172.26.1.114", "camera_addr": 14},
    {"ccu_addr": "172.26.1.115", "camera_addr": 15},
    {"ccu_addr": "172.26.1.116", "camera_addr": 16},
    {"ccu_addr": "172.26.1.117", "camera_addr": 17},
    {"ccu_addr": "172.26.1.118", "camera_addr": 18},
    {"ccu_addr": "172.26.1.119", "camera_addr": 19},
    {"ccu_addr": "172.26.1.124", "camera_addr": 24},
    {"ccu_addr": "172.26.1.125", "camera_addr": 25},
    {"ccu_addr": "172.26.1.126", "camera_addr": 26},
    {"ccu_addr": "172.26.1.127", "camera_addr": 27},
    {"ccu_addr": "172.26.1.134", "camera_addr": 34},
    {"ccu_addr": "172.26.1.136", "camera_addr": 36},
    {"ccu_addr": "172.26.1.137", "camera_addr": 37},
    {"ccu_addr": "172.26.1.138", "camera_addr": 38},
    {"ccu_addr": "172.26.1.139", "camera_addr": 39},
    {"ccu_addr": "172.26.1.141", "camera_addr": 41},
]

def set_stuff(ccu_addr, cam_addr):
    def set_four_numbers(num_list):
        if len(num_list) != 4:
            raise Exception(f"not four numbers")
        
        for num in num_list:
            ap.change_octet(num)
            ap.down()
        
    with sync_playwright() as p:
        browser = p.chromium.launch(slow_mo=100, headless=False)
        context = browser.new_context(
        http_credentials={"username": 'admin', "password": 'hdcu5500'},
        viewport={"height": 720, "width": 1280}
        )
        page = context.new_page()
        page.goto(f"http://{ccu_addr}")

        ap = AutoPilot(page)
        ap.open_osd()
        ap.return_to_main_menu()
        ap.verticle_scroll_to('NETWORK')
        ap.find_page_by_text('N02')
        ap.verticle_scroll_to('CNS MODE')
        if not "GMCS" in ap.get_osd_current_text():
          ap.down()
        ap.enter()
        
        # confirm GMCS ok
        ap.down()
        ap.enter()
        
        ap.verticle_scroll_to('REDUNDANT')
        if not "ENABLE" in ap.get_osd_current_text():
          ap.down()
        ap.enter()
        
        ap.down()
        
        set_four_numbers([172,26,1,100])
                
        set_four_numbers([172,26,1,102])
        
        ap.down(5)
                
        ap.enter()
        ap.down()
        ap.enter()

        
        ap.cancel()
        ap.find_page_by_text('N01')
        ap.verticle_scroll_to('PORT')
        if not "CAMERA" in ap.get_osd_current_text():
          ap.down()
        ap.enter()
        ap.down(2)
        
        set_four_numbers([172, 26, 1, cam_addr])
        
        ap.enter()
        ap.down()
        ap.enter()
    
# for pair in ccu_camera_pairs:
#   set_stuff(ccu_addr=pair["ccu_addr"], cam_addr=pair["camera_addr"])

threads = []

for pair in ccu_camera_pairs:
  threads.append(Thread(target=set_stuff, args=(pair["ccu_addr"], pair["camera_addr"])))

for thread in threads:
  thread.start()

for thread in threads:
  thread.join() 