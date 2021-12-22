from pandas import DataFrame
import os
from parsing.replay import Stage

from parsing import Replay, Character, Player
import time
from collections import Counter


def stage_count(replays):
    """ Counts the occurrences of each stage in a list of Replay instances. """
    count = [0 for i in range(len(Stage))]

    for replay in replays:
        if int(replay.stage) < 1:
            raise Exception("Invalid Replay", replay.name)

        count[replay.stage] += 1

    return count


def player_char_count(replays, target_name):

    target_count = [0 for i in range(len(Character))]
    other_count = [0 for i in range(len(Character))]

    for replay in replays:
        print(target_name)
        target_player = next(p for p in replay.players if p.name == target_name)
        other_player = next(p for p in replay.players if p.name != target_name)

        if int(target_player.character) < 2 or int(other_player.character) < 2:
            raise Exception("Invalid Character")

        target_count[target_player.character] += 1
        other_count[other_player.character] += 1

    return target_count, other_count


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
        for i in range(1, 17):
            if row[i]:
                if prev_row is None or (not prev_row[i]):
                    count += 1
                    break
        prev_row = row

    return count


def inputs_per_minute(df):
    n_inputs = num_inputs(df)

    return (3600 * n_inputs) / df.iloc[-1]["Frame"]


def get_names(players):
    """ Returns the list of names for a list of players. """
    names = []
    for player in players:
        names.append(player.name)

    return names


def get_target_player(replays):
    """Determine the player to analyze in given a target set of replays.

    Precondition: The input array is not empty.
    """
    possible_player_names = get_names(replays[0].players)

    for replay in replays:
        replay_names = get_names(replay.players)
        if Counter(replay_names) == Counter(possible_player_names):
            continue
        elif possible_player_names[0] in replay_names:
            return possible_player_names[0]
        elif possible_player_names[1] in replay_names:
            return possible_player_names[1]


if __name__ == "__main__":
    replays = [r for r in get_replays("../replays") if len(r.players) == 2]
    # for replay in replays:
    #     print(replay.name)
    #     print(replay.stage)
    #
    # print(stage_count(replays))
    # print(player_char_count(replays, 1))
    #
    # start_time = time.time()
    # for replay in replays:
    #     player = replay.players[0]
    #     df = DataFrame(player.states)
    #     print(replay._unknown_2)
    #     print("IPM:", inputs_per_minute(df))
    #     # print(df)
    #
    # print("time to analyze {r} replays: {t}".format(r=len(replays), t=time.time()-start_time))
    # get_target_player(replays)
    target_name = get_target_player(replays)
    target_replays = [r for r in replays if any(p.name == target_name for p in r.players)]
    print(player_char_count(target_replays, target_name))
