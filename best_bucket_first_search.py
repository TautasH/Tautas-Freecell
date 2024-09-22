from time import time

def is_goal_state(state):
    for suit, stack in state['foundations'].items():
        if len(stack) != 13:
            return False
        expected_order = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        if [card[0] for card in stack] != expected_order:
            return False
    return True


def initialize_buckets(num_buckets=53):
    return [[] for _ in range(num_buckets)]


def hash_state(state):
    # Convert tableau to string representation
    tableau_hash = '|'.join([' '.join(column) for column in state['tableau']])

    # Convert free_cells to string representation
    free_cells_hash = ' '.join([cell if cell is not None else 'None' for cell in state['free_cells']])

    # Convert foundations to string representation
    foundations_hash = '|'.join(
        [suit + ':' + ' '.join(cards) for suit, cards in sorted(state['foundations'].items())])

    return (tableau_hash, free_cells_hash, foundations_hash)


def hFunction(state):
    # Simple heuristic: Count cards not in foundations.
    return sum(13 - len(stack) for stack in state['foundations'].values())


def best_bucket_first_search(cap=5000, initial_state=None):
    from game_application import generate_possible_moves, apply_move, reconstruct_path
    if initial_state is None:
        raise ValueError("No initial state provided. The program will be interrupted.")
    time_a = time()
    buckets = initialize_buckets()
    initial_hash = hash_state(initial_state)
    states_checked = set()
    states = {initial_hash: initial_state}  # Store states by their hash
    parentAndPathDict = {initial_hash: (None, None)}
    current_state_hash = initial_hash

    initial_score = hFunction(initial_state)
    buckets[initial_score].append(initial_hash)  # Add the hash instead of the state

    counter = 0

    while any(buckets) and counter < cap:
        for score, bucket in enumerate(buckets):
            if bucket:
                current_state_hash = bucket.pop(0)  # Pop a state's hash
                current_state = states[current_state_hash]  # Retrieve the state using its hash
                break
        else:
            print("No more states to expand.")
            return None, None, counter, 0

        if current_state_hash in states_checked:
            continue
        states_checked.add(current_state_hash)

        counter += 1
        print(f"\rStates visited: {counter}, Current Score: {score}, Dic size: {len(parentAndPathDict)}", end="")

        if is_goal_state(current_state):
            total_time = time() - time_a
            path = reconstruct_path(parentAndPathDict, current_state_hash)
            return True, path, counter, total_time

        for move in generate_possible_moves(current_state):
            new_state = apply_move(current_state, move)
            new_state_hash = hash_state(new_state)
            if new_state_hash not in states_checked:
                states[new_state_hash] = new_state
                new_score = hFunction(new_state)
                buckets[new_score].append(new_state_hash)
                parentAndPathDict[new_state_hash] = (move, current_state_hash)

    if counter >= cap:
        total_time = time() - time_a
        path = reconstruct_path(parentAndPathDict, current_state_hash)
        return None, path, cap, total_time
    else:
        print("\nSearch ended without finding a goal state.")
        return None, None, counter, 0



if __name__ == "__main__":
    from game_generator import generate_initial_state
    from time import time

    win_count = 0
    total_path_length = 0
    total_runs = 1000

    start = time()
    for game_no in range(1, total_runs + 1):
        init_state = generate_initial_state(game_no)

        check, path, counter, total_time = best_bucket_first_search(initial_state=init_state, cap=200000)

        if check is not None:
            print(f"\nGoal reached for game {game_no} after visiting {counter} states in {total_time:.2f} seconds.")
            print(path)
            print(f'Path length: {len(path)}')
            win_count += 1
            total_path_length += len(path)
            average_path_length = total_path_length / win_count
            print(f"Average path length over {win_count} wins: {average_path_length:.2f}")
        else:
            print(f"\nCap reached for game {game_no} in {total_time} seconds.")
            print("\nBest path found:")
            print(path)
        print(f"Game {game_no}/{total_runs}. Win count: {win_count}")

    end = time()
    total_time_seconds = end - start
    minutes = total_time_seconds // 60
    seconds = total_time_seconds % 60

    print(f"Total wins out of {total_runs} games: {win_count}")
    print(f"Total time for {total_runs} games: {int(minutes)} minutes and {seconds:.0f} seconds")