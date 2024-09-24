import json
import os
from collections import deque
from multiprocessing import Pool, cpu_count
from game_application import generate_all_possible_moves, apply_move


def hash_state(state):
    return (
        tuple(tuple(col) for col in state['tableau']),
        tuple(state['free_cells']),
        tuple((suit, tuple(cards)) for suit, cards in state['foundations'].items())
    )

def bfs_count_states_per_depth(initial_state, max_depth):

    depth_count = {i: 0 for i in range(max_depth + 1)}
    queue = deque([(initial_state, 0)])
    visited = set()

    while queue:
        current_state, depth = queue.popleft()
        current_state_hash = hash_state(current_state)

        if current_state_hash in visited:
            continue

        visited.add(current_state_hash)
        if depth <= max_depth:
            depth_count[depth] += 1

        if depth < max_depth:
            for move in generate_all_possible_moves(current_state):
                new_state = apply_move(current_state, move)
                queue.append((new_state, depth + 1))

    return depth_count

def process_game(game_number, max_depth):
    from game_generator import generate_initial_state

    print(f"Processing game {game_number}")
    initial_state = generate_initial_state(game_number)
    depth_count = bfs_count_states_per_depth(initial_state, max_depth)
    return game_number, depth_count

def calculate_state_counts(start_game, end_game, max_depth):
    num_workers = min(cpu_count(), 3)
    pool = Pool(processes=num_workers)

    results = {}
    game_numbers = list(range(start_game, end_game + 1))
    os.makedirs('state_counts_data', exist_ok=True)

    for i in range(0, len(game_numbers), 100):
        chunk = game_numbers[i:i + 100]
        args = [(game_number, max_depth) for game_number in chunk]

        for game_number, depth_count in pool.starmap(process_game, args):
            results[game_number] = depth_count

        output_file = f"state_counts_data/state_counts_per_depth_{start_game}_{i + 100}.json"
        save_results_to_json(results, output_file)
        results = {}

    pool.close()
    pool.join()

    return results

def save_results_to_json(results, output_file):
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)

def main():
    max_depth = 6
    calculate_state_counts(0, 32000, max_depth)
    print("Processing complete.")

if __name__ == "__main__":
    main()
