def OneUpRowConstraints(self, RowGroupMap):
        
    # Collect all the  unique row-groups across the puzzle
    # Mark group of cells that are to be ignored as 0 in the UID
    UIDs = set([RowGroupMap[i, j] for i in range(self.Rows) for j in range(self.Cols)]) - {0}
    for UID in UIDs:
        
        # Collect all the cells in each group marked by a UID
        Cells = [self.Cells[i][j] for i in range(self.Rows) for j in range(self.Cols) if RowGroupMap[i, j] == UID]
        
        # Say that all the entries in a group must be different
        self.Model.AddAllDifferent(Cells)
        
        # Add a constraint that the maximum value of cells in a group
        # must be the number of cells in the group and all cells
        # must be less than or equal to this number.
        for Cell in Cells:
            self.Model.Add(Cell <= len(Cells))
        
    print("One-up Row Groups Added!")

def OneUpColConstraints(self, ColGroupMap):
    
    # Collect all the  unique column-groups across the puzzle
    # Mark group of cells that are to be ignored as 0 in the UID
    UIDs = set([ColGroupMap[i, j] for i in range(self.Rows) for j in range(self.Cols)]) - {0}
    for UID in UIDs:
        
        # Collect all the cells in each group marked by a UID
        Cells = [self.Cells[i][j] for i in range(self.Rows) for j in range(self.Cols) if ColGroupMap[i, j] == UID]
        
        # Say that all the entries in a group must be different
        self.Model.AddAllDifferent(Cells)
        
        # Add a constraint that the maximum value of cells in a group
        # must be the number of cells in the group and all cells
        # must be less than or equal to this number.
        for Cell in Cells:
            self.Model.Add(Cell <= len(Cells))
        
    print("One-up Row Groups Added!")

def ClassicOneUpConstraints(self, RowGroups, ColGroups):
    
    self.OneUpColConstraints(ColGroups)
    self.OneUpRowConstraints(RowGroups)
    self.InitializeGivenEntries()
    
    print("One-up All Constraints Added!")