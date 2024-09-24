import json
import os

looking_glass_dir = 'solutions-looking_glass'
video_editing_dir = 'solutions-video-editing'

def load_data_from_directory(directory_path):
    aggregated_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):  # Only consider JSON files
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                aggregated_data.extend(data)
    return aggregated_data

def calculate_metrics(data):
    wins = sum(1 for game in data if game['solvable'])
    total_states_generated = sum(int(game['states_generated']) for game in data)
    states_generated_won = sum(int(game['states_generated']) for game in data if game['solvable'])
    average_states_generated = total_states_generated / len(data) if data else 0
    average_states_generated_won = states_generated_won / wins if wins > 0 else 0

    total_time_taken = sum(game['duration'] for game in data)
    average_time_taken = total_time_taken / len(data) if data else 0

    total_time_taken_won = sum(game['duration'] for game in data if game['solvable'])
    average_time_taken_won = total_time_taken_won / wins if wins > 0 else 0

    average_path_length_won = sum(game['solution_length'] for game in data if game['solvable']) / wins if wins > 0 else 0
    max_path_length = max(game['solution_length'] for game in data)

    return {
        'Wins': wins,
        'Total states generated': total_states_generated,
        'States generated (won games)': states_generated_won,
        'Average states generated': average_states_generated,
        'Average states generated (won games)': average_states_generated_won,
        'Average time taken (seconds) over all games': average_time_taken,
        'Average time taken (seconds) over won games': average_time_taken_won,
        'Average path length (won games)': average_path_length_won,
        'Max path length': max_path_length
    }

def main():
    looking_glass_data = load_data_from_directory(looking_glass_dir)
    video_editing_data = load_data_from_directory(video_editing_dir)

    looking_glass_metrics = calculate_metrics(looking_glass_data)
    video_editing_metrics = calculate_metrics(video_editing_data)

    print("Looking Glass Metrics:")
    for key, value in looking_glass_metrics.items():
        print(f"{key}: {value}")

    print("\nVideo Editing Metrics:")
    for key, value in video_editing_metrics.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
