import requests
import re
import itertools 

from collections import Counter

card_cache = {}
oracle_tag_cache = {}
oracle_text_search_cache = {}
is_cache = {}
combo_lookup_cache = None

## urls
oracle_tag_prefix = "https://api.scryfall.com/cards/search?q=oracletag:"
is_prefix = "https://api.scryfall.com/cards/search?q=is:"
oracle_text_search_prefix = "https://api.scryfall.com/cards/search?q=oracle:"

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

def fetch_combo_lookup():
    global combo_lookup_cache
    if combo_lookup_cache is not None:
        return combo_lookup_cache

    url = "https://backend.commanderspellbook.com/variants?format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch combos: {e}")
        combo_lookup_cache = {}
        return {}

    data = response.json()
    results = data.get("results", [])
    combo_lookup = {}

    for variant in results:
        uses = variant.get("uses", [])
        if len(uses) != 2:
            continue  # Only interested in 2-card combos

        # Check if any component is commander-locked
        if any(u.get("mustBeCommander", False) for u in uses):
            continue

        try:
            cards = [u["card"]["name"] for u in uses]
        except (KeyError, TypeError):
            continue

        key = frozenset(card.lower() for card in cards)
        combo_lookup[key] = {
            "cards": cards,
            "features": [f["feature"]["name"] for f in variant.get("produces", [])],
            "description": variant.get("description", ""),
            "prerequisites": variant.get("notablePrerequisites", "") or variant.get("easyPrerequisites", "")
        }

    combo_lookup_cache = combo_lookup
    return combo_lookup

def fetch_custom_query_set(queryValue, url, cacheName):
    if queryValue in cacheName:
        return cacheName[queryValue]
    
    card_names = set()

    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching Scryfall query: {url}")
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
            cacheName[queryValue] = set()  # Cache as empty to avoid retries
            return set()

        data = response.json()
        if "data" not in data:
            print(f"Unexpected response structure for {url}")
            print(f"Response: {data}")
            cacheName[queryValue] = set()
            return set()

        for card in data["data"]:
            card_names.add(card["name"])
        url = data.get("next_page")

    cacheName[queryValue] = card_names
    return card_names

def fetch_tagged_set(tag: str, tag_type: str = "oracletag"):
    url_map = {
        "oracletag": oracle_tag_prefix,
        "is": is_prefix,
        "oracle": oracle_text_search_prefix
    }
    cache_map = {
        "oracletag": oracle_tag_cache,
        "is": is_cache,
        "oracle": oracle_text_search_cache
    }

    if tag_type not in url_map:
        raise ValueError(f"Unknown tag type: {tag_type}")

    # wrap the tag in single quotes for oracle text queries
    formatted_tag = f"'{tag}'" if tag_type == "oracle" else tag

    url = f"{url_map[tag_type]}{formatted_tag}"
    return fetch_custom_query_set(tag, url, cache_map[tag_type])

def find_matching_card_names_skip_lands(cards, name_set):
    return [card.get("name", "") for card in skip_land_cards(cards) if card.get("name", "") in name_set]

def find_matching_card_names(cards, name_set):
    return [card.get("name", "") for card in cards if card.get("name", "") in name_set]

def preload_all_oracle_tag_sets(tags=["ramp", "removal", "boardwipe", "counterspell", "graveyardhate", "draw", "recursion", "tribal", "win-condition", "land-removal", "lockdown-land", "extra-turn", "tutor"]):
    for tag in tags:
        fetch_tagged_set(tag, "oracletag")

def preload_all_is_sets(tags=["gamechanger"]):
    for tag in tags:
        fetch_tagged_set(tag, "is")

def preload_all_oracle_text_sets(phrases=["destroy all lands"]):
    for phrase in phrases:
        fetch_tagged_set(phrase, "oracle")

def preload_all_combo_lookups():
    fetch_combo_lookup()

def preload_all_cached_data():
    preload_all_oracle_tag_sets()
    preload_all_is_sets()
    preload_all_oracle_text_sets()
    preload_all_combo_lookups()

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
    for card in skip_land_cards(cards):
        cmc = card.get("cmc", 0)
        total_cmc += cmc
        count += 1
    return round(total_cmc / count, 2) if count else 0

def analyze_gamechangers(cards):
    win_condition_cards = fetch_tagged_set('win-condition', 'oracletag')
    gamechanger_names = fetch_tagged_set('gamechanger', 'is')

    # Combine both sets to check against as gamechangers
    all_gamechanger_cards = win_condition_cards | gamechanger_names

    found = find_matching_card_names_skip_lands(cards, all_gamechanger_cards)

    return {
        "gamechanger_count": len(found),
        "gamechanger_cards": found
    }

