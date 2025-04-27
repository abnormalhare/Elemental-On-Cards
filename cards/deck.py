import discord

from std.bot import bot
from std.info import card_stats, cards, packs, print_cmd


@bot.command()
async def deck(ctx):
  message = ctx.message
  split = message.content.split(" ", 1)
  embed: discord.Embed | None= None

  if len(split) < 2 or split[1].title() not in cards:
    embed = discord.Embed(title="Decks", color=0x00ff00)
    for deck in cards:
      embed.add_field(name=f"{deck} (Level {packs[deck]})",
                      value=", ".join(cards[deck]),
                      inline=False)
  elif split[1].title() in cards:
    deck = split[1].title()
    embed = discord.Embed(
        title=f"{split[1].title()} Deck (Level {packs[deck]})", color=0x00ff00)
    for card in cards[deck]:
      card_type = card_stats[card]["Type"]
      if card_type == "Land":
        embed.add_field(name=f"{card} ({card_type})",
                        value=f"Mana Gain: {card_stats[card]['Mana']}",
                        inline=False)
      elif card_type == "Attacker":
        embed.add_field(
            name=f"{card} ({card_type})",
            value=
            f"Mana Cost: {card_stats[card]['Mana']}, Attack: {card_stats[card]['Attack']}, Defense: {card_stats[card]['Defense']}",
            inline=False)
      elif card_type == "Spell" or card_type == "Instant":
        embed.add_field(
            name=f"{card} ({card_type})",
            value=
            f"Mana Cost: {card_stats[card]['Mana']}, Attack: {card_stats[card]['Attack']}",
            inline=False)

  await ctx.send(embed=embed)
