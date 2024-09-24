import os
import json

directory = "solutions-looking-glass"

def read_json_files(directory):
    all_games_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r') as file:
                    games_data = json.load(file)
                    all_games_data.extend(games_data)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file {filepath}")
    return all_games_data

def print_requested_games(games_data, requested_games):
    game_data_dict = {game['game_number']: game for game in games_data}

    for game_no in requested_games:
        game = game_data_dict.get(game_no)
        if game:
            print(f"Game {game_no}: States generated: {game['states_generated']}")
        else:
            print(f"Game {game_no}: Data not found")

def main():
    requested_games = [285, 617, 657, 829, 1025, 1661, 1734, 2081, 2241, 2563, 2670, 3015, 3130, 3685, 4609, 5157, 5707, 6139, 6381, 6775, 6834, 6918, 7103, 7305, 7477, 8591, 9209, 9784, 9790, 9877]

    all_games_data = read_json_files(directory)
    print_requested_games(all_games_data, requested_games)

if __name__ == "__main__":
    main()