def analyze_extra_turns(cards):
    extra_turn_cards = fetch_tagged_set('extra-turn', 'oracletag')

    found = find_matching_card_names(cards, extra_turn_cards)

    return {
        "extra_turn_count": len(found),
        "extra_turn_cards": found
    }

def analyze_non_land_tutors(cards):
    tutor_card_names = fetch_tagged_set('tutor', 'oracletag')

    # skip land cards for tutor analysis
    found = find_matching_card_names_skip_lands(cards, tutor_card_names)

    return {
        "tutor_count": len(found),
        "tutor_cards": found
    }

def analyze_mass_land_denial(cards):
    land_removal_card_names_scryfall = fetch_tagged_set('land-removal', 'oracletag')
    lockdown_land_card_names_scryfall = fetch_tagged_set('lockdown-land', 'oracletag')
    destroy_all_land_card_names_scryfall = fetch_tagged_set('destroy all lands', 'oracle')

    # combine all to check against as land denial
    all_land_denial_cards = land_removal_card_names_scryfall | lockdown_land_card_names_scryfall | destroy_all_land_card_names_scryfall

    found = find_matching_card_names_skip_lands(cards, all_land_denial_cards)

    return {
        "land_denial_count": len(found),
        "land_denial_cards": found
    }

def analyze_2_card_combos(cards, deck_list):
    if not deck_list or not cards:
        return {"error": "Deck list or card data missing"}

    deck_card_names = [card.get("name", "").lower() for card in cards]
    commander_name = deck_list[0].strip().lower()
    combo_lookup = fetch_combo_lookup()

    matches = []
    for pair in itertools.combinations(deck_card_names, 2):
        key = frozenset(pair)
        combo = combo_lookup.get(key)

        if combo:
            prerequisites = combo.get("prerequisites", "").lower()

            # Only skip commander-locked combos if they mention a *different* commander than in deck_list
            if "commander" in prerequisites and commander_name not in prerequisites:
                continue  # locked to a different commander

            matches.append(combo)

    return {
        "combo_count": len(matches),
        "combo_details": matches
    }

def analyze_mana_curve_histogram(cards):
    histogram = {}

    # skip land cards for mana curve histogram
    for card in skip_land_cards(cards):
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

    # skip land cards for max CMC calculation
    for card in skip_land_cards(cards):
        converted_mana_cost = card.get("cmc", 0)
        if converted_mana_cost > max_converted_mana_cost:
            max_converted_mana_cost = converted_mana_cost
    return max_converted_mana_cost

# ramp analysis
def analyze_ramp(cards):
    ramp_card_names_scryfall = fetch_tagged_set('ramp', 'oracletag')

    found = find_matching_card_names_skip_lands(cards, ramp_card_names_scryfall)

    return {
        "ramp_count": len(found),
        "ramp_cards": found
    }

# interaction analysis
def analyze_interaction(cards):
    removal_card_names_scryfall = fetch_tagged_set('removal', 'oracletag')
    board_wipe_card_names_scryfall = fetch_tagged_set('boardwipe', 'oracletag')
    counterspell_card_names_scryfall = fetch_tagged_set('counterspell', 'oracletag')
    graveyard_hate_card_names_scryfall = fetch_tagged_set('graveyardhate', 'oracletag')

    interaction_tags = {
        "removal": fetch_tagged_set("removal"),
        "board_wipes": fetch_tagged_set("boardwipe"),
        "counterspells": fetch_tagged_set("counterspell"),
        "graveyard_hate": fetch_tagged_set("graveyardhate"),
    }

    interaction_summary = {k: 0 for k in interaction_tags}
    interaction_summary.update({f"{k}_cards": [] for k in interaction_tags})
    interaction_summary["interaction_cards"] = []

    for card in cards:
        name = card.get("name", "Unknown")
        matched = False
        for tag, name_set in interaction_tags.items():
            if name in name_set:
                interaction_summary[tag] += 1
                interaction_summary[f"{tag}_cards"].append(name)
                matched = True
        if matched:
            interaction_summary["interaction_cards"].append(name)

    return interaction_summary

# card draw analysis
def analyze_card_draw(cards):
    draw_card_names_scryfall = fetch_tagged_set('draw', 'oracletag')
    found = find_matching_card_names(cards, draw_card_names_scryfall)

    return {
        "card_draw_count": len(found),
        "card_draw_cards": found
    }

# tribal synergy analysis
def analyze_tribal_synergy(cards):
    tribal_synergy_card_names_scryfall = fetch_tagged_set('tribal', 'oracletag')

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
    recursion_card_names_scryfall = fetch_tagged_set('recursion', 'oracletag')

    found = find_matching_card_names(cards, recursion_card_names_scryfall)

    return {
        "recursion_count": len(found),
        "recursion_cards": found
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
