def LineDifferences(self, differences, difference_conditions, lines, linecolour=None, loop=False):
        
    '''
    Line Difference Conditions.
    
    Cells along the given lines must be atleast/equal/utmost the given differences.
    If Line difference is atleast 5, then it becomes a German Whispher condition.
    
    If the differences are 5 or above - this becomes German Whisphers
    If the differences are 4 or above - this becomes Dutch Whisphers
    
    Example Puzzle: https://www.youtube.com/watch?v=HMdV3F5wK48
    
    Args:
        differences (list): list of difference values for each line
        difference_conditions (list): list of numbers indicating if the difference should be
        greater than, equal to, or less than the differences
        lines (list): list of lists containing the line of cells.
    '''
    
    for idx, (diff, diff_con, line) in enumerate(zip(differences, difference_conditions, lines)):
        
        diff_string = ""
        if diff_con == 1:
            diff_string = "greater than" 
        elif diff_con == -1:
            diff_string = "less than"
        elif diff_con == 0:
            diff_string = "equal to"
        else:
            diff_string = "ERROR!"
        
        LineLength = len(line)
        
        for i in range(LineLength - 1):
            (r1, c1), (r2, c2) = line[i], line[i + 1]
            
            cell1 = self.Cells[r1][c1]
            cell2 = self.Cells[r2][c2]
            
            # Create boolean variables for the two possible conditions
            # Forward difference and Reverse Difference
            condition1 = self.Model.NewBoolVar(f"condition1_difference_{idx}_{r1}_{c1}")
            condition2 = self.Model.NewBoolVar(f"condition2_difference_{idx}_{r1}_{c1}")
            
            # Add enforce constraints for both conditions
            if diff_con == 1:
                self.Model.Add(cell1 - cell2 >= diff).OnlyEnforceIf(condition1)
                self.Model.Add(cell2 - cell1 >= diff).OnlyEnforceIf(condition2)
            elif diff_con == 0:
                self.Model.Add(cell1 - cell2 == diff).OnlyEnforceIf(condition1)
                self.Model.Add(cell2 - cell1 == diff).OnlyEnforceIf(condition2)
            elif diff_con == -1:
                self.Model.Add(cell1 - cell2 <= diff).OnlyEnforceIf(condition1)
                self.Model.Add(cell2 - cell1 <= diff).OnlyEnforceIf(condition2)
            
            # At least one of the conditions must hold
            self.Model.AddBoolOr([condition1, condition2])
            
        print(f"Line Difference condition {idx + 1} with difference {diff_string} {diff} added.")

def RenbanLinesConstraints(self, lines, linecolour=None, loop=False, TreatAsCells=False):
    
    '''
    Renban Sudoku Conditions.
    
    Cells along the given lines must be consecutive and non-repeating in any order
    
    Example Puzzle: https://www.youtube.com/watch?v=DtZRGc9ej3w
    '''
    
    for I, line in enumerate(lines):
        
        UniqueCells = list(set([(i, j) for i, j in line]))
        Cells = [self.Cells[i][j] for i, j in UniqueCells]
        
        # Add the Uniqueness condition
        self.Model.AddAllDifferent(Cells)
        
        PairDifferences = []
        for i in range(len(Cells)):
            for j in range(len(Cells)):
                RenbanDiffForward = self.Model.NewBoolVar(f"RenbanDiff_Forward{I}_{i}_{j}")
                RenbanDiffBackward = self.Model.NewBoolVar(f"RenbanDiff_Backward{I}_{i}_{j}")
                self.Model.Add(Cells[i] == Cells[j] + 1).OnlyEnforceIf(RenbanDiffForward)
                self.Model.Add(Cells[j] == Cells[i] + 1).OnlyEnforceIf(RenbanDiffBackward)
                PairDifferences.append(RenbanDiffForward)
                PairDifferences.append(RenbanDiffBackward)
        self.Model.Add(sum(PairDifferences) == 2*len(Cells) - 2)
        
    print("Renban Conditions Added")

