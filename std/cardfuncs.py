from std.card import req_more_info
from std.info import deuse_card, discard_card, get_dm, increase_mana, players, use_card


async def cloud_on_play(ctx, player: str, opponent: str, info: str):
  if "Land" in players[player]["has_played"]:
    await ctx.send("You have already played a Land this turn!")
    return

  if await req_more_info(ctx, info):
    return

  split = info.split(" ", 1)

  if split[0].title() == "Skip":
    opp_dm = await get_dm(opponent)
    await ctx.send("You played **Cloud** and gained 1 mana!")
    await opp_dm.send(f"<@{player}> played **Cloud** and gained 1 mana!")
    return

  if len(split) < 2:
    await ctx.send(
        "This card requires additional information. Use &play Cloud|<player> <attacker>"
    )
    return

  set_player = split[0]
  card = split[1].title()

  if card not in players[set_player]["attackers_played"]:
    await ctx.send(f"**{card}** isn't on the battlefield!")
    return

  use_card(player, "Cloud")
  players[player]["has_played"].append("Land")
  increase_mana(player, 1)
  deuse_card(set_player, card)

  if set_player == players[player]["name"]:
    pronoun = "Your"
  elif set_player == players[opponent]["name"]:
    pronoun = "Their"
  else:
    await ctx.send("Invalid player!")
    return

  opp_dm = await get_dm(opponent)
  await ctx.send("You played **Cloud** and gained 1 mana!")
  await opp_dm.send(f"<@{player}> played **Cloud** and gained 1 mana!")
  await ctx.send(
      f"**{pronoun} {card}** has been placed back in {pronoun.lower()} hand!")
  pronoun = "Your" if pronoun == "Their" else "Their"
  await opp_dm.send(
      f"**{pronoun} {card}** has been placed back in {pronoun.lower()} hand!")
  
  discard_card(player, "Cloud")
