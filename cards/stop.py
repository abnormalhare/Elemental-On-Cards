from std.bot import bot
import os


@bot.command()
async def stop(ctx):
  author = ctx.author
  
  if author.id != 501430174227759105:
    await ctx.send("You are not authorized to use this command.")
    return

  # Run the command `go run update.go`
  await ctx.send("Stopping...")
  
  os._exit(0)

