import discord

from std.bot import bot
from std.info import (
    get_searching_players,
    init_player,
)


@bot.command()
async def duels(ctx):
    init_player(ctx.author.id, ctx.author.name)

    # get list of searching players
    opponents = get_searching_players()

    embed = discord.Embed(title="Duels", color=0x00ff00)
    embed.add_field(name="Searching Players", value=", ".join(opponents), inline=False)

    await ctx.send(embed=embed)