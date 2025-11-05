def RatioPairs(self, numerators, denominators, pairs):
    """
    Adds constraints to enforce specific ratios between pairs of cells in either direction.
    
    Example Puzzle: https://www.youtube.com/watch?v=gvi2UEgEjDE

    Args:
        numerators (list): List of numerators for the ratio constraints.
        denominators (list): List of denominators for the ratio constraints.
        pairs (list): List of tuples, where each tuple contains two cell coordinates (row, col) 
                    specifying the cells that must satisfy the ratio.
    """
    
    if len(numerators) != len(denominators) or len(numerators) != len(pairs):
        raise ValueError("Numerators, denominators, and pairs must have the same length.")
    
    for idx, (numerator, denominator, pair) in enumerate(zip(numerators, denominators, pairs)):
        if denominator == 0:
            raise ValueError(f"Denominator cannot be zero for ratio constraint at index {idx}.")
        
        # Extract the coordinates of the two cells
        (row1, col1), (row2, col2) = pair
        cell1 = self.Cells[row1][col1]
        cell2 = self.Cells[row2][col2]

        # Debug information
        print(f"Adding ratio constraint {idx + 1}: "
            f"Cell ({row1}, {col1}) and Cell ({row2}, {col2}) with ratio {numerator}/{denominator}")
        
        # Create boolean variables for the two possible conditions
        condition1 = self.Model.NewBoolVar(f"condition1_ratio_{idx}")
        condition2 = self.Model.NewBoolVar(f"condition2_ratio_{idx}")

        # Add ratio constraints for both conditions
        self.Model.Add(numerator * cell2 == denominator * cell1).OnlyEnforceIf(condition1)
        self.Model.Add(numerator * cell1 == denominator * cell2).OnlyEnforceIf(condition2)

        # At least one of the conditions must hold
        self.Model.AddBoolOr([condition1, condition2])

        # Debug each condition explicitly
        print(f"Condition 1: {numerator} * Cell({row2}, {col2}) == {denominator} * Cell({row1}, {col1})")
        print(f"Condition 2: {numerator} * Cell({row1}, {col1}) == {denominator} * Cell({row2}, {col2})")

def DifferencePairs(self, differences, pairs):
    """
    Adds constraints to enforce specific differences between pairs of cells in either direction.
    
    Example Puzzle: https://www.youtube.com/watch?v=gvi2UEgEjDE
    
    Args:
        differences (list): List of differences for the difference constraints.
        pairs (list): List of tuples, where each tuple contains two cell coordinates (row, col) 
                    specifying the cells that must satisfy the difference.
    """
    
    if len(differences) != len(pairs):
        raise ValueError("Differences and pairs must have the same length.")
    
    for idx, (difference, pair) in enumerate(zip(differences, pairs)):
        
        # Extract the coordinates of the two cells
        (row1, col1), (row2, col2) = pair
        cell1 = self.Cells[row1][col1]
        cell2 = self.Cells[row2][col2]

        # Debug information
        print(f"Adding Difference constraint {idx + 1}: "
            f"|Cell ({row1}, {col1}) - Cell ({row2}, {col2}) = {difference}|")
        
        # Create boolean variables for the two possible conditions
        condition1 = self.Model.NewBoolVar(f"condition1_difference_{idx}")
        condition2 = self.Model.NewBoolVar(f"condition2_difference_{idx}")

        # Add enforce constraints for both conditions
        self.Model.Add(cell1 - cell2 == difference).OnlyEnforceIf(condition1)
        self.Model.Add(cell2 - cell1 == difference).OnlyEnforceIf(condition2)

        # At least one of the conditions must hold
        self.Model.AddBoolOr([condition1, condition2])

    print(f"Total {len(pairs)} difference constraints added.")

def AdditionPairs(self, sums, pairs):
    """
    Addition Pairs: Sum of a pair of cells is equal to a value. This is applicable
    for XV sudokus as well.

    Args:
        sums (list): list containing the sum of the pair of cells
        pairs (list of tuples): list of all pairs using the constraint
    """
    
    if len(sums) != len(pairs):
        raise ValueError("Sums and pairs must have the same length.")
    
    for idx, (addition, pair) in enumerate(zip(sums, pairs)):
        
        # Extract the coordinates of the two cells
        (row1, col1), (row2, col2) = pair
        cell1 = self.Cells[row1][col1]
        cell2 = self.Cells[row2][col2]

        # Add enforce constraint for the condition
        self.Model.Add(cell1 + cell2 == addition)
        
        print(f"Addition constraint {idx + 1} for {(row1, col1)} + {(row2, col2)} = {addition} added.")

    print(f"Total {len(pairs)} addition pair constraints added.")

def MultiAdditionPairs(self, sums, pairs):
    
    if len(sums) != len(pairs):
        raise ValueError("Sums and pairs must have the same length.")
    
    for idx, (addition_sums, pair) in enumerate(zip(sums, pairs)):
        
        # Extract the coordinates of the two cells
        (row1, col1), (row2, col2) = pair
        cell1 = self.Cells[row1][col1]
        cell2 = self.Cells[row2][col2]
        
        # For each possible sum the pair can have, create a boolean that checks if the addition is valid
        Addition_Conditions = []
        for addition_sum in addition_sums:
            condition = self.Model.NewBoolVar(f"Multi_Addition_Sum_{addition_sum}_{idx}")
            # Add enforce constraint for the condition
            self.Model.Add(cell1 + cell2 == addition_sum).OnlyEnforceIf(condition)
            Addition_Conditions.append(condition)
        
        # Ensure that the sums of the cells matches exactly one sum
        self.Model.AddBoolOr(Addition_Conditions)

    print(f"Total {len(pairs)} Multi-Addition-Sum constraints added.")  
    
def RatioPairsOrDifferencePairs(self, numerators, denominators, differences, pairs):
    
    """
    Adds constraints to enforce specific differences between pairs of cells in either direction.
    or the numbers are in ratio m:n or n:m or both.
    
    Example Puzzle: https://www.youtube.com/watch?v=le1pe4WMGZY
    """
    if len(differences) != len(pairs) or len(numerators) != len(pairs) or len(denominators) != len(pairs):
        raise ValueError("Differences/Numerators/Denominators and pairs must have the same length.")
    
    for idx, (difference, numerator, denominator, pair) in enumerate(zip(differences, numerators, denominators, pairs)):
        
        # Extract the coordinates of the two cells
        (row1, col1), (row2, col2) = pair
        cell1 = self.Cells[row1][col1]
        cell2 = self.Cells[row2][col2]

        # Debug information
        print(f"Adding Difference constraint {idx + 1}: "
            f"|Cell ({row1}, {col1}) - Cell ({row2}, {col2}) = {difference}|")
        
        # Create boolean variables for the two possible conditions
        condition1 = self.Model.NewBoolVar(f"condition1_difference_{idx}")
        condition2 = self.Model.NewBoolVar(f"condition2_difference_{idx}")

        # Add enforce constraints for both conditions
        self.Model.Add(cell1 - cell2 == difference).OnlyEnforceIf(condition1)
        self.Model.Add(cell2 - cell1 == difference).OnlyEnforceIf(condition2)
        
        # Create boolean variables for the two possible conditions
        condition3 = self.Model.NewBoolVar(f"condition1_ratio_{idx}")
        condition4 = self.Model.NewBoolVar(f"condition2_ratio_{idx}")

        # Add enforce constraints for both conditions
        self.Model.Add(numerator * cell2 == denominator * cell1).OnlyEnforceIf(condition3)
        self.Model.Add(numerator * cell1 == denominator * cell2).OnlyEnforceIf(condition4)

        # At least one of the conditions must hold
        self.Model.AddBoolOr([condition1, condition2, condition3, condition4])
