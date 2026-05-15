import numpy as np

def ExtendedSudokuRowConstraint(self, Solutions, AllowedRepeats):

    FilteredSolutions = []
    AllValues = set(range(self.LowerBound, self.UpperBound + 1))

    for I, Solution in enumerate(Solutions):
        ExtendedRows = []

        for i in range(self.Rows):
            RowVals = sorted(AllValues - set(Solution[i]))
            ExtendedRows.append(tuple(RowVals))

        repeats = len(ExtendedRows) - len(set(ExtendedRows))

        if repeats == AllowedRepeats:
            FilteredSolutions.append(Solution)
            # print(f"For solution {I}, Filtered Solution = {Solution}")

    return FilteredSolutions

def ExtendedSudokuColConstraint(self, Solutions, AllowedRepeats):

    FilteredSolutions = []
    AllValues = set(range(self.LowerBound, self.UpperBound + 1))

    for Solution in Solutions:
        ExtendedCols = []

        for i in range(self.Cols):
            ColVals = sorted(AllValues - set(Solution[j][i] for j in range(self.Rows)))
            ExtendedCols.append(tuple(ColVals))

        repeats = len(ExtendedCols) - len(set(ExtendedCols))

        if repeats <= AllowedRepeats:
            FilteredSolutions.append(Solution)

    return FilteredSolutions


def ExtendedSudokuSubGridConstraint(self, Solutions, AllowedRepeats):

    FilteredSolutions = []
    AllValues = set(range(self.LowerBound, self.UpperBound + 1))

    for Solution in Solutions:
        ExtendedSubGrids = []

        for I in range(self.OrderCol):
            for J in range(self.OrderRow):
                SubGridVals = sorted(AllValues - set(
                    Solution[I * self.OrderRow + i][J * self.OrderCol + j]
                    for i in range(self.OrderRow)
                    for j in range(self.OrderCol)
                ))
                ExtendedSubGrids.append(tuple(SubGridVals))

        repeats = len(ExtendedSubGrids) - len(set(ExtendedSubGrids))

        if repeats <= AllowedRepeats:
            FilteredSolutions.append(Solution)

    return FilteredSolutions

# def ExtendedSudokuRowConstraint(self, NoOfCellExtensions, RepeatArrays):

#     '''
#     All the rows have a unique set of k numbers from a total of n numbers ranging from
#     lower bound to upper bound, where k is the length of each row.

#     Eg: If each cell can take 0-11, and reach row has 9 entries, the
#     rows can take 9 values between 0 to 11.

#     Here, the rows CAN repeat. So, NoOfRepeatDigits says how many numbers can repeat.

#     Example Puzzle: https://www.youtube.com/watch?v=ZJs3bCio94c

#     '''

#     # Create individual Extended Entries for each row
#     ExtendedArray = []
#     for i in range(self.Rows):
#         RowArray = []
#         for j in range(NoOfCellExtensions):
#             OutsideEntry = self.Model.NewIntVar(self.LowerBound, self.UpperBound,
#                             f"Extended_Row_Entry_{i}_{j}")
#             RowArray.append(OutsideEntry)
#         ExtendedArray.append(RowArray)
    
#     # Add Row Constraints
#     for i in range(self.Rows):
#         RowCollection = []
        
#         for j in range(self.Cols):
#             RowCollection.append(self.Cells[i][j])
        
#         for k in range(NoOfCellExtensions):
#             RowCollection.append(ExtendedArray[i][k])
    
#         # Define that the entire row and the extended collection combined
#         # are distinct and unique
#         self.Model.AddAllDifferent(RowCollection)
    
#     # Create Counter Variables
#     CounterVars = []
#     for j in range(NoOfCellExtensions):
#         CounterVars_j = []
#         for i in range(self.Rows):
#             CounterVars_ji = []
#             for value in range(self.LowerBound, self.UpperBound + 1):
#                 Counter = self.Model.new_bool_var(f"Extended_Row_Entry_{i}_{j}_is_{value}")
#                 CounterVars_ji.append(Counter)
#                 self.Model.Add(ExtendedArray[i][j] == value).OnlyEnforceIf(Counter)
#                 self.Model.Add(ExtendedArray[i][j] != value).OnlyEnforceIf(Counter.Not())
#             CounterVars_j.append(CounterVars_ji)
#         CounterVars.append(CounterVars_j)

#     # For each Extended column, check if a number is repeated
#     for j in range(NoOfCellExtensions):
#         is_duplicate = []
#         for value in range(self.LowerBound, self.UpperBound + 1):
#             count_var = self.Model.new_int_var(0, self.Rows, f"Extended_Row_Entry_CountCol_{j}_is_{value}")
#             self.Model.Add(sum(CounterVars[j][i][value] for i in range(self.Rows)) == count_var)

