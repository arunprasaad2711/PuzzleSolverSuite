def OrthogonalMinDifferenceConstraints(self, min_diff=2):
        
    """
    Adds orthogonal constraints ensuring that any two orthogonally adjacent cells
    have a difference of at least `min_diff`.

    Args:
        min_diff (int): Minimum absolute difference between orthogonal neighbors.
    """
    # Loop through all cells
    for i in range(self.Rows):
        for j in range(self.Cols):
            # Check all orthogonal neighbors of the current cell
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # orthogonal directions
                ni, nj = i + di, j + dj
                # Ensure indices are within bounds
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    # Enforce the absolute difference condition
                    abs_diff = self.Model.NewIntVar(0, self.FullOrder - 1, f"orthogonal_abs_diff_{i}_{j}_{ni}_{nj}")
                    self.Model.AddAbsEquality(abs_diff, self.Cells[i][j] - self.Cells[ni][nj])
                    self.Model.Add(abs_diff >= min_diff)

    print(f"Orthogonal min-difference constraints added with min_diff = {min_diff}.")

def DiagonalMinDifferenceConstraints(self, min_diff=2):
    """
    Adds diagonal constraints ensuring that any two diagonally adjacent cells
    have a difference of at least `min_diff`.

    Args:
        min_diff (int): Minimum absolute difference between diagonal neighbors.
    """
    # Loop through all cells
    for i in range(self.Rows):
        for j in range(self.Cols):
            # Check all diagonal neighbors of the current cell
            for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Diagonal directions
                ni, nj = i + di, j + dj
                # Ensure indices are within bounds
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    # Enforce the absolute difference condition
                    abs_diff = self.Model.NewIntVar(0, self.FullOrder - 1, f"diagonal_abs_diff_{i}_{j}_{ni}_{nj}")
                    self.Model.AddAbsEquality(abs_diff, self.Cells[i][j] - self.Cells[ni][nj])
                    self.Model.Add(abs_diff >= min_diff)

    print(f"Diagonal min-difference constraints added with min_diff = {min_diff}.")
