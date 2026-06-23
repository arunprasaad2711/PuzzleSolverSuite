def HitoriGridConstraints(self, GridMap):

    '''
    Refer to global_connectivity_constraint.py script. Run that first before this
    to make variables available
    '''

    # set the cells to be shaded or unshaded based on the connectivity cell state
    for i in range(self.Rows):
        for j in range(self.Cols):
            self.Model.Add(self.Cells[i][j] == 1).OnlyEnforceIf(self.ConnectivityCells[i][j])
            self.Model.Add(self.Cells[i][j] == 0).OnlyEnforceIf(~self.ConnectivityCells[i][j])
    
    # CONSTRAINT 1 & 2: No duplicate values in row/col unless one is black
    for r in range(self.Rows):
        for c1 in range(self.Cols):
            for c2 in range(c1 + 1, self.Cols):
                if GridMap[r][c1] == GridMap[r][c2]:
                    self.Model.AddBoolOr([self.ConnectivityCells[r][c1], self.ConnectivityCells[r][c2]])

    for c in range(self.Cols):
        for r1 in range(self.Rows):
            for r2 in range(r1 + 1, self.Rows):
                if GridMap[r1][c] == GridMap[r2][c]:
                    self.Model.AddBoolOr([self.ConnectivityCells[r1][c], self.ConnectivityCells[r2][c]])

    # CONSTRAINT 3: No two adjacent black cells
    for r in range(self.Rows):
        for c in range(self.Cols):
            if r + 1 < self.Rows:
                self.Model.AddBoolOr([~self.ConnectivityCells[r][c], ~self.ConnectivityCells[r+1][c]])
            if c + 1 < self.Cols:
                self.Model.AddBoolOr([~self.ConnectivityCells[r][c], ~self.ConnectivityCells[r][c+1]])
    
    print(f"Hitori Cell Shading Condition Added")

def ClassicHitoriConstraint(self, GridMap):

    self.GlobalConnectivityConstraint(True)
    self.HitoriGridConstraints(GridMap)

    print("Hitori Constraints Added")

