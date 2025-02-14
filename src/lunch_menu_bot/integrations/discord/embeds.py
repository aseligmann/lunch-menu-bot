import random
import discord
from lunch_menu_bot.integrations.constants import EMBED_GIFS


class EmbedFactory:
    @staticmethod
    def create_embed_from_type(embed_type: str) -> discord.Embed:
        embed = discord.Embed()
        urls = {
            "confused": random.choice(EMBED_GIFS["confused"]),
            "fail": random.choice(EMBED_GIFS["fail"]),
            "chicken": random.choice(EMBED_GIFS["chicken"]),
        }
        if url := urls.get(embed_type):
            embed.set_image(url=url)
        return embed

    @staticmethod
    def create_embed_from_url(url: str) -> discord.Embed:
        embed = discord.Embed()
        embed.set_image(url=url)
        return embed
