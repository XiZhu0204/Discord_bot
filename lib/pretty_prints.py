def code_block_str(input_str):
  return f"```\n{input_str}\n```"


def code_block_list(input_list, header = "", footer = ""):
  text = "```\n"

  if header:
    text += f"{header}\n"

  for entry in input_list:
    text += f"{entry}\n"

  if footer:
    text += f"{footer}"

  text += "\n```"

  return text


def block_quote_str(input_str):
  return f">>>{input_str}"


def block_quote_list(input_list, header = "", footer = ""):
  text = ">>>"

  if header:
    text += f"{header}\n"

  for entry in input_list:
    text += f"{entry}\n"

  if footer:
    text += f"{footer}"

  return text