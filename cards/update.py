from std.bot import bot
import os
import subprocess


@bot.command()
async def update(ctx):
  author = ctx.author
  
  if author.id != 501430174227759105:
    await ctx.send("You are not authorized to use this command.")
    return
  
  # Change directory to one folder above
  os.chdir("..")

  # Run the command `go run update.go`
  await ctx.send("Updating...")
  subprocess.Popen(["go", "run", "update.go"])

  # Kill the current process
  await ctx.send("Shutting down the current process...")
  os._exit(0)

