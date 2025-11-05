def SandwichConstraints(self, RowSums, ColSums, LowNumber=1, HighNumber=9):
            
    # Sandwich constraints along a Row
    # Scan through each row one-by-one
    for i, RowSum in enumerate(RowSums):
        
        if RowSum == None:
            continue
        
        MasterConditions = []
        
        # Scan left-to-right for the left cell containing LowNumber/HighNumber
        for j in range(self.Cols - 1):
            
            LeftCell = self.Cells[i][j]
            
            # Condition to see if the left cell is a high value in cell (i,j)
            LeftCellHighCondition = self.Model.NewBoolVar(f"SandwichLeftValHigh_Row_{i}_{j}")
            
            # Condition to see if the left cell is a low value in cell (i,j)
            LeftCellLowCondition = self.Model.NewBoolVar(f"SandwichLeftValLow_Row_{i}_{j}")
            
            # Only enforce this if the left cell is a high/Low value
            self.Model.Add(LeftCell == HighNumber).OnlyEnforceIf(LeftCellHighCondition)
            self.Model.Add(LeftCell == LowNumber).OnlyEnforceIf(LeftCellLowCondition)
            
            # Scan left-to-right for the right cell containing LowNumber/HighNumber
            for k in range(j + 1, self.Cols):
                
                RightCell = self.Cells[i][k]
            
                # Condition to see if the right cell is a high value in cell (i,j)
                RightCellHighCondition = self.Model.NewBoolVar(f"SandwichRightValHigh_Row_{i}_{k}")
                
                # Condition to see if the right cell is a low value in cell (i,j)
                RightCellLowCondition = self.Model.NewBoolVar(f"SandwichRightValLow_Row_{i}_{k}")
                
                # Only enforce this if the right cell is a high/Low value
                self.Model.Add(RightCell == HighNumber).OnlyEnforceIf(RightCellHighCondition)
                self.Model.Add(RightCell == LowNumber).OnlyEnforceIf(RightCellLowCondition)
                
                # Add all the cells inbetween the potential low-high cells
                CellsBetween = self.Cells[i][j+1:k]
                
                # Boolean to keep track of sandwich sum
                SandwichSumCondition = self.Model.NewBoolVar(f"SandwichCondition_Row_{i}_{j}_{k}")

                # Enforce that sum of numbers between the bounds equals RowSum
                self.Model.Add(sum(CellsBetween) == RowSum).OnlyEnforceIf(SandwichSumCondition)
                
                # Define conditions for the SandwichSumCondition
                LeftLow_RightHigh = self.Model.NewBoolVar(f"LeftLow_RightHigh_Row_{i}_{j}_{k}")
                self.Model.AddBoolAnd([LeftCellLowCondition, RightCellHighCondition]).OnlyEnforceIf(LeftLow_RightHigh)

                LeftHigh_RightLow = self.Model.NewBoolVar(f"LeftHigh_RightLow_Row_{i}_{j}_{k}")
                self.Model.AddBoolAnd([LeftCellHighCondition, RightCellLowCondition]).OnlyEnforceIf(LeftHigh_RightLow)
                
                # Combine both into the SandwichSumCondition
                self.Model.AddBoolOr([LeftLow_RightHigh, LeftHigh_RightLow]).OnlyEnforceIf(SandwichSumCondition)

                # Collect all possible master conditions for the row
                MasterConditions.append(SandwichSumCondition)
        
        # Among all the permutations possible, atleast one condition must be true
        self.Model.AddBoolOr(MasterConditions)
        
        print(f"Sandwich Row Condition for Row {i} with sum {RowSum} added")
    
    # Scan through each column one-by-one
    for i, ColSum in enumerate(ColSums):
        
        if ColSum == None:
            continue
        
        MasterConditions = []
        
        # Scan top-to-bottom for the top cell containing LowNumber/HighNumber
        for j in range(self.Rows - 1):
            
            TopCell = self.Cells[j][i]
            
            # Condition to see if the Top cell is a high value in cell (j,i)
            TopCellHighCondition = self.Model.NewBoolVar(f"SandwichTopValHigh_Col_{j}_{i}")
            
            # Condition to see if the Top cell is a low value in cell (j,i)
            TopCellLowCondition = self.Model.NewBoolVar(f"SandwichTopValLow_Col_{j}_{i}")
            
            # Only enforce this if the top cell is a high/Low value
            self.Model.Add(TopCell == HighNumber).OnlyEnforceIf(TopCellHighCondition)
            self.Model.Add(TopCell == LowNumber).OnlyEnforceIf(TopCellLowCondition)
            
            # Scan top-to-bottom for the bottom cell containing LowNumber/HighNumber
            for k in range(j + 1, self.Rows):
                
                BottomCell = self.Cells[k][i]
            
                # Condition to see if the bottom cell is a high value in cell (k,i)
                BottomCellHighCondition = self.Model.NewBoolVar(f"SandwichBottomValHigh_Col_{k}_{i}")
                
                # Condition to see if the bottom cell is a low value in cell (k,i)
                BottomCellLowCondition = self.Model.NewBoolVar(f"SandwichBottomValLow_Col_{k}_{i}")
                
                # Only enforce this if the bottom cell is a high/Low value
                self.Model.Add(BottomCell == HighNumber).OnlyEnforceIf(BottomCellHighCondition)
                self.Model.Add(BottomCell == LowNumber).OnlyEnforceIf(BottomCellLowCondition)
                
                # Add all the cells inbetween the potential low-high cells
                CellsBetween = [self.Cells[row][i] for row in range(j+1, k)]
                
                # Boolean to keep track of sandwich sum
                SandwichSumCondition = self.Model.NewBoolVar(f"SandwichCondition_Col_{i}_{j}_{k}")

                # Enforce that sum of numbers between the bounds equals RowSum
                self.Model.Add(sum(CellsBetween) == ColSum).OnlyEnforceIf(SandwichSumCondition)
                
                # Define conditions for the SandwichSumCondition
                TopLow_BottomHigh = self.Model.NewBoolVar(f"TopLow_BottomHigh_Col_{i}_{j}_{k}")
                self.Model.AddBoolAnd([TopCellLowCondition, BottomCellHighCondition]).OnlyEnforceIf(TopLow_BottomHigh)

                TopHigh_BottomLow = self.Model.NewBoolVar(f"TopHigh_BottomLow_Col_{i}_{j}_{k}")
                self.Model.AddBoolAnd([TopCellHighCondition, BottomCellLowCondition]).OnlyEnforceIf(TopHigh_BottomLow)
                
                # Combine both into the SandwichSumCondition
                self.Model.AddBoolOr([TopLow_BottomHigh, TopHigh_BottomLow]).OnlyEnforceIf(SandwichSumCondition)

                # Collect all possible master conditions for the column
                MasterConditions.append(SandwichSumCondition)
        
        # Among all the permutations possible, atleast one condition must be true
        self.Model.AddBoolOr(MasterConditions)
        
        print(f"Sandwich Column Condition for Column {i} with sum {ColSum} added")
