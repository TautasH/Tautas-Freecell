import json
import matplotlib.pyplot as plt

path = '/home/tautas/IdeaProjects/MasterT/Analysis/game-evolver-data/evolution_results_difficult_looking_glass.json'

with open(path, 'r') as file:
    data = json.load(file)

iterations = [entry['iteration'] for entry in data]
states_generated = [entry['most_difficult_states_generated'] for entry in data]
boards = [entry['most_difficult_board'] for entry in data]

jumps = []
for i in range(1, len(states_generated)):
    jump = abs(states_generated[i] - states_generated[i - 1])
    jumps.append((jump, i))

jumps.sort(reverse=True, key=lambda x: x[0])
top_3_jumps = jumps[:3]

def print_jump_info(jump, iteration_index):
    print(f'\nThe jump is {jump} between iterations {iteration_index} and {iteration_index + 1}')
    print('Board configuration before the jump:')
    for line in boards[iteration_index - 1]:
        print(line)
    print('\nBoard configuration after the jump:')
    for line in boards[iteration_index]:
        print(line)

    print('\nChanges between the two configurations:')
    for row_index, (before_row, after_row) in enumerate(zip(boards[iteration_index - 1], boards[iteration_index])):
        before_cards = before_row.split()
        after_cards = after_row.split()

        for col_index, (before_card, after_card) in enumerate(zip(before_cards, after_cards)):
            if before_card != after_card:
                print(f"Row {row_index + 1}, Column {col_index + 1}: {before_card} -> {after_card}")

for jump, iteration_index in top_3_jumps:
    print_jump_info(jump, iteration_index)


ax = plt.gca()
ax.set_facecolor('#f5f5f5')
plt.plot(iterations, states_generated, marker='o')
plt.xlabel('Iteration', fontsize=12)
plt.ylabel('States Generated to find a solution', fontsize=12)
plt.title('Evolving for the most difficult game')
plt.grid(True)
plt.show()
