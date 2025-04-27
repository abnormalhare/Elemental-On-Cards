from collections.abc import Callable

import std.cardfuncs as cf


class Card:
  name: str
  type: str
  pack: str
  mana_cost: int | Callable
  on_play: Callable
  on_attack: Callable
  on_defend: Callable
  on_destroy: Callable
  on_discard: Callable

  def __init__(self, name, type, pack, mana_cost, on_play, on_attack,
               on_defend, on_destroy, on_discard):
    self.name = name
    self.type = type
    self.pack = pack
    self.mana_cost = mana_cost
    self.on_play = on_play
    self.on_attack = on_attack
    self.on_defend = on_defend
    self.on_destroy = on_destroy
    self.on_discard = on_discard

async def req_more_info(ctx, info: str) -> bool:
  if info == "":
    await ctx.send("This card requires additional information. Use &play Cloud|<info>")
    return True
  return False