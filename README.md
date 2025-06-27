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

Send a JSON object with a `deck` field containing an array of card names.

```json
{
  "deck": [
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
      "type_counts": {
        "Artifact": 10,
        "Creature": 26,
        "Sorcery": 7
      },
      "color_counts": {
        "W": 10,
        "U": 17,
        "B": 0,
        "R": 8,
        "G": 20,
        "C": 1
      },
      "avg_converted_mana_cost": 3.26,
      "mana_curve_histogram": {
        "0": 2,
        "1": 6,
        "2": 12,
        "3": 14,
        "4": 9,
        "5": 6,
        "6": 2,
        "7+": 3
      },
      "max_converted_mana_cost": 9,
      "ramp_analysis": {
        "ramp_count": 10,
        "ramp_cards": [
          "Sol Ring",
          "Arcane Signet",
          "Nature's Lore"
        ]
      },
      "interaction_analysis": {
        "removal": 5,
        "board_wipes": 2,
        "counterspells": 1,
        "graveyard_hate": 0,
        "interaction_cards": [
          "Chaos Warp",
          "Swords to Plowshares"
        ]
      },
      "card_draw_analysis": {
        "card_draw_count": 7,
        "card_draw_cards": [
          "Harmonize",
          "Skullclamp"
        ]
      },
      "tribal_synergy_analysis": {
        "most_common_tribe": "Elf",
        "tribe_card_count": 9,
        "tribal_enablers": [
          "Elvish Archdruid",
          "Sylvan Messenger"
        ]
      },
      "recursion_analysis": {
        "recursion_count": 3,
        "recursion_cards": [
          "Eternal Witness",
          "Sun Titan"
        ]
      },
      "commander_analysis": {
        "commander_name": "Tatyova, Benthic Druid",
        "commander_type_line": "Legendary Creature — Merfolk Druid",
        "commander_colors": ["U", "G"],
        "commander_oracle_text": "Whenever a land enters the battlefield under your control, you gain 1 life and draw a card.",
        "is_legendary": true
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