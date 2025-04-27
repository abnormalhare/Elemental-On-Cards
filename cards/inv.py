import discord

from std.bot import bot
from std.info import cards, init_player, packs, players, print_cmd


@bot.command(aliases=["inventory"])
async def inv(ctx):
  init_player(ctx.author.id, ctx.author.name)
  author = ctx.author
  player = str(author.id)

  if ctx.message.guild is None:
    embed = discord.Embed(title="Cards Left", color=0x00ff00)
  else:
    embed = discord.Embed(title=f"{author.name}'s Inventory", color=0x00ff00)
  if players[player]["deck"] == "":
    embed.add_field(name="Deck", value="*None*", inline=False)
  else:
    embed.add_field(
        name="Deck",
        value=
        f"{players[player]['deck']} (Level {packs[players[player]['deck']]})",
        inline=False)

  if players[player]["deck"] != "":
    inv_str = ""
    for card in cards[players[player]['deck']]:
      if ctx.message.guild is None:
        count = players[player]["curr_inv"].count(card)
      else:
        count = players[player]["inventory"].count(card)
      inv_str += f"{card}: x{count}\n"
  
    embed.add_field(name="Inventory", value=inv_str, inline=False)

  await ctx.send(embed=embed)
  await print_cmd(player, "inv")