from std.bot import bot
from std.info import check_duel, get_dm, init_player, players


@bot.command()
async def say(ctx):
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
  opponent = players[player]["opponents"][0]

  o_dm = await get_dm(opponent)
  await ctx.send(f"Sent to <@{opponent}>")
  await o_dm.send(f"<@{player}> says: {message.content[5:]}")
  await print_cmd(player, message.content)