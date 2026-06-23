def GlobalConnectivityConstraint(self, ShadeIsOne=True):

    '''
    Global Connectivity Constraint.
    The implementation came from this source:
    https://www.cs.ru.nl/bachelors-theses/2021/Gerhard_van_der_Knijff___1006946___Solving_and_generating_puzzles_with_a_connectivity_constraint.pdf

    More importantly, the connectivity idea came from Zantema and Joosten, 2015
    H. Zantema and S.J.C Joosten. Latin squares with graph properties.
    https://www.win.tue.nl/~hzantema/lsqj.pdf, 2015

    The idea is this:
    1. Create a matrix of cells holding boolean values - 0 or 1.
    2. Decide one of them to be shaded and the other unshaded as per the puzzle convenience
    3. Pick a cell that needs to be connected. Assign that to be a root cell and set the Number
    to be zero.
    4. Now, ensure that only one cell is a root cell and that is an unshaded cell.
    5. For each cell, find if each cell is a non-root unshaded cell. That means, it should not be root and unshaded.
    6. If it is a non-root shaded cell, check if the adjacent cell is an unshaded cell.
    7. Make sure that all the neighbouring unshaded cells have a number such that atleast one of them is less them
    the current cell's value.

    What is happening:
    Connectivity happens when all the cells are connected to form a single region.
    One way to make this work is by picking a cell and adding numbers to each cell.

    So, pick a starting cell, called the root cell. Set it to 0. Now, find all the 
    adjacent cells that are unshaded and assign numbers n+1. Then, assign n+2 to all the neighbours
    that were assigned n+1. Leave out any numbers that were already assigned n.

    By this logic, if all the unshaded cells are connected, then every cell can be traced back to the root.

    So, let's say there are two brances of numbers

    0 1 2 3 4 5 ... 25*
    0 1 2 3 4 5 .. 15*.

    To move from 25* to 15*, one might backtrack from 25 to 24, 23, 22, ... all the way
    till 14. And since 15 will be next to 14, one of the neighbours around 14 will be 15*
    '''

    # This one helps in flipping the shading and unshading cells
    # by default shaded cells are 1. When made false, unshaded cells
    # are 1
    def unshaded(i, j):
        if ShadeIsOne:
            return ~self.ConnectivityCells[i][j]
        else:
            return self.ConnectivityCells[i][j]

    def shaded(i, j):
        if ShadeIsOne:
            return self.ConnectivityCells[i][j]
        else:
            return ~self.ConnectivityCells[i][j]

    # This one keeps track of cells that are shaded or unshaded.
    self.ConnectivityCells = [
        [
            self.Model.NewBoolVar(
            f"GlobalConnectivityCellState_{i}_{j}")
            for j in range(self.Cols)
        ]
        for i in range(self.Rows)
    ]

    # Here, assign a number to each cell
    NMax = self.Rows * self.Cols
    ConnectivityNumber = [
        [
            self.Model.NewIntVar(0, NMax,
            f"GlobalConnectivityCellNumber_{i}_{j}")
            for j in range(self.Cols)
        ]
        for i in range(self.Rows)
    ]

    # Create a Root Matrix - one that tracks which cell is the root
    ConnectivityRoot = [
        [
            self.Model.NewBoolVar(
            f"GlobalConnectivityIsRoot_{i}_{j}")
            for j in range(self.Cols)
        ]
        for i in range(self.Rows)
    ]

    # Make sure that only one cell is a root. Rest of them are not.
    self.Model.AddExactlyOne([ConnectivityRoot[i][j] for i in range(self.Rows) for j in range(self.Cols)])

    # Make sure that a non-shaded cell could be a root.
    # A shaded cell can't be a root.
    # And only a root cell has the connectivity number to be zero.
    for i in range(self.Rows):
        for j in range(self.Cols):
            self.Model.AddBoolAnd([unshaded(i, j)]).OnlyEnforceIf(ConnectivityRoot[i][j])
            self.Model.Add(ConnectivityNumber[i][j] == 0).OnlyEnforceIf(ConnectivityRoot[i][j])

    # create a boolean to check if the cell here is unshaded and not a root cell
    for i in range(self.Rows):
        for j in range(self.Cols):
            IsNonRootUnshaded = self.Model.NewBoolVar(f"GlobalConnectivity_IsNonRootUnshaded_{i}_{j}")
            # A cell to be unshaded and not a root
            self.Model.AddBoolAnd([unshaded(i, j), ~ConnectivityRoot[i][j]]).OnlyEnforceIf(IsNonRootUnshaded)
            # A cell should not be shaded nor a root cell
            self.Model.AddBoolOr([shaded(i, j), ConnectivityRoot[i][j]]).OnlyEnforceIf(IsNonRootUnshaded.Not())

            # If both conditions are true, then it is a valid non shaded cell that can take a number
            self.Model.Add(ConnectivityNumber[i][j] >= 1).OnlyEnforceIf(IsNonRootUnshaded)

            UnshadedConnectedNeighbourCell = []
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = i + dr, j + dc
                if 0 <= nr < self.Rows and 0 <= nc < self.Cols:
                    ConnectedNeighbourCellIsUnshaded = self.Model.NewBoolVar(f"ConnectedNeighbourCellIsUnshaded_{i}_{j}_{nr}_{nc}")
                    # Make sure that the neighbour is unshaded
                    self.Model.AddBoolAnd([unshaded(nr, nc)]).OnlyEnforceIf(ConnectedNeighbourCellIsUnshaded)
                    # Make sure that one of the neighbouring cell has a value less than the current cell
                    self.Model.Add(ConnectivityNumber[nr][nc] < ConnectivityNumber[i][j]).OnlyEnforceIf(ConnectedNeighbourCellIsUnshaded)

                    UnshadedConnectedNeighbourCell.append(ConnectedNeighbourCellIsUnshaded)
            
            self.Model.AddBoolOr(UnshadedConnectedNeighbourCell).OnlyEnforceIf(IsNonRootUnshaded)
    
    print(f"Global Unshaded Cells Connectivity Constraints Added")
