import json
import matplotlib.pyplot as plt

path = '/home/tautas/IdeaProjects/MasterT/Analysis/game-evolver-data/evolution_results_easy_looking_glass.json'

with open(path, 'r') as file:
    data = json.load(file)

print("Sample entry:", data[0])

iterations = [entry['iteration'] for entry in data]
states_checked = [entry['easiest_states_generated'] for entry in data]

boards = [entry['easiest_board'] for entry in data]

biggest_jump = 0
biggest_jump_iteration = 0
for i in range(1, len(states_checked)):
    jump = abs(states_checked[i] - states_checked[i - 1])
    if jump > biggest_jump:
        biggest_jump = jump
        biggest_jump_iteration = i

print(f'The biggest jump is {biggest_jump} between iterations {biggest_jump_iteration} and {biggest_jump_iteration + 1}')
print('Board configuration before the biggest jump:')
print(boards[biggest_jump_iteration - 1])
print('\nBoard configuration after the biggest jump:')
print(boards[biggest_jump_iteration])

ax = plt.gca()
ax.set_facecolor('#f5f5f5')
plt.plot(iterations, states_checked, marker='o')
plt.xlabel('Iteration')
plt.ylabel('States Generated to find a solution')
plt.title('Evolving for the easiest game')
plt.grid(True)
plt.show()
