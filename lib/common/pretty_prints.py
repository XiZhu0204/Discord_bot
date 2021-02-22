<<<<<<< HEAD
import discord



=======
from discord import Embed, Colour

<<<<<<< HEAD
=======
EMPTY = "\u200b"
>>>>>>> origin/master
>>>>>>> origin/master

def embed_str(in_str, header = "", footer = ""):
  text = ""

  if header:
    text += f"{header}\n"

  text += f"{in_str}\n"

  if footer:
    text += footer
  

  return create_embed(text)


def embed_list(in_list, header = "", footer = ""):
  text = ""
  
  if header:
    text += f"{header}\n"

  for entry in in_list:
    text += f"{entry}\n"

  if footer:
    text += footer

  return create_embed(text)


def create_embed(in_str):
  return Embed(title = in_str, description = Embed.Empty, colour = Colour.blue())