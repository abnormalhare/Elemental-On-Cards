import random

from std.bot import bot
from std.info import MAX_CARDS, cards, collection, custom_decks, init_player, packs, players, save, print_cmd


async def newdeck_create(ctx, message):
  author = ctx.author
  player = str(author.id)
  split = message.content.split(" ", 3)

  if len(split) < 4:
    await ctx.send("The format of the command is `&newdeck create <deck name> <card1> <amount1> <card2> <amount2> ...\nDecks must also be 40 cards!`")
    return
  
  name = split[2].title()
  if name in packs:
    await ctx.send(f"Deck **{name}** already exists")
    return
  
  split = split[3].split(" ")
  deck = {}
  card = ""
  count = 0
  for i in split:
    if i.isdigit():
      amount = int(i)
      if amount < 1 or amount > 40:
        await ctx.send(f"Amount must be between 1 and 40")
        return
      deck[card] = amount
      count += amount
      card = ""

      if count > 40:
        await ctx.send(f"Deck must be 40 cards! ({count} cards)")
        return
    else:
      card += i.title()
      if card not in cards:
        await ctx.send(f"Card **{card}** does not exist")
        return
      if card in deck:
        await ctx.send(f"Card **{card}** already exists")
        return
  
  if count < 40:
    await ctx.send(f"Deck must be 40 cards! ({count} cards)")
    return
  
  for card in deck:
    players[player]["inventory"] += [card] * deck[card]
  
  players[player]["deck"] = name
  custom_decks[name] = deck
  packs[name] = players[player]["level"]

  await ctx.send(f"Deck **{name}** created!")
  await print_cmd(player, message.content)
  save()


@bot.command(aliases=["nd"])
async def newdeck(ctx):
  init_player(ctx.author.id, ctx.author.name)

  random_cards = False
  message = ctx.message
  author = ctx.author
  player = str(author.id)
  split = message.content.split(" ", 1)

  if players[player]["in_duel"]:
    await ctx.send("You are in a duel! Please end the duel before changing decks.")
    return

  if len(split) < 2:
    await ctx.send("Please specify a deck.")
    return

  deck = split[1].title()

  if "Random" in deck[:7]:
    random_cards = True
    split = split[1].split(" ", 1)
    deck = split[1].title()

  if "Create" in deck[:7]:
    await newdeck_create(ctx, message)
    return

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
  await print_cmd(player, message.content)
