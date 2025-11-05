def KakurasuRowConstraints(self, RowSums):
        
    '''
    Kakurasu Row Constraints. The given sums are sum of the shaded cell's column index values
    '''
    
    self.LeftColumnNums = [i for i in range(1, len(RowSums) + 1)]
    self.RightColumnNums = RowSums
    
    for i, rowsum in enumerate(RowSums):
        if rowsum == None:
            continue
        Weights = [self.Cells[i][j] * (j + 1) for j in range(self.Cols)]
        self.Model.Add(sum(Weights) == rowsum)
    print("Kakurasu Row Constraints added")
    
def KakurasuColConstraints(self, ColSums):
    
    '''
    Kakurasu Column Constraints. The given sums are sum of the shaded cell's row index values
    '''
    
    self.TopRowNums = [i for i in range(1, len(ColSums) + 1)]
    self.BottomRowNums = ColSums
    
    for j, colsum in enumerate(ColSums):
        if colsum == None:
            continue
        Weights = [self.Cells[i][j] * (i + 1) for i in range(self.Rows)]
        self.Model.Add(sum(Weights) == colsum)
    print("Kakurasu Column Constraints added")

def ClassicKakurasuConstraints(self, RowSums, ColSums):
    
    '''
    Classic Kakurasu Problem constraints. The sum of the shaded cells' row/column indices must match
    the given row/column sums.
    '''
    
    self.KakurasuColConstraints(ColSums)
    self.KakurasuRowConstraints(RowSums)
    
    print("Classic Kakurasu Constraints added.")