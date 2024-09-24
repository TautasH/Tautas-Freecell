import os
import json

my_data_directory = '/home/tautas/IdeaProjects/MasterT/Analysis/my-data/games_data_200.000'
fish_data_file = '/home/tautas/IdeaProjects/MasterT/Analysis/fish-data/Fish_solutions125_executed_paths_NEW.json'
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

def read_video_editing_data(directory):
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

def count_shorter_paths(my_data, fish_data, video_advanced_data):
    bbf_shorter_than_fish_count = 0
    mp_bbf_shorter_than_fish_count = 0
    either_shorter_than_fish_count = 0
    total_fish_comparisons = 0

    bbf_shorter_than_video_count = 0
    mp_bbf_shorter_than_video_count = 0
    either_shorter_than_video_count = 0
    total_video_comparisons = 0

    for game_number, my_game in my_data.items():
        fish_game = fish_data.get(game_number)
        video_game = video_advanced_data.get(game_number)

        if fish_game:
            my_bbf = my_game.get('best_bucket_first_search', {})
            my_mpbbf = my_game.get('mp_best_bucket_first_search', {})

            # Check if all three methods won the game
            if my_game.get('game_won') and my_bbf.get('game_won') and my_mpbbf.get('game_won') and fish_game.get('game_won'):
                fish_path_length = len(fish_game.get('executedSteps', []))
                bbf_path_length = len(my_bbf.get('path', []))
                mp_bbf_path_length = len(my_mpbbf.get('path', []))

                total_fish_comparisons += 1

                if bbf_path_length < fish_path_length:
                    bbf_shorter_than_fish_count += 1
                if mp_bbf_path_length < fish_path_length:
                    mp_bbf_shorter_than_fish_count += 1
                if bbf_path_length < fish_path_length or mp_bbf_path_length < fish_path_length:
                    either_shorter_than_fish_count += 1

        if video_game:
            my_bbf = my_game.get('best_bucket_first_search', {})
            my_mpbbf = my_game.get('mp_best_bucket_first_search', {})

            # Check if all three methods won the game
            if my_game.get('game_won') and my_bbf.get('game_won') and my_mpbbf.get('game_won') and video_game.get('solvable'):
                video_path_length = video_game.get('solution_length', float('inf'))
                bbf_path_length = len(my_bbf.get('path', []))
                mp_bbf_path_length = len(my_mpbbf.get('path', []))

                total_video_comparisons += 1

                if bbf_path_length < video_path_length:
                    bbf_shorter_than_video_count += 1
                if mp_bbf_path_length < video_path_length:
                    mp_bbf_shorter_than_video_count += 1
                if bbf_path_length < video_path_length or mp_bbf_path_length < video_path_length:
                    either_shorter_than_video_count += 1

    return (bbf_shorter_than_fish_count, mp_bbf_shorter_than_fish_count, either_shorter_than_fish_count,
            bbf_shorter_than_video_count, mp_bbf_shorter_than_video_count, either_shorter_than_video_count,
            total_fish_comparisons, total_video_comparisons)

if __name__ == "__main__":
    my_data = read_my_data(my_data_directory)
    fish_data = read_fish_data(fish_data_file)
    video_advanced_data = read_video_editing_data(video_editing_directory)

    (bbf_shorter_than_fish_count, mp_bbf_shorter_than_fish_count, either_shorter_than_fish_count,
     bbf_shorter_than_video_count, mp_bbf_shorter_than_video_count, either_shorter_than_video_count,
     total_fish_comparisons, total_video_comparisons) = count_shorter_paths(my_data, fish_data, video_advanced_data)

    print(f"{total_fish_comparisons} games were compared:")
    print(f"Number of times BBF path is shorter than Fish path: {bbf_shorter_than_fish_count}")
    print(f"Number of times MP BBF path is shorter than Fish path: {mp_bbf_shorter_than_fish_count}")
    print(f"Number of times either BBF or MP BBF path is shorter than Fish path: {either_shorter_than_fish_count}")

    print(f"{total_video_comparisons} games were compared:")
    print(f"Number of times BBF path is shorter than Video Advanced path: {bbf_shorter_than_video_count}")
    print(f"Number of times MP BBF path is shorter than Video Advanced path: {mp_bbf_shorter_than_video_count}")
    print(f"Number of times either BBF or MP BBF path is shorter than Video Advanced path: {either_shorter_than_video_count}")
