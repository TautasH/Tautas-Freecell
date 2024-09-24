import os
import json

my_data_directory = '/home/tautas/IdeaProjects/MasterT/Analysis/my-data/games_data_200.000'
fish_data_file = '/home/tautas/IdeaProjects/MasterT/Analysis/fish-data/Fish_solutions125_executed_paths_NEW.json'
looking_glass_directory = '/home/tautas/IdeaProjects/MasterT/Analysis/fc-solve-data/batch_solutions_looking_glass'
video_editing_directory = '/home/tautas/IdeaProjects/MasterT/Analysis/fc-solve-data/batch_solutions_video_editing'

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

def read_path_data(directory):
    path_data = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    games_data = json.load(file)
                    for game in games_data:
                        game_number = game['game_number']
                        path_data[game_number] = game
    return path_data

def find_shortest_and_longest_paths(my_data, fish_data, looking_glass_data, video_advanced_data):
    shortest_bbf = None
    longest_bbf = None
    shortest_mpbbf = None
    longest_mpbbf = None
    shortest_fish = None
    longest_fish = None
    shortest_lg = None
    longest_lg = None
    shortest_va = None
    longest_va = None

    shortest_bbf_len = float('inf')
    longest_bbf_len = 0
    shortest_mpbbf_len = float('inf')
    longest_mpbbf_len = 0
    shortest_fish_len = float('inf')
    longest_fish_len = 0
    shortest_lg_len = float('inf')
    longest_lg_len = 0
    shortest_va_len = float('inf')
    longest_va_len = 0

    for game_number, my_game in my_data.items():
        if game_number in fish_data:
            fish_game = fish_data[game_number]

            my_bbf = my_game.get('best_bucket_first_search', {})
            my_mpbbf = my_game.get('mp_best_bucket_first_search', {})

            if my_game.get('game_won') and my_bbf.get('game_won') and my_mpbbf.get('game_won') and fish_game.get('game_won'):
                fish_path_length = len(fish_game.get('executedSteps', []))
                bbf_path_length = len(my_bbf.get('path', []))
                mp_bbf_path_length = len(my_mpbbf.get('path', []))

                if bbf_path_length < shortest_bbf_len:
                    shortest_bbf_len = bbf_path_length
                    shortest_bbf = (game_number, bbf_path_length)
                if bbf_path_length > longest_bbf_len:
                    longest_bbf_len = bbf_path_length
                    longest_bbf = (game_number, bbf_path_length)

                if mp_bbf_path_length < shortest_mpbbf_len:
                    shortest_mpbbf_len = mp_bbf_path_length
                    shortest_mpbbf = (game_number, mp_bbf_path_length)
                if mp_bbf_path_length > longest_mpbbf_len:
                    longest_mpbbf_len = mp_bbf_path_length
                    longest_mpbbf = (game_number, mp_bbf_path_length)

                if fish_path_length < shortest_fish_len:
                    shortest_fish_len = fish_path_length
                    shortest_fish = (game_number, fish_path_length)
                if fish_path_length > longest_fish_len:
                    longest_fish_len = fish_path_length
                    longest_fish = (game_number, fish_path_length)

        if game_number in looking_glass_data:
            lg_game = looking_glass_data[game_number]

            if lg_game.get('game_won') or lg_game.get('solvable'):
                lg_path_length = lg_game.get('solution_length', 0)
                if lg_path_length < shortest_lg_len:
                    shortest_lg_len = lg_path_length
                    shortest_lg = (game_number, lg_path_length)
                if lg_path_length > longest_lg_len:
                    longest_lg_len = lg_path_length
                    longest_lg = (game_number, lg_path_length)

        if game_number in video_advanced_data:
            va_game = video_advanced_data[game_number]

            if va_game.get('game_won') or va_game.get('solvable'):
                va_path_length = va_game.get('solution_length', 0)
                if va_path_length < shortest_va_len:
                    shortest_va_len = va_path_length
                    shortest_va = (game_number, va_path_length)
                if va_path_length > longest_va_len:
                    longest_va_len = va_path_length
                    longest_va = (game_number, va_path_length)

    return (shortest_bbf, longest_bbf, shortest_mpbbf, longest_mpbbf, shortest_fish, longest_fish, shortest_lg, longest_lg, shortest_va, longest_va)

if __name__ == "__main__":
    my_data = read_my_data(my_data_directory)
    fish_data = read_fish_data(fish_data_file)
    looking_glass_data = read_path_data(looking_glass_directory)
    video_advanced_data = read_path_data(video_editing_directory)

    (shortest_bbf, longest_bbf, shortest_mpbbf, longest_mpbbf, shortest_fish, longest_fish,
     shortest_lg, longest_lg, shortest_va, longest_va) = find_shortest_and_longest_paths(my_data, fish_data, looking_glass_data, video_advanced_data)

    def print_result(name, result):
        if result:
            print(f"{name}: Game number {result[0]}, Path length {result[1]}")
        else:
            print(f"{name}: No valid path found")

    print_result("Shortest BBF path", shortest_bbf)
    print_result("Shortest MP BBF path", shortest_mpbbf)
    print_result("Shortest Fish path", shortest_fish)
    print_result("Shortest Looking Glass path", shortest_lg)
    print_result("Shortest Video Advanced path", shortest_va)
    print("\n")
    print_result("Longest BBF path", longest_bbf)
    print_result("Longest MP BBF path", longest_mpbbf)
    print_result("Longest Fish path", longest_fish)
    print_result("Longest Looking Glass path", longest_lg)
    print_result("Longest Video Advanced path", longest_va)
