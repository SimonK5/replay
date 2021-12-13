from pandas import DataFrame
import os
from parsing.replay import Stage

from parsing import Replay
from parsing import Character


def stage_count(replays):
    """ Counts the occurrences of each stage in a list of Replay instances. """
    count = [0 for i in range(len(Stage))]

    for replay in replays:
        if int(replay.stage) < 1:
            raise Exception("Invalid Replay", replay.name)

        count[replay.stage] += 1

    return count


def player_char_count(replays, player_number):
    count = [0 for i in range(len(Character))]

    for replay in replays:
        if int(replay.players[player_number].character) < 2:
            raise Exception("Invalid Character")

        count[replay.players[player_number].character] += 1

    return count


def get_replays(dir):
    """ Converts a directory of replay files into Replay instances. """
    replays = []
    for subdir, dirs, files in os.walk(dir):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filename.endswith(".roa"):
                replay = Replay(open(filepath).read())
                replays.append(replay)

    return replays


def num_inputs(df):
    """ Calculates the approximate number of inputs by one player over a single replay. """
    count = 0
    prev_row = None
    for row in df.iloc:
        for i in range(0, 17):
            if row[i + 1]:
                if prev_row is None or (not prev_row[i + 1]):
                    count += 1
                    break
        prev_row = row

    return count


def inputs_per_minute(df):
    n_inputs = num_inputs(df)

    return (3600 * n_inputs) / df.iloc[-1]["Frame"]


if __name__ == "__main__":
    replays = get_replays("../replays")
    for replay in replays:
        print(replay.name)
        print(replay.stage)

    print(stage_count(replays))
    print(player_char_count(replays, 1))

    for replay in replays:
        player = replay.players[0]
        df = DataFrame(player.states)
        print("IPM:", inputs_per_minute(df))
