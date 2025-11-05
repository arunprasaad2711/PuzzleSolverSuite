import numpy as np

def SumpleteRowConstraints(self, RowSums):
    '''
    Sumplete Row Constraints. Sum of Row Values must be equal to the sum given
    '''
    
    for i, rowsum in enumerate(RowSums):
        
        if np.isnan(rowsum):
            continue
        
        RowProduct = [self.Cells[i][j]*self.InputMatrix[i, j] for j in range(self.Cols)]
        self.Model.Add(sum(RowProduct) == rowsum)
    
    print("Sumplete Row Constraints Added")

def SumpleteColConstraints(self, ColSums):
    
    '''
    Sumplete Column Constraints. Sum of Column Values must be equal to the sum given.
    '''
    
    for j, colsum in enumerate(ColSums):
        
        if colsum == None:
            continue
        
        RowProduct = [self.Cells[i][j]*self.InputMatrix[i, j] for i in range(self.Rows)]
        self.Model.Add(sum(RowProduct) == colsum)
    
    print("Sumplete Column Constraints Added")

def ClassicSumpleteConstraints(self, RowSums, ColSums):
    
    '''
    Classic Sumplete Constraints. Sum of numbers in any row/column should be equal to the
    corresponding given sums.
    '''
    
    self.SumpleteRowConstraints(RowSums)
    self.SumpleteColConstraints(ColSums)
    
    print("Sumplete Constraints Added")