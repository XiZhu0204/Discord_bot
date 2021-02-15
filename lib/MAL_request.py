import asyncio
from jikanpy import AioJikan

import lib.common.pretty_prints as pprint
from lib.common.time_functions import get_weekday

async def ani_today_cmd(ctx):
  weekday = get_weekday().lower()
  async with AioJikan() as requester:
    ani_tdy = await requester.schedule(weekday)
  animes = []
  for entry in ani_tdy[weekday]:
    title = entry["title"]
    url = entry["url"]
    info = f"{title}\n{url}\n"
    animes.append(info)
  
  header = "The animes that come out today are:"
  response = pprint.code_block_list(animes, header = header)
  await ctx.send(response)