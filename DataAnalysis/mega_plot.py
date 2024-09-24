import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

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

def read_algo_directory(directory, game_key, length_key, counter_key):
    data = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    try:
                        games_data = json.load(file)
                        if isinstance(games_data, list):
                            for game in games_data:
                                if game.get('solvable', False):
                                    length = game[length_key]
                                    counter = int(game[counter_key])
                                    data[game[game_key]] = (length, counter)
                        elif isinstance(games_data, dict):
                            if games_data.get('solvable', False):
                                length = games_data[length_key]
                                counter = int(games_data[counter_key])
                                data[games_data[game_key]] = (length, counter)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file {filepath}")
    return data

def calculate_statistics(bbf_mpbbf_data, fish_data, looking_glass_data, video_editing_data):
    algorithm_keys = {
        'best_bucket_first_search': 'best_bucket_first_search',
        'mp_best_bucket_first_search': 'mp_best_bucket_first_search',
        'Fish': 'executedSteps',
        'LookingGlass': 'solution_length',
        'VideoEditing': 'solution_length'
    }

    stats = {
        'best_bucket_first_search': {'counters': [], 'path_lengths': [], 'wins': 0},
        'mp_best_bucket_first_search': {'counters': [], 'path_lengths': [], 'wins': 0},
        'Fish': {'counters': [], 'path_lengths': [], 'wins': 0},
        'LookingGlass': {'counters': [], 'path_lengths': [], 'wins': 0},
        'VideoEditing': {'counters': [], 'path_lengths': [], 'wins': 0}
    }

    for game in bbf_mpbbf_data:
        if isinstance(game, dict):
            for algo_key, algo in algorithm_keys.items():
                if algo_key in game:
                    algo_data = game.get(algo_key, {})
                    if algo_data.get('game_won', False):
                        if algo in ['LookingGlass', 'VideoEditing']:
                            path_length = algo_data.get('solution_length', 0)
                            counter = int(algo_data.get('states_generated', 0))
                        else:
                            path_length = len(algo_data.get('path', []))
                            counter = algo_data.get('counter', 0)
                        stats[algo]['counters'].append(counter)
                        stats[algo]['path_lengths'].append(path_length)
                        stats[algo]['wins'] += 1

    for fish_game in fish_data:
        if isinstance(fish_game, dict):
            executed_steps = fish_game.get('executedSteps', [])
            game_won = fish_game.get('game_won', False)
            counter = fish_game.get('counter', 0)
            path_length = len(executed_steps)
            if game_won:
                stats['Fish']['counters'].append(counter)
                stats['Fish']['path_lengths'].append(path_length)
                stats['Fish']['wins'] += 1

    for game_number, (path_length, counter) in looking_glass_data.items():
        stats['LookingGlass']['path_lengths'].append(path_length)
        stats['LookingGlass']['counters'].append(counter)
        stats['LookingGlass']['wins'] += 1

    for game_number, (path_length, counter) in video_editing_data.items():
        stats['VideoEditing']['path_lengths'].append(path_length)
        stats['VideoEditing']['counters'].append(counter)
        stats['VideoEditing']['wins'] += 1

    calculate_averages_and_plot(stats)

def calculate_averages_and_plot(stats):
    averages = {algo: defaultdict(list) for algo in stats.keys()}

    for algo in stats.keys():
        for path_length, counter in zip(stats[algo]['path_lengths'], stats[algo]['counters']):
            averages[algo][path_length].append(counter)


    avg_stats = {algo: {'path_lengths': [], 'avg_counters': [], 'counts': []} for algo in stats.keys()}

    for algo in averages.keys():
        for path_length in sorted(averages[algo].keys()):
            if averages[algo][path_length]:
                avg_stats[algo]['path_lengths'].append(path_length)
                avg_stats[algo]['avg_counters'].append(sum(averages[algo][path_length]) / len(averages[algo][path_length]))
                avg_stats[algo]['counts'].append(len(averages[algo][path_length]))

    plot_data(avg_stats, stats)

def plot_data(avg_stats, stats):
    plt.rcParams.update({
        'font.size': 14,       # General font size
        'axes.titlesize': 18,  # Title font size
        'axes.labelsize': 18,  # Axes labels font size
        'xtick.labelsize': 11, # X-axis tick labels font size
        'ytick.labelsize': 11, # Y-axis tick labels font size
        'legend.fontsize': 14  # Legend font size
    })

    legend_mapping = {
        'best_bucket_first_search': 'BBF',
        'mp_best_bucket_first_search': 'mp-bbf',
        'Fish': 'Fish',
        'LookingGlass': 'LookingGlass',
        'VideoEditing': 'VideoEditing'
    }

    algorithms = ['best_bucket_first_search', 'mp_best_bucket_first_search', 'Fish', 'LookingGlass', 'VideoEditing']
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    markers = ['o', 'x', 's', '^', 'd']

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16), sharex=True)


    for algo, color, marker in zip(algorithms, colors, markers):
        label = f"{legend_mapping[algo]} Avg States Generated"
        ax1.plot(avg_stats[algo]['path_lengths'], avg_stats[algo]['avg_counters'], color=color, marker=marker, label=label)

    # ax1.set_title('Average States generated by Solution Length')
    # ax1.set_xlabel('Solution Length')
    ax1.set_facecolor('#f5f5f5')
    ax1.set_ylabel('Average States Generated')
    ax1.set_xlim(min(min(avg_stats[algo]['path_lengths']) for algo in algorithms), 160)
    ax1.set_ylim(0, 350000)
    ax1.grid(True)
    ax1.legend(loc='upper right')

    ax1.set_xticklabels([])

    for algo, color, marker in zip(algorithms, colors, markers):
        label = f"{legend_mapping[algo]} Solution Count"
        ax2.plot(avg_stats[algo]['path_lengths'], avg_stats[algo]['counts'], color=color, marker=marker, linestyle='--', label=label)

    # ax2.set_title('Solution Counts by Solution Length')
    ax2.set_facecolor('#f5f5f5')
    ax2.set_xlabel('Solution Length')
    ax2.set_ylabel('Solution Count')
    ax2.set_xlim(min(min(avg_stats[algo]['path_lengths']) for algo in algorithms), 180)
    ax2.set_ylim(0, 3000)
    ax2.grid(True)
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()



def main():
    bbf_mpbbf_directory = "/home/tautas/IdeaProjects/MasterT/Analysis/my-data/games_data_200.000"
    fish_directory = "/home/tautas/IdeaProjects/MasterT/Analysis/fish-data/Fish_solutions125_executed_paths_NEW.json"
    looking_glass_directory = "/home/tautas/IdeaProjects/MasterT/Analysis/fc-solve-data/batch_solutions_looking_glass"
    video_editing_directory = "/home/tautas/IdeaProjects/MasterT/Analysis/fc-solve-data/batch_solutions_video_editing"

    bbf_mpbbf_data = read_game_data(bbf_mpbbf_directory)
    fish_data = read_fish_data(fish_directory)
    looking_glass_data = read_algo_directory(looking_glass_directory, 'game_number', 'solution_length', 'states_generated')
    video_editing_data = read_algo_directory(video_editing_directory, 'game_number', 'solution_length', 'states_generated')

    print(f"Total games in Fish: {len(fish_data)}")
    print(f"Total games in Looking-Glass: {len(looking_glass_data)}")
    print(f"Total games in Video-Editing: {len(video_editing_data)}")

    calculate_statistics(bbf_mpbbf_data, fish_data, looking_glass_data, video_editing_data)

if __name__ == "__main__":
    main()
