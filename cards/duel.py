import random

from std import info
from std.bot import bot
from std.info import (
    begin_duel,
    get_dm,
    get_searching_players,
    init_player,
    players,
    print_cmd,
    save,
)


async def duel_random(ctx, player: str, opponents):
  # check for opponents
  if len(opponents) == 0:
    await ctx.send("You are waiting for a duel.")
    players[player]["awaiting_duel"] = True
    return

  opponent = random.choice(opponents)
  await begin_duel(ctx, player, opponent)


async def duel_accept(ctx, player: str, opponents):
  # check for opponents
  if len(opponents) == 0:
    await ctx.send("There's no one to accept a duel from!")
    return

  # find opponent
  for opponent in opponents:
    if player in players[opponent]["opponents"]:
      await begin_duel(ctx, opponent, player)
      return

  #if there is none...
  await ctx.send("There's no one to accept a duel from!")


async def duel_decline(ctx, player: str, opponents):
  declined_players = players[player]["opponents"]

  # check for opponents
  if len(opponents) == 0:
    await ctx.send("There's no one to decline a duel from!")
    return

  # remove player from opponents
  for opponent in opponents:
    if player in players[opponent]["opponents"]:
      players[opponent]["opponents"] = list(
          filter(lambda a: a != player, players[opponent]["opponents"]))

  # check for declined players
  if len(declined_players) == 0:
    await ctx.send("There's no one to decline a duel from!")
    return

  declined_players = [f"<@{player}>" for player in declined_players]
  await ctx.send(f"Declined duel from {', '.join(declined_players)}")


async def duel_player(ctx, player: str, opponents, name: str):
  opponent = name
  nonsearching_opponents = []

  if "<@" in opponent:
    await ctx.send("Please use the player's name, don't ping them!")
    return

  # find opponent
  for op_id in players:
    if players[op_id]["name"] == opponent:
      opponent = op_id
      break
  else:
    await ctx.send(f"Player **{opponent}** does not exist!")
    return

  # add opponent to player's opponents
  players[player]["opponents"].append(opponent)
  if opponent not in opponents:
    nonsearching_opponents.append(opponent)
  players[opponent]["opponents"].append(player)

  # check for nonsearching opponents
  if len(nonsearching_opponents) == 0:
    await begin_duel(ctx, opponent, player)
    return
  else:
    opponent = await get_dm(nonsearching_opponents[0])
    nonsearching_opponents = [
        f"<@{player}>" for player in nonsearching_opponents
    ]
    await ctx.send(f"Duel requested from {', '.join(nonsearching_opponents)}")

    # check if in DM
    if ctx.message.guild is None:
      # send DM to opponent
      await opponent.send(
          f"<@{player}> has requested a duel with you! Use &duel accept to accept or &duel decline to decline."
      )
    players[player]["awaiting_duel"] = True


@bot.command()
async def duel(ctx):
  init_player(ctx.author.id, ctx.author.name)
  author = ctx.author
  player = str(author.id)

  split = ctx.message.content.split(" ")
  opponents = get_searching_players()

  # check for inventory
  if players[player]["inventory"] == []:
    await ctx.send("Please select a deck before entering battle.")
    return

  # check if in duel
  if players[player]["in_duel"]:
    if len(split) > 1 and split[1] == "abort":
      opponent = players[player]["opponents"][0]
      players[player]["in_duel"] = False
      players[player]["opponents"] = []
      players[opponent]["in_duel"] = False
      players[opponent]["opponents"] = []
      await ctx.send(f"Duel with <@{opponent}> has been aborted.")
      save()
    else:
      await ctx.send("You are already in a duel!")
    return

  # check if waiting for duel
  if players[player]["awaiting_duel"]:
    if len(split) > 1 and split[1] == "abort":
      players[player]["awaiting_duel"] = False
      await ctx.send("You are no longer waiting for a duel.")
      save()
      return
    await ctx.send("You are already waiting for a duel!")
    return

  # otherwise, start duel
  if len(split) == 1:
    await duel_random(ctx, player, opponents)
  elif split[1] == "accept":
    await duel_accept(ctx, player, opponents)
  elif split[1] == "decline":
    await duel_decline(ctx, player, opponents)
  elif split[1] == "abort":
    await ctx.send("You are not in a duel!")
  else:
    await duel_player(ctx, player, opponents, split[1])
  save()
  await print_cmd(player, "duel")
