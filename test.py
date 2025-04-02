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
  


para = """Line 1 

Line 3
Line 4
"""

borders = create_border_block(para)

print(borders)