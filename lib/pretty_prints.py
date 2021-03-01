from discord import Embed, Colour


def gen_text_str(in_str, header = "", footer = ""):
  text = ""

  if header:
    text += f"{header}\n"

  text += f"{in_str}\n"

  if footer:
    text += footer

  return text


def gen_text_list(in_list, header = "", footer = ""):
  text = ""
  
  if header:
    text += f"{header}\n"

  for entry in in_list:
    text += f"{entry}\n"

  if footer:
    text += footer

  return text


def code_block_str(in_str, header = "", footer = ""):
  return f"```\n{gen_text_str(in_str, header, footer)}\n```"


def code_block_list(in_list, header = "", footer = ""):
  return f"```\n{gen_text_list(in_list, header, footer)}\n```"


def block_quote_str(in_str, header = "", footer = ""):
  return f">>> {gen_text_str(in_str, header, footer)}"


def block_quote_list(in_list, header = "", footer = ""):
  return f">>> {gen_text_list(in_list, header, footer)}"


def embed_str(in_str, header = "", footer = ""):
  return create_embed(gen_text_str(in_str, header, footer))


def embed_list(in_list, header = "", footer = ""):
  return create_embed(gen_text_list(in_list, header, footer))


def create_embed(in_str):
  return Embed(title = in_str, description = Embed.Empty, colour = Colour.blue())