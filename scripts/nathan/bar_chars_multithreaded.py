import pandas as pd
from bar_chars_single import write_ccu_bar_char
from threading import Thread

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
  print(f"ip_addr: {ip_addr}")
  print(f"Para:")
  print(para)

threads = []

for thing in ccu_dict_arr:
  threads.append(Thread(target=write_ccu_bar_char, args=(thing["para"], thing["ip_addr"])))

for thread in threads:
  thread.start()

for thread in threads:
  thread.join() 