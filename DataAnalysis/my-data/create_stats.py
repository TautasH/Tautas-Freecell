import json
import os

def read_game_data(directory):
    all_games_data = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    games_data = json.load(file)
                    all_games_data.extend(games_data)
    return all_games_data

def calculate_statistics(games_data):
    total_games = len(games_data)
    total_wins = sum(1 for game in games_data if game.get('game_won'))
    null_path_game_numbers = []

    print(f"Total games: {total_games}")
    print(f"Games won: {total_wins}\n")

    print(f"{'Statistic':<40} {'Best Bucket First Search':<40} {'MP Best Bucket First Search':<20}")

    stats = {
        'Best Bucket First Search': {'counters': [], 'times': [], 'path_lengths': [], 'wins': 0, 'won_counters': [], 'won_path_lengths': [], 'game_numbers': [], 'won_game_numbers': []},
        'MP Best Bucket First Search': {'counters': [], 'times': [], 'path_lengths': [], 'wins': 0, 'won_counters': [], 'won_path_lengths': [], 'game_numbers': [], 'won_game_numbers': []}
    }

    for game in games_data:
        algo_data_bbf = game.get('best_bucket_first_search', {})
        path_bbf = algo_data_bbf.get('path')
        game_number = game.get('game_number', 'Unknown')
        if algo_data_bbf:
            stats['Best Bucket First Search']['counters'].append(game['best_bucket_first_search'].get('counter', 0))
            stats['Best Bucket First Search']['game_numbers'].append(game_number)
            if path_bbf is not None:
                stats['Best Bucket First Search']['path_lengths'].append(len(game['best_bucket_first_search'].get('path', [])))
            if game['best_bucket_first_search'].get('game_won'):
                stats['Best Bucket First Search']['wins'] += 1
                stats['Best Bucket First Search']['won_counters'].append(game['best_bucket_first_search']['counter'])
                stats['Best Bucket First Search']['won_path_lengths'].append(len(game['best_bucket_first_search'].get('path', [])))
                stats['Best Bucket First Search']['times'].append(game['best_bucket_first_search']['total_time'])
                stats['Best Bucket First Search']['won_game_numbers'].append(game_number)

        algo_data_mpbbf = game.get('mp_best_bucket_first_search', {})
        path_mpbbf = algo_data_mpbbf.get('path')
        if algo_data_mpbbf:
            stats['MP Best Bucket First Search']['counters'].append(game['mp_best_bucket_first_search'].get('counter', 0))
            stats['MP Best Bucket First Search']['game_numbers'].append(game_number)
            if path_mpbbf:
                stats['MP Best Bucket First Search']['path_lengths'].append(len(game['mp_best_bucket_first_search'].get('path', [])))
            if game['mp_best_bucket_first_search'].get('game_won'):
                stats['MP Best Bucket First Search']['wins'] += 1
                stats['MP Best Bucket First Search']['won_counters'].append(game['mp_best_bucket_first_search']['counter'])
                stats['MP Best Bucket First Search']['won_path_lengths'].append(len(game['mp_best_bucket_first_search'].get('path', [])))
                stats['MP Best Bucket First Search']['times'].append(game['mp_best_bucket_first_search']['total_time'])
                stats['MP Best Bucket First Search']['won_game_numbers'].append(game_number)

    print(f"{'Wins':<40} {stats['Best Bucket First Search']['wins']:<40} {stats['MP Best Bucket First Search']['wins']:<20}")
    print(f"{'Total states visited':<40} {sum(stats['Best Bucket First Search']['counters']):<40} {sum(stats['MP Best Bucket First Search']['counters']):<20}")
    print(f"{'States visited (won games)':<40} {sum(stats['Best Bucket First Search']['won_counters']):<40} {sum(stats['MP Best Bucket First Search']['won_counters']):<20}")

    for stat_name, stat_data in [('Average states visited', 'counters'), ('Average states visited (won games)', 'won_counters'), ('Average time taken (seconds)', 'times'), ('Average path length (won games)', 'won_path_lengths')]:
        row = [stat_name] + [
            f"{(sum(data[stat_data]) / len(data[stat_data])):.2f}" if data[stat_data] else "0.00"
            for data in stats.values()
        ]
        print(f"{row[0]:<40} {row[1]:<40} {row[2]:<20}")

    max_path_length_bbf = max(stats['Best Bucket First Search']['path_lengths'], default=0)
    max_path_length_mpbbf = max(stats['MP Best Bucket First Search']['path_lengths'], default=0)

    max_path_game_bbf = 'Unknown'
    if max_path_length_bbf > 0:
        max_path_index_bbf = stats['Best Bucket First Search']['path_lengths'].index(max_path_length_bbf)
        max_path_game_bbf = stats['Best Bucket First Search']['game_numbers'][max_path_index_bbf]

    max_path_game_mpbbf = 'Unknown'
    if max_path_length_mpbbf > 0:
        max_path_index_mpbbf = stats['MP Best Bucket First Search']['path_lengths'].index(max_path_length_mpbbf)
        max_path_game_mpbbf = stats['MP Best Bucket First Search']['game_numbers'][max_path_index_mpbbf]

    for game in games_data:
        if (game.get('best_bucket_first_search') and game['best_bucket_first_search'].get('path') is None and not game['best_bucket_first_search'].get('game_won')) or \
                (game.get('mp_best_bucket_first_search') and game['mp_best_bucket_first_search'].get('path') is None and not game['mp_best_bucket_first_search'].get('game_won')):
            null_path_game_numbers.append(game.get('game_number'))

    null_path_game_numbers.sort()
    print(f"\nNumber of games with no solution: {len(null_path_game_numbers)}")
    print(f"{'Max path length (Best Bucket First Search)':<35} {max_path_length_bbf:<20} Game number: {max_path_game_bbf}")
    print(f"{'Max path length (MP Best Bucket First Search)':<35} {max_path_length_mpbbf:<20} Game number: {max_path_game_mpbbf}")
    if null_path_game_numbers:
        print(f"Games with no solution: {', '.join(map(str, null_path_game_numbers))}")

def main():
    directory = "/home/tautas/IdeaProjects/MasterT/Analysis/my-data/games_data_200.000"
    games_data = read_game_data(directory)
    calculate_statistics(games_data)

if __name__ == "__main__":
    main()
