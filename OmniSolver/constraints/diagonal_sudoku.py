def TLBR_DiagonalConstraint(self):
        
    '''
    Diagonal (Top-left to bottom-right) is unique and contain the digits 1 to n.
    '''
     
    # Add Main Diagonal Constraint
    diagonal = [self.Cells[i][i] for i in range(self.Rows)]
    self.Model.AddAllDifferent(diagonal)
    
    print("TLBR Diagonal constraint added.")

def TRBL_DiagonalConstraint(self):
    
    '''
    Diagonal (Top-right to bottom-left) is unique and contain the digits 1 to n.
    '''
    
    # Add Anti-Diagonal Constraint
    diagonal = [self.Cells[i][self.Rows - 1 - i] for i in range(self.Rows)]
    self.Model.AddAllDifferent(diagonal)

    print("TRBL Diagonal constraint added.")