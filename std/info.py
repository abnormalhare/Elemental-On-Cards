import json
import os
import random

import discord

from std.bot import bot

packs = {
    "Air": 1,
    "Earth": 1,
    "Fire": 1,
    "Water": 1,
    "Light": 2,
    "Dark": 2,
    "Nature": 2,
    "Metal": 2,
    "Lightning": 3,
    "Ice": 3,
    "Wind": 3,
    "Poison": 3,
    "Shadow": 3,
    "Space": 4,
    "Logic": 5,
    "Chaos": 5,
}

cards = {
    "Air": ["Cloud", "Floating Island", "Falcon", "Gale", "Tornado"],
    "Earth": ["Mound", "Continent", "Mole", "Earthquake", "Landslide"],
    "Fire": ["Campfire", "Volcano", "Phoenix", "Inferno", "Wildfire"],
    "Water": ["Pond", "Delta", "Shark", "Tsunami", "Flood"],
    "Light": ["Coming soon..."],
    "Dark": ["Coming soon..."],
    "Nature": ["Coming soon..."],
    "Metal": ["Coming soon..."],
}

collection = {  # 40 in each deck
    "Air": {
        "Cloud": 10,
        "Floating Island": 10,
        "Falcon": 8,
        "Gale": 6,
        "Tornado": 6
    },
    "Earth": {
        "Mound": 10,
        "Continent": 10,
        "Mole": 7,
        "Earthquake": 7,
        "Landslide": 6
    },
    "Fire": {
        "Campfire": 9,
        "Volcano": 9,
        "Phoenix": 7,
        "Inferno": 7,
        "Wildfire": 8
    },
    "Water": {
        "Pond": 9,
        "Delta": 9,
        "Shark": 9,
        "Tsunami": 7,
        "Flood": 6
    }
}

card_stats: dict
players: dict

try:
  with open("cards.json", "r") as f:
    card_stats = json.load(f)
except FileNotFoundError:
  print("cards.json not found, ending program")
  exit(1)
except Exception as e:
  print(f"Error loading cards.json: {e}")
  exit(1)

try:
  with open("players.json", "r") as f:
    players = json.load(f)
except FileNotFoundError:
  print("cards.json not found, ending program")
  exit(1)
except Exception as e:
  print(f"Error loading cards.json: {e}")
  exit(1)

MAX_CARDS = 40
MAX_HEALTH = 30
PLAYER_COLOR = 0xFF0000
OPPONENT_COLOR = 0x0000FF


def get_searching_players() -> list:
  return [player for player in players if players[player]["awaiting_duel"]]


def get_random_card_for(player: str):
  p_card: str = random.choice(players[player]["curr_inv"])
  players[player]["hand"].append(p_card)
  players[player]["curr_inv"].remove(p_card)


async def get_dm(player: str):
  return await bot.fetch_user(int(player))


def save():
  # create new json and store players
  with open('players.json', 'w') as f:
    json.dump(players, f)


def init_player(player_id: int, name: str) -> None:
  if str(player_id) not in players:
    players[str(player_id)] = {
        # basic info
        "name": name,
        "deck": "",
        "inventory": [],
        # battle info
        "color": 0,
        "health": 30,
        "mana": 0,
        "curr_mana": 0,
        "opponents": [],
        "curr_inv": [],
        "hand": [],
        "used": [],
        "has_played": [],
        "attackers_played": [],
        "discard": [],
        "exile": [],
        # system info
        "in_duel": False,
        "awaiting_duel": False,
        "is_turn": False,
        # stats
        "level": 1,
        "won": 0,
        "lost": 0,
        "tied": 0
    }
  save()


def check_duel(ctx, player: str) -> bool:
  if (not players[player]["in_duel"]):
    ctx.send("You aren't in a duel!")
    return False
  else:
    return True


def reset_player(player: str):
  players[player]["curr_inv"] = players[player]["inventory"].copy()
  players[player]["hand"] = []
  players[player]["used"] = []
  players[player]["has_played"] = []
  players[player]["attackers_played"] = []
  players[player]["mana"] = 0
  players[player]["curr_mana"] = 0
  players[player]["health"] = MAX_HEALTH


def end_duel(player: str, opponent: str):
  players[player]["in_duel"] = False
  players[player]["opponents"] = []
  players[opponent]["in_duel"] = False
  players[opponent]["opponents"] = []


def use_card(player: str, card: str):
  players[player]["hand"].remove(card)
  players[player]["used"].append(card)


def deuse_card(player: str, card: str):
  players[player]["hand"].append(card)
  players[player]["used"].remove(card)
  if card in players[player]["attackers_played"]:
    players[player]["attackers_played"].remove(card)


def discard_card(player: str, card: str):
  players[player]["discard"].append(card)


def kill_card(player: str, card: str):
  players[player]["attackers_played"].remove(card)
  players[player]["discard"].append(card)


def increase_mana(player: str, mana: int):
  players[player]["mana"] += mana
  players[player]["curr_mana"] += mana


async def print_cmd(player: str, cmd: str):
  print("CMD: ", cmd)
  print("NAME:", players[player]["name"])
  print("HAND:", players[player]["hand"])
  print("DECK:", players[player]["deck"])
  print("CURRINV:", players[player]["curr_inv"])
  print()


async def begin_duel(ctx, player: str, opponent: str):
  if opponent == "0":
    init_player(0, "testbot")
    players["0"]["inventory"] = [
        "Cloud", "Floating Island", "Falcon", "Gale", "Tornado"
    ]
  # set players to being in battle
  players[player]["awaiting_duel"] = False
  players[opponent]["awaiting_duel"] = False
  players[player]["in_duel"] = True
  players[opponent]["in_duel"] = True
  if player not in players[opponent]["opponents"]:
    players[opponent]["opponents"].append(player)
  if opponent not in players[player]["opponents"]:
    players[player]["opponents"].append(opponent)

  # announce to the world
  await ctx.send(f"Duel started: <@{player}> VS <@{opponent}>")

  # store player colors
  players[player]["color"] = PLAYER_COLOR
  players[opponent]["color"] = OPPONENT_COLOR
  # setup game
  reset_player(player)
  reset_player(opponent)

  p_name = players[player]["name"]
  o_name = players[opponent]["name"]

  # setup embed to send
  embed_player = discord.Embed(title=f"{p_name} VS {o_name}",
                               color=PLAYER_COLOR)
  embed_player.add_field(name="Your Hand", value="", inline=False)
  embed_player.add_field(name="Your Health",
                         value=players[player]["health"],
                         inline=False)
  embed_player.add_field(name="Your Mana",
                         value=players[player]["curr_mana"],
                         inline=False)

  embed_opponent = discord.Embed(title=f"{p_name} VS {o_name}",
                                 color=OPPONENT_COLOR)
  embed_opponent.add_field(name="Your Hand", value="", inline=False)
  embed_opponent.add_field(name="Your Health",
                           value=players[opponent]["health"],
                           inline=False)
  embed_opponent.add_field(name="Your Mana",
                           value=players[opponent]["curr_mana"],
                           inline=False)

  for _ in range(5):
    get_random_card_for(player)
    get_random_card_for(opponent)

  embed_o_player = discord.Embed(title=f"{p_name} VS {o_name}",
                                 color=OPPONENT_COLOR)
  embed_o_player.add_field(name="Their Card Count",
                           value=len(players[opponent]["hand"]),
                           inline=False)
  embed_o_player.add_field(name="Their Health",
                           value=players[opponent]["health"],
                           inline=False)
  embed_o_player.add_field(name="Their Mana",
                           value=players[opponent]["curr_mana"],
                           inline=False)

  embed_o_opponent = discord.Embed(title=f"{p_name} VS {o_name}",
                                   color=PLAYER_COLOR)
  embed_o_opponent.add_field(name="Their Card Count",
                             value=len(players[player]["hand"]),
                             inline=False)
  embed_o_opponent.add_field(name="Their Health",
                             value=players[player]["health"],
                             inline=False)
  embed_o_opponent.add_field(name="Their Mana",
                             value=players[player]["curr_mana"],
                             inline=False)

  # set values correctly
  embed_player.set_field_at(0,
                            name="Your Hand",
                            value=", ".join(players[player]["hand"]),
                            inline=False)
  embed_opponent.set_field_at(0,
                              name="Your Hand",
                              value=", ".join(players[opponent]["hand"]),
                              inline=False)

  # draw for start of turn
  get_random_card_for(opponent)

  # send to players
  p_dm = await get_dm(player)
  await p_dm.send(embed=embed_player)
  await p_dm.send(embed=embed_o_player)
  await p_dm.send("It is your turn!")

  o_dm = await get_dm(opponent)
  await o_dm.send(embed=embed_opponent)
  await o_dm.send(embed=embed_o_opponent)
  await o_dm.send(f"It is <@{player}>'s turn!")

  players[player]["is_turn"] = True

  save()


