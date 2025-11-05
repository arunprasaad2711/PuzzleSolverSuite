def OddEvenConstraints(self, OddEvenMap):
    
    '''
    Constraints that specify that only odd/even numbers can exist in cell
    0 - any, 1 - odd, 2 - even
    '''
    
    for i in range(self.Rows):
        for j in range(self.Cols):
            parity = OddEvenMap[i, j]
            if parity == 1:
                self.Model.AddModuloEquality(1, self.Cells[i][j], 2)
            elif parity == 2:
                self.Model.AddModuloEquality(0, self.Cells[i][j], 2)
    
    print("Odd-Even Constraints added")

def OrthogonalNeighbouringSums(self, cells):
    
    '''
    The given cells are the sum of all the orthogonal neighbours
    
    eg: https://www.youtube.com/watch?v=MTAwIzxyad0
    '''
    
    for x, y in cells:
        Neighbours = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Orthogonally adjacent cells
            ni, nj = x + di, y + dj
            if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                Neighbours.append(self.Cells[ni][nj])
        self.Model.Add(self.Cells[x][y] == sum(Neighbours))
        print(f"Orthogonal Neighbouring Sum constaint added for cell {(x,y)}")

def RestrictedCellsConstraints(self, CellMap, CellValLists):
    
    '''
    Cells contain only specific values instead of all values.
    '''
    
    # First, find all the unique entries in the Map
    UIDs = set()
    for i in range(self.Rows):
        for j in range(self.Cols):
            if CellMap[i, j] not in UIDs:
                UIDs.add(CellMap[i, j])
    
    # Remove 0 so that cells with 0 are not clubbed together as another group
    if 0 in UIDs:
        UIDs.remove(0)
    
    # Loop through all the restricted entry cells
    for UID, CellValList in zip(UIDs, CellValLists):
        # Get all the cells pertaining to a given condition
        subgrid = [self.Cells[i][j] for i in range(self.Rows) for j in range(self.Cols) if UID == CellMap[i, j]]
        for i, cell in enumerate(subgrid):
            # Create a boolean value list
            CellBoolList = []
            for val in CellValList:
                # Enforce a boolean condition that the cell has to be the value in the cellvalue list
                CellBool = self.Model.NewBoolVar(f"Cell_{i}_UID_{UID}_isVal_{val}")
                self.Model.Add(cell==val).OnlyEnforceIf(CellBool)
                self.Model.Add(cell!=val).OnlyEnforceIf(CellBool.Not())
                CellBoolList.append(CellBool)
            # Ensure that atleast one of the boolean conditions should be true
            self.Model.AddBoolOr(CellBoolList)
            
        print(f"Restricted assignment for UID = {UID} with restricted values {CellValList} added")
    
def CloneRegions(self, Set1, Set2):
    '''
    Clone Regions. All the numbers in each region of set 1 appear in the
    exact positon in the corresponding region in set 2.
    
    Example puzzle: https://www.youtube.com/watch?v=3IM60jSmV6Y
    '''
    
    for (region1, region2) in zip(Set1, Set2):
        
        Cells1 = [self.Cells[i][j] for i, j in region1]
        Cells2 = [self.Cells[i][j] for i, j in region2]
        
        for cell1, cell2 in zip(Cells1, Cells2):
            self.Model.Add(cell1 == cell2)

def SameSetRegions(self, Set1, Set2):
    '''
    Same Set Regions. All the numbers in each region of set 1 appear in the corresponding
    region in set 2, but not necessarily in the same order.
    
    Example Puzzle: https://www.youtube.com/watch?v=OkDyZvHDoiA
    '''
    
    for idx, (region1, region2) in enumerate(zip(Set1, Set2)):
        
        Cells1 = [self.Cells[i][j] for i, j in region1]
        Cells2 = [self.Cells[i][j] for i, j in region2]
        
        Region1_Counters = []
        Region2_Counters = []
        
        # Run through all numbers 1-n
        for num in range(self.LowerBound, self.UpperBound+1):
            
            # In each cell, check if the cell is equal to the number
            Region1_numCounter = []
            Region2_numCounter = []
            
            for i in range(len(Cells1)):
                
                # This variable checks if the cell in the given position is equal to the number
                count_R1 = self.Model.NewBoolVar(f'count_R1_{num}_{idx}_pos_{i}')
                count_R2 = self.Model.NewBoolVar(f'count_R2_{num}_{idx}_pos_{i}')
                
                self.Model.Add(Cells1[i] == num).OnlyEnforceIf(count_R1)
                self.Model.Add(Cells1[i] != num).OnlyEnforceIf(count_R1.Not())
                self.Model.Add(Cells2[i] == num).OnlyEnforceIf(count_R2)
                self.Model.Add(Cells2[i] != num).OnlyEnforceIf(count_R2.Not())
                
                # This keeps record of all the occurrences of a number "num" in the cell
                Region1_numCounter.append(count_R1)
                Region2_numCounter.append(count_R2)
            
            # Count the number of occurrences of a number "num" in the regions.
            Region1_Counters.append(sum(Region1_numCounter))
            Region2_Counters.append(sum(Region2_numCounter))
            
        # Enforce equality of counts
        # That is, for two regions to have the same numbers - regardless of order
        # the counters for each number should be the same.
        for var1, var2 in zip(Region1_Counters, Region2_Counters):
            self.Model.Add(var1 == var2)
    
    print("Same Set Region Constraint added.")
