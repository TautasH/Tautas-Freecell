from collections import deque
import sys

def random_generator(seed, n):
    max_int32 = 0x7FFFFFFF
    seed &= max_int32
    random_numbers = []
    while len(random_numbers) < n:
        seed = (seed * 214013 + 2531011) & max_int32
        random_numbers.append(seed >> 16)
    return random_numbers


def generate_initial_state(seed):
    tableau = generate_deck(seed)
    free_cells = [None for _ in range(4)]  # Assuming 4 free cells, all empty initially
    foundations = {'C': [], 'D': [], 'H': [], 'S': []}  # No cards in any foundation pile initially

    initial_state = {
        'tableau': tableau,
        'free_cells': free_cells,
        'foundations': foundations,
    }

    return initial_state


def generate_deck(seed):
    nc = 52
    cards = list(range(nc))[::-1]
    rnd = random_generator(seed, nc)
    for index, r in enumerate(rnd):
        j = (nc - 1) - r % (nc - index)
        cards[index], cards[j] = cards[j], cards[index]

    # Format the deck
    ranks = 'A23456789TJQK'
    suits = 'CDHS'
    formatted_deck = [f'{ranks[c // 4]}{suits[c % 4]}' for c in cards]

    # Deal cards into 8 columns
    tableau = [deque() for _ in range(8)]
    for i, card in enumerate(formatted_deck):
        tableau[i % 8].append(card)

    return tableau


def print_game_state(initial_state):
    print("Foundations:", end=" ")
    for suit, cards in initial_state['foundations'].items():
        if cards:
            print(f"{suit}: {' '.join(cards)}", end="    ")
        else:
            print(f"{suit}: Empty", end="    ")
    print()

    print("Free Cells:", end=" ")
    for cell in initial_state['free_cells']:
        if cell:
            print(cell, end=" ")
        else:
            print("Empty", end=" ")
    print("\n")

    print("Tableau:")
    max_height = max(len(column) for column in initial_state['tableau'])
    for row in range(max_height):
        row_display = []
        for col in initial_state['tableau']:
            if row < len(col):
                card = col[row]
                row_display.append(card)
            else:
                row_display.append('   ')
        print(' '.join(row_display))

if __name__ == "__main__":
    seed = int(input("Enter the seed: ")) if len(sys.argv) == 2 else 1
    initial_state = generate_initial_state(seed)
    print_game_state(initial_state)
