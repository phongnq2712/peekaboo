import random

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = '\n'.join([' '.join(['X ' for _ in range(size)]) for _ in range(size)])
        self.revealed_cell = set()
        self.uncover_cell = set()
        self.pairs = self.generate_grid_pairs()

    def generate_grid_pairs(self):
        number_range = list(range(self.size * self.size // 2))
        pairs = number_range + number_range
        random.shuffle(pairs)
        return pairs
    
    def is_cell_revealed(self, row, col):
        return (row, col) in self.revealed_cell

    def uncover_element(self, row, col):
        self.uncover_cell.add((row, col))

    def reveal_cell(self, row, col):
        self.revealed_cell.add((row, col))
        return self.pairs[row * self.size + col]
        
    def get_value_at(self, row, col):
        if self.is_cell_revealed(row, col):
            return str(self.pairs[row * self.size + col])
        return 'X'

    def revoke_revealed_cell(self, row, col):
        if (row, col) not in self.uncover_cell:
            self.revealed_cell.remove((row, col))

    def is_ending_game(self):
        return len(self.revealed_cell) == self.size * self.size

    def reset_new_game(self):
        self.revealed_cell = set()
        self.uncover_cell = set()

    def __str__(self):
        grid_str = ''
        grid_str += ' ' * 6
        for col in range(self.size):
            grid_str += f'[{chr(ord("A") + col)}] '
        grid_str += '\n'

        for row in range(self.size):
            grid_str += f'[{row}]  '
            for col in range(self.size):
                grid_str += f'{self.get_value_at(row, col):>4}'
            grid_str += '\n'
        grid_str += '\n     '
        
        return grid_str