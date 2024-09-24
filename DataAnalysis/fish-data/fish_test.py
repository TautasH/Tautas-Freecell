import json

def read_fish_data(filepath):
    try:
        with open(filepath, 'r') as file:
            games_data = json.load(file)
            return games_data
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filepath}")
        return []

def get_statistics(fish_data):
    total_states_visited = 0
    total_states_visited_won = 0
    won_games = 0
    total_games = len(fish_data)

    max_path_length = 0
    max_path_length_game_no = 0
    lost_games = []

    all_game_numbers = set(range(1, 30001))  # Assuming we have games numbered 1 to 30000
    found_game_numbers = set()

    for game in fish_data:
        if isinstance(game, dict):
            game_no = game.get('gameNo')
            if game_no:
                found_game_numbers.add(game_no)

            states_visited = game.get('counter', 0)
            total_states_visited += states_visited
            if game.get('game_won', False):
                total_states_visited_won += states_visited
                won_games += 1
            else:
                lost_games.append(game_no)

            # Calculate path length based on the number of moves
            executed_steps = game.get('executedSteps', [])
            path_length = len(executed_steps)

            if path_length > max_path_length:
                max_path_length = path_length
                max_path_length_game_no = game_no

    # Determine missing game numbers and count them as lost games
    missing_game_numbers = all_game_numbers - found_game_numbers
    lost_games.extend(missing_game_numbers)

    avg_states_visited = total_states_visited / total_games if total_games else 0
    avg_states_visited_won = total_states_visited_won / won_games if won_games else 0

    return {
        "total_states_visited": total_states_visited,
        "total_states_visited_won": total_states_visited_won,
        "avg_states_visited": avg_states_visited,
        "avg_states_visited_won": avg_states_visited_won,
        "won_games": won_games,
        "total_games": total_games,
        "max_path_length": max_path_length,
        "max_path_length_game_no": max_path_length_game_no,
        "lost_games": sorted(lost_games),  # Sorting the lost games
        "number_of_games_with_no_solution": len(lost_games)
    }

def main():
    fish_file = "/home/tautas/IdeaProjects/MasterT/Analysis/fish-data/Fish_solutions125_executed_paths_NEWNEW.json"

    fish_data = read_fish_data(fish_file)

    stats = get_statistics(fish_data)

    # Print the calculated statistics
    print(f"{'Total states visited':<40}{stats['total_states_visited']:<35}")
    print(f"{'States visited (won games)':<40}{stats['total_states_visited_won']:<35}")
    print(f"{'Average states visited':<40}{stats['avg_states_visited']:<35}")
    print(f"{'Average states visited (won games)':<40}{stats['avg_states_visited_won']:<35}")
    print()
    print(f"Max path length (Fish) {stats['max_path_length']}                  Game number: {stats['max_path_length_game_no']}")
    print()
    print(f"Number of games with no solution: {stats['number_of_games_with_no_solution']}")
    if stats['lost_games']:
        print("Games not won in the fish data:")
        print(", ".join(map(str, stats['lost_games'])))
    else:
        print("All games in the fish data were won.")

if __name__ == "__main__":
    main()
