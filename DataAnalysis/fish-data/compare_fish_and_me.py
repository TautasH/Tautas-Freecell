import os
import json


my_data_directory = '/home/tautas/IdeaProjects/MasterT/Analysis/my-data/games_data_200.000'
fish_data_file = '/home/tautas/IdeaProjects/MasterT/Analysis/fish-data/Fish_solutions125_executed_paths_NEW.json'

def read_my_data(directory):
    all_games_data = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    games_data = json.load(file)
                    for game in games_data:
                        game_number = game['game_number']
                        all_games_data[game_number] = game
    return all_games_data

def read_fish_data(filepath):
    with open(filepath, 'r') as file:
        games_data = json.load(file)
    return {game['gameNo']: game for game in games_data}

def compare_data(my_data, fish_data):
    total_my_bbf_path_length = 0
    total_fish_path_length = 0
    total_my_bbf_counter = 0
    total_fish_counter = 0
    total_my_mpbbf_path_length = 0
    total_my_mpbbf_counter = 0
    count = 0

    for game_number, my_game in my_data.items():
        if game_number in fish_data:
            fish_game = fish_data[game_number]
            my_bbf = my_game.get('best_bucket_first_search', {})
            my_mpbbf = my_game.get('mp_best_bucket_first_search', {})

            if my_game.get('game_won') and my_bbf.get('game_won') and my_mpbbf.get('game_won') and fish_game.get('game_won'):
                total_my_bbf_path_length += len(my_bbf.get('path', []))
                total_fish_path_length += len(fish_game.get('executedSteps', []))
                total_my_bbf_counter += my_bbf.get('counter', 0)
                total_fish_counter += fish_game.get('counter', 0)
                total_my_mpbbf_path_length += len(my_mpbbf.get('path', []))
                total_my_mpbbf_counter += my_mpbbf.get('counter', 0)
                count += 1

    averages = {
        'average_my_bbf_path_length': total_my_bbf_path_length / count if count > 0 else 0,
        'average_fish_path_length': total_fish_path_length / count if count > 0 else 0,
        'average_my_bbf_counter': total_my_bbf_counter / count if count > 0 else 0,
        'average_fish_counter': total_fish_counter / count if count > 0 else 0,
        'average_my_mpbbf_path_length': total_my_mpbbf_path_length / count if count > 0 else 0,
        'average_my_mpbbf_counter': total_my_mpbbf_counter / count if count > 0 else 0
    }

    return averages, count


if __name__ == "__main__":
    my_data = read_my_data(my_data_directory)
    fish_data = read_fish_data(fish_data_file)

    averages, count = compare_data(my_data, fish_data)

    print(f"Averages for games won by all three methods (over {count} games):")
    for key, value in averages.items():
        print(f"{key}: {value:.2f}")
