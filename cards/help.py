import discord

from std.bot import bot

commands_list = {
  "help":
  """
Format: &help <command>

Displays help for a command. Which is this!

Command List:
attack, deck, decks, discard, duel, duels, endturn, help, howtoplay, info, inv, newdeck, play, say, stats, stop, update
""",
  
"attack":
    """
  Format: &attack <card> <target>
  Usage: Only in battle

Attacks a target with a card. You can only attack with each card you have once per turn.
  """,

"deck":
    """
Format: &deck <deck>

Displays a deck. If no deck is specified, displays all decks.
""",

"discard":
    """
  Format: &discard <card>
  Usage: Only in battle

Discards a card from your hand. You can only discard cards if you have more than 8 cards in your hand.
  """,

"duel":
    """
Format: &duel
        &duel <player>
        &duel (accept|decline)
        &duel abort

Starts a duel with the specified player. If no player is specified, you will be added to the duel queue. Use accept or decline to accept or decline a duel from a player.
  """,
  
"duels":
  """
Format: &duels

Gets a list of players who are currently searching for a duel.
  """,

"endturn":
  """
Format: &endturn
Usage: Only in battle

Ends your turn. You can only end your turn if it is your turn.
  """,

"howtoplay":
  """
Format: &howtoplay

Displays how to play the game!
  """,
  
"info":
  """
Format: &info <card>
Aliases: i

Gets information about a card. Useful for checking stats and type.
""",

"inv":
  """
Format: &inv
Aliases: &inventory

Displays your inventory and deck.
  """,
  
"newdeck":
  """
Format: &newdeck <deck>
        &newdeck random <deck>
        &newdeck create <deck> <card1> <amount1> [card] [amount] ...
Aliases: &nd

Sets your deck to the specified deck. You can only set decks that are lower level than you.
  """,
  
"play":
  """
Format: &play <card>
Usage: Only in battle

Plays a card from your hand. You can only play one type of card per turn.
""",
  
"say":
  """
Format: &say <message>
Usage: Only in battle

Sends a message to your opponent. Useful for communicating with your opponent.
""",

"stats":
  """
Format: &stats

Displays your level and your win/loss/tie ratio.
  """,

"stop":
  """
Format: &stop

Stops the bot. Only @createsource can use this command.
  """,

"update":
  """
Format: &update

Updates the bot. Only @createsource can use this command.
  """,
}


@bot.command()
async def help(ctx):
  msg = ctx.message
  split = msg.content.split(" ", 1)
  cmd: str

  cmd = 'help' if len(split) < 2 else split[1]

  if cmd not in commands_list:
    await ctx.send(f"Command **{cmd}** does not exist")
    return

  embed = discord.Embed(title=f"Help: {cmd}", color=0x00ff00)
  embed.add_field(name="Description", value=commands_list[cmd], inline=False)
  await ctx.send(embed=embed)
