from std.bot import bot
from std.carddefs import test_card_stats
from std.info import (
    card_stats,
    check_duel,
    check_health,
    deal_damage,
    discard_card,
    get_dm,
    increase_mana,
    init_player,
    players,
    print_cmd,
    save,
    use_card,
)


async def play_new(ctx, split):
  author = ctx.author
  player = str(author.id)
  split2 = split[1].split("|", 2)
  card = split2[0].strip().title()

  if card not in test_card_stats:
    await ctx.send(f"**{card}** is not a valid card!")
    return

  if len(split2) < 2:
    await test_card_stats[card].on_play(ctx, player,
                                        players[player]["opponents"][0], "")
  else:
    await test_card_stats[card].on_play(ctx, player,
                                        players[player]["opponents"][0],
                                        split2[1].strip())


# to be changed. a lot
@bot.command()
async def play(ctx):
  init_player(ctx.author.id, ctx.author.name)
  if not check_duel(ctx, str(ctx.author.id)):
    await ctx.send("You aren't in a duel!")
    return

  message = ctx.message
  author = ctx.author
  player = str(author.id)

  if message.guild is not None:
    await ctx.send(
        "Please use DMs to play to ensure no one peeks while you play!")
    return

  split = message.content.split(" ", 1)
  if len(split) < 2:
    await ctx.send("Please specify a card.")
    return

  if "|" in split[1]:
    card = split[1].split("|", 1)[0].strip().title()
    print(f"CARD: '{card}'")
  else:
    card = split[1].title()
  
  if card not in players[player]["hand"]:
    await ctx.send(f"You don't have a **{card}** in your hand!")
    return

  if not players[player]["is_turn"] and card_stats[card]["Type"] != "Instant":
    await ctx.send("It is not your turn!")

  if card_stats[card]["Type"] in players[player]["has_played"]:
    await ctx.send(
        f"You have already played a **{card_stats[card]['Type']}** this turn!")
    return

  if card in test_card_stats:
    await play_new(ctx, split)
    return

  opponent = players[player]["opponents"][0]
  opp_dm = await get_dm(opponent)

  mana = card_stats[card]["Mana"]
  if card_stats[card]["Type"] == "Land":
    increase_mana(player, mana)
    players[player]["has_played"].append("Land")
    await ctx.send(f"You played **{card}** and gained {mana} mana!")
    await opp_dm.send(f"<@{player}> played **{card}** and gained {mana} mana!")
    use_card(player, card)

  elif card_stats[card]["Type"] == "Attacker":
    if players[player]["curr_mana"] < mana:
      await ctx.send("You don't have enough mana to play that card!")
      return

    use_card(player, card)
    players[player]["curr_mana"] -= mana
    await ctx.send(
        f"You played **{card}**! You now have {players[player]['curr_mana']} mana!"
    )
    await opp_dm.send(
        f"<@{player}> played **{card}** and has {players[player]['curr_mana']} mana left!"
    )

  elif card_stats[card]["Type"] == "Instant" or card_stats[card][
      "Type"] == "Spell":
    if players[player]["curr_mana"] < mana:
      await ctx.send("You don't have enough mana to play that card!")
      return

    use_card(player, card)
    players[player]["has_played"].append(card_stats[card]["Type"])
    players[player]["curr_mana"] -= mana
    await deal_damage(ctx, player, opponent, card)
    discard_card(player, card)

  await check_health(ctx, player, opponent)

  save()
  await print_cmd(player, "play")
