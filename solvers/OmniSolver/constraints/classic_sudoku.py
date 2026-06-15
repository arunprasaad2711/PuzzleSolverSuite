import numpy as np

def ClassicSudokuConstraints(self):
        
    '''
    Classic Sudoku Constraints: All rows/cols/subgrids must be unique. Add givens
    '''
    self.SudokuRowConstraints()
    self.SudokuColConstraints()
    self.SudokuSubGridConstraints()
    
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

def RowSumConstraints(self, RowSums):

    '''
    Sum of the row must be equal to some number

    eg: https://www.youtube.com/watch?v=6tYM2ClmjVo
    '''
    # Add Row Constraints
    for i, RowSum in zip(range(self.Rows), RowSums):
        RowCollection = []
        
        for j in range(self.Cols):
            RowCollection.append(self.Cells[i][j])
        
        self.Model.Add(sum(RowCollection) == RowSum)
    
    print("RowSum Constraints Added.")
    
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

def ColSumConstraints(self, ColSums):
    
    '''
    Sum of the column must be equal to some number

    eg: https://www.youtube.com/watch?v=6tYM2ClmjVo
    '''
    
    # Add Column Constraints
    for i, ColSum in zip(range(self.Rows), ColSums):
        ColCollection = []
        
        for j in range(self.Cols):    
            ColCollection.append(self.Cells[j][i])
        
        self.Model.Add(sum(ColCollection) == ColSum)
    
    print("ColSum constraints added.")


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
            subgrid_id = subgrid_row * (self.Rows // self.OrderCol) + subgrid_col + 1
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
    
    self.SubGridMap = self.GenerateClassicSubgridMap()
    
    print("SubGrid constraints added.")

def SubGridSumConstraints(self, SubGridSums):
    
    '''
    Sum of the subgrid must be equal to some number

    eg: https://www.youtube.com/watch?v=6tYM2ClmjVo
    '''
    
    # Add SubGrid Constraints
    K = 0
    for I in range(self.OrderCol):
        for J in range(self.OrderRow):
            subgrid = [ self.Cells[I * self.OrderRow + i][J * self.OrderCol + j] 
                        for i in range(self.OrderRow) for j in range(self.OrderCol) ]
            self.Model.Add(sum(subgrid) == SubGridSums[K])
            K += 1
    
    print("SubGridSum Constraints Added.")

def SudokuCustomGridConstraints(self, SubGridMap):
    
    '''
    Custom Subgrid Sudoku Constraints: Here, the subgrids are not standard
    OrderRow x OrderCol square/rectangular grids. They can take any custom shape.
    
    SubGridMap is a 2D NumPy array having the IDs of the subgrids. IDs range from 1-n
    indicating the cells belonging to the region/subgrid with IDs 1-n.
    
    0 is used to mark free cells - cells that do not belong to any subgrid/region
    '''

    SubGridMap = np.array(SubGridMap, dtype=np.int32)
    
    # First, find all the unique entries in the SubGridMap
    UIDs = set()
    for i in range(self.Rows):
        for j in range(self.Cols):
            if SubGridMap[i, j] not in UIDs:
                UIDs.add(SubGridMap[i, j])
    print(UIDs)
    
    # Remove 0 so that cells with 0 are not clubbed together as another group
    if 0 in UIDs:
        UIDs.remove(0)
    
    for entry in UIDs:
        subgrid = [ self.Cells[i][j] for i in range(self.Rows) 
                    for j in range(self.Cols) if entry == SubGridMap[i, j]]
        self.Model.AddAllDifferent(subgrid)
        print(f"Custom Subgrid with UID {entry} added.")
    
    self.SubGridMap = SubGridMap
    
    print("Custom SubGrid constraints added.")

def InitializeGivenEntries(self):

    '''
    Initial Value Constraints: Add the givens into the sudoku.
    '''

    for i in range(self.Rows):
        for j in range(self.Cols):
            if self.InputMatrix[i, j] != 0:
                if self.InputMatrix[i, j] == self.ZeroMaskingDigit:
                    self.Model.Add(self.Cells[i][j] == 0)
                else:
                    self.Model.Add(self.Cells[i][j] == self.InputMatrix[i, j])