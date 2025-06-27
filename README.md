# Commander Party API 🧙‍♂️

A Flask-based API for analyzing Magic: The Gathering Commander (EDH) decks. This project uses the [Scryfall API](https://scryfall.com/docs/api) and the [Commander Spellbook API](https://github.com/SpaceCowMedia/commander-spellbook-backend) to fetch card data and provides a detailed breakdown of a deck’s structure, including ramp, interaction, card draw, recursion, tribal synergy, and commander identity.

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
            "2_card_combo_analysis": {
                "combo_count": 1,
                "combo_details": [
                    {
                        "cards": [
                            "Bloodchief Ascension",
                            "Mindcrank"
                        ],
                        "description": "Cause one or more opponents to lose life.\nMindcrank triggers once for each life loss event, causing that player to mill cards equal to the amount of life lost.\nBloodchief Ascension triggers once for each card milled, causing that player to lose 2 life and you to gain 2 life for each trigger.\nRepeat from step 2.",
                        "features": [
                            "Infinite mill",
                            "Near-infinite lifegain",
                            "Near-infinite lifegain triggers",
                            "Near-infinite lifeloss"
                        ],
                        "prerequisites": "Three or more quest counters on Bloodchief Ascension.\nYou have a way to make an opponent lose life."
                    }
                ]
            },
            "avg_converted_mana_cost": 2.96,
            "card_draw_analysis": {
                "card_draw_cards": [
                    "Anowon, the Ruin Thief",
                    "Court of Cunning",
                    "Dimir Locket",
                    "Folio of Fancies",
                    "Fractured Sanity",
                    "Jace's Archivist",
                    "Minds Aglow",
                    "Notion Thief",
                    "Pilfered Plans",
                    "Teferi's Tutelage",
                    "Windfall",
                    "Whispering Madness"
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
            "extra_turns_analysis": {
                "extra_turn_cards": [],
                "extra_turn_count": 0
            },
            "gamechanger_analysis": {
                "gamechanger_cards": [
                    "Notion Thief"
                ],
                "gamechanger_count": 1
            },
            "interaction_analysis": {
                "board_wipes": 0,
                "board_wipes_cards": [],
                "counterspells": 7,
                "counterspells_cards": [
                    "Counterspell",
                    "Drown in the Loch",
                    "Didn't Say Please",
                    "Faerie Trickery",
                    "Induce Paranoia",
                    "Psychic Strike",
                    "Thought Collapse"
                ],
                "graveyard_hate": 5,
                "graveyard_hate_cards": [
                    "Bojuka Bog",
                    "Ashiok, Dream Render",
                    "Crypt Incursion",
                    "Tormod's Crypt",
                    "Vessel of Endless Rest"
                ],
                "interaction_cards": [
                    "Bojuka Bog",
                    "Ashiok, Dream Render",
                    "Counterspell",
                    "Crypt Incursion",
                    "Drown in the Loch",
                    "Didn't Say Please",
                    "Faerie Trickery",
                    "Grisly Spectacle",
                    "Go for the Throat",
                    "Feed the Swarm",
                    "Infernal Grasp",
                    "Ichthyomorphosis",
                    "Induce Paranoia",
                    "Murder",
                    "Psychic Strike",
                    "Witness Protection",
                    "Kasmina's Transmutation",
                    "Tormod's Crypt",
                    "Thought Collapse",
                    "Vessel of Endless Rest"
                ],
                "removal": 9,
                "removal_cards": [
                    "Drown in the Loch",
                    "Grisly Spectacle",
                    "Go for the Throat",
                    "Feed the Swarm",
                    "Infernal Grasp",
                    "Ichthyomorphosis",
                    "Murder",
                    "Witness Protection",
                    "Kasmina's Transmutation"
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
            "mass_land_denial_analysis": {
                "land_denial_cards": [],
                "land_denial_count": 0
            },
            "max_converted_mana_cost": 7.0,
            "ramp_analysis": {
                "ramp_cards": [
                    "Arcane Signet",
                    "Charcoal Diamond",
                    "Darksteel Ingot",
                    "Dimir Locket",
                    "Dimir Signet",
                    "Dimir Keyrune",
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
                    "Thieves' Guild Enforcer",
                    "Soaring Thought-Thief",
                    "Zareth San, the Trickster"
                ],
                "most_common_tribe": "Rogue",
                "tribal_synergy_card_count": 7,
                "tribal_synergy_cards": [
                    "Anowon, the Ruin Thief",
                    "Faerie Trickery",
                    "Oona's Blackguard",
                    "Path of Ancestry",
                    "Thieves' Guild Enforcer",
                    "Soaring Thought-Thief",
                    "Zareth San, the Trickster"
                ],
                "tribe_creature_count": 8
            },
            "tutor_analysis": {
                "tutor_cards": [
                    "Dimir Machinations",
                    "Solve the Equation",
                    "Trophy Mage"
                ],
                "tutor_count": 3
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
- [Commander Spellbook API](https://github.com/SpaceCowMedia/commander-spellbook-backend) for the combo reference data set