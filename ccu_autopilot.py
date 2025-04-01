from playwright.sync_api import Page

chars = [
    " ", "!", "#", "$", "%", "&", "'", "(", ")", "+", ",", "-", ".", 
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ";", "=", 
    "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", 
    "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", 
    "X", "Y", "Z", "[", "]", "^", "_", "`", "a", "b", "c", "d", 
    "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", 
    "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]

class AutoPilot:
  def __init__(self, page):
    self.page: Page = page

  def __repr__(self):
    return(f"AutoPilot Object for {self.ip_addr}")
  
  def open_osd(self):
    "From the home page, opens the OSD pop-up."
    button = self.page.get_by_text("OSD Menu")
    button.click()

  def not_initialized(self):
    if not isinstance(self.page, Page):
      raise Exception("playwright was probably not initialized correctly")
    
  def return_to_main_menu(self):

    if self.not_initialized(): return
    for _ in range(10):
      self.cancel()

  def get_osd_current_text(self):
    """
    Returns the entire OSD text with whitespace removed. Recommend using with something like:
      if not "VIDEO" in get_osd_current_text():
        ap.up()

    Can be useful to print this value to see whats going awry.
    """
    if self.not_initialized(): return
    # self.page.wait_for_load_state('networkidle') 
    # TODO: find a way to detect when js has fully rerendered the DOM 
    #   after the websocket update is recieved.
    #   wait_for_load_state only works for server-rendered content
    #   could be possible to reference the item you know will be changing 
    #   and wait for its css selector with wait_for_selector()
    osd_table = self.page.locator(".proui-ext-message-box-message")
    return osd_table.inner_text().strip().replace("\n", "").replace("\t", "").replace(" ", "")
  
  def get_osd_cursorline_text(self):
    """
    Returns the horizontal cursor inner text. This is mostly used in menus
    where you are scrolling vertically to select sub-menus, but works on most menus.

    Can be useful to print this value to see whats going awry.
    """
    if self.not_initialized(): return
    # self.page.wait_for_load_state('networkidle')
    # TODO
    cursorline = self.page.locator(".cursorLine")
    return cursorline.inner_text().replace("\n", "").replace("\t", "")
        
  def get_osd_selected_character(self):
    """
    This is specifically for using the OSD keyboard to set bar characters.
    """
    if self.not_initialized(): return
    return "".join(self.page.locator(".charRev").all_inner_texts())

  def get_osd_bar_char_line_number(self):
    """
    This is specifically for using the OSD keyboard to set bar characters.
    """
    if self.not_initialized(): return
    cursorline = self.page.locator(".cursorLine")
    return cursorline.locator("span").first.inner_text()
  
  def verticle_scroll_to(self, text):
    """
    Extension of get_osd_cursorline_text.
    Can be used to hunt through a menu for a selector string. 
    Note that when there are multiple selectable items on a single horizontal line,
    this method cannot guarantee repeatable behavior.
    In those scenarios, recommend searching for a stable reference point on the
    page and counting up or down from there.
    """
    if self.not_initialized(): return
    ttl = 100
    while not text in self.get_osd_cursorline_text() and ttl > 0:
      self.down()
      ttl -= 1
    if ttl == 0:
      raise Exception(f"Could not find {text}")
    else:
      self.enter()
      return True
    
  def find_page_by_text(self, text):
    """
    Extension of get_osd_current_text.
    Can be used to hunt through a set of pages for a selector string. 
    """
    if self.not_initialized(): return
    ttl = 30
    while not text in self.get_osd_current_text() and ttl > 0:
      self.down()
      ttl -= 1
    if ttl == 0:
      raise Exception(f"Could not find {text}")
    else:
      self.enter()
      return True
    
  def up(self, n: int = 1):
    if self.not_initialized(): return
    for _ in range(n):
        self.page.locator(".up-button").click()

  def down(self, n: int = 1):
    if self.not_initialized(): return
    for _ in range(n):
        self.page.locator(".down-button").click()

  def cancel(self, n: int = 1):
    if self.not_initialized(): return
    for _ in range(n):
        self.page.locator(".cancel-button").click()

  def enter(self, n: int = 1):
    if self.not_initialized(): return
    for _ in range(n):
        self.page.locator(".enter-button").click()

  def get_selected_number(self):
    """
    For reading the current value of 3 digit IP address octets.
    """
    if self.not_initialized(): return
    self.page.wait_for_timeout(30)
    el = self.page.locator('text=?')
    parent = el.locator("../..")
    digits = []
    sibling = parent.evaluate_handle('el => el.nextElementSibling')
    for _ in range(3):
      digits.append(sibling.inner_text())
      sibling = sibling.evaluate_handle('el => el.nextElementSibling')
    return int("".join(digits))
  
  def change_octet(self, n: int):
    """
    Accepts an integer 0-255 and sets the digit. 
    It will press enter to begin editing, scroll to n, than press enter to set.
    """
    if 0 > n > 255:
      raise Exception("wrongo numbero")
    self.enter()
    x = self.get_selected_number()
    up_distance = (n - x) % 256
    down_distance = (x - n) % 256
    if up_distance <= down_distance:
        for _ in range(up_distance):
            self.down()
    else:
        for _ in range(down_distance):
            self.up()
    self.enter()

  def bar_char_type_letter(self, letter):
    """
    For bar characters.
    Begins from line edit mode (keyboard visible, while up/down navigates from character to character)
    """
    if not letter in chars:
      print(f'invalid character: {letter}')
      return 
    index = chars.index(letter)
    self.enter()
    if index < 42:
      for _ in range(index):
        self.down()
    else:
      for _ in range(86 - index):
        self.up()
    self.enter()

  def bar_char_type_line(self, line):
    """
    For bar characters.
    Begins from line selection mode (no keyboard visible, up/down navigates from line to line)
    """
    self.enter()
    for char in list(line):
      self.type_letter(char)
    for _ in range(36):
      self.down()
    self.enter()



