from discord import Embed, Colour

EMPTY = "\u200b"

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


def embed_str(in_str, header = "", footer = ""):
  embed = Embed(colour = Colour.blue())

  if header:
    embed.add_field(name = header, value = in_str, inline = False)
  else:
    embed.add_field(name = EMPTY, value = in_str, inline = False)

  if footer:
    embed.set_footer(text = footer)

  return embed


def embed_list(in_list, header = "", footer = ""):
  embed = Embed(colour = Colour.blue())

  text = ""
  for entry in in_list:
    text += f"{entry}\n"

  if header:
    embed.add_field(name = header, value = text, inline = False)
  else:
    embed.add_field(name = EMPTY, value = text, inline = False)

  if footer:
    embed.set_footer(text = footer)

  return embed