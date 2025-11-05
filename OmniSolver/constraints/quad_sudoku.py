def QuadsConstraints(self, QuadsIDs, QuadsVals):
    '''
    Quadruple or Quad sudoku. Upto 4 given numbers must be present atleast once in the quaduple
    cells.
    Give ONLY the top-left corner cell ID in QuadsIDs. The remaining IDs will be calculated.
    '''
    
    # Iterate through all the values for each quad
    for vals, quad in zip(QuadsVals, QuadsIDs):
        
        # Extract the first cell - Top-Left corner
        I, J = quad
        # Create all the cells of the quaduple
        quads = [(I, J), (I, J + 1), (I + 1, J), (I + 1, J + 1)]
        self.QuadsIDs.append(quads)
        
        for k, val in enumerate(vals):
            ValInQuad_list = []
            # Take a value and check if it is present in a cell.
            for i, j in quads:
                ValInQuad = self.Model.NewBoolVar(f"val_{val}_in_{i}_{j}_{k}")
                self.Model.Add(self.Cells[i][j] == val).OnlyEnforceIf(ValInQuad)
                self.Model.Add(self.Cells[i][j] != val).OnlyEnforceIf(ValInQuad.Not())
                ValInQuad_list.append(ValInQuad)
            # the given value must be present in atleast 1 cell
            self.Model.AddBoolOr(ValInQuad_list)
                
    print("Quad/Quadruple Sudoku Constraints added")
