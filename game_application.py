def generate_possible_moves(state):
    possible_moves = []
    tableau, free_cells, foundations = state['tableau'], state['free_cells'], state['foundations']
    card_values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                   '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13}

    def can_place_on(card, target):
        if not card or not target or len(card) < 2 or len(target) < 2:
            return False

        color_map = {'H': 'red', 'D': 'red', 'C': 'black', 'S': 'black'}
        return (color_map[card[1]] != color_map[target[1]]) and (
                card_values[card[0]] == card_values[target[0]] - 1)

    def can_move_to_foundation(card, suit):
        if not foundations[suit]:
            return card[0] == 'A'
        top_card = foundations[suit][-1]
        return (card[1] == suit) and (card_values[card[0]] == card_values[top_card[0]] + 1)

    # Tableau to Foundations
    for i, col in enumerate(tableau):
        if col:
            card = col[-1]
            if can_move_to_foundation(card, card[1]):
                possible_moves.append(('tableau_to_foundation', i, card[1]))
                return possible_moves

    # Free Cells to Foundations
    for i, cell in enumerate(free_cells):
        if cell and can_move_to_foundation(cell, cell[1]):
            possible_moves.append(('freecell_to_foundation', i, cell[1]))
            return possible_moves

    # Free Cells to Tableau
    for i, cell in enumerate(free_cells):
        if cell:
            for j, col in enumerate(tableau):
                if not col or can_place_on(cell, col[-1]):
                    possible_moves.append(('freecell_to_tableau', i, j))

    # Tableau to Tableau
    for i, src_col in enumerate(tableau):
        if src_col:  # If the source column is not empty
            src_card = src_col[-1]
            for j, dst_col in enumerate(tableau):
                if i != j and (not dst_col or can_place_on(src_card, dst_col[-1])):
                    possible_moves.append(('tableau_to_tableau', i, j))

    # Tableau to Free Cells
    for i, col in enumerate(tableau):
        if col:  # Check if the column is not empty
            for free_cell_index, cell in enumerate(free_cells):
                if cell is None:  # Find the first empty free cell
                    possible_moves.append(('tableau_to_freecell', i, free_cell_index))
                    break  # Only need one move per column, so break after finding the first empty free cell

    num_freecells = sum(1 for cell in free_cells if cell is None)
    num_empty_cols = sum(1 for col in tableau if not col)

    # Maximum number of cards that can be moved in a stack, considering free cells and empty tableau columns
    max_movable = (num_freecells + 1) * (2 ** num_empty_cols) if num_empty_cols else (num_freecells + 1)

    for i, src_col in enumerate(tableau):
        if len(src_col) < 2:
            continue

        for stack_height in range(2, len(src_col) + 1):
            valid_stack = True
            for k in range(1, stack_height):
                if not can_place_on(src_col[-k], src_col[-(k + 1)]):
                    valid_stack = False
                    break
            if valid_stack and stack_height <= max_movable:
                for j, dst_col in enumerate(tableau):
                    if i != j and (not dst_col or can_place_on(src_col[-stack_height], dst_col[-1])):
                        possible_moves.append(('move_stack', i, j, stack_height))
                        break
            if not valid_stack or stack_height >= max_movable:
                break

    return possible_moves


def apply_move(state, move):
    new_state = custom_deepcopy_state(state)

    if len(move) == 3:
        move_type, src, dst = move
        stack_size = 1
    elif len(move) == 4:
        move_type, src, dst, stack_size = move
    else:
        raise ValueError("Invalid move format")

    if move_type == 'tableau_to_tableau':
        if stack_size == 1:
            card = new_state['tableau'][src].pop()
            new_state['tableau'][dst].append(card)
        else:
            stack = new_state['tableau'][src][-stack_size:]
            new_state['tableau'][src] = new_state['tableau'][src][:-stack_size]
            new_state['tableau'][dst].extend(stack)

    elif move_type == 'tableau_to_freecell':
        card = new_state['tableau'][src].pop()
        new_state['free_cells'][dst] = card

    elif move_type == 'freecell_to_tableau':
        card = new_state['free_cells'][src]
        new_state['free_cells'][src] = None
        new_state['tableau'][dst].append(card)

    elif move_type == 'tableau_to_foundation':
        card = new_state['tableau'][src].pop()
        new_state['foundations'][card[1]].append(card)

    elif move_type == 'freecell_to_foundation':
        card = new_state['free_cells'][src]
        new_state['free_cells'][src] = None
        new_state['foundations'][card[1]].append(card)

    elif move_type == 'move_stack':
        if len(move) == 4:
            _, src, dst, stack_size = move
            stack_to_move = []
            for _ in range(stack_size):
                card = new_state['tableau'][src].pop()
                stack_to_move.append(card)
            stack_to_move.reverse()
            new_state['tableau'][dst].extend(stack_to_move)
        else:
            print(f"Invalid move format for stack move: {move}")

    else:
        print("Unknown move type:", move_type)

    return new_state


