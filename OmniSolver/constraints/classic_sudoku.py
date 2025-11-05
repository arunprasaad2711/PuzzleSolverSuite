import numpy as np

def ClassicSudokuConstraints(self):
        
    '''
    Classic Sudoku Constraints: All rows/cols/subgrids must be unique. Add givens
    '''
    self.SudokuRowConstraints()
    self.SudokuColConstraints()
    self.SudokuSubGridConstraints()
    self.InitializeGivenEntries()
    
    print("Classic Constraints added.")
    
def SudokuRowConstraints(self):
    
    '''
    Row Sudoku Constraints: All rows must contain unique entries
    '''
    
    # Add Row Constraints
    for i in range(self.Rows):
        RowCollection = []
        
        for j in range(self.Cols):
            RowCollection.append(self.Cells[i][j])
        
        self.Model.AddAllDifferent(RowCollection)
    
    print("Row constraints added.")
    
def SudokuColConstraints(self):
    
    '''
    Column Sudoku Constraints: All columns must contain unique entries
    '''
    
    # Add Column Constraints
    for i in range(self.Rows):
        ColCollection = []
        
        for j in range(self.Cols):    
            ColCollection.append(self.Cells[j][i])
        
        self.Model.AddAllDifferent(ColCollection)
    
    print("Column constraints added.")

def LatinSquares(self):
    
    '''
    Classic Latin Squares Constraint. All rows and columns must contain unique entries
    '''
    
    self.SudokuRowConstraints()
    self.SudokuColConstraints()
    self.InitializeGivenEntries()
    
    print("Latin Squares Constraints added.")

def GenerateClassicSubgridMap(self):
    
    SubGridMap = np.zeros((self.Rows, self.Cols), np.int32)
    
    for i in range(self.Rows):
        for j in range(self.Cols):
            subgrid_row = i // self.OrderRow
            subgrid_col = j // self.OrderCol
            subgrid_id = subgrid_row * (self.FullOrder // self.OrderCol) + subgrid_col + 1
            SubGridMap[i, j] = subgrid_id
    
    return SubGridMap

def SudokuSubGridConstraints(self):
    
    '''
    Subgrid Sudoku Constraints: All subgrids must contain unique entries
    '''
    
    # Add SubGrid Constraints
    for I in range(self.OrderCol):
        for J in range(self.OrderRow):
            subgrid = [ self.Cells[I * self.OrderRow + i][J * self.OrderCol + j] 
                        for i in range(self.OrderRow) for j in range(self.OrderCol) ]
            self.Model.AddAllDifferent(subgrid)
    
    self.SubgridMap = self.GenerateClassicSubgridMap()
    
    print("SubGrid constraints added.")

def SudokuCustomGridConstraints(self, SubGridMap):
    
    '''
    Custom Subgrid Sudoku Constraints: Here, the subgrids are not standard
    OrderRow x OrderCol square/rectangular grids. They can take any custom shape.
    
    SubGridMap is a 2D NumPy array having the IDs of the subgrids. IDs range from 1-n
    indicating the cells belonging to the region/subgrid with IDs 1-n.
    
    0 is used to mark free cells - cells that do not belong to any subgrid/region
    '''
    
    # First, find all the unique entries in the SubGridMap
    UIDs = set()
    for i in range(self.Rows):
        for j in range(self.Cols):
            if SubGridMap[i, j] not in UIDs:
                UIDs.add(SubGridMap[i, j])
    
    # Remove 0 so that cells with 0 are not clubbed together as another group
    if 0 in UIDs:
        UIDs.remove(0)
    
    for entry in UIDs:
        subgrid = [ self.Cells[i][j] for i in range(self.Rows) 
                    for j in range(self.Cols) if entry == SubGridMap[i, j]]
        self.Model.AddAllDifferent(subgrid)
        print(f"Custom Subgrid with UID {entry} added.")
    
    self.SubgridMap = SubGridMap
    
    print("Custom SubGrid constraints added.")

def InitializeGivenEntries(self):
        
    '''
    Initial Value Constraints: Add the givens into the sudoku.
    '''
    # Add the Sudoku Problem Givens
    for i in range(self.Rows):
        for j in range(self.Cols):
            if self.InputMatrix[i, j] != 0:
                self.Model.Add(self.Cells[i][j] == self.InputMatrix[i, j])