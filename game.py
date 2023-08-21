from grid import Grid
import time
import os

MINIMUM_GUESSES_2 = 2
MINIMUM_GUESSES_4 = 8
MINIMUM_GUESSES_6 = 18
total_score = 0
actual_guesses = 0
uncover_times = 0

def print_menu():
    print("-------------------------------------------------")
    print("PEEK-A-BOO")
    print("1. Let me select two elements")
    print("2. Uncover one element for me")
    print("3. I give up -  reveal the grid")
    print("4. New game")
    print("5. Exit")

def build_grid(size_demension):
    grid = Grid(size_demension)
    return grid

def is_valid_input(input, size):
    if ((size == 2 and (int(input[1]) >= 2 or input[0].upper() not in ['A','B'])) or (size == 4 and (int(input[1]) >= 4 or input[0].upper() not in ['A','B','C','D'])) 
        or (size == 6 and (int(input[1]) >= 6 or input[0].upper() not in ['A','B','C','D','E','F']))):
        return False
   
    return True

def get_cell_coordinates(cell, size):
    input = cell.upper()
    if len(input) == 2 and input[0].isalpha() and input[1].isdigit() and is_valid_input(input, size):
        row = int(input[1])
        col = ord(input[0]) - ord('A')

        return row, col
    else:
        print("Input error: column entry is out out range for this grid. Please try again.")
        return None, None

def uncover_one_cell(grid):
    is_cheated = False
    cell = input("Enter cell coordinates (e.g., a0): ")
    row, col = get_cell_coordinates(cell, grid.size)
    grid.reveal_cell(row, col)
    grid.uncover_element(row, col)
    global uncover_times
    uncover_times += 1
    global actual_guesses
    actual_guesses += 2

    print(grid)

    if ((grid.size == 2 and uncover_times == 4) or (grid.size == 4 and uncover_times == 16)
        or (grid.size == 6 and uncover_times == 36)):
        print("You cheated - Loser!. Your score is 0!")
        is_cheated = True
    
    if grid.is_ending_game() and is_cheated == False:
        total_score = calculate_total_score(grid.size, actual_guesses)
        print("Oh Happy Day. You've won!! Your score is: " + str(round(total_score,2)))              

def reveal_grid(grid):
    for row in range(grid.size):
        for col in range(grid.size):
            grid.reveal_cell(row, col)
    print(grid)

def guess_pair(grid):
    cell1 = input("Enter the first cell coordinates: ")
    row1, col1 = get_cell_coordinates(cell1, grid.size)
    cell2 = input("Enter the second cell coordinates: ")
    row2, col2 = get_cell_coordinates(cell2, grid.size)

    value_cell1 = grid.reveal_cell(row1, col1)
    value_cell2 = grid.reveal_cell(row2, col2)
    print(grid)

    global actual_guesses
    actual_guesses += 1
    print("Actual guesses: " + str(actual_guesses))
    print("\n")

    if value_cell1 == value_cell2:
        print("Good job! You're right!")
        if grid.is_ending_game():
            total_score = calculate_total_score(grid.size, actual_guesses)
            print("Oh Happy Day. You've won!! Your score is: " + str(round(total_score,2)))
    else:
        time.sleep(2)
        os.system('clear')
        # revoke revealed cells
        grid.revoke_revealed_cell(row1, col1)
        grid.revoke_revealed_cell(row2, col2)
        print(grid)
        print("This pair is not correctly matched. Please try again!")

def calculate_total_score(size, actual_guesses):
    if size == 2:
        total_score = (MINIMUM_GUESSES_2 / actual_guesses) * 100
    elif size == 4:
        total_score = (MINIMUM_GUESSES_4 / actual_guesses) * 100
    elif size == 6:
        total_score = (MINIMUM_GUESSES_6 / actual_guesses) * 100

    return total_score

def start_new_game(grid):
    grid = build_grid(grid.size)
    grid.reset_new_game()
    global uncover_times
    uncover_times = 0
    global total_score
    total_score = 0
    global actual_guesses
    actual_guesses = 0
    print(grid)
    print("Start a new game!")

    return grid

def process(grid):
    while True:
        print_menu()
        try:
            choice = int(input("Select: "))
            if choice == 1:
                guess_pair(grid)
            elif choice == 2:
                uncover_one_cell(grid)
            elif choice == 3:
                reveal_grid(grid)
            elif choice == 4:
                grid = start_new_game(grid)
            elif choice == 5:
                break
            else:
                print("Invalid choice! Please re-enter your choice (1-5)")
        except ValueError:
            print("Invalid input: you must enter a number (1-5)")

def main():
    import sys
    if len(sys.argv) != 2 or sys.argv[1] not in ['2', '4', '6']:
        print("Please enter the valid size of grid (2,4,6)")
        return
    size_demension = int (sys.argv[1])
    grid_object = build_grid(size_demension)
    # print the unrevealed grid
    print(grid_object)
    process(grid_object)

if __name__ == '__main__':
    main()

