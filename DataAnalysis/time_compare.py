import os
import json

path_bbf_mpbbf = 'my-data/games_data_200.000'
path_fish = 'fish-data/Fish_solutions125_executed_paths.json'
path_looking_glass = 'fc-solve-data/batch_solutions_looking_glass'
path_video_editing = 'fc-solve-data/batch_solutions_video_editing'

total_times_including_lost = {'BBF': 0.0, 'MP-BBF': 0.0, 'Fish': 0.0, 'Looking-Glass': 0.0, 'Video-Editing': 0.0}
total_times_excluding_lost = {'BBF': 0.0, 'MP-BBF': 0.0, 'Fish': 0.0, 'Looking-Glass': 0.0, 'Video-Editing': 0.0}
total_games_including_lost = {'BBF': 0, 'MP-BBF': 0, 'Fish': 0, 'Looking-Glass': 0, 'Video-Editing': 0}
total_games_excluding_lost = {'BBF': 0, 'MP-BBF': 0, 'Fish': 0, 'Looking-Glass': 0, 'Video-Editing': 0}


def read_algo_data(directory):
    data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    for item in json_data:
                        data[item['game_number']] = {
                            'duration': item.get('duration', 0.0),
                            'solvable': item['solvable']
                        }
    return data


def read_fish_data(file_path):
    data = {}
    with open(file_path, 'r') as f:
        json_data = json.load(f)
        for item in json_data:
            data[item['gameNo']] = {
                'duration': item.get('time', 0.0),
                'solvable': item.get('game_won', False)
            }
    return data


looking_glass_data = read_algo_data(path_looking_glass)
video_editing_data = read_algo_data(path_video_editing)
fish_data = read_fish_data(path_fish)

def read_bbf_mpbbf_data(directory):
    bbf_data = {}
    mpbbf_data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    for item in json_data:
                        game_number = item['game_number']
                        bbf_data[game_number] = {
                            'duration': item['best_bucket_first_search'].get('total_time', 0.0),
                            'solvable': item['best_bucket_first_search'].get('game_won', False)
                        }
                        mpbbf_data[game_number] = {
                            'duration': item['mp_best_bucket_first_search'].get('total_time', 0.0),
                            'solvable': item['mp_best_bucket_first_search'].get('game_won', False)
                        }
    return bbf_data, mpbbf_data


bbf_data, mpbbf_data = read_bbf_mpbbf_data(path_bbf_mpbbf)

for game_number in range(1, 32001):
    # BBF
    if game_number in bbf_data:
        total_times_including_lost['BBF'] += bbf_data[game_number]['duration']
        total_games_including_lost['BBF'] += 1
        if bbf_data[game_number]['solvable']:
            total_times_excluding_lost['BBF'] += bbf_data[game_number]['duration']
            total_games_excluding_lost['BBF'] += 1
    # MP-BBF
    if game_number in mpbbf_data:
        total_times_including_lost['MP-BBF'] += mpbbf_data[game_number]['duration']
        total_games_including_lost['MP-BBF'] += 1
        if mpbbf_data[game_number]['solvable']:
            total_times_excluding_lost['MP-BBF'] += mpbbf_data[game_number]['duration']
            total_games_excluding_lost['MP-BBF'] += 1
    # Fish
    if game_number in fish_data:
        total_times_including_lost['Fish'] += fish_data[game_number]['duration']
        total_games_including_lost['Fish'] += 1
        if fish_data[game_number]['solvable']:
            total_times_excluding_lost['Fish'] += fish_data[game_number]['duration']
            total_games_excluding_lost['Fish'] += 1
    # Looking-Glass
    if game_number in looking_glass_data:
        total_times_including_lost['Looking-Glass'] += looking_glass_data[game_number]['duration']
        total_games_including_lost['Looking-Glass'] += 1
        if looking_glass_data[game_number]['solvable']:
            total_times_excluding_lost['Looking-Glass'] += looking_glass_data[game_number]['duration']
            total_games_excluding_lost['Looking-Glass'] += 1
    # Video-Editing
    if game_number in video_editing_data:
        total_times_including_lost['Video-Editing'] += video_editing_data[game_number]['duration']
        total_games_including_lost['Video-Editing'] += 1
        if video_editing_data[game_number]['solvable']:
            total_times_excluding_lost['Video-Editing'] += video_editing_data[game_number]['duration']
            total_games_excluding_lost['Video-Editing'] += 1

print(
    f"Total time for BBF (Best Bucket First Search) including lost games: {total_times_including_lost['BBF']:.6f} seconds, for {total_games_including_lost['BBF']} games")
print(
    f"Total time for BBF (Best Bucket First Search) excluding lost games: {total_times_excluding_lost['BBF']:.6f} seconds, for {total_games_excluding_lost['BBF']} games")

print(
    f"Total time for MP-BBF (Moves Penalized Best Bucket First Search) including lost games: {total_times_including_lost['MP-BBF']:.6f} seconds, for {total_games_including_lost['MP-BBF']} games")
print(
    f"Total time for MP-BBF (Moves Penalized Best Bucket First Search) excluding lost games: {total_times_excluding_lost['MP-BBF']:.6f} seconds, for {total_games_excluding_lost['MP-BBF']} games")

print(
    f"Total time for Fish algorithm including lost games: {total_times_including_lost['Fish']:.6f} seconds, for {total_games_including_lost['Fish']} games")
print(
    f"Total time for Fish algorithm excluding lost games: {total_times_excluding_lost['Fish']:.6f} seconds, for {total_games_excluding_lost['Fish']} games")

print(
    f"Total time for Looking-Glass algorithm including lost games: {total_times_including_lost['Looking-Glass']:.6f} seconds, for {total_games_including_lost['Looking-Glass']} games")
print(
    f"Total time for Looking-Glass algorithm excluding lost games: {total_times_excluding_lost['Looking-Glass']:.6f} seconds, for {total_games_excluding_lost['Looking-Glass']} games")

print(
    f"Total time for Video-Editing algorithm including lost games: {total_times_including_lost['Video-Editing']:.6f} seconds, for {total_games_including_lost['Video-Editing']} games")
print(
    f"Total time for Video-Editing algorithm excluding lost games: {total_times_excluding_lost['Video-Editing']:.6f} seconds, for {total_games_excluding_lost['Video-Editing']} games")

print(
    f"\nTotal number of games considered across all algorithms: {min(total_games_including_lost['BBF'], total_games_including_lost['MP-BBF'], total_games_including_lost['Fish'], total_games_including_lost['Looking-Glass'], total_games_including_lost['Video-Editing'])}")