def WarpingRenbanLinesConstraints(self, LineSet1, LineSet2, linecolour=None):
    
    '''
    Warping Renban Lines
    
    Lines in either sets of lines can be individual renban lines or pair up with their corresponding
    line pair to form a bigger line that obeys renban condition
    
    Example Puzzle: https://www.youtube.com/watch?v=SYSS_GD-vaU
    '''
    
    for I, (line1, line2) in enumerate(zip(LineSet1, LineSet2)):
        
        UniqueCells1 = list(set([(i, j) for i, j in line1]))
        Cells1 = [self.Cells[i][j] for i, j in UniqueCells1]
        
        UniqueCells2 = list(set([(i, j) for i, j in line2]))
        Cells2 = [self.Cells[i][j] for i, j in UniqueCells2]
        
        Cells3 = Cells1 + Cells2
        
        # Add the Uniqueness condition for each line - regardless of
        # being a standalone renban line, they have distinct numbers
        # self.Model.AddAllDifferent(Cells1)
        # self.Model.AddAllDifferent(Cells2)
        
        # Run Renban Test for line 1
        PairDifferences1 = []
        WarpingRenbanLine1 = self.Model.NewBoolVar(f"WarpingRenbanSet1_{I}")
        
        for i in range(len(Cells1)):
            for j in range(len(Cells1)):
                RenbanDiffForward = self.Model.NewBoolVar(f"WarpingRenbanDiff1_Forward{I}_{i}_{j}")
                RenbanDiffBackward = self.Model.NewBoolVar(f"WarpingRenbanDiff1_Backward{I}_{i}_{j}")
                self.Model.Add(Cells1[i] == Cells1[j] + 1).OnlyEnforceIf(RenbanDiffForward)
                self.Model.Add(Cells1[j] == Cells1[i] + 1).OnlyEnforceIf(RenbanDiffBackward)
                PairDifferences1.append(RenbanDiffForward)
                PairDifferences1.append(RenbanDiffBackward)
        
        # enforce the renban condition on the line if WarpingRenbanLine1 is True
        self.Model.AddAllDifferent(Cells1).OnlyEnforceIf(WarpingRenbanLine1)
        self.Model.Add(sum(PairDifferences1) == 2*len(Cells1) - 2).OnlyEnforceIf(WarpingRenbanLine1)
        
        # Run Renban Test for line 2
        PairDifferences2 = []
        WarpingRenbanLine2 = self.Model.NewBoolVar(f"WarpingRenbanSet2_{I}")
        
        for i in range(len(Cells2)):
            for j in range(len(Cells2)):
                RenbanDiffForward = self.Model.NewBoolVar(f"WarpingRenbanDiff2_Forward{I}_{i}_{j}")
                RenbanDiffBackward = self.Model.NewBoolVar(f"WarpingRenbanDiff2_Backward{I}_{i}_{j}")
                self.Model.Add(Cells2[i] == Cells2[j] + 1).OnlyEnforceIf(RenbanDiffForward)
                # self.Model.Add(Cells2[i] != Cells2[j] + 1).OnlyEnforceIf(RenbanDiffForward.Not())
                self.Model.Add(Cells2[j] == Cells2[i] + 1).OnlyEnforceIf(RenbanDiffBackward)
                # self.Model.Add(Cells2[j] != Cells2[i] + 1).OnlyEnforceIf(RenbanDiffBackward.Not())
                PairDifferences2.append(RenbanDiffForward)
                PairDifferences2.append(RenbanDiffBackward)
        
        # enforce the renban condition on the line if WarpingRenbanLine3 is True
        self.Model.AddAllDifferent(Cells2).OnlyEnforceIf(WarpingRenbanLine2)
        self.Model.Add(sum(PairDifferences2) == 2*len(Cells2) - 2).OnlyEnforceIf(WarpingRenbanLine2)
        
        # Run Renban Test for line 3 - the combined line 1 and 2
        PairDifferences3 = []
        
        for i in range(len(Cells3)):
            for j in range(len(Cells3)):
                RenbanDiffForward = self.Model.NewBoolVar(f"WarpingRenbanDiff3_Forward{I}_{i}_{j}")
                RenbanDiffBackward = self.Model.NewBoolVar(f"WarpingRenbanDiff3_Backward{I}_{i}_{j}")
                self.Model.Add(Cells3[i] == Cells3[j] + 1).OnlyEnforceIf(RenbanDiffForward)
                # self.Model.Add(Cells3[i] != Cells3[j] + 1).OnlyEnforceIf(RenbanDiffForward.Not())
                self.Model.Add(Cells3[j] == Cells3[i] + 1).OnlyEnforceIf(RenbanDiffBackward)
                # self.Model.Add(Cells3[j] != Cells3[i] + 1).OnlyEnforceIf(RenbanDiffBackward.Not())
                PairDifferences3.append(RenbanDiffForward)
                PairDifferences3.append(RenbanDiffBackward)
                            
        # Check if both the lines are Renban or not
        DoubleRenban = self.Model.NewBoolVar(f"WarpingDoubleRenban_{I}")
        self.Model.AddBoolAnd([WarpingRenbanLine1, WarpingRenbanLine2]).OnlyEnforceIf(DoubleRenban)
        
        # Condition for Line 3 to be a Renban - Both the unique entries and difference condtions must be valid
        RenbanLine3Condition = self.Model.NewBoolVar(f"WarpingRenbanLine3_Condition{I}")
        self.Model.Add(sum(PairDifferences3) == 2*len(Cells3) - 2).OnlyEnforceIf(RenbanLine3Condition)
        self.Model.AddAllDifferent(Cells3).OnlyEnforceIf(RenbanLine3Condition)
        
        # Condition for Warped Renban:
        # Line 1 or Line 2 or both are not Renbans -> Line 3 must be a Renban
        # Both lines are Renbans -> Line 3 might not be a Renban
        self.Model.Add(sum([RenbanLine3Condition, DoubleRenban]) >=1)
    
    print("Warping Renban Line Constraints Added")

def NabnerLinesConstraints(self, lines, linecolour=None, loop=False, TreatAsCells=False):
    
    '''
    Nabner Sudoku Conditions.
    
    Cells along the given lines must be non-consecutive and non-repeating in any order
    
    Example Puzzle: https://www.youtube.com/watch?v=x7mZpCjcccs
    '''
    
    for I, line in enumerate(lines):
        
        UniqueCells = list(set([(i, j) for i, j in line]))
        Cells = [self.Cells[i][j] for i, j in UniqueCells]
        
        # Add the Uniqueness condition
        self.Model.AddAllDifferent(Cells)
        
        PairDifferences = []
        for i in range(len(Cells)):
            for j in range(len(Cells)):
                NabnerDiffForward = self.Model.NewBoolVar(f"NabnerDiff_Forward{I}_{i}_{j}")
                NabnerDiffBackward = self.Model.NewBoolVar(f"NabnerDiff_Backward{I}_{i}_{j}")
                self.Model.Add(Cells[i] == Cells[j] + 1).OnlyEnforceIf(NabnerDiffForward)
                self.Model.Add(Cells[i] != Cells[j] + 1).OnlyEnforceIf(NabnerDiffForward.Not())
                self.Model.Add(Cells[j] == Cells[i] + 1).OnlyEnforceIf(NabnerDiffBackward)
                self.Model.Add(Cells[j] != Cells[i] + 1).OnlyEnforceIf(NabnerDiffBackward.Not())
                PairDifferences.append(NabnerDiffForward)
                PairDifferences.append(NabnerDiffBackward)
        self.Model.Add(sum(PairDifferences) == 0)
        
    print("Nabner Conditions Added")

def PalindromeLineConstraints(self, Lines):
        
    '''
    Each line of cells are palindromes. They read the same from left-right and right-left
    '''
    
    for Line in Lines:
        # Extract all the cells 
        Cells = [self.Cells[i][j] for i, j in Line]
        
        # Find the mid point index of the palindrome line
        MidRangeValue = 0
        if len(Cells) % 2 == 0:
            MidRangeValue = (len(Cells) + 1) // 2
        else:
            MidRangeValue = len(Cells) // 2
        
        # Assign the palindrome condition
        for i in range(MidRangeValue):
            self.Model.Add(Cells[i] == Cells[-i-1])

    print("Palindrome Line Constraint added")