#             is_dup = self.Model.new_bool_var(f"Extended_Row_Entry_CountCol_{j}_is_{value}_Duplicate")
#             self.Model.Add(count_var > 1).OnlyEnforceIf(is_dup)
#             self.Model.Add(count_var <= 1).OnlyEnforceIf(is_dup.Not())
#             is_duplicate.append(is_dup)
        
#         self.Model.Add(sum(is_duplicate) == RepeatArrays[j])
    
# def ExtendedSudokuColumnConstraint(self, NoOfCellExtensions, RepeatArrays):

#     '''
#     All the cols have a unique set of k numbers from a total of n numbers ranging from
#     lower bound to upper bound, where k is the length of each row.

#     Eg: If each cell can take 0-11, and reach row has 9 entries, the
#     cols can take 9 values between 0 to 11.

#     Here, the cols CAN repeat. So, NoOfRepeatDigits says how many numbers can repeat.

#     Example Puzzle: https://www.youtube.com/watch?v=ZJs3bCio94c

#     '''

#     # Create individual Extended Entries for each column
#     ExtendedArray = []
#     for j in range(self.Cols):
#         ColArray = []
#         for k in range(NoOfCellExtensions):
#             OutsideEntry = self.Model.NewIntVar(self.LowerBound, self.UpperBound,
#                             f"Extended_Col_Entry_{j}_{k}")
#             ColArray.append(OutsideEntry)
#         ExtendedArray.append(ColArray)
    
#     # Add Column Constraints
#     for j in range(self.Cols):
#         ColCollection = []
        
#         for i in range(self.Rows):
#             ColCollection.append(self.Cells[i][j])
        
#         for k in range(NoOfCellExtensions):
#             ColCollection.append(ExtendedArray[j][k])
    
#         self.Model.AddAllDifferent(ColCollection)
    
#     # Create Counter Variables
#     CounterVars = []
#     for k in range(NoOfCellExtensions):
#         CounterVars_k = []
#         for j in range(self.Cols):
#             CounterVars_kj = []
#             for value in range(self.LowerBound, self.UpperBound + 1):
#                 Counter = self.Model.new_bool_var(f"Extended_Col_Entry_{j}_{k}_is_{value}")
#                 CounterVars_kj.append(Counter)
#                 self.Model.Add(ExtendedArray[j][k] == value).OnlyEnforceIf(Counter)
#                 self.Model.Add(ExtendedArray[j][k] != value).OnlyEnforceIf(Counter.Not())
#             CounterVars_k.append(CounterVars_kj)
#         CounterVars.append(CounterVars_k)

#     # For each Extended row, check if a number is repeated
#     for k in range(NoOfCellExtensions):
#         is_duplicate = []
#         for value in range(self.LowerBound, self.UpperBound + 1):
#             count_var = self.Model.new_int_var(0, self.Cols, f"Extended_Col_Entry_CountRow_{k}_is_{value}")
#             self.Model.Add(sum(CounterVars[k][j][value] for j in range(self.Cols)) == count_var)

#             is_dup = self.Model.new_bool_var(f"Extended_Col_Entry_CountRow_{k}_is_{value}_Duplicate")
#             self.Model.Add(count_var > 1).OnlyEnforceIf(is_dup)
#             self.Model.Add(count_var <= 1).OnlyEnforceIf(is_dup.Not())
#             is_duplicate.append(is_dup)
        
#         self.Model.Add(sum(is_duplicate) == RepeatArrays[k])

# def ExtendedSudokuSubGridConstraint(self, NoOfCellExtensions, RepeatArrays):

#     # Create individual Extended Entries for each subgrid
#     ExtendedArray = []
#     for I in range(self.OrderCol):
#         for J in range(self.OrderRow):
#             SubGridArray = []
#             for k in range(NoOfCellExtensions):
#                 OutsideEntry = self.Model.NewIntVar(self.LowerBound, self.UpperBound,
#                                 f"Extended_SubGrid_Entry_{I}_{J}_{k}")
#                 SubGridArray.append(OutsideEntry)
#             ExtendedArray.append(SubGridArray)
    
#     # Add SubGrid Constraints
#     subgrid_idx = 0
#     for I in range(self.OrderCol):
#         for J in range(self.OrderRow):
#             SubGridCollection = []

#             subgrid = [self.Cells[I * self.OrderRow + i][J * self.OrderCol + j]
#                         for i in range(self.OrderRow) for j in range(self.OrderCol)]
#             SubGridCollection.extend(subgrid)

#             for k in range(NoOfCellExtensions):
#                 SubGridCollection.append(ExtendedArray[subgrid_idx][k])

#             self.Model.AddAllDifferent(SubGridCollection)
#             subgrid_idx += 1

#     # Create Counter Variables
#     CounterVars = []
#     for k in range(NoOfCellExtensions):
#         CounterVars_k = []
#         for sg in range(self.OrderCol * self.OrderRow):
#             CounterVars_ksg = []
#             for value in range(self.LowerBound, self.UpperBound + 1):
#                 Counter = self.Model.new_bool_var(f"Extended_SubGrid_Entry_{sg}_{k}_is_{value}")
#                 CounterVars_ksg.append(Counter)
#                 self.Model.Add(ExtendedArray[sg][k] == value).OnlyEnforceIf(Counter)
#                 self.Model.Add(ExtendedArray[sg][k] != value).OnlyEnforceIf(Counter.Not())
#             CounterVars_k.append(CounterVars_ksg)
#         CounterVars.append(CounterVars_k)

#     # For each Extended subgrid column, check if a number is repeated
#     num_subgrids = self.OrderCol * self.OrderRow
#     for k in range(NoOfCellExtensions):
#         is_duplicate = []
#         for value in range(self.LowerBound, self.UpperBound + 1):
#             count_var = self.Model.new_int_var(0, num_subgrids, f"Extended_SubGrid_Entry_Count_{k}_is_{value}")
#             self.Model.Add(sum(CounterVars[k][sg][value] for sg in range(num_subgrids)) == count_var)

#             is_dup = self.Model.new_bool_var(f"Extended_SubGrid_Entry_Count_{k}_is_{value}_Duplicate")
#             self.Model.Add(count_var > 1).OnlyEnforceIf(is_dup)
#             self.Model.Add(count_var <= 1).OnlyEnforceIf(is_dup.Not())
#             is_duplicate.append(is_dup)
        
#         self.Model.Add(sum(is_duplicate) == RepeatArrays[k])

# def ExtraEntitiesNonRepeatableRowConstraint(self):

#     '''
#     All the rows have a unique set of k numbers from a total of n numbers ranging from
#     lower bound to upper bound, where k is the length of each row.

#     Eg: If each cell can take 0-11, and reach row has 9 entries, the
#     rows can take 9 values between 0 to 11.

#     Here, the rows CANNOT repeat. Meaning, if one row takes
#     say 0-8 as the 9 values, other rows cannot take the exact 0-8 entries.

#     Example Puzzle: https://www.youtube.com/watch?v=ZJs3bCio94c

#     '''

#     Base = self.UpperBound + 1
#     NumberOfMissingElementsPerRow = Base - self.Rows
#     SingularAllRowCollections = []
#     AllRowCollections = []
#     HashVars = []
#     # print(NumberOfMissingElementsPerRow)

#     # Add Row Constraints
#     for i in range(self.Rows):
#         RowCollection = []
#         AdditionalCollection = []
        
#         # Collect all the row entries
#         for j in range(self.Cols):
#             RowCollection.append(self.Cells[i][j])
        
#         # Create entries for the missing elements and add them to the row collection
#         for k in range(NumberOfMissingElementsPerRow):
#             OutsideEntry = self.Model.NewIntVar(self.LowerBound, self.UpperBound,
#                             f"Missing_row_entry_{i}_{k}")
#             # print(OutsideEntry)
#             RowCollection.append(OutsideEntry)
#             AdditionalCollection.append(OutsideEntry)

#         # Ensure that the total row colelction is unique and the missing collection
#         # is also unique
#         print(RowCollection)
#         self.Model.AddAllDifferent(RowCollection)

#     #     if NumberOfMissingElementsPerRow > 1:
#     #         self.Model.AddAllDifferent(AdditionalCollection)

#     #         # Ensure that all the missing entries are sorted to produce a unique hash
#     #         for k in range(NumberOfMissingElementsPerRow - 1):
#     #             self.Model.Add(AdditionalCollection[k] < AdditionalCollection[k+1])
            
#     #         # Save the variables for further uniqueness
#     #         AllRowCollections.append(AdditionalCollection)
#     #     else:
#     #         SingularAllRowCollections.append(AdditionalCollection[0])
    
#     # MaxHash = sum(self.UpperBound * (Base ** i) 
#     #           for i in range(NumberOfMissingElementsPerRow))
    
#     # if NumberOfMissingElementsPerRow == 1:
#     #     print(SingularAllRowCollections)
#     #     self.Model.AddAllDifferent(SingularAllRowCollections)
#     # else:
#     #     for l, AdditionalCollection in enumerate(AllRowCollections):
#     #         # Calculate the unique Hash for each row
#     #         HashVar = self.Model.NewIntVar(0, MaxHash,
#     #                                     f"row_hash_{l}")
#     #         HashExpression = sum(entry * (Base ** i) for i, entry in enumerate(AdditionalCollection))
#     #         self.Model.Add(HashVar == HashExpression)
#     #         HashVars.append(HashVar)
        
#     #     # Make sure that the hashes are unique across rows
#     #     self.Model.AddAllDifferent(HashVars)