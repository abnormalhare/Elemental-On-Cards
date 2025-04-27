from std.bot import bot
from std.info import check_duel, init_player, players, swap_turns


@bot.command()
async def endturn(ctx):
  init_player(ctx.author.id, ctx.author.name)
  if not check_duel(ctx, str(ctx.author.id)):
    await ctx.send("You aren't in a duel!")
    return

  if ctx.message.guild is not None:
    await ctx.send(
        "Please use DMs to play to ensure no one peeks while you play!")
    return

  author = ctx.author
  player = str(author.id)
  opponent = players[player]["opponents"][0]

  if not players[player]["is_turn"]:
    await ctx.send(
        "It is not your turn! Please wait for your opponent to end their turn."
    )
    return

  if len(players[player]["hand"]) > 8:
    await ctx.send("You must discard down to 8 cards in your hand!")
    return

  await swap_turns(ctx, player, opponent)