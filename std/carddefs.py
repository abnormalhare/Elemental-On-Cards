import std.cardfuncs as cf
from std.card import Card

test_card_stats = {
   "Cloud": Card(name="Cloud",
   type="Land",
   pack="Air",
   mana_cost=1,
   on_play=cf.cloud_on_play,
   on_attack=None,
   on_defend=None,
   on_destroy=None,
   on_discard=None)
}