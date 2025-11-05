def MagicSquareConstraints(self, magic_square_list):
    """
    Adds multiple magic square constraints to the Sudoku model.
    Magic Square: Sum of elements along any row/column/diagonal is a constant.

    Args:
        magic_square_list (list of lists): Each inner list contains tuples specifying
                                            the coordinates (row, col) of the cells in the magic square.
    """
    
    for square_id, cell_coords in enumerate(magic_square_list):
        
        # Extract the corresponding cells
        cells = [self.Cells[row][col] for row, col in cell_coords]

        # Calculate the size of the square (assumes square is complete)
        size = int(len(cells)**0.5)  # Magic square is assumed to be square (n x n)

        if size**2 != len(cells):
            raise ValueError(f"Magic square {square_id} is not a complete square.")

        # Calculate the magic constant
        magic_constant = size * (size**2 + 1) // 2

        # Add row constraints
        for i in range(size):
            self.Model.Add(
                sum(self.Cells[row][col] for row, col in cell_coords[i * size:(i + 1) * size]) == magic_constant
            )

        # Add column constraints
        for i in range(size):
            self.Model.Add(
                sum(self.Cells[cell_coords[j][0]][cell_coords[j][1]] for j in range(i, len(cells), size)) == magic_constant
            )

        # Add diagonal constraints (main and anti-diagonal)
        self.Model.Add(
            sum(self.Cells[cell_coords[i * (size + 1)][0]][cell_coords[i * (size + 1)][1]] for i in range(size)) == magic_constant
        )
        self.Model.Add(
            sum(self.Cells[cell_coords[(i + 1) * (size - 1)][0]][cell_coords[(i + 1) * (size - 1)][1]] for i in range(size)) == magic_constant
        )

        # Ensure all numbers in the magic square are unique
        self.Model.AddAllDifferent(cells)

        print(f"Magic square {square_id + 1} added with magic constant {magic_constant}.")
