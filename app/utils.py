import requests
import re
from collections import Counter

card_cache = {}
oracle_tag_cache = {}


## general utility
def parse_card_names(deck_list):
    # remove duplicates and whitespace from the deck list
    # but keep user input order
    seen = set()
    result = []
    for name in deck_list:
        cleaned = name.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return result

def fetch_card_data(name):
    if name in card_cache:
        return card_cache[name]

    url = f'https://api.scryfall.com/cards/named'
    response = requests.get(url, params={'fuzzy': name})

    if response.status_code == 200:
        card_data = response.json()
        card_cache[name] = card_data
        return card_data
    else:
        return {
            'name': name,
            'error': f'Scryfall lookup failed ({response.status_code})'
        }

def fetch_oracle_tag_set(tagName):
    if tagName in oracle_tag_cache:
        return oracle_tag_cache[tagName]

    card_names = set()
    url = f"https://api.scryfall.com/cards/search?q=oracletag:{tagName}"

    while url:
        response = requests.get(url)
        data = response.json()
        for card in data["data"]:
            card_names.add(card["name"])
        url = data.get("next_page")
    
    oracle_tag_cache[tagName] = card_names
    return card_names

def preload_all_oracle_tag_sets(tags=["ramp", "removal", "boardwipe", "counterspell", "graveyardhate", "draw", "recursion", "tribal"]):
    for tag in tags:
        fetch_oracle_tag_set(tag)

def skip_land_cards(cards):
    return [
        card for card in cards
        if "Land" not in card.get("type_line", "").split()
    ]

## card type analysis/counts
def count_card_types(cards):
    type_counts = {}
    for card in cards:
        types = card.get("type_line", "")
        for card_type in ["Creature", "Instant", "Sorcery", "Artifact", "Enchantment", "Land", "Planeswalker"]:
            if card_type in types:
                type_counts[card_type] = type_counts.get(card_type, 0) + 1
    return type_counts

def count_colors(cards):
    color_count = {"W": 0, "U": 0, "B": 0, "R": 0, "G": 0, "C": 0}

    for card in cards:
        identity = card.get("color_identity", [])

        if identity:
            for color in identity:
                color_count[color] += 1
        else:
            # Colorless
            color_count["C"] += 1

    return {
        "color_count": color_count
    }

## mana curve analysis
def analyze_avg_converted_mana_cost(cards):
    total_cmc = 0
    count = 0
    # skip land cards for average CMC calculation
    cards = skip_land_cards(cards)
    for card in cards:
        cmc = card.get("cmc", 0)
        total_cmc += cmc
        count += 1
    return round(total_cmc / count, 2) if count else 0

def analyze_mana_curve_histogram(cards):
    histogram = {}

    # skip land cards for mana curve histogram
    cards = skip_land_cards(cards)
    for card in cards:
        converted_mana_cost = int(card.get("cmc", 0))
        # Group anything 7+ into the "7+" bucket
        key = str(converted_mana_cost) if converted_mana_cost < 7 else "7+"
        histogram[key] = histogram.get(key, 0) + 1

    # make sure 0–6 + "7+" keys always appear, even if 0 counts
    for i in range(0, 7):
        histogram.setdefault(str(i), 0)
    histogram.setdefault("7+", 0)

    # Return keys sorted in order for cleaner frontend display
    return {k: histogram[k] for k in sorted(histogram.keys(), key=lambda x: int(x.replace('+','9')))}

def analyze_max_converted_mana_cost(cards):
    max_converted_mana_cost = 0
    for card in cards:
        if "Land" in card.get("type_line", "").split():
            continue
        converted_mana_cost = card.get("cmc", 0)
        if converted_mana_cost > max_converted_mana_cost:
            max_converted_mana_cost = converted_mana_cost
    return max_converted_mana_cost

# ramp analysis
def analyze_ramp(cards):
    ramp_card_names_scryfall = fetch_oracle_tag_set('ramp')
    ramp_count = 0
    ramp_cards = []

    cards = skip_land_cards(cards)

    for card in cards:
        name = card.get("name", "")
        oracle_text = card.get("oracle_text", "").lower()

        if name in ramp_card_names_scryfall:
            ramp_count += 1
            ramp_cards.append(name)

    return {
        "ramp_count": ramp_count,
        "ramp_cards": ramp_cards
    }

# interaction analysis
def analyze_interaction(cards):
    removal_card_names_scryfall = fetch_oracle_tag_set('removal')
    board_wipe_card_names_scryfall = fetch_oracle_tag_set('boardwipe')
    counterspell_card_names_scryfall = fetch_oracle_tag_set('counterspell')
    graveyard_hate_card_names_scryfall = fetch_oracle_tag_set('graveyardhate')

    interaction_summary = {
        "removal": 0,
        "board_wipes": 0,
        "counterspells": 0,
        "graveyard_hate": 0,
        "interaction_cards": []
    }
    
    # skip land cards for interaction analysis
    cards = skip_land_cards(cards)
    for card in cards:
        oracle_text = card.get("oracle_text", "").lower()
        name = card.get("name", "Unknown")
        matched = False

        if name in removal_card_names_scryfall:
            interaction_summary["removal"] += 1
            matched = True
        if name in board_wipe_card_names_scryfall:
            interaction_summary["board_wipes"] += 1
            matched = True
        if name in counterspell_card_names_scryfall:
            interaction_summary["counterspells"] += 1
            matched = True
        if name in graveyard_hate_card_names_scryfall:
            interaction_summary["graveyard_hate"] += 1
            matched = True

        if matched:
            interaction_summary["interaction_cards"].append(name)

    return interaction_summary

# card draw analysis
def analyze_card_draw(cards):
    draw_card_names_scryfall = fetch_oracle_tag_set('draw')
    draw_count = 0
    draw_cards = []

    # skip land cards for card draw analysis
    cards = skip_land_cards(cards)
    for card in cards:
        oracle = card.get("oracle_text", "").lower()
        name = card.get("name", "Unknown")
        matched = False

        if name in draw_card_names_scryfall:
            draw_count += 1
            draw_cards.append(card.get("name", "Unknown"))

    return {
        "card_draw_count": draw_count,
        "card_draw_cards": draw_cards
    }

# tribal synergy analysis
def analyze_tribal_synergy(cards):
    tribal_synergy_card_names_scryfall = fetch_oracle_tag_set('tribal')

    subtype_counts = Counter()
    tribal_synergy_cards = []

    for card in cards:
        name = card.get("name", "Unknown")
        type_line = card.get("type_line", "")
        oracle = card.get("oracle_text", "").lower()

        if name in tribal_synergy_card_names_scryfall:
            tribal_synergy_cards.append({
                "name": name,
                "oracle_text": oracle
            })

        if "—" in type_line and "Creature" in type_line:
            subtypes_str = type_line.split("—")[1].strip()
            subtypes = re.split(r"\s+|/", subtypes_str)
            for subtype in subtypes:
                if subtype.isalpha():
                    subtype_counts[subtype] += 1

    most_common = subtype_counts.most_common(1)[0] if subtype_counts else None

    if most_common:
        tribe = most_common[0].lower()
        tribe_creature_count = most_common[1]

        tribe_matching_synergy = [
            card["name"] for card in tribal_synergy_cards
            if tribe in card["oracle_text"]
        ]
    else:
        tribe = None
        tribe_creature_count = 0
        tribe_matching_synergy = []

    # TO-DO: Add score for how much of the tribal synergy cards in the deck match the most common tribe
    return {
        "most_common_tribe": tribe.capitalize() if tribe else None,
        "tribe_creature_count": tribe_creature_count,
        "tribal_synergy_card_count": len(tribal_synergy_cards),
        "tribal_synergy_cards": [card["name"] for card in tribal_synergy_cards],
        "matching_synergy_cards_for_tribe": tribe_matching_synergy,
        "matching_synergy_card_count": len(tribe_matching_synergy)
    }


# recursion/graveyard analysis
def analyze_recursion(cards):
    recursion_card_names_scryfall = fetch_oracle_tag_set('recursion')
    recursion_count = 0
    recursion_cards = []

    for card in cards:
        oracle = card.get("oracle_text", "").lower()
        name = card.get("name", "Unknown")
        matched = False

        if name in recursion_card_names_scryfall:
            recursion_count += 1
            recursion_cards.append(card.get("name", "Unknown"))

    return {
        "recursion_count": recursion_count,
        "recursion_cards": recursion_cards
    }

# commander analysis
def analyze_commander(cards, deck_list=None):
    if not deck_list or not cards:
        return {"error": "Deck list or card data missing"}

    commander_name = deck_list[0].strip().lower()

    for card in cards:
        name = card.get("name", "").lower()
        type_line = card.get("type_line", "")
        if name == commander_name:
            return {
                "commander_name": card.get("name"),
                "commander_type_line": type_line,
                "commander_colors": card.get("color_identity", []),
                "commander_oracle_text": card.get("oracle_text", ""),
                "is_legendary": "Legendary" in type_line
            }

    return {"error": f"Commander '{deck_list[0]}' not found or invalid (may be a typo)"}
