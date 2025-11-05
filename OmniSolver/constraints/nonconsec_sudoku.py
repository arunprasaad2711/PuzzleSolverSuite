def DiagonalNonConsecConstraints(self):
        
    '''
    Diagonal Non-Consecutive Condition: Cells that are Diagonally adjacent (top, bottom, left, 
    right) must not be consecutive
    '''
    
    # Add non-consecutive constraints
    for i in range(self.Rows):
        for j in range(self.Cols):
            for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Diagonally adjacent cells
                ni, nj = i + di, j + dj
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    self.Model.Add(self.Cells[i][j] != self.Cells[ni][nj] + 1)
                    self.Model.Add(self.Cells[i][j] != self.Cells[ni][nj] - 1)
    
    print("Diagonal Non-Consecutive constraints added.")

def DiagonalNonConsecCells(self, cells):
    
    '''
    Diagonal Non-Consecutive Cells: Cells constrained such that none of the diagonally
    adjacent neighbours are consecutive
    '''
    for i, j in cells:
        for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Diagonally adjacent cells
                ni, nj = i + di, j + dj
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    self.Model.Add(self.Cells[i][j] != self.Cells[ni][nj] + 1)
                    self.Model.Add(self.Cells[i][j] != self.Cells[ni][nj] - 1)

def OrthogonalNonConsecConstraints(self):
    
    '''
    Orthogonal Non-Consecutive Condition: Cells that are orthogonally adjacent (top, bottom, left, 
    right) must not be consecutive
    '''
    
    # Add non-consecutive constraints
    for i in range(self.Rows):
        for j in range(self.Cols):
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Orthogonally adjacent cells
                ni, nj = i + di, j + dj
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    self.Model.Add(self.Cells[i][j] != self.Cells[ni][nj] + 1)
                    self.Model.Add(self.Cells[i][j] != self.Cells[ni][nj] - 1)
    
    print("Orthogonal Non-Consecutive constraints added.")

def OrthogonalNonConsecCells(self, cells):
    
    '''
    Orthogonal Non-Consecutive Cells: Cells constrained such that none of the orthogonally
    adjacent neighbours are consecutive
    '''
    for i, j in cells:
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Orthogonally adjacent cells
                ni, nj = i + di, j + dj
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    self.Model.Add(self.Cells[i][j] != self.Cells[ni][nj] + 1)
                    self.Model.Add(self.Cells[i][j] != self.Cells[ni][nj] - 1)