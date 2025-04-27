import discord

from std.bot import bot
from std.info import card_stats, packs


@bot.command(aliases=["i"])
async def info(ctx):
  msg = ctx.message
  split = msg.content.split(" ", 1)

  if len(split) < 2:
    await ctx.send("Please specify a card.")
    return

  card_name: str = split[1].title()

  if card_name not in card_stats:
    await ctx.send(f"Card **{card_name}** does not exist")
    return

  embed_title = "Info: " + card_name
  embed = discord.Embed(title=embed_title, color=0x00ff00)

  card_type = card_stats[card_name]["Type"]
  level = packs[card_stats[card_name]["Pack"]]
  embed.add_field(name="Type",
                  value=f"{card_type} (Level {level})",
                  inline=False)
  if card_type == "Land":
    embed.add_field(name=f"{card_name} ({card_type})",
                    value=f"Mana Gain: {card_stats[card_name]['Mana']}",
                    inline=False)
  elif card_type == "Attacker":
    embed.add_field(
        name=f"{card_name} ({card_type})",
        value=
        f"Mana Cost: {card_stats[card_name]['Mana']}, Attack: {card_stats[card_name]['Attack']}, Defense: {card_stats[card_name]['Defense']}",
        inline=False)
  elif card_type == "Spell" or card_type == "Instant":
    embed.add_field(
        name=f"{card_name} ({card_type})",
        value=
        f"Mana Cost: {card_stats[card_name]['Mana']}, Attack: {card_stats[card_name]['Attack']}",
        inline=False)

  embed.add_field(name="Description",
                  value=card_stats[card_name]["Description"],
                  inline=False)

  await ctx.send(embed=embed)