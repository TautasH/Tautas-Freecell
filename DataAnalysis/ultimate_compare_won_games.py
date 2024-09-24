import os
import json

looking_glass_path = 'fc-solve-data/batch_solutions_looking_glass'
video_editing_path = 'fc-solve-data/batch_solutions_video_editing'
fish_path = 'fish-data/Fish_solutions125_executed_paths_NEW.json'
bbf_mpbbf_path = 'my-data/games_data_200.000'

shortest_path_count_unique = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
shortest_path_count_total = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
path_lengths = {1: [], 2: [], 3: [], 4: [], 5: []}

def read_algo_data(directory):
    data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    for item in json_data:
                        if item['solvable']:
                            data[item['game_number']] = item['solution_length']
    return data

looking_glass_data = read_algo_data(looking_glass_path)
video_editing_data = read_algo_data(video_editing_path)

def read_fish_data(file_path):
    data = {}
    with open(file_path, 'r') as f:
        json_data = json.load(f)
        for item in json_data:
            if item['game_won']:
                game_number = item['gameNo']
                data[game_number] = len(item['executedSteps'])
    return data

fish_data = read_fish_data(fish_path)

def read_bbf_mpbbf_data(directory):
    data_bbf = {}
    data_mpbbf = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    for item in json_data:
                        game_number = item['game_number']
                        if item['best_bucket_first_search']['game_won']:
                            data_bbf[game_number] = len(item['best_bucket_first_search']['path'])
                        if item['mp_best_bucket_first_search']['game_won']:
                            data_mpbbf[game_number] = len(item['mp_best_bucket_first_search']['path'])
    return data_bbf, data_mpbbf

bbf_data, mpbbf_data = read_bbf_mpbbf_data(bbf_mpbbf_path)

considered_games = []

for game_number in range(1, 32001):
    if all(game_number in data for data in [looking_glass_data, video_editing_data, fish_data]) and game_number in bbf_data and game_number in mpbbf_data:
        lengths = {
            1: looking_glass_data[game_number],
            2: video_editing_data[game_number],
            3: fish_data[game_number],
            4: bbf_data[game_number],
            5: mpbbf_data[game_number]
        }
        shortest_length = min(lengths.values())
        shortest_algorithms = [algo for algo, length in lengths.items() if length == shortest_length]

        for algo, length in lengths.items():
            path_lengths[algo].append(length)

        considered_games.append(game_number)

        if len(shortest_algorithms) == 1:
            shortest_path_count_unique[shortest_algorithms[0]] += 1

        for algo in shortest_algorithms:
            shortest_path_count_total[algo] += 1

average_path_lengths = {algo: (sum(lengths) / len(lengths) if lengths else float('inf'), len(lengths)) for algo, lengths in path_lengths.items()}


print("Unique shortest paths:")
for algo, count in shortest_path_count_unique.items():
    print(f"Algorithm {algo} had the shortest unique path {count} times.")

print("\nTotal shortest paths (including ties):")
for algo, count in shortest_path_count_total.items():
    print(f"Algorithm {algo} had the shortest path {count} times (including ties).")

print(f"\nTotal number of games considered: {len(considered_games)}")

print("\nAverage path lengths over all won games:")
for algo, (average_length, num_games) in average_path_lengths.items():
    print(f"Algorithm {algo}: Average path length = {average_length}, Number of games = {num_games}")
