from flask import Blueprint, request, jsonify
from .utils import *
from concurrent.futures import ThreadPoolExecutor, as_completed

deck_blueprint = Blueprint('deck', __name__)

@deck_blueprint.route('/analyzeDeck', methods=['POST'])
def analyze_deck():
    try:
        data = request.get_json()
        deck_list = data.get('deck', [])

        if not isinstance(deck_list, list):
            return jsonify({'error': 'Deck must be a list of strings'}), 400

        card_names = parse_card_names(deck_list)
        cards_data = []
        results_data = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_name = {executor.submit(fetch_card_data, name): name for name in card_names}
            for future in as_completed(future_to_name):
                cards_data.append(future.result())
        
        results_data.append({
            'type_counts': count_card_types(cards_data), 
            'color_counts': count_colors(cards_data), 
            'avg_converted_mana_cost': analyze_avg_converted_mana_cost(cards_data), 
            'mana_curve_histogram': analyze_mana_curve_histogram(cards_data), 
            'max_converted_mana_cost': analyze_max_converted_mana_cost(cards_data),
            'ramp_analysis': analyze_ramp(cards_data),
            'interaction_analysis': analyze_interaction(cards_data),
            'card_draw_analysis': analyze_card_draw(cards_data),
            'tribal_synergy_analysis': analyze_tribal_synergy(cards_data),
            'recursion_analysis': analyze_recursion(cards_data),
            'commander_analysis': analyze_commander(cards_data, card_names),
            'gamechanger_analysis': analyze_gamechangers(cards_data),
            'mass_land_denial_analysis': analyze_mass_land_denial(cards_data),
            '2_card_combo_analysis': analyze_2_card_combos(cards_data, card_names),
            'extra_turns_analysis': analyze_extra_turns(cards_data),
            'tutor_analysis': analyze_non_land_tutors(cards_data)
            })

        return jsonify({'analysis': results_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500