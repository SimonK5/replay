from pandas import DataFrame
from parsing.replay import Stage
from parsing import Replay, Character
from collections import Counter
import numpy as np

rivals = ["Zetterburn", "Orcane", "Wrastor", "Kragg", "Forsburn", "Maypul", "Absa", "Etalus", "Ori", "Ranno",
          "Clairen", "Sylvanos", "Elliana", "Shovel Knight", "Mollo", "Hodan", "Pomme", "Olympia"]
stage_names = ["Treetop Lodge", "Fire Capitol", "Air Armada", "Rock Wall", "Merchant Port", "Blazing Hideout",
               "Tower of Heaven", "Tempest Peak", "Frozen Fortress", "Aetherial Gates", "Endless Abyss",
               "Spirit Tree", "Forest Floor", "Julesvale", "Troupple Pond"]


def filter_extra_stage_freqs(stage_freq):
    """ Combines stage skins and deletes unused stage entries from the list of stage frequencies. """
    stage_freq[Stage.FIRE_CAPITOL] += stage_freq[Stage.NEO_FIRE_CAPITAL]
    stage_freq[Stage.AIR_ARMADA] += stage_freq[Stage.DIAMOND_GROVE]
    stage_freq[Stage.ROCK_WALL] += stage_freq[Stage.CEO_RING] + \
        stage_freq[Stage.ROA_RING]
    stage_freq[Stage.MERCHANT_PORT] += stage_freq[Stage.SWAMPY_ESTUARY]
    stage_freq[Stage.TOWER_HEAVEN] += stage_freq[Stage.AETHER_HIGH]
    stage_freq[Stage.AETHERIAL_GATES] += stage_freq[Stage.FROZEN_GATES]
    stage_freq[Stage.ENDLESS_ABYSS] += stage_freq[Stage.TUTORIAL_GRID]
    stage_freq[Stage.TROUPPLE_POND] += stage_freq[Stage.PRIDEMOOR_KEEP]

    stage_freq[Stage.BLAZING_HIDEOUT] += stage_freq[Stage.NEO_BLAZING_RAIL]
    stage_freq[Stage.TREETOP_LODGE] += stage_freq[Stage.HIGHDIVE_HIDEAWAY]
    stage_freq[Stage.JULESVALE] += stage_freq[Stage.NEO_JULESVALE]
    stage_freq[Stage.FOREST_FLOOR] += stage_freq[Stage.CRYSTAL_OASIS]

    return stage_freq[1:6] + stage_freq[7:13] + [stage_freq[15]] + stage_freq[19:22]


def stage_count(replays):
    """ Counts the occurrences of each stage in a list of Replay instances. """
    count = [0 for _ in range(len(Stage) - 1)]

    for replay in replays:
        stage_num = replay.stage
        if int(stage_num) < 1:
            raise Exception("Invalid Replay: Incorrect Stage", replay.name)

        count[stage_num] += 1

    return count


def player_char_count(replays, target_name):

    target_count = [0 for _ in range(len(Character) - 3)]
    other_count = [0 for _ in range(len(Character) - 3)]

    for replay in replays:
        target_player = next(
            p for p in replay.players if p.name == target_name)
        other_player = next(p for p in replay.players if p.name != target_name)

        try:
            target_count[target_player.character - 2] += 1
            other_count[other_player.character - 2] += 1
        except ValueError:
            pass

    return target_count, other_count


def get_replays(files):
    """ Converts a directory of replay files into Replay instances. """
    replays = []
    for file in files:
        # if file.filename.endswith(".roa"):
        # replay = Replay(file.read().decode('utf-8'))
        replay = Replay(file)
        replays.append(replay)

    # reverse to get most recent replays first
    return replays[::-1]


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


def actions_per_minute(df):
    n_inputs = num_inputs(df)

    return (3600 * n_inputs) / df.iloc[-1]["Frame"]


def get_names(players):
    """ Returns the list of names for a list of players. """
    names = []
    for player in players:
        names.append(player.name)

    return names


def avg_apm_recent(target_name, target_replays, num=5):
    cumulative_apm = 0

    iterations = min(num, len(target_replays))

    for i in range(iterations):
        target_player = next(
            p for p in target_replays[i].players if p.name == target_name)
        df = DataFrame(target_player.states)
        cumulative_apm += actions_per_minute(df)

    return cumulative_apm / iterations


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

    return possible_player_names[0]


def get_stats(files):
    replays = [r for r in get_replays(files) if len(r.players) == 2]
    # replays = files
    if len(replays) == 0:
        return None, 0

    target_name = get_target_player(replays)
    target_replays = [r for r in replays if any(
        p.name == target_name for p in r.players)]
    my_chars, opp_chars = player_char_count(target_replays, target_name)
    count_stage = stage_count(replays)
    filtered_count_stage = filter_extra_stage_freqs(count_stage)
    apm = round(avg_apm_recent(target_name, target_replays), ndigits=0)

    return {"num_replays": len(target_replays),
            "my_chars": ([{"name": name, "value": freq} for name, freq in zip(rivals, my_chars)]),
            "opp_chars": ([{"name": name, "value": freq} for name, freq in zip(rivals, opp_chars)]),
            "stage_count": ([{"name": name, "value": freq} for name, freq in zip(stage_names, filtered_count_stage)]),
            "apm": apm}


if __name__ == "__main__":
    replays = [r for r in get_replays(
        "../replays/salmon-replays") if len(r.players) == 2]

    target_name = get_target_player(replays)
    target_replays = [r for r in replays if any(
        p.name == target_name for p in r.players)]
    print(len(target_replays))
    print(player_char_count(target_replays, target_name))
    print(stage_count(target_replays))

    print(avg_apm_recent(target_name, target_replays, num=5))
