# I changed a lot of how the library works and added better helper functions 
# but this is a useful example

from old_ccu_autopilot import AutoPilot
import pandas as pd

try:
  addresses = pd.read_csv('multicast_template.csv')['multicast_addresses'].tolist()

  ap = AutoPilot(ip_addr="10.72.6.21", username="admin", password="hdcu5500", headless=True, slow_mo=40)

  ap.start()

  ap.return_to_main_menu()

  ap.verticle_scroll_to("NETWORK")

  ap.find_page_by_text("N00TOP")

  ap.verticle_scroll_to("08 <MULTICAST ADDRESS 1-1>")

  ap.enter()

  while(not "<MULTICAST ADDRESS 1-1>" in ap.get_osd_cursorline_text()):
    ap.up()

  ap.down()
  ap.down()

  def set_four_numbers(num_list):
    if len(num_list) != 4:
      raise Exception(f"not four numbers")
    
    for num in num_list:
      ap.change_octet(num)
      ap.down()
  
  def set_ip_address(address):
    split = address.split('.')
    split_nums = [int(n) for n in split]
    set_four_numbers(split_nums)

  for item in addresses:
    set_ip_address(item)
    ap.down()

  ap.stop()

except Exception as e:
  print(e)
  ap.stop()