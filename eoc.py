import os
import psutil

from dotenv import load_dotenv

from cards import (
    attack,
    deck,
    discard,
    duel,
    duels,
    endturn,
    help,
    howtoplay,
    info,
    inv,
    newdeck,
    play,
    say,
    stats,
    stop,
    update,
)
from std.bot import bot
from std.info import players


@bot.event
async def on_ready():
  global guilds
  print(f'Logged in as {bot.user}')

  channel = bot.get_channel(847293815311826954)
  await channel.send("It's time to d-d-d-d-d-duel")


async def setup(bot):
  await bot.add_command(attack)
  await bot.add_command(deck)
  await bot.add_command(discard)
  await bot.add_command(duel)
  await bot.add_command(duels)
  await bot.add_command(endturn)
  await bot.add_command(help)
  await bot.add_command(howtoplay)
  await bot.add_command(inv)
  await bot.add_command(info)
  await bot.add_command(newdeck)
  await bot.add_command(play)
  await bot.add_command(say)
  await bot.add_command(stats)
  await bot.add_command(stop)
  await bot.add_command(update)

  await bot.load_extension("attack")
  await bot.load_extension("deck")
  await bot.load_extension("discard")
  await bot.load_extension("duel")
  await bot.load_extension("duels")
  await bot.load_extension("endturn")
  await bot.load_extension("help")
  await bot.load_extension("howtoplay")
  await bot.load_extension("inv")
  await bot.load_extension("info")
  await bot.load_extension("newdeck")
  await bot.load_extension("play")
  await bot.load_extension("say")
  await bot.load_extension("stats")
  await bot.load_extension("stop")
  await bot.load_extension("update")


if __name__ == "__main__":
  load_dotenv()
  token: str | None = os.getenv("TOKEN")
  if token is None:
    print("No token found")
    exit()
  bot.run(token)
