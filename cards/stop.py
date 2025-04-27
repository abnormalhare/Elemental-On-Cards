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

  # Run the command `go run update.go`
  await ctx.send("Stopping...")
  
  os._exit(0)

