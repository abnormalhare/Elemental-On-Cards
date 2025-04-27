import discord

from std.bot import bot
from std.info import init_player, players
import os
import subprocess


@bot.command()
async def update(ctx):
  init_player(ctx.author.id, ctx.author.name)

  author = ctx.author
  
  if author.id != 501430174227759105:
    await ctx.send("You are not authorized to use this command.")
    return
  
  # Change directory to one folder above
  os.chdir("..")

  # Run the command `go run update.go`
  await ctx.send("Updating...")
  process = subprocess.run(["go", "run", "update.go"], capture_output=True, text=True)

  # Send the output of the command to the Discord channel
  if process.returncode == 0:
    await ctx.send(f"Command executed successfully:\n{process.stdout}")
  else:
    await ctx.send(f"Command failed with error:\n{process.stderr}")

  # Kill the current process
  await ctx.send("Shutting down the current process...")
  os._exit(0)

