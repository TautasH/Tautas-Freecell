import os
import json

my_data_directory = 'my-data/games_data_200.000'
fish_data_file = 'fish-data/Fish_solutions125_executed_paths.json'
looking_glass_directory = 'fc-solve-data/batch_solutions_looking_glass'
video_editing_directory = 'fc-solve-data/batch_solutions_video_editing'

def read_game_data(directory):
    all_games_data = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    try:
                        games_data = json.load(file)
                        if isinstance(games_data, list):
                            all_games_data.extend(games_data)
                        elif isinstance(games_data, dict):
                            all_games_data.append(games_data)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file {filepath}")
    return all_games_data

def read_fish_data(filepath):
    with open(filepath, 'r') as file:
        try:
            games_data = json.load(file)
            if isinstance(games_data, list):
                return games_data
            elif isinstance(games_data, dict):
                return [games_data]
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {filepath}")
    return []

def read_path_data(directory):
    path_data = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    try:
                        games_data = json.load(file)
                        if isinstance(games_data, list):
                            path_data.extend(games_data)
                        elif isinstance(games_data, dict):
                            path_data.append(games_data)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file {filepath}")
    return path_data

def find_min_visited_states(games_data, fish_data, looking_glass_data, video_advanced_data):
    min_states = {
        'best_bucket_first_search': {'gameNo': None, 'states': float('inf')},
        'mp_best_bucket_first_search': {'gameNo': None, 'states': float('inf')},
        'Fish': {'gameNo': None, 'states': float('inf')},
        'Looking_Glass': {'gameNo': None, 'states': float('inf')},
        'Video_Advanced': {'gameNo': None, 'states': float('inf')}
    }

    for game in games_data:
        if isinstance(game, dict):
            for algo_key in ['best_bucket_first_search', 'mp_best_bucket_first_search']:
                if algo_key in game:
                    algo_data = game.get(algo_key, {})
                    if algo_data.get('game_won', False):
                        states = algo_data.get('counter', float('inf'))
                        if states < min_states[algo_key]['states']:
                            min_states[algo_key]['states'] = states
                            min_states[algo_key]['gameNo'] = game.get('game_number', 'Unknown')

    for fish_game in fish_data:
        if isinstance(fish_game, dict):
            executed_steps = fish_game.get('executedSteps', [])
            game_won = fish_game.get('game_won', False)
            states = fish_game.get('counter', float('inf'))
            if game_won and states < min_states['Fish']['states']:
                min_states['Fish']['states'] = states
                min_states['Fish']['gameNo'] = fish_game.get('gameNo', 'Unknown')

    for lg_game in looking_glass_data:
        if isinstance(lg_game, dict):
            game_won = lg_game.get('solvable', False)
            states = int(lg_game.get('states_generated', float('inf')))
            if game_won and states < min_states['Looking_Glass']['states']:
                min_states['Looking_Glass']['states'] = states
                min_states['Looking_Glass']['gameNo'] = lg_game.get('game_number', 'Unknown')

    for va_game in video_advanced_data:
        if isinstance(va_game, dict):
            game_won = va_game.get('solvable', False)
            states = int(va_game.get('states_generated', float('inf')))
            if game_won and states < min_states['Video_Advanced']['states']:
                min_states['Video_Advanced']['states'] = states
                min_states['Video_Advanced']['gameNo'] = va_game.get('game_number', 'Unknown')

    return min_states

def find_max_visited_states(games_data, fish_data, looking_glass_data, video_advanced_data):
    max_states = {
        'best_bucket_first_search': {'gameNo': None, 'states': 0},
        'mp_best_bucket_first_search': {'gameNo': None, 'states': 0},
        'Fish': {'gameNo': None, 'states': 0},
        'Looking_Glass': {'gameNo': None, 'states': 0},
        'Video_Advanced': {'gameNo': None, 'states': 0}
    }

    for game in games_data:
        if isinstance(game, dict):
            for algo_key in ['best_bucket_first_search', 'mp_best_bucket_first_search']:
                if algo_key in game:
                    algo_data = game.get(algo_key, {})
                    if algo_data.get('game_won', False):
                        states = algo_data.get('counter', 0)
                        if states > max_states[algo_key]['states']:
                            max_states[algo_key]['states'] = states
                            max_states[algo_key]['gameNo'] = game.get('game_number', 'Unknown')

    for fish_game in fish_data:
        if isinstance(fish_game, dict):
            executed_steps = fish_game.get('executedSteps', [])
            game_won = fish_game.get('game_won', False)
            states = fish_game.get('counter', 0)
            if game_won and states > max_states['Fish']['states']:
                max_states['Fish']['states'] = states
                max_states['Fish']['gameNo'] = fish_game.get('gameNo', 'Unknown')

    for lg_game in looking_glass_data:
        if isinstance(lg_game, dict):
            game_won = lg_game.get('solvable', False)
            states = int(lg_game.get('states_generated', 0))
            if game_won and states > max_states['Looking_Glass']['states']:
                max_states['Looking_Glass']['states'] = states
                max_states['Looking_Glass']['gameNo'] = lg_game.get('game_number', 'Unknown')

    for va_game in video_advanced_data:
        if isinstance(va_game, dict):
            game_won = va_game.get('solvable', False)
            states = int(va_game.get('states_generated', 0))
            if game_won and states > max_states['Video_Advanced']['states']:
                max_states['Video_Advanced']['states'] = states
                max_states['Video_Advanced']['gameNo'] = va_game.get('game_number', 'Unknown')

    return max_states

def main():
    games_data = read_game_data(my_data_directory)
    fish_data = read_fish_data(fish_data_file)
    looking_glass_data = read_path_data(looking_glass_directory)
    video_editing_data = read_path_data(video_editing_directory)

    min_states = find_min_visited_states(games_data, fish_data, looking_glass_data, video_editing_data)
    max_states = find_max_visited_states(games_data, fish_data, looking_glass_data, video_editing_data)

    print("Games with the minimum amount of generated states:")
    for algo, data in min_states.items():
        print(f"{algo}: Game number {data['gameNo']}, States generated {data['states']}")

    print("\nGames with the maximum amount of generated states:")
    for algo, data in max_states.items():
        print(f"{algo}: Game number {data['gameNo']}, States generated {data['states']}")

if __name__ == "__main__":
    main()
