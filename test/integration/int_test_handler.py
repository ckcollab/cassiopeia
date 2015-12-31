import os
import sys

from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


if sys.version_info.major == 2:
    import future.standard_library

    future.standard_library.install_aliases()


RIOT_API_KEY = os.environ.get("RIOT_API_KEY")
if RIOT_API_KEY:
    riotapi.set_api_key(os.environ["RIOT_API_KEY"])
    riotapi.set_region("NA")
    riotapi.print_calls(True)
    riotapi.set_load_policy(LoadPolicy.lazy)

RIOT_API_KEY_LIMITS = os.environ.get("RIOT_API_KEY_LIMITS")
if RIOT_API_KEY_LIMITS:
    # Expected ENV var format is something like:
    # RIOT_API_KEY_LIMITS=1500/10,90000/600
    rates = RIOT_API_KEY_LIMITS.replace(" ", "")
    rate_tuples = []
    for rate in rates.split(","):
        calls, time = rate.split("/")
        rate_tuples.append((int(calls), int(time)))
    riotapi.set_rate_limits(*rate_tuples)


champion_id = 35
champion_name = "Thresh"
mastery_id = 6361
match_id = 1505030444
rune_id = 5234
summoner_id = 22508641
summoner_name = "FatalElement"
summoner_spell_id = 7
team_id = "TEAM-49fc9f10-1290-11e3-80a6-782bcb4d0bb2"
item_id = 3031


def test_result(result=None):
    assert True  # ??? was Pass previously
