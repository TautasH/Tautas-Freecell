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

def calculate_statistics(games_data, fish_data, algo_1_data, algo_2_data):
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

    for game in games_data:
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

    print("LookingGlass data before adding to stats:", len(algo_1_data))
    print("VideoEditing data before adding to stats:", len(algo_2_data))
    print("First few LookingGlass entries:", list(algo_1_data.items())[:5])
    print("First few VideoEditing entries:", list(algo_2_data.items())[:5])

    for game_number, (path_length, counter) in algo_1_data.items():
        print(f"Adding LookingGlass path length: game_number={game_number}, path_length={path_length}, counter={counter}")
        stats['LookingGlass']['path_lengths'].append(path_length)
        stats['LookingGlass']['counters'].append(counter)
        stats['LookingGlass']['wins'] += 1

    for game_number, (path_length, counter) in algo_2_data.items():
        print(f"Adding VideoEditing path length: game_number={game_number}, path_length={path_length}, counter={counter}")
        stats['VideoEditing']['path_lengths'].append(path_length)
        stats['VideoEditing']['counters'].append(counter)
        stats['VideoEditing']['wins'] += 1

    print("LookingGlass stats:", stats['LookingGlass'])
    print("VideoEditing stats:", stats['VideoEditing'])

    calculate_averages_and_plot(stats)

def calculate_averages_and_plot(stats):
    averages = {algo: defaultdict(list) for algo in stats.keys()}

    for algo in stats.keys():
        for path_length, counter in zip(stats[algo]['path_lengths'], stats[algo]['counters']):
            print(f"Adding to averages for {algo}: path_length={path_length}, counter={counter}")
            averages[algo][path_length].append(counter)

    print("Averages dictionary after population for LookingGlass:", averages['LookingGlass'])
    print("Averages dictionary after population for VideoEditing:", averages['VideoEditing'])

    avg_stats = {algo: {'path_lengths': [], 'avg_counters': [], 'counts': []} for algo in stats.keys()}

    for algo in averages.keys():
        for path_length in sorted(averages[algo].keys()):
            if averages[algo][path_length]:
                avg_stats[algo]['path_lengths'].append(path_length)
                avg_stats[algo]['avg_counters'].append(sum(averages[algo][path_length]) / len(averages[algo][path_length]))
                avg_stats[algo]['counts'].append(len(averages[algo][path_length]))

    print("avg_stats for LookingGlass:", avg_stats['LookingGlass'])
    print("avg_stats for VideoEditing:", avg_stats['VideoEditing'])

    plot_data(avg_stats, stats)

def plot_algorithm_data(avg_stats, stats, algo, color, filename):
    plt.rcParams.update({
        'font.size': 22,       # General font size
        # 'axes.titlesize': 20,  # Title font size
        'axes.labelsize': 18,  # Axes labels font size
        'xtick.labelsize': 14, # X-axis tick labels font size
        'ytick.labelsize': 14, # Y-axis tick labels font size
        'legend.fontsize': 14  # Legend font size
    })

    fig, ax = plt.subplots(figsize=(10, 7))
    ax2 = ax.twinx()
    ax.plot(avg_stats[algo]['path_lengths'], avg_stats[algo]['avg_counters'], color=color, marker='o', label='Avg States Generated')
    ax2.plot(avg_stats[algo]['path_lengths'], avg_stats[algo]['counts'], color='gray', marker='x', linestyle='--', label='Solution Count')

    # ax.set_title(f"{algo} (Games Won: {stats[algo]['wins']})", pad=30)
    ax.set_xlabel('Solution Length')
    ax.set_ylabel('Average States Generated')
    ax2.set_ylabel('Solution Count')

    #ax.set_xlim(min(avg_stats[algo]['path_lengths']), 160)# max(avg_stats[algo]['path_lengths']))
    #ax.set_ylim(0, 350000)
    #ax2.set_ylim(0, 3000)

    # ax.set_ylim(min(avg_stats[algo]['avg_counters']), max(avg_stats[algo]['avg_counters']))
    # ax2.set_ylim(min(avg_stats[algo]['counts']), max(avg_stats[algo]['counts']))


    ax.grid(True)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

def plot_data(avg_stats, stats):
    algorithms = ['best_bucket_first_search', 'mp_best_bucket_first_search', 'Fish', 'LookingGlass', 'VideoEditing']
    colors = ['blue', 'green', 'red', 'purple', 'orange']

    for algo, color in zip(algorithms, colors):
        plot_algorithm_data(avg_stats, stats, algo, color, f"{algo}_plot.png")

def main():
    bbf_mpbbf_directory = "/home/tautas/IdeaProjects/MasterT/Analysis/my-data/games_data_200.000"
    fish_directory = "/home/tautas/IdeaProjects/MasterT/Analysis/fish-data/Fish_solutions125_executed_paths_NEW.json"
    looking_glass_directory = "/home/tautas/IdeaProjects/MasterT/Analysis/fc-solve-data/batch_solutions_looking_glass"
    video_editing_directory = "/home/tautas/IdeaProjects/MasterT/Analysis/fc-solve-data/batch_solutions_video_editing"

    bbf_mpbbf_data = read_game_data(bbf_mpbbf_directory)
    fish_data = read_fish_data(fish_directory)
    looking_glass_data = read_algo_directory(looking_glass_directory, 'game_number', 'solution_length', 'states_generated')
    video_editing_data = read_algo_directory(video_editing_directory, 'game_number', 'solution_length', 'states_generated')

    print(f"Total games in LookingGlass: {len(looking_glass_data)}")
    print(f"Total games in VideoEditing: {len(video_editing_data)}")

    calculate_statistics(bbf_mpbbf_data, fish_data, looking_glass_data, video_editing_data)

if __name__ == "__main__":
    main()
