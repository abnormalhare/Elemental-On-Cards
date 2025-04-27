import discord

from std.bot import bot


@bot.command()
async def howtoplay(ctx):
  value="""
Elemental on Cards is a card game where you can duel with your friends! Currently it is in development, so expect bugs and missing features. If you find any bugs, please report them to @createsource.

Here's how to play:
- Use `&deck` to see all the decks, and `&deck <deck>` to see the cards in a deck.
- Use `&info <card>` to see more specifically what a card does. Sometimes it has a special effect!
- Use `&newdeck <deck>` to select a deck. You can only select decks that are available to you. Use &inv to check the cards out! Note: They're randomized every time you run the command!
- You can check your level and win/lose ratio with `&stats`.
- Use `&duel` to start a duel. You can duel with a specific player by using `&duel <player>`. You can also accept or decline a duel with `&duel accept` or `&duel decline`, or stop looking for a duel with `&duel abort`.
- Both you and your opponent start with 30 health and 5 cards. You win if your opponent's health reaches 0. You lose if your health reaches 0. If both of your health reaches 0 at the same time, it's a tie. (which currently cant happen!)
- Use `&play <card>` to play a card. You can only play cards that are in your hand.
- There are 4 types of cards: Land, Attacker, Spell, and Instant. Land cards give you mana. Attacker cards deal damage. Spell cards deal damage immediately. Instant cards are like spell cards but can be played once on anyone's turn.
- Use `&attack <card>` to attack with a card. You can only attack with cards attackers that you have played already.
- Attackers also prevent damage from all attacks! They can stop all damage from an attack, unless the attack is 5 or more, where they can only stop all but 2 damage.
- Use `&endturn` to end your turn. You can only have less than 8 cards in your hand at the end of your turn. If you have more, use `&discard <card>` to discard a specific card.
- Leveling up is simple! You gain them just by playing the game. You'll never decrease in level, so don't worry about losing a duel.
- Use `&help` to see the rest of the commands.

Thanks for playing!
"""


  embed = discord.Embed(title="How to Play", description=value, color=0x00ff00)
  await ctx.send(embed=embed)