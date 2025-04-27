import random

from std.bot import bot
from std.info import MAX_CARDS, cards, collection, init_player, packs, players, save, print_cmd


@bot.command(aliases=["nd"])
async def newdeck(ctx):
  init_player(ctx.author.id, ctx.author.name)

  random_cards = False
  message = ctx.message
  author = ctx.author
  player = str(author.id)
  split = message.content.split(" ", 1)

  if len(split) < 2:
    await ctx.send("Please specify a deck.")
    return

  deck = split[1].title()

  if "Random" in deck[:7]:
    random_cards = True
    split = split[1].split(" ", 1)
    deck = split[1].title()

  if deck not in packs:
    await ctx.send(f"Deck **{deck}** does not exist")
    return

  if packs[deck] > players[player]["level"]:
    await ctx.send(
        f"Deck **{deck}** is not available to you. You are level {players[player]['level']}"
    )
    return

  players[player]["deck"] = deck

  players[player]["inventory"] = []
  if random_cards:
    for _ in range(MAX_CARDS):
      players[player]["inventory"].append(random.choice(cards[deck]))
  else:
    for card in collection[deck]:
      players[player]["inventory"] += [card] * collection[deck][card]
  save()
  await ctx.send(f"Deck **{deck}** set.")
  await print_cmd(player, "newdeck")
