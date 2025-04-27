import discord

from std.bot import bot
from std.info import init_player, players


@bot.command()
async def stats(ctx):
  init_player(ctx.author.id, ctx.author.name)

  author = ctx.author
  player = str(author.id)

  embed = discord.Embed(title="Stats", color=0x00ff00)
  embed.add_field(
      name="Win/Losses/Ties",
      value=
      f"{players[player]['won']}/{players[player]['lost']}/{players[player]['tied']}",
      inline=False)
  embed.add_field(name="Level", value=players[player]["level"], inline=False)

  await ctx.send(embed=embed)
