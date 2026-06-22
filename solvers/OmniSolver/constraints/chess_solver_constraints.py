def ChessRowConstraint(self):
    
    print(f"{self.Rows}")
    # Collect all rows and columns separately.
    for i in range(self.Rows):
        RowCollection = []
        
        for j in range(self.Cols):
            RowCollection.append(self.Cells[i][j])
        
        # Put a condition that you can have only 1 piece in every row
        self.Model.Add(sum(RowCollection) == 1)
    
    print("Chess Row Collections Added")

def ChessColConstraint(self):
    
    # Collect all rows and columns separately.
    for i in range(self.Rows):
        ColCollection = []
        
        for j in range(self.Cols):
            ColCollection.append(self.Cells[j][i])
        
        # Put a condition that you can have only 1 piece in every column
        self.Model.Add(sum(ColCollection) == 1)
    
    print("Chess Column Rook Collections Added")

def NQueensConstraint(self):
    
    self.ChessRowConstraint()
    self.ChessColConstraint()
    self.ChessDiagonalAntiDiagonalConstraint()
    
    print(f"{self.Order} Queens Constraints Added.")

def NRooksConstraint(self):
    
    self.ChessRowConstraint()
    self.ChessColConstraint()
    
    print(f"{self.Order} Rooks Constraints Added.")

def NBishopsConstraint(self, RowConstraint=False):
    
    if RowConstraint:
        self.ChessRowConstraint()
        self.ChessDiagonalAntiDiagonalConstraint()
        
        print(f"{self.Order} Bishops on {self.Order} Rows Constraints Added.")
    else:
        self.ChessColConstraint()
        self.ChessDiagonalAntiDiagonalConstraint()
        
        print(f"{self.Order} Bishops on {self.Order} Cols Constraints Added.")

def ChessDiagonalAntiDiagonalConstraint(self):
    
    # Get all the Anti-Diagonals and Diagonals and set their sum to be utmost 1
    for i in range(0, self.Order):
        AntiDiagonals = self.DiagonalTRBL_ids(0, i)
        # print(i, AntiDiagonals)
        
        Cells = [self.Cells[r][c] for r, c in AntiDiagonals]
        self.Model.Add(sum(Cells) <= 1)
    
    for i in range(1, self.Order):
        AntiDiagonals = self.DiagonalTRBL_ids(i, self.Order-1)
        # print(i, AntiDiagonals)
        
        Cells = [self.Cells[r][c] for r, c in AntiDiagonals]
        self.Model.Add(sum(Cells) <= 1)
    
    for i in range(self.Order-1, -1, -1):
        Diagonals = self.DiagonalTLBR_ids(i, 0)
        # print(i, Diagonals)
        
        Cells = [self.Cells[r][c] for r, c in Diagonals]
        self.Model.Add(sum(Cells) <= 1)
    
    for i in range(1, self.Order):
        Diagonals = self.DiagonalTLBR_ids(0, i)
        # print(i, Diagonals)
        
        Cells = [self.Cells[r][c] for r, c in Diagonals]
        self.Model.Add(sum(Cells) <= 1)
    
    print("Diagonal/Anti-Diagonal Bishop Collections Added")

def DiagonalTRBL_ids(self, RowID, ColID):
    
    IDs = []
    
    x, y = RowID, ColID
    while x <= self.Rows - 1 and y >= 0:
        IDs.append((x, y))
        x += 1
        y -= 1
    
    return IDs

def DiagonalTLBR_ids(self, RowID, ColID):
    
    IDs = []
    
    x, y = RowID, ColID
    while x <= self.Rows - 1 and y <= self.Cols - 1:
        IDs.append((x, y))
        x += 1
        y += 1
    
    return IDs