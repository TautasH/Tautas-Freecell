import os
import json

def read_game_results(directory):
    bbf_results = []
    mp_bbf_results = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    try:
                        games_data = json.load(file)
                        if isinstance(games_data, list):
                            for game in games_data:
                                if 'best_bucket_first_search' in game:
                                    bbf_data = game['best_bucket_first_search']
                                    if bbf_data.get('game_won', False):
                                        game_number = game.get('game_number')
                                        counter = bbf_data.get('counter', 0)
                                        bbf_results.append({
                                            'game_number': game_number,
                                            'counter': counter
                                        })
                                if 'mp_best_bucket_first_search' in game:
                                    mp_bbf_data = game['mp_best_bucket_first_search']
                                    if mp_bbf_data.get('game_won', False):
                                        game_number = game.get('game_number')
                                        counter = mp_bbf_data.get('counter', 0)
                                        mp_bbf_results.append({
                                            'game_number': game_number,
                                            'counter': counter
                                        })
                        elif isinstance(games_data, dict):
                            if 'best_bucket_first_search' in games_data:
                                bbf_data = games_data['best_bucket_first_search']
                                if bbf_data.get('game_won', False):
                                    game_number = games_data.get('game_number')
                                    counter = bbf_data.get('counter', 0)
                                    bbf_results.append({
                                        'game_number': game_number,
                                        'counter': counter
                                    })
                            if 'mp_best_bucket_first_search' in games_data:
                                mp_bbf_data = games_data['mp_best_bucket_first_search']
                                if mp_bbf_data.get('game_won', False):
                                    game_number = games_data.get('game_number')
                                    counter = mp_bbf_data.get('counter', 0)
                                    mp_bbf_results.append({
                                        'game_number': game_number,
                                        'counter': counter
                                    })
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file {filepath}")

    return bbf_results, mp_bbf_results

def main():
    directory = "my-data/games_data_200.000"
    bbf_results, mp_bbf_results = read_game_results(directory)

    specific_games = [285, 617, 657, 829, 1025, 1661, 1734, 2081, 2241, 2563, 2670, 3015, 3130, 3685, 4609, 5157, 5707, 6139, 6381, 6775, 6834, 6918, 7103, 7305, 7477, 8591, 9209, 9784, 9790, 9877]
    print(f"Total games with Best Bucket First Search results: {len(bbf_results)}")
    print(f"Total games with MP Best Bucket First Search results: {len(mp_bbf_results)}\n")

    for game_number in specific_games:
        bbf_result = next((result for result in bbf_results if result['game_number'] == game_number), None)
        mp_bbf_result = next((result for result in mp_bbf_results if result['game_number'] == game_number), None)

        if bbf_result:
            print(f"Game #{game_number} (BBF): Counter = {bbf_result['counter']}")
        else:
            print(f"Game #{game_number} not found or was not won using Best Bucket First Search.")

        if mp_bbf_result:
            print(f"Game #{game_number} (MP BBF): Counter = {mp_bbf_result['counter']}")
        else:
            print(f"Game #{game_number} not found or was not won using MP Best Bucket First Search.")

        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()
