from std.bot import bot
from std.info import (
  card_stats,
  check_duel,
  check_health,
  deal_damage,
  init_player,
  players,
  print_cmd,
  save,
)


@bot.command()
async def attack(ctx):
  init_player(ctx.author.id, ctx.author.name)
  if not check_duel(ctx, str(ctx.author.id)):
    await ctx.send("You aren't in a duel!")
    return

  if ctx.message.guild is not None:
    await ctx.send(
        "Please use DMs to play to ensure no one peeks while you play!")
    return

  all = False
  message = ctx.message
  author = ctx.author
  player = str(author.id)
  opponent = players[player]["opponents"][0]

  if not players[player]["is_turn"]:
    await ctx.send(
        "It is not your turn! Please wait for your opponent to end their turn."
    )
    return

  split = message.content.split(" ", 2)
  if len(split) < 2:
    await ctx.send("Please specify a card.")
    return

  if split[1] == "all":
    all = True
    split = split[1].split(" ", 1)
    if len(split) < 2:
      await ctx.send("Please specify a card.")
      return
  
  card = split[1].title()
  if card not in players[player]["used"]:
    await ctx.send(f"You don't have a **{card}** in your used cards!")
    return

  if card_stats[card]["Type"] != "Attacker":
    await ctx.send(f"**{card}** is not an attacker!")
    return

  attackers_played = players[player]["attackers_played"]
  if card in attackers_played and players[player]["used"].count(card) < attackers_played.count(card):
    await ctx.send(f"You have already attacked with **{card}** this turn!")
    return

  if all:
    for card in players[player]["used"]:
      if card_stats[card]["Type"] == "Attacker":
        await deal_damage(ctx, player, opponent, card)
        await check_health(ctx, player, opponent)
  else:
    players[player]["attackers_played"].append(card)
    
    await deal_damage(ctx, player, opponent, card)
    await check_health(ctx, player, opponent)

  save()
  await print_cmd(player, "attack")