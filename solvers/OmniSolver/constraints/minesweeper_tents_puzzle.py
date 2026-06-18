import numpy as np

def ClassicMineSweeperConstraints(self, GridMap, NeighbourMode="King"):

    '''
    Similar to the minesweeper game, you have to find all the mines in the field.
    The gridmap tells how many mines are present in the neighbourhood.

    The Neighbour mode tells what cells can be neighbours.
    King mode - both orthogonal and diagonal cells
    Knight mode - cells that are knight's move apart
    Orthogonal mode - purely orthogonal cells
    Diagonal mode - purely diagonal cells
    '''

    GridMap = np.array(GridMap)

    if NeighbourMode == "King":
        Neighbours = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
    elif NeighbourMode == "Knight":
        Neighbours = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]
    elif NeighbourMode == "Orthogonal":
        Neighbours = [
            (-1, 0), (0, -1), (0, 1), (1, 0),
        ]
    elif NeighbourMode == "Diagonal":
        Neighbours = [
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]
    
    # Minesweeper constraints
    for i in range(self.Rows):
        for j in range(self.Cols):

            if GridMap[i, j] > 0 or GridMap[i, j] == self.ZeroMaskingDigit:

                # Constraint 1 - if the GridMap has a number, then there are no mines:
                self.Model.Add(self.Cells[i][j] == 0)

                # Constraint 2 - sum of all the neighbours around the GridMap must be
                # equal to the grid map number.
                ValidNeighbours = []
                for move in Neighbours:
                    ni, nj = i + move[0], j + move[1]
                    if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                        ValidNeighbours.append(self.Cells[ni][nj])
                
                # Setting up constraint 2. Since zero is valid, adjustment
                # is done for it as well.
                if GridMap[i, j] > 0:
                    self.Model.Add(sum(ValidNeighbours) == GridMap[i, j])
                elif GridMap[i, j] == self.ZeroMaskingDigit:
                    self.Model.Add(sum(ValidNeighbours) == 0)
    
    print(f"MineSweeper Constraints Added")

def ClassicTentsConstraints(self, TentsTreeMap, TentsAlongRows, TentsAlongCols):
    self.TentsRowCounts(TentsAlongRows)
    self.TentsColCounts(TentsAlongCols)
    self.TentsAndTreeConstraints(TentsTreeMap)

def TentsRowCounts(self, TentsAlongRows):

    for i, count in zip(range(self.Rows), TentsAlongRows):
        RowCollection = []
        
        for j in range(self.Cols):
            RowCollection.append(self.Cells[i][j])
        
        self.Model.Add(sum(RowCollection) == count)
        # print(f"Tents Puzzle Row Constraints placed for row = {i}, count = {count}")
    
    print(f"Tents Puzzle Row Constraints Added.")

def TentsColCounts(self, TentsAlongCols):

    for i, count in zip(range(self.Cols), TentsAlongCols):
        ColCollection = []
        
        for j in range(self.Rows):
            ColCollection.append(self.Cells[j][i])
        
        self.Model.Add(sum(ColCollection) == count)
    
        # print(f"Tents Puzzle Column Constraints placed for column = {i}, count = {count}")
    
    print(f"Tents Puzzle Column Constraints Added.")

def TentsAndTreeConstraints(self, TentsTreeMap):

    '''
    Classic Tents Puzzle Constraints
    Example: https://www.youtube.com/watch?v=DdxYyMzkG-I

    Place 1 tent orthogonally adjacent to every tree in the grid such that each row/column
    contains the given number of tents. Tents cannot be orthogonally or diagonally adjacent.
    '''

    TentsTreeMap = np.array(TentsTreeMap)

    AllNeighbours = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
    OrthogonalNeighbours = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    DiagonalNeighbours = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    SharedNeighbourSpots = [
        (-2, 0), (-1, -1), (-1, 1), (0, -2), (0, 2), (1, -1), (1, 1), (2, 0)
    ]

    # Constraint 1: Number of Tents = Number of Trees
    self.Model.Add(sum([Cell for row in self.Cells for Cell in row]) == np.sum(TentsTreeMap))

    AllIndicesSet = set()
    for i in range(self.Rows):
        for j in range(self.Cols):

            AllIndicesSet.add((i, j))
            
            NoOfTreesOrthogonallyAroundThisSpot = 0
            for move in OrthogonalNeighbours:
                ni, nj = i + move[0], j + move[1]
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    NoOfTreesOrthogonallyAroundThisSpot += TentsTreeMap[ni, nj]
            
            OrthogonalTentSpotsAroundThisSpot = []
            for move in OrthogonalNeighbours:
                ni, nj = i + move[0], j + move[1]
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols and TentsTreeMap[ni, nj] == 0:
                    OrthogonalTentSpotsAroundThisSpot.append(self.Cells[ni][nj])
            
            NoOfTreesDiagonallyAroundThisSpot = 0
            for move in DiagonalNeighbours:
                ni, nj = i + move[0], j + move[1]
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    NoOfTreesDiagonallyAroundThisSpot += TentsTreeMap[ni, nj]
            
            AllNeighboursAroundThisSpot = []
            for move in AllNeighbours:
                ni, nj = i + move[0], j + move[1]
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    AllNeighboursAroundThisSpot.append(self.Cells[ni][nj])
            
            # Constraint 2: If a cell is a tree, then it can't be a tent
            if TentsTreeMap[i, j] == 1:
                self.Model.Add(self.Cells[i][j] == 0)
                AllIndicesSet.discard((i, j))
                # print(f"Cell ({i}, {j}) is a Tree. Setting it to 0")
            
            # Constraint 3: If a cell is unassigned and not near a tree, it can't be a tent
            if TentsTreeMap[i, j] == 0 and NoOfTreesOrthogonallyAroundThisSpot == 0:
                self.Model.Add(self.Cells[i][j] == 0)
                AllIndicesSet.discard((i, j))
                # print(f"Cell ({i}, {j}) is an Empty Spot with no trees nearby. Setting it to 0")
            
            # Constraint 4: If a cell is a tent, there can be no tents around it.
            if TentsTreeMap[i, j] == 0:
                self.Model.Add(sum(AllNeighboursAroundThisSpot) == 0).OnlyEnforceIf(self.Cells[i][j])
            
            # Constraint 5 and 6: Check if pairs of trees have shared neighbours or not 
            if TentsTreeMap[i, j] == 1:

                LoneTree = True
                SharedNeighbourPairs = []

                for move in SharedNeighbourSpots:
                    ni, nj = i + move[0], j + move[1]
                    if 0 <= ni < self.Rows and 0 <= nj < self.Cols and TentsTreeMap[ni, nj] == 1:
                        LoneTree = False
                        SharedNeighbourPairs.append([(i, j), (ni, nj)])
                        # print(f"Found a shared neighbour pair ({i}, {j}) and ({ni}, {nj})")
                
                # If the tree has no shared neighbours with other trees, it is a lone tree
                # Constraint 5: Sum of tents around a lone tree = 1
                if LoneTree:
                    # print(f"Found a Lone Tree ({i}, {j})")
                    self.Model.Add(sum(OrthogonalTentSpotsAroundThisSpot) == 1)
                # Constraint 6: The tree has an adjacent tree
                else:
                    for Tree1, Tree2 in SharedNeighbourPairs:
                        # print(f"Constraining Cells around Trees {Tree1} and {Tree2}")

                        NeighboursTree1 = []
                        NeighboursTree2 = []

                        x1, y1 = Tree1
                        x2, y2 = Tree2

                        for move in OrthogonalNeighbours:

                            ni, nj = x1 + move[0], y1 + move[1]
                            if 0 <= ni < self.Rows and 0 <= nj < self.Cols and TentsTreeMap[ni, nj] == 0:
                                # NeighboursTree1.add(self.Cells[ni][nj])
                                NeighboursTree1.append((ni, nj))
                            
                            ni, nj = x2 + move[0], y2 + move[1]
                            if 0 <= ni < self.Rows and 0 <= nj < self.Cols and TentsTreeMap[ni, nj] == 0:
                                # NeighboursTree2.add(self.Cells[ni][nj])
                                NeighboursTree2.append((ni, nj))
                        
                        NeighbourCellsForBothTrees   = sorted(set(NeighboursTree1 + NeighboursTree2))

                        CellsForTree1     = [self.Cells[X][Y] for (X, Y) in NeighboursTree1]
                        CellsForTree2     = [self.Cells[X][Y] for (X, Y) in NeighboursTree2]
                        CellsForBothTrees = [self.Cells[X][Y] for (X, Y) in NeighbourCellsForBothTrees]

                        # Constraint 6: Each tree has atleast 1 tent.
                        # But both trees combined should have exactly 2 tents it the pair
                        # is isolated, but more than 2 if one of the trees has more paired up trees
                        self.Model.Add(sum(CellsForTree1) >= 1)
                        self.Model.Add(sum(CellsForTree2) >= 1)
                        self.Model.Add(sum(CellsForBothTrees) >= 2)

    print("Tents Puzzle Tree-Tent Constraint added")

            
