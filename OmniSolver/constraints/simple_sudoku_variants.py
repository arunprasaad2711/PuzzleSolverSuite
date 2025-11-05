def ArgyleConstraints(self):
        
    '''
    Marked diagonals must also have distinct entries
    '''
    
    ArgyleLines = [
        [(0, 4), (1, 5), (2, 6), (3, 7), (4, 8)],
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)],
        [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7)],
        [(4, 0), (5, 1), (6, 2), (7, 3), (8, 4)],
        [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)],
        [(7, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7)],
        [(8, 1), (7, 2), (6, 3), (5, 4), (4, 5), (3, 6), (2, 7), (1, 8)],
        [(8, 4), (7, 5), (6, 6), (5, 7), (4, 8)],
    ]
    
    for line in ArgyleLines:
        Cells = [self.Cells[i][j] for i, j in line]
        self.Model.AddAllDifferent(Cells)

def GirandolaConstraints(self):
    '''
    Girandola Constraints. The given 9 cells must also contain numbers 1-9
    '''
    GirandolaIDs = [
        (0, 0), (0, 8), (1, 4), (4, 1), (4, 4), (4, 7), (7, 4), (8, 0), (8, 8)
    ]
    
    Cells = [self.Cells[i][j] for i, j in GirandolaIDs]
    self.Model.AddAllDifferent(Cells)

def CentreDotConstraints(self):
    '''
    Centre Dot Constraints. The given 9 cells must also contain numbers 1-9
    '''
    CentreDotIDs = [
        (1, 1), (1, 4), (1, 7), (4, 1), (4, 4), (4, 7), (7, 1), (7, 4), (7, 7),
    ]
    
    Cells = [self.Cells[i][j] for i, j in CentreDotIDs]
    self.Model.AddAllDifferent(Cells)

def AsteriskConstraints(self):
    '''
    Asterisk Constraints. The given 9 cells must also contain numbers 1-9
    '''
    AsteriskIDs = [
        (2, 2), (1, 4), (2, 6), (4, 1), (4, 4), (4, 7), (6, 2), (7, 4), (6, 6),
    ]
    
    Cells = [self.Cells[i][j] for i, j in AsteriskIDs]
    self.Model.AddAllDifferent(Cells)