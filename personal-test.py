from pandas import DataFrame
from parsing.replay import Replay, get_player_data
from parsing.player import Player
import pandas as pd

with open('replays/takffyvsdanielwf/2021-12-09-210547777149.roa') as f:
    replay = Replay(f.read())
    game_version = replay.version
    print("version:", game_version)
    match_duration = replay.duration
    print("duration:", match_duration)
    print("stage:", replay.stage)
    print("stage type:", replay.stage_type)
    print("stock:", replay.stock)
    print("time:", replay.time)
    print("teams enabled:", replay.is_teams_enabled)
    print("friendly fire enabled:", replay.is_friendly_fire_enabled)
    print("online:", replay.is_online)
    print()

    players = replay.players
    for player in players:
        print("name:", player.name)
        print("is human:", player.is_human)
        print("tag:", player.tag)
        print("character:", player.character)
        print()

    states = players[0].states
    states2 = players[1].states
    df = DataFrame(states)
    df2 = DataFrame(states2)
    print(df)
    print(df2)

    print("P1 last frame:", df.iloc[-1]["Frame"])
    print("P2 last frame:", df2.iloc[-1]["Frame"])

    count = 0
    prevRow = None
    for row in df.iloc:
        for i in range(0, 17):
            current = False
            if row[i + 1]:
                if prevRow is None or (not prevRow[i + 1]):
                    count += 1
                    current = True
                    break
        prevRow = row

    print("inputs second method", count)
    print("IPM second method", (3600 * count) / df.iloc[-1]["Frame"])
    print(list(df.iloc[:, 0]))
    print(df.iloc[:, 0])



