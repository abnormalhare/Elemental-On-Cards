from std.bot import bot
from std.info import check_duel, init_player, players, print_cmd, save


@bot.command()
async def discard(ctx):
  init_player(ctx.author.id, ctx.author.name)
  if not check_duel(ctx, str(ctx.author.id)):
    await ctx.send("You aren't in a duel!")
    return

  if ctx.message.guild is not None:
    await ctx.send(
        "Please use DMs to play to ensure no one peeks while you play!")
    return

  message = ctx.message
  author = ctx.author
  player = str(author.id)

  if not players[player]["is_turn"]:
    await ctx.send(
        "It is not your turn! Please wait for your opponent to end their turn."
    )
    return

  if len(players[player]["hand"]) <= 8:
    await ctx.send(
        "You cant't discard any cards! You must have more than 8 cards in your hand to do that."
    )
    return

  split = message.content.split(" ", 1)
  if len(split) < 2:
    await ctx.send("Please specify a card.")

  card = split[1].title()
  if card not in players[player]["hand"]:
    await ctx.send(f"You don't have a **{card}** in your hand!")
    return

  players[player]["hand"].remove(card)
  save()
  await print_cmd(player, message.content)