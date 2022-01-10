import stats.player_stats as ps
import io
from PIL import Image
import matplotlib.pyplot as plt
from parsing.replay import Stage

rivals = ["Zetterburn", "Orcane", "Wrastor", "Kragg", "Forsburn", "Maypul", "Absa", "Etalus", "Ori", "Ranno",
              "Clairen", "Sylvanos", "Elliana", "Shovel Knight"]
stage_names = ["Treetop Lodge", "Fire Capitol", "Air Armada", "Rock Wall", "Merchant Port", "Blazing Hideout",
            "Tower of Heaven", "Tempest Peak", "Frozen Fortress", "Aetherial Gates", "Endless Abyss",
            "Spirit Tree", "Forest Floor", "Julesvale", "Troupple Pond"]


def filter_extra_stage_freqs(stage_freq):
    """ Combines stage skins and deletes unused stage entries from the list of stage frequencies. """
    stage_freq[Stage.FIRE_CAPITOL] += stage_freq[Stage.NEO_FIRE_CAPITAL]
    stage_freq[Stage.AIR_ARMADA] += stage_freq[28]
    stage_freq[Stage.ROCK_WALL] += stage_freq[Stage.CEO_RING] + stage_freq[Stage.ROA_RING]
    stage_freq[Stage.MERCHANT_PORT] += stage_freq[Stage.SWAMPY_ESTUARY]
    stage_freq[Stage.TOWER_HEAVEN] += stage_freq[Stage.AETHER_HIGH]
    stage_freq[Stage.AETHERIAL_GATES] += stage_freq[Stage.FROZEN_GATES]
    stage_freq[Stage.ENDLESS_ABYSS] += stage_freq[Stage.TUTORIAL_GRID]
    stage_freq[Stage.TROUPPLE_POND] += stage_freq[Stage.PRIDEMOOR_KEEP]

    return stage_freq[1:6] + stage_freq[7:13] + [stage_freq[15]] + stage_freq[19:22]


def stage_graph(count):
    filtered_stage_freqs = filter_extra_stage_freqs(count)
    plt.cla()
    plt.bar(stage_names, filtered_stage_freqs)
    ax = plt.subplot()
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

    plt.title("Stage Usage")

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    im = Image.open(img_buf)

    return im


def filter_unused_labels(labels, freq):
    new_labels = []
    new_freq = []
    for i in range(len(labels)):
        if freq[i] != 0:
            new_labels.append(labels[i])
            new_freq.append(freq[i])

    return new_labels, new_freq


def character_graph(count, title):
    used_rivals, used_count = filter_unused_labels(rivals, count)

    plt.cla()
    plt.pie(used_count, labels=used_rivals, autopct='%1.1f%%')
    plt.title(title)

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    im = Image.open(img_buf)

    return im


if __name__ == "__main__":
    replays = [r for r in ps.get_replays("../replays") if len(r.players) == 2]
    target_name = ps.get_target_player(replays)
    target_replays = [r for r in replays if any(p.name == target_name for p in r.players)]
    y1, y2 = ps.player_char_count(target_replays, target_name)

    im1 = character_graph(y1, "My Character Usage")
    im2 = character_graph(y2, "Opponent Character Usage")

    back_im = Image.new("RGB", (1920, 1080), (255, 255, 255))

    back_im.paste(im1, (10, 10))
    back_im.paste(im2, (10, 500))

    y3 = ps.stage_count(replays)

    im3 = stage_graph(y3)
    back_im.paste(im3, (600, 10))

    back_im.show()
