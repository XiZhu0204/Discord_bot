import discord




def code_block_str(input_str, header = "", footer = ""):
  text = "```\n"

  if header:
    text += f"{header}\n"

  text += f"{input_str}\n"

  if footer:
    text += footer

  text += "\n```"

  return text


def code_block_list(input_list, header = "", footer = ""):
  text = "```\n"

  if header:
    text += f"{header}\n"

  for entry in input_list:
    text += f"{entry}\n"

  if footer:
    text += footer

  text += "\n```"

  return text


def block_quote_str(input_str, header = "", footer = ""):
  text = ">>> "

  if header:
    text += f"{header}\n"

  text += f"{input_str}\n"

  if footer:
    text += footer

  return text


def block_quote_list(input_list, header = "", footer = ""):
  text = ">>> "

  if header:
    text += f"{header}\n"

  for entry in input_list:
    text += f"{entry}\n"

  if footer:
    text += footer

  return text