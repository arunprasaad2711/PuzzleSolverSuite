def RowCountConstraint(self, count=2):
        
    '''
    Row count constraint. The sum of all cells in a row must be the given count.
    For star battle, the count is 2 by default.
    '''
    
    # Add Row Constraints
    for i in range(self.Rows):
        RowCollection = []
        
        for j in range(self.Cols):
            RowCollection.append(self.Cells[i][j])
        
        self.Model.Add(sum(RowCollection) == count)

def ColCountConstraint(self, count=2):
    
    '''
    Column count constraint. The sum of all cells in a column must be the given count.
    For star battle, the count is 2 by default.
    '''
    
    # Add Column Constraints
    for i in range(self.Rows):
        ColCollection = []
        
        for j in range(self.Cols):    
            ColCollection.append(self.Cells[j][i])
        
        self.Model.Add(sum(ColCollection) == count)

def ClassicNoriNoriConstraints(self):
    
    self.GridCountConstraints()
    self.NoriNoriAdjacencyConstraint()
    
    print("NoriNori Constraints Added!")

def ClassicStarBattleConstraints(self, stars=2):
    
    self.RowCountConstraint(stars)
    self.ColCountConstraint(stars)
    self.GridCountConstraints(stars)
    self.StarBattleAdjacencyConstraint()
    
    print("Star Battle Constraints Added!")

def GridCountConstraints(self, count=2):
    
    '''
    Grid/Region Constraints. Every Region can only have x Norinori/Starbattle cells.
    '''
    
    # First, find all the unique entries in the SubGridMap
    UIDs = set()
    for i in range(self.Rows):
        for j in range(self.Cols):
            if self.InputMatrix[i, j] not in UIDs:
                UIDs.add(self.InputMatrix[i, j])
    
    # Remove 0 so that cells with 0 are not clubbed together as another group
    if 0 in UIDs:
        UIDs.remove(0)
    
    for entry in UIDs:
        subgrid = [ self.Cells[i][j] for i in range(self.Rows) 
                    for j in range(self.Cols) if entry == self.InputMatrix[i, j]]
        self.Model.Add(sum(subgrid) == count)
        print(f"Custom Subgrid with UID {entry} added.")
    
    self.GridBoxBoundaryMaker()

def NoriNoriAdjacencyConstraint(self):
    
    '''
    Adjacency Constraints. If a cell is a norinori cell, then one of the orthogonally
    adjacent cell must also be a norinori cell so that norinoris form a domino
    '''
    
    for i in range(self.Rows):
        for j in range(self.Cols):
            Neighbours = []
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Orthogonally adjacent cells
                ni, nj = i + di, j + dj
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    Neighbours.append(self.Cells[ni][nj])

            IsNoriNori = self.Model.NewBoolVar(f"cell_{i}_{j}_is_norinori")
            
            # Add equivalence for `self.Cells[i][j] == 1` to `is_norinori`
            self.Model.Add(self.Cells[i][j] == 1).OnlyEnforceIf(IsNoriNori)
            self.Model.Add(self.Cells[i][j] != 1).OnlyEnforceIf(IsNoriNori.Not())

            # If the cell is a NoriNori cell, enforce exactly one neighbor is a NoriNori cell
            self.Model.Add(sum(Neighbours) == 1).OnlyEnforceIf(IsNoriNori)
            
    print("NoriNori Companion Cell Constraint Added")

def StarBattleAdjacencyConstraint(self):
    
    '''
    Adjacency Constraints. If a cell is a star cell, then none of the orthogonally and diagonally
    adjacent cells must be another star
    '''
    
    # Define neighbour's moves
    neighbour_moves = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Anti-king constraints
    for i in range(self.Rows):
        for j in range(self.Cols):
            Neighbours = []
            for move in neighbour_moves:
                ni, nj = i + move[0], j + move[1]
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    Neighbours.append(self.Cells[ni][nj])

            IsStar = self.Model.NewBoolVar(f"cell_{i}_{j}_is_star")
            
            # Add equivalence for `self.Cells[i][j] == 1` to `is_star`
            self.Model.Add(self.Cells[i][j] == 1).OnlyEnforceIf(IsStar)
            self.Model.Add(self.Cells[i][j] != 1).OnlyEnforceIf(IsStar.Not())

            # If the cell is a star cell, enforce none of the neighbours (orthogonal and adjacent)
            # are stars
            self.Model.Add(sum(Neighbours) == 0).OnlyEnforceIf(IsStar)
            
    print("Star Battle Star Cell Constraint Added")
