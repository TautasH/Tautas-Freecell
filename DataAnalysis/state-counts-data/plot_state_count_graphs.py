import json
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def read_json_files(directory):
    data = []
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as f:
                data.append(json.load(f))
                filenames.append(filename)
    return data, filenames

def compute_averages(data):
    combined_data = {}
    count = 0

    for entry in data:
        count += len(entry)
        for game_id, depths in entry.items():
            for depth, state_count in depths.items():
                if depth not in combined_data:
                    combined_data[depth] = 0
                combined_data[depth] += state_count

    averages = {depth: state_count / count for depth, state_count in combined_data.items()}
    return averages

def find_extremes(data, filenames):
    max_depth_values = []
    for game_data, filename in zip(data, filenames):
        for game_id, depths in game_data.items():
            if '6' in depths:
                max_depth = 6
                max_value = depths[str(max_depth)]
                max_depth_values.append((filename, max_value, max_depth, game_id))

    if max_depth_values:
        max_depth_values = sorted(max_depth_values, key=lambda x: x[1])
        lowest = max_depth_values[0]
        highest = max_depth_values[-1]
    else:
        lowest = highest = (None, 0, 0, 0)  # Default values if no valid data

    return highest, lowest

def plot_averages(averages, estimate_at_60):
    keys = list(map(int, averages.keys()))
    values = list(averages.values())

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.set_facecolor('#f5f5f5')
    ax.plot(keys, values, marker='o', linestyle='-', color='skyblue', label='Average Amount of States')
    ax.set_xlabel('Depth', fontsize=12)
    ax.set_ylabel('Average Amount of States', fontsize=12)
    ax.set_yscale('log')
    # ax.set_title('Average Amount of States per Depth (Logarithmic Scale)')

    log_values = np.log(values)
    slope, intercept, r_value, p_value, std_err = linregress(keys, log_values)
    fit_line = [np.exp(slope * x + intercept) for x in keys]
    ax.plot(keys, fit_line, color='red', label=f'Fitted Line\ny = exp({slope:.4f}x + {intercept:.4f})')

    estimate_at_60_text = f'{estimate_at_60:.2e}'
    ax.text(50, max(values) * 0.5, f'Estimate at depth 60: {estimate_at_60_text}', fontsize=10, color='red')

    table_data = [[k, f'{v:.2f}'] for k, v in zip(keys, values)]
    col_labels = ['Depth', 'Average Amount of States']
    table = plt.table(cellText=table_data, colLabels=col_labels, cellLoc='center', loc='upper left', bbox=[0.59, 0.02, 0.4, 0.35])
    table.scale(1, 1.5)
    table.auto_set_font_size(False)
    table.set_fontsize(11)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
    ax.legend(loc='upper left', fontsize=14)
    plt.show()

def main(directory):
    data, filenames = read_json_files(directory)
    if not data:
        print("No JSON files found in the directory.")
        return
    averages = compute_averages(data)
    highest, lowest = find_extremes(data, filenames)

    if highest[0] and lowest[0]:
        print(f'Game with highest number at depth 6: in {highest[0]} game #{highest[3]} with {highest[1]}')
        print(f'Game with lowest number at depth 6: in {lowest[0]} game #{lowest[3]} with {lowest[1]}')
    else:
        print("No valid data found for depth 6 calculations.")

    keys = list(map(int, averages.keys()))
    values = list(averages.values())
    log_values = np.log(values)
    slope, intercept, r_value, p_value, std_err = linregress(keys, log_values)
    estimate_at_60 = np.exp(slope * 60 + intercept)

    print(f'Estimated amount of states at depth 60: {estimate_at_60:.2e}')

    plot_averages(averages, estimate_at_60)

if __name__ == "__main__":
    directory = "state-counts-data/foundation-first"
    main(directory)