async def swap_turns(ctx, player: str, opponent: str):
  players[player]["is_turn"] = False
  if "Instant" in players[player]["has_played"]:
    players[player]["has_played"].remove("Instant")

  players[opponent]["is_turn"] = True
  players[opponent]["curr_mana"] = players[opponent]["mana"]
  players[opponent]["has_played"] = []
  players[opponent]["attackers_played"] = []

  get_random_card_for(opponent)

  l_name: str
  r_name: str
  if players[player]["color"] == PLAYER_COLOR:
    l_name = players[player]["name"]
    r_name = players[opponent]["name"]
  else:
    l_name = players[opponent]["name"]
    r_name = players[player]["name"]

  cards_in_play = ", ".join(
      players[player]["attackers_played"]
  ) if players[player]["attackers_played"] != [] else "*None*"

  opp_dm = await get_dm(opponent)
  embed_opponent = discord.Embed(title=f"{l_name} VS {r_name}",
                                 color=OPPONENT_COLOR)
  embed_opponent.add_field(name="Your Hand",
                           value=", ".join(players[opponent]["hand"]),
                           inline=False)
  embed_opponent.add_field(name="Your Health",
                           value=players[opponent]["health"],
                           inline=False)
  embed_opponent.add_field(name="Your Mana",
                           value=players[opponent]["curr_mana"],
                           inline=False)
  embed_opponent.add_field(name="Your Cards in Play",
                           value=cards_in_play,
                           inline=False)
  await opp_dm.send("It is now your turn!")
  await opp_dm.send(embed=embed_opponent)

  embed_player = discord.Embed(title=f"{l_name} VS {r_name}",
                               color=PLAYER_COLOR)
  embed_player.add_field(name="Their Card Count",
                         value=len(players[opponent]["hand"]),
                         inline=False)
  embed_player.add_field(name="Their Health",
                         value=players[opponent]["health"],
                         inline=False)
  embed_player.add_field(name="Their Mana",
                         value=players[opponent]["curr_mana"],
                         inline=False)
  embed_player.add_field(name="Their Cards in Play",
                         value=cards_in_play,
                         inline=False)

  await ctx.send(f"It is now <@{opponent}>'s turn!")
  await ctx.send(embed=embed_player)

  save()

async def inc_level(ctx, player: str):
  level = players[player]["level"]
  next_level = 4 * (level * (level + 1)) // 2
  wins = players[player]["won"] + (2 * players[player]["tied"] // 3) + (players[player]["lost"] // 3)

  if wins >= next_level:
    dm = await get_dm(player)
    players[player]["level"] += 1
    await ctx.send(f"<@{player}> has leveled up to level {players[player]['level']}!")
    await dm.send(f"You have leveled up to level {players[player]['level']}!")
    if players[player]["level"] % 5 == 0:
      pack_msg = "You have unlocked new packs: "
      for pack in packs:
        if players[player]["level"] == packs[pack]:
          pack_msg += f"{pack}, "
      pack_msg = pack_msg[:-2] + "!"
      await ctx.send(pack_msg)


async def check_health(ctx, player: str, opponent: str):
  opp_dm = await get_dm(opponent)
  if players[player]["health"] <= 0 and players[opponent]["health"] <= 0:
    await ctx.send("It's a tie!")
    await opp_dm.send("It's a tie!")
    end_duel(player, opponent)
    players[player]["tied"] += 1
    players[opponent]["tied"] += 1
  elif players[opponent]["health"] <= 0:
    await ctx.send(f"<@{opponent}> has been defeated!")
    await opp_dm.send(f"You have been defeated by <@{player}>!")
    end_duel(player, opponent)
    players[player]["won"] += 1
    players[opponent]["lost"] += 1
  elif players[player]["health"] <= 0:
    await ctx.send(f"You have been defeated by <@{opponent}>!")
    await opp_dm.send(f"<@{opponent}> has been defeated!")
    end_duel(player, opponent)
    players[player]["lost"] += 1
    players[opponent]["won"] += 1
  await inc_level(ctx, player)


async def deal_damage(ctx, player: str, opponent: str, card):
  opp_dm = await get_dm(opponent)
  att_stat = 0
  def_stat = 0

  players[opponent]["health"] -= card_stats[card]["Attack"]
  att_stat = card_stats[card]["Attack"]
  if players[opponent]["attackers_played"] != []:
    for a_card in players[opponent]["attackers_played"]:
      def_stat += card_stats[a_card]["Defense"]
  if def_stat > att_stat and att_stat >= 5:
    def_stat = att_stat - 2
  elif def_stat > att_stat:
    def_stat = att_stat
  players[opponent]["health"] += def_stat

  await ctx.send(
      f"You played **{card}**! You now have {players[player]['curr_mana']} mana!"
  )
  await opp_dm.send(
      f"<@{player}> played **{card}** and has {players[player]['curr_mana']} mana left!"
  )
  if def_stat != 0:
    await ctx.send(
        f"<@{opponent}>'s attackers reduced the damage by {def_stat}!")
    await opp_dm.send(f"Your attackers reduced the damage by {def_stat}!")

  await ctx.send(f"You dealt {att_stat - def_stat} damage to <@{opponent}>!")
  await opp_dm.send(f"<@{player}> dealt {att_stat - def_stat} damage to you!")
