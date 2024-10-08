import json
import logging
import logging.handlers
from datetime import datetime

from endplay.dealer import generate_deal
from endplay.evaluate import bergen_hcp_scale, hcp

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)


def opening_bid(score):
    return score >= 13


def generate_hands(timestamp, game_no=1):
    d = generate_deal()

    north_bergen = hcp(d.north, bergen_hcp_scale)
    east_bergen = hcp(d.east, bergen_hcp_scale)
    south_bergen = hcp(d.south, bergen_hcp_scale)
    west_bergen = hcp(d.west, bergen_hcp_scale)

    skewed = any(
        [
            opening_bid(score)
            for score in [north_bergen, south_bergen, east_bergen, west_bergen]
        ]
    )
    game = f"S{game_no}" if skewed else f"R{game_no}"
    return skewed, {
        "Gen": timestamp,
        "Game": game,
        "N": {
            "hand": d.north.to_pbn(),
            "hcp": hcp(d.north),
            "bergen_adj3": north_bergen,
        },
        "E": {"hand": d.east.to_pbn(), "hcp": hcp(d.east), "bergen_adj3": east_bergen},
        "S": {
            "hand": d.south.to_pbn(),
            "hcp": hcp(d.south),
            "bergen_adj3": south_bergen,
        },
        "W": {
            "hand": d.west.to_pbn(),
            "hcp": hcp(d.west),
            "bergen_adj3": west_bergen,
        },
    }


def parse_v2_format(v1_hands, count):
    v2 = {
        "id": count + 1,
        "gen": v1_hands["Gen"],
        "game": v1_hands["Game"],
        "n": v1_hands["N"],
        "e": v1_hands["E"],
        "s": v1_hands["S"],
        "w": v1_hands["W"],
    }

    return v2


def generate_multiple_hands(number=10):
    nowTime = datetime.now()
    timestamp = nowTime.strftime("%Y-%m-%d-%H%M%S")
    logger.info(f"Generating {number} deals")
    skewed_count, random_count = 0, 0
    skewed_result = {"deals": []}
    random_result = {"deals": []}
    v2_skewed = []
    iteration = 0
    while (skewed_count or random_count) < number:
        iteration += 1
        skewed, hands = generate_hands(timestamp, iteration)
        if skewed:
            skewed_result["deals"].append(hands)
            v2_skewed.append(parse_v2_format(hands, skewed_count))
            skewed_count += 1
        if len(random_result["deals"]) < number:
            random_result["deals"].append(hands)
            random_count += 1
    return json.dumps(skewed_result), json.dumps(random_result), json.dumps(v2_skewed)


if __name__ == "__main__":
    skewed_deals, random_deals, v2_skewed = generate_multiple_hands(500)

    with open("./data/bridge-hands-random.json", "w") as outfile:
        outfile.write(random_deals)

    with open("./data/bridge-hands-skewed.json", "w") as outfile:
        outfile.write(skewed_deals)

    with open("./data/v2/bridge-hands-skewed.json", "w") as outfile:
        outfile.write(v2_skewed)