def custom_deepcopy_state(state):
    from collections import deque
    new_state = {}
    new_state['tableau'] = [deque(column) for column in state['tableau']]
    new_state['free_cells'] = list(state['free_cells'])
    new_state['foundations'] = {suit: list(cards) for suit, cards in state['foundations'].items()}
    return new_state


def reconstruct_path(parent_dict, end_state_hash):
    path = []
    current_state_hash = end_state_hash
    while current_state_hash in parent_dict:
        move, prev_state_hash = parent_dict[current_state_hash]
        if move is not None:
            path.append(move)
        current_state_hash = prev_state_hash
    return path[::-1]


def is_goal_state(state):
    for suit, stack in state['foundations'].items():
        if len(stack) != 13:
            return False
        expected_order = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        if [card[0] for card in stack] != expected_order:
            return False
    return True

def generate_all_possible_moves(state):
    possible_moves = []
    tableau, free_cells, foundations = state['tableau'], state['free_cells'], state['foundations']
    card_values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                   '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13}

    def can_place_on(card, target):
        if not card or not target or len(card) < 2 or len(target) < 2:
            return False

        color_map = {'H': 'red', 'D': 'red', 'C': 'black', 'S': 'black'}
        return (color_map[card[1]] != color_map[target[1]]) and (
                card_values[card[0]] == card_values[target[0]] - 1)

    def can_move_to_foundation(card, suit):
        if not foundations[suit]:
            return card[0] == 'A'
        top_card = foundations[suit][-1]
        return (card[1] == suit) and (card_values[card[0]] == card_values[top_card[0]] + 1)

    # Tableau to Foundations
    for i, col in enumerate(tableau):
        if col:
            card = col[-1]
            if can_move_to_foundation(card, card[1]):
                possible_moves.append(('tableau_to_foundation', i, card[1]))

    # Free Cells to Foundations
    for i, cell in enumerate(free_cells):
        if cell and can_move_to_foundation(cell, cell[1]):
            possible_moves.append(('freecell_to_foundation', i, cell[1]))

    # Free Cells to Tableau
    for i, cell in enumerate(free_cells):
        if cell:
            for j, col in enumerate(tableau):
                if not col or can_place_on(cell, col[-1]):
                    possible_moves.append(('freecell_to_tableau', i, j))

    # Tableau to Tableau
    for i, src_col in enumerate(tableau):
        if src_col:  # If the source column is not empty
            src_card = src_col[-1]
            for j, dst_col in enumerate(tableau):
                if i != j and (not dst_col or can_place_on(src_card, dst_col[-1])):
                    possible_moves.append(('tableau_to_tableau', i, j))

    # Tableau to Free Cells
    for i, col in enumerate(tableau):
        if col:  # Check if the column is not empty
            for free_cell_index, cell in enumerate(free_cells):
                if cell is None:  # Find the first empty free cell
                    possible_moves.append(('tableau_to_freecell', i, free_cell_index))
                    break  # Only need one move per column, so break after finding the first empty free cell

    num_freecells = sum(1 for cell in free_cells if cell is None)
    num_empty_cols = sum(1 for col in tableau if not col)

    # Maximum number of cards that can be moved in a stack, considering free cells and empty tableau columns
    max_movable = (num_freecells + 1) * (2 ** num_empty_cols) if num_empty_cols else (num_freecells + 1)

    print(f"num_freecells: {num_freecells}, num_empty_cols: {num_empty_cols}, max_movable: {max_movable}")

    for i, src_col in enumerate(tableau):
        if len(src_col) < 2:
            continue

        print(f"Evaluating stack moves from column {i}")

        for stack_height in range(2, len(src_col) + 1):
            valid_stack = True
            for k in range(1, stack_height):
                if not can_place_on(src_col[-k], src_col[-(k + 1)]):
                    valid_stack = False
                    break
            if valid_stack and stack_height <= max_movable:
                for j, dst_col in enumerate(tableau):
                    if i != j and (not dst_col or can_place_on(src_col[-stack_height], dst_col[-1])):
                        possible_moves.append(('move_stack', i, j, stack_height))
                        print(f"Added move_stack: from {i} to {j} with height {stack_height}")
            if not valid_stack or stack_height >= max_movable:
                break

    print(f"Generated possible moves: {possible_moves}")
    return possible_moves
