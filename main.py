import json
import os
from game_generator import generate_initial_state, print_game_state
from best_bucket_first_search import best_bucket_first_search
from mp_best_bucket_first_search import mp_best_bucket_first_search

start_game = 0
total_games = 100
batch_size = 100  # Number of games per file
output_folder = "games_data"  # Name of the main folder to store JSON files

os.makedirs(output_folder, exist_ok=True)

for start_game in range(start_game, total_games, batch_size):
    end_game = min(start_game + batch_size - 1, total_games)
    games_data = []

    for i in range(start_game, end_game + 1):
        print(f"\n\nGame #{i}:\n")
        # print_game_state(generate_initial_state(i))

        best_check, best_path, best_counter, best_total_time = best_bucket_first_search(cap=50000, initial_state=generate_initial_state(i))
        mp_check, mp_path, mp_counter, mp_total_time = mp_best_bucket_first_search(cap=50000, initial_state=generate_initial_state(i))

        game_data = {
            'game_number': i,
            'best_bucket_first_search': {
                'game_won': best_check,
                'path': best_path,
                'counter': best_counter,
                'total_time': best_total_time
            },
            'mp_best_bucket_first_search': {
                'game_won': mp_check,
                'path': mp_path,
                'counter': mp_counter,
                'total_time': mp_total_time
            },
            'game_won': mp_check or best_check
        }
        games_data.append(game_data)

    # Calculate which subfolder the current batch should go into
    subfolder_range_start = ((start_game - 1) // 1000) * 1000
    subfolder_range_end = ((end_game - 1) // 1000) * 1000 + 999  # Adjusted to include 999 games per folder
    subfolder_name = f'games_{subfolder_range_start}-{subfolder_range_end}'
    subfolder_path = os.path.join(output_folder, subfolder_name)
    os.makedirs(subfolder_path, exist_ok=True)

    # Dynamically name the file based on the games played and construct path with subfolder
    filename = os.path.join(subfolder_path, f'games_{start_game}-{end_game}.json')

    with open(filename, 'w') as file:
        json.dump(games_data, file, indent=4)

    print(f"\nFinished processing games {start_game} to {end_game}. Data saved to {filename}.\n")
