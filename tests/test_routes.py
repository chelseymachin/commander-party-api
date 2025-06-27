import json
from app import create_app

def test_analyze_deck_valid(monkeypatch):
    app = create_app()
    client = app.test_client()

    # Mock the fetch_card_data function to avoid actual API calls
    def mock_fetch_card_data(name):
        return {'name': name, 'mocked': True}

    monkeypatch.setattr("app.routes.fetch_card_data", mock_fetch_card_data)

    payload = {
        "deck": ["Ajani's Pridemate", "Island"]
    }

    response = client.post('/analyzeDeck',
                           data=json.dumps(payload),
                           content_type='application/json')

    assert response.status_code == 200
    data = response.get_json()
    assert len(data['cards']) == 2
    assert all(card.get('mocked') for card in data['cards'])

def test_analyze_deck_with_invalid_input():
    app = create_app()
    client = app.test_client()

    response = client.post('/analyzeDeck',
                           data=json.dumps({"deck": "notalist"}),
                           content_type='application/json')

    assert response.status_code == 400