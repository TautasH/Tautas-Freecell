import json
import os

def read_json_files(directory):
    data = []
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as f:
                data.append(json.load(f))
                filenames.append(filename)
    return data, filenames

def compute_states_until_depth_6(data):
    states_per_game_until_depth_6 = {}

    for entry in data:
        for game_id, depths in entry.items():
            total_states = sum(states for depth, states in depths.items() if int(depth) <= 6)
            states_per_game_until_depth_6[game_id] = total_states

    return states_per_game_until_depth_6

def find_extremes(data):
    states_per_game_until_depth_6 = compute_states_until_depth_6(data)
    sorted_games = sorted(states_per_game_until_depth_6.items(), key=lambda x: x[1])

    lowest = sorted_games[:5]
    highest = sorted_games[-5:]

    return highest, lowest

def main(directory):
    data, filenames = read_json_files(directory)
    if not data:
        print("No JSON files found in the directory.")
        return

    highest, lowest = find_extremes(data)

    print("Games with the highest cumulative number of states until depth 6:")
    for game_id, total_states in highest:
        print(f'Game #{game_id} with {total_states} states')

    print("\nGames with the lowest cumulative number of states until depth 6:")
    for game_id, total_states in lowest:
        print(f'Game #{game_id} with {total_states} states')

if __name__ == "__main__":
    directory = "state-counts-data/all-possible-moves"
    main(directory)
