# CCU AutoPilot – Playwright Automation for Sony HDCU5500 Web UI OSD

Helper functions for navigating the Sony HDCU5500 OSD menu with playwright for python.

### Important note!
I haven't found a reliable way to register when js updates the DOM from incoming websocket data. I have found ways to listen to incoming websocket data, so I have some ideas.

For now, you can just use slow_mo = 50, if not 70 or 100. It's kinda slow, but reliable.

It takes ~3 minutes to set the bar characters with slow_mo = 100. You can do them all in parallel.

## Quickstart
Clone this repository
```
git clone https://git.nmahoney.dev/nathan-public/ccu-autopilot.git
```
Create a venv and install dependencies
```
python -m venv venv
source venv/bin/activate # bash
venv/scripts/activate.ps1 # powershell

pip install -r requirements.txt
playwright install
```
Make a new folder with your name for your custom scripts so you can make a pull request to share them. 
Import and initialize some constants.
You have to modify the sys path to import from the parent directory.
```python
from playwright.sync_api import sync_playwright
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_dir)
from ccu_autopilot import AutoPilot

IP_ADDR = "192.168.420.69"
USER = "admin"
PW = "password"
```
Initialize the playwright session with a context manager. **Note that at least slow_mo=50 will probably be required.**
Set headless = False if you want to see the browser page.
```python
with sync_playwright() as p:
  browser = p.chromium.launch(slow_mo=50, headless=False)
  context = browser.new_context(
    http_credentials={"username": USER, "password": PW},
    viewport={"height": 1080, "width": 1920}
  )
  page = context.new_page()
  page.goto(f"http://{IP_ADDR}")
```
Pass the page to an instance of AutoPilot at the top of your script. Use ap methods when useful, or use playwright normally.
```python
  ap = AutoPilot(page)

  ap.open_osd()
  item = page.get_by_text("thing")
  print(item.inner_text())
```

## Multithreading
Will eventually replace this with real examples.
```python
from threading import Thread

def write_bar_chars(thing):
  # with sync_playwright() as p:
  #   ap = AutoPilot(page)
  #   ap.do_things()
  pass

for thing in bar_chars:
  Thread(target=write_bar_chars, args=(thing))
  .start()
  .join()
```

## Methods
### `open_osd()`
From the home page, opens the OSD pop-up.

---

### `return_to_main_menu()`
Navigates back to the main menu by pressing the cancel button repeatedly.

---

### `get_osd_current_text()`
Returns the entire OSD text with whitespace removed.  
Recommended usage:

```python
if "ITEM" not in get_osd_current_text():
  ap.up()
```

Useful for debugging OSD state.

---

### `get_osd_cursorline_text()`
Returns the current cursor line's text, typically used when scrolling vertically in menus.

---

### `get_osd_selected_character()`
Used with the OSD keyboard to retrieve the currently selected character.

---

### `get_osd_bar_char_line_number()`
Returns the current line number when setting bar characters.

---

### `verticle_scroll_to(text: str)`
Scrolls vertically through a menu to find a specific text string and selects it.

**Note:** May behave unpredictably when multiple items are on one horizontal line.

---

### `find_page_by_text(text: str)`
Scrolls through multiple pages looking for a specific string in the full OSD text.

---

### `up(n: int = 1)`
Clicks the up button `n` times.

---

### `down(n: int = 1)`
Clicks the down button `n` times.

---

### `cancel(n: int = 1)`
Clicks the cancel button `n` times.

---

### `enter(n: int = 1)`
Clicks the enter button `n` times.

---

### `get_selected_number()`
Reads the current value from a 3-digit numeric selector (e.g., for IP address octets).

---

### `change_octet(n: int)`
Sets the value of a 3-digit numeric selector to an integer between 0–255.

- Begins with pressing enter.
- Scrolls up/down to the correct number.
- Presses enter to confirm.

---

### `bar_char_type_letter(letter: str)`
Sets a single character on a bar character line.

- Starts in **line edit mode** (keyboard visible).
- Selects the character using up/down navigation.
- Invalid characters are ignored with a warning.

---

### `bar_char_type_line(line: str)`
Types a full line of characters for bar text configuration.

- Starts in **line selection mode** (keyboard not visible).
- Switches to character mode and types each character.
- Scrolls down to the confirmation button and confirms.

