import stats.player_stats as ps
import io
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from parsing.replay import Stage
from stats.player_stats import rivals, stage_names, filter_extra_stage_freqs


def stage_graph(count):
    filtered_stage_freqs = filter_extra_stage_freqs(count)
    plt.cla()
    plt.figure(figsize=(6, 7))
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


def make_graphic(files):
    plt.switch_backend('Agg')

    replays = [r for r in ps.get_replays(files) if len(r.players) == 2]
    if len(replays) == 0:
        return None, 0

    target_name = ps.get_target_player(replays)
    target_replays = [r for r in replays if any(
        p.name == target_name for p in r.players)]
    my_chars, opp_chars = ps.player_char_count(target_replays, target_name)

    back_im = Image.new("RGB", (1200, 980), (255, 255, 255))
    draw = ImageDraw.Draw(back_im)

    im1 = character_graph(my_chars, "My Character Usage")
    im2 = character_graph(opp_chars, "Opponent Character Usage")

    back_im.paste(im1, (10, 50))
    back_im.paste(im2, (10, 440))

    stage_count = ps.stage_count(replays)

    im3 = stage_graph(stage_count)
    back_im.paste(im3, (600, 50))

    apm = round(ps.avg_apm_recent(target_name, target_replays), ndigits=2)

    text_font = ImageFont.truetype("frontend_old/Arial.ttf", 30)

    draw.text((642, 800), "Average APM (last 5 matches): {}".format(
        apm), fill="black", font=text_font)

    plt.close()

    return back_im, len(target_replays)


if __name__ == "__main__":
    make_graphic("../replays/salmon-replays")
