import discord
from lunch_menu_bot.integrations.constants import EMBED_GIFS


embed_confused = discord.Embed()
embed_confused.set_image(url=EMBED_GIFS["confused"])

embed_fail = discord.Embed()
embed_fail.set_image(url=EMBED_GIFS["fail"])

embed_chicken1 = discord.Embed()
embed_chicken1.set_image(url=EMBED_GIFS["chicken"][0])

embed_chicken2 = discord.Embed()
embed_chicken2.set_image(url=EMBED_GIFS["chicken"][1])

embed_chicken3 = discord.Embed()
embed_chicken3.set_image(url=EMBED_GIFS["chicken"][2])
