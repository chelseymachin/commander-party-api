# Commander Party API 🧙‍♂️

A Flask-based API for analyzing Magic: The Gathering Commander (EDH) decks. This project uses the [Scryfall API](https://scryfall.com/docs/api) to fetch card data and provides a detailed breakdown of a deck’s structure, including ramp, interaction, card draw, recursion, tribal synergy, and commander identity.

Can be hit live at the following url: 'https://commander-party-api-production.up.railway.app'

Try it out in Postman!

---

## 🔧 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/commander-party-api.git
   cd commander-party-api
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask app:**

   ```bash
   flask run
   ```

---

## API Endpoint

### `POST /analyzeDeck`

Analyzes a submitted Commander deck list and returns structured analysis results.

---

### Request Body

Send a JSON object with a `deck` field containing an array of card names.  The first card in the deck NEEDS to be your commander.  This is pretty standard in deck export/imports for commanders as it's pretty hard to determine which individual card COULD be a commander for the deck.

```json
{
  "deck": [
    "YourCommanderHere"
    "Sol Ring",
    "Cultivate",
    "Command Tower",
    "Tatyova, Benthic Druid",
    "Rampant Growth"
  ]
}
```

---

### Response Format

Returns a JSON object with deck breakdown results:

```json
{
    "analysis": [
        {
            "avg_converted_mana_cost": 2.96,
            "card_draw_analysis": {
                "card_draw_cards": [
                    "Anowon, the Ruin Thief",
                    "Court of Cunning",
                    "Dimir Locket",
                    "Fractured Sanity",
                    "Jace's Archivist",
                    "Minds Aglow",
                    "Notion Thief",
                    "Folio of Fancies",
                    "Pilfered Plans",
                    "Teferi's Tutelage",
                    "Whispering Madness",
                    "Windfall"
                ],
                "card_draw_count": 12
            },
            "color_counts": {
                "color_count": {
                    "B": 40,
                    "C": 12,
                    "G": 0,
                    "R": 0,
                    "U": 58,
                    "W": 0
                }
            },
            "commander_analysis": {
                "commander_colors": [
                    "B",
                    "U"
                ],
                "commander_name": "Oona, Queen of the Fae",
                "commander_oracle_text": "Flying\n{X}{U/B}: Choose a color. Target opponent exiles the top X cards of their library. For each card of the chosen color exiled this way, create a 1/1 blue and black Faerie Rogue creature token with flying.",
                "commander_type_line": "Legendary Creature — Faerie Wizard",
                "is_legendary": true
            },
            "interaction_analysis": {
                "board_wipe_cards": [],
                "board_wipes": 0,
                "counterspell_cards": [
                    "Counterspell",
                    "Didn't Say Please",
                    "Drown in the Loch",
                    "Faerie Trickery",
                    "Induce Paranoia",
                    "Psychic Strike",
                    "Thought Collapse"
                ],
                "counterspells": 7,
                "graveyard_hate": 4,
                "graveyard_hate_cards": [
                    "Ashiok, Dream Render",
                    "Crypt Incursion",
                    "Tormod's Crypt",
                    "Vessel of Endless Rest"
                ],
                "interaction_cards": [
                    "Ashiok, Dream Render",
                    "Counterspell",
                    "Crypt Incursion",
                    "Didn't Say Please",
                    "Drown in the Loch",
                    "Faerie Trickery",
                    "Feed the Swarm",
                    "Grisly Spectacle",
                    "Ichthyomorphosis",
                    "Go for the Throat",
                    "Induce Paranoia",
                    "Infernal Grasp",
                    "Murder",
                    "Psychic Strike",
                    "Kasmina's Transmutation",
                    "Tormod's Crypt",
                    "Vessel of Endless Rest",
                    "Witness Protection",
                    "Thought Collapse"
                ],
                "removal": 9,
                "removal_cards": [
                    "Drown in the Loch",
                    "Feed the Swarm",
                    "Grisly Spectacle",
                    "Ichthyomorphosis",
                    "Go for the Throat",
                    "Infernal Grasp",
                    "Murder",
                    "Kasmina's Transmutation",
                    "Witness Protection"
                ]
            },
            "mana_curve_histogram": {
                "0": 1,
                "1": 8,
                "2": 17,
                "3": 25,
                "4": 7,
                "5": 6,
                "6": 2,
                "7+": 2
            },
            "max_converted_mana_cost": 7.0,
            "ramp_analysis": {
                "ramp_cards": [
                    "Arcane Signet",
                    "Charcoal Diamond",
                    "Darksteel Ingot",
                    "Dimir Locket",
                    "Dimir Keyrune",
                    "Dimir Signet",
                    "Sol Ring",
                    "Sky Diamond",
                    "Vessel of Endless Rest",
                    "Zareth San, the Trickster"
                ],
                "ramp_count": 10
            },
            "recursion_analysis": {
                "recursion_cards": [
                    "Codex Shredder",
                    "Halo Forager",
                    "Mystic Sanctuary",
                    "Vessel of Endless Rest",
                    "Zareth San, the Trickster"
                ],
                "recursion_count": 5
            },
            "tribal_synergy_analysis": {
                "matching_synergy_card_count": 5,
                "matching_synergy_cards_for_tribe": [
                    "Anowon, the Ruin Thief",
                    "Oona's Blackguard",
                    "Soaring Thought-Thief",
                    "Zareth San, the Trickster",
                    "Thieves' Guild Enforcer"
                ],
                "most_common_tribe": "Rogue",
                "tribal_synergy_card_count": 7,
                "tribal_synergy_cards": [
                    "Anowon, the Ruin Thief",
                    "Faerie Trickery",
                    "Oona's Blackguard",
                    "Path of Ancestry",
                    "Soaring Thought-Thief",
                    "Zareth San, the Trickster",
                    "Thieves' Guild Enforcer"
                ],
                "tribe_creature_count": 8
            },
            "type_counts": {
                "Artifact": 14,
                "Creature": 23,
                "Enchantment": 9,
                "Instant": 12,
                "Land": 15,
                "Planeswalker": 1,
                "Sorcery": 11
            }
        }
    ]
}
```

---

## Features

- **Ramp Analysis** – Detects ramp cards via Scryfall oracle tags and keyword logic
- **Interaction Breakdown** – Identifies removal, wipes, counterspells, and graveyard hate
- **Card Draw Analysis** – Finds cards that increase hand size or provide draw advantage
- **Tribal Synergy Detection** – Determines common tribes and tribal-supporting cards
- **Recursion Detection** – Analyzes cards that bring permanents/spells back from the graveyard
- **Commander Insight** – Pulls out commander identity, type, text, and colors
- **Mana Curve Metrics** – Calculates average and max mana costs and generates a histogram

---

## Performance

To reduce Scryfall API calls and improve performance:
- Oracle tag datasets (e.g., `ramp`, `removal`, `draw`) are **preloaded and cached** in memory at app startup
- Individual card fetches are **cached in memory** for the duration of the app runtime
- Multithreaded fetching accelerates large deck lookups to avoid waiting for sequential calls

---

## 📂 Project Structure

```
commander-party-api/
│
├── app/
│   ├── __init__.py          # Initializes Flask app
│   ├── routes.py            # Main route handling and POST /analyzeDeck logic
│   └── utils.py             # All analysis and helper functions
│
├── tests/
│   └── test_routes.py       # Basic test coverage
│
├── app.py                   # Entry point (Flask runner)
├── requirements.txt         # Dependencies
├── README.md                # This file :)
```

---

## ✅ To Do

- [ ] Add persistent disk cache for oracle tag data
- [ ] Add Swagger/OpenAPI documentation
- [ ] Improve test coverage for each analysis function
- [ ] Add in Commander bracket determination estimate
- [ ] Add frontend visualization for results

---

## Acknowledgments

- [Scryfall API](https://scryfall.com/docs/api) for the card database and API 