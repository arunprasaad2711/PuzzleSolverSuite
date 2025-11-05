def AntiKnightConstraints(self):
        
    '''
    Anti-knight constraint. Two cells that are a knight's move apart must be unique.
    '''
    
    # Define knight's moves
    knight_moves = [
        (-2, -1), (-2, 1), (2, -1), (2, 1),
        (-1, -2), (-1, 2), (1, -2), (1, 2)
    ]

    # Anti-knight constraints
    for i in range(self.Rows):
        for j in range(self.Cols):
            for move in knight_moves:
                ni, nj = i + move[0], j + move[1]
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    self.Model.Add(self.Cells[i][j] != self.Cells[ni][nj])
    
    print("Anti-Knight constraints added.")

def AntiKingConstraints(self):
    
    '''
    Anti-king constraint. Two cells that are a king's move apart must be unique.
    '''
    
    # Define king's moves
    king_moves = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Anti-king constraints
    for i in range(self.Rows):
        for j in range(self.Cols):
            for move in king_moves:
                ni, nj = i + move[0], j + move[1]
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                    self.Model.Add(self.Cells[i][j] != self.Cells[ni][nj])
    
    print("Anti-King constraints added.")