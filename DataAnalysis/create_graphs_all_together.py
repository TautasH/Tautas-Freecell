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

    plot_all_algos_single_labels(avg_stats)

def plot_all_algos_single_labels(avg_stats):
    fig, axs = plt.subplots(2, 2, figsize=(12, 12), sharex=True, sharey=True)

    plt.subplots_adjust(wspace=0.05, hspace=0.3)

    algos = ['best_bucket_first_search', 'mp_best_bucket_first_search', 'Fish', 'LookingGlass']
    legend_labels = ['BBF Avg States \nGenerated', 'MP-BBF Avg States\nGenerated', 'Fish Avg States Generated', 'Looking-Glass Avg States\nGenerated']
    solution_count_labels = ['BBF Solution Count', 'MP-BBF Solution Count', 'Fish Solution \nCount', 'Looking-Glass\nSolution Count', 'Video-Editing\nSolution Count']
    colors = ['blue', 'green', 'red', 'purple']

    positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

    x_min, x_max = 60, 180
    y_min, y_max = 0, 350000
    y2_min, y2_max = 0, 3000

    for i, algo in enumerate(algos):
        row, col = positions[i]
        ax = axs[row, col]
        ax.set_facecolor('#f5f5f5')
        ax2 = ax.twinx()
        ax2.set_facecolor('#f5f5f5')

        ax.plot(avg_stats[algo]['path_lengths'], avg_stats[algo]['avg_counters'], color=colors[i], marker='o', label=legend_labels[i])
        ax2.plot(avg_stats[algo]['path_lengths'], avg_stats[algo]['counts'], color='gray', marker='x', linestyle='--', label=solution_count_labels[i])

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax2.set_ylim(y2_min, y2_max)

        if algo in ['best_bucket_first_search', 'Fish']:
            ax2.set_yticklabels([])

        ax.grid(True)

        ax.legend(loc='upper left', fontsize=11, bbox_to_anchor=(0, 1))
        ax2.legend(loc='upper right', fontsize=11, bbox_to_anchor=(1, 1))

    ax = axs[1, 1]
    ax2 = ax.twinx()
    ax.plot(avg_stats['LookingGlass']['path_lengths'], avg_stats['LookingGlass']['avg_counters'], color='purple', marker='o')
    ax2.plot(avg_stats['LookingGlass']['path_lengths'], avg_stats['LookingGlass']['counts'], color='gray', marker='x', linestyle='--', label=solution_count_labels[3])

    ax.plot(avg_stats['VideoEditing']['path_lengths'], avg_stats['VideoEditing']['avg_counters'], color='orange', marker='o', label='Video-Editing Avg States\nGenerated')
    ax2.plot(avg_stats['VideoEditing']['path_lengths'], avg_stats['VideoEditing']['counts'], color='gray', marker='x', linestyle='--', label=solution_count_labels[4])

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax2.set_ylim(y2_min, y2_max)

    ax.legend(loc='upper left', fontsize=11, bbox_to_anchor=(0, 1))
    ax2.legend(loc='upper right', fontsize=11, bbox_to_anchor=(1, 1))

    fig.text(0.5, 0.04, 'Solution Length', ha='center', fontsize=16)
    fig.text(0.04, 0.5, 'Average States Generated', va='center', rotation='vertical', fontsize=16)
    fig.text(0.96, 0.5, 'Solution Count', va='center', rotation='vertical', fontsize=16)

    plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
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

    calculate_statistics(bbf_mpbbf_data, fish_data, looking_glass_data, video_editing_data)

if __name__ == "__main__":
    main()
