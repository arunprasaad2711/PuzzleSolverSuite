def CreekShadingConstraints(self, Groups, GroupValues):

    '''
    Refer to global_connectivity_constraint.py script. Run that first before this
    to make variables available
    '''

    # set the cells to be shaded or unshaded based on the connectivity cell state
    for i in range(self.Rows):
        for j in range(self.Cols):
            self.Model.Add(self.Cells[i][j] == 1).OnlyEnforceIf(self.ConnectivityCells[i][j])
            self.Model.Add(self.Cells[i][j] == 0).OnlyEnforceIf(~self.ConnectivityCells[i][j])

    for Group, Value in zip(Groups, GroupValues):
        # print(Group, Value)

        CellGroup = [self.Cells[i][j] for i, j in Group]
        self.Model.Add(sum(CellGroup) == Value)
        # print(f"Added Creek Sum Constraint {Value} for {Group}")
    
    print(f"Creek Sum Constraints Added")

def ClassicCreekConstraint(self, Groups, GroupValues):

    self.GlobalConnectivityConstraint(True)
    self.CreekShadingConstraints(Groups, GroupValues)

    print(f"Creek Puzzle Constraints Added")