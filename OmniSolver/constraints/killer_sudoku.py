from itertools import combinations

def KillerSudokuConstraints(self, KillerCageSums, KillerCageMap):
    """
    Adds the Killer Sudoku constraints to the model. Each cage must have distinct values,
    and the sum of the values in the cage must equal the specified sum.
    
    The killer cages are entered into the puzzle as a 2D array having numbers 1-n 
    used to mark the Unique IDs (UIDs) of the killer cages.
    0 is used to mark cells that don't belong to any cage.
    
    Example Puzzle: https://www.youtube.com/watch?v=Be_dJxde06g

    Args:
        KillerCageSums (list): List/Array of the sums of the corresponding killer cages
        KillerCageMap (array): A 2D map of all the cells belonging to a killer cage marked by unique numbers.
    """
    
    # First, find all the unique entries in the Killer Cage Map
    UIDs = set()
    for i in range(self.Rows):
        for j in range(self.Cols):
            if KillerCageMap[i, j] not in UIDs:
                UIDs.add(KillerCageMap[i, j])
    
    # Remove 0 so that cells with 0 are not clubbed together as another group
    if 0 in UIDs:
        UIDs.remove(0)
    
    for (entry, cage_sum) in zip(UIDs, KillerCageSums):
        
        subgrid = [ self.Cells[i][j] for i in range(self.Rows) 
                    for j in range(self.Cols) if entry == KillerCageMap[i, j]]
        
        # Constraint saying the cells are unique
        self.Model.AddAllDifferent(subgrid)
        
        # This is used to tell if a cage sum is given or not
        # -1 implies cage sum is not given.
        if cage_sum != -1:
            # Constraint equating the sum of the cells
            self.Model.Add(sum(subgrid) == cage_sum)
        print(f"Custom Subgrid with UID {entry} added.")
    
    print("Partial/Full Killer Cage Constraints added.")

def LittleKillerSudokuConstraints(self, KillerCageSums, KillerCageMap):
    """
    Adds the Little Killer Sudoku constraints to the model. Each cage must have distinct values,
    and the sum of the values in the cage must equal the specified sum.
    
    The little killer cages are entered into the puzzle as a 2D array having numbers 1-n 
    used to mark the Unique IDs (UIDs) of the killer cages.
    0 is used to mark cells that don't belong to any cage.
    
    Example Puzzle: https://www.youtube.com/watch?v=Be_dJxde06g

    Args:
        KillerCageSums (list): List/Array of the sums of the corresponding little killer cages
        KillerCageMap (array): A 2D map of all the cells belonging to a little killer cage marked by unique numbers.
    """
    
    # First, find all the unique entries in the Killer Cage Map
    UIDs = set()
    for i in range(self.Rows):
        for j in range(self.Cols):
            if KillerCageMap[i, j] not in UIDs:
                UIDs.add(KillerCageMap[i, j])
    
    # Remove 0 so that cells with 0 are not clubbed together as another group
    if 0 in UIDs:
        UIDs.remove(0)
    
    for (entry, cage_sum) in zip(UIDs, KillerCageSums):
        
        subgrid = [ self.Cells[i][j] for i in range(self.Rows) 
                    for j in range(self.Cols) if entry == KillerCageMap[i, j]]
        
        # Constraint saying the cells are unique
        # self.Model.AddAllDifferent(subgrid)
        
        # This is used to tell if a cage sum is given or not
        # None implies cage sum is not given.
        if cage_sum != None:
            # Constraint equating the sum of the cells
            self.Model.Add(sum(subgrid) == cage_sum)
        print(f"Custom Subgrid with UID {entry} added.")
    
    print("Little Killer Cage Constraints added.")

def KillerCageConstraintsWithUnknownSums(self, KillerCageMap, UnknownSums=False,
                                             SumOfAllCagesGiven=False, SumOfAllCages=0,
                                             SameSumCageGroups=False, SameSumCageGroupIDs=None,
                                             UniqueCageGroupSums=False, EqualSumCages=False):
        
        # Helper function to get cells for a given cage ID
        def get_cage_cells(cage_id):
            return [self.Cells[i][j] for i in range(self.Rows) for j in range(self.Cols) if KillerCageMap[i, j] == cage_id]
    
        # Unique cage IDs, excluding 0
        UIDs = {KillerCageMap[i, j] for i in range(self.Rows) for j in range(self.Cols)} - {0}
        
        # The sums of killer cages not given. So, only apply the uniqueness condition.
        # example: https://www.youtube.com/watch?v=M7H0mpeYW00
        if UnknownSums:
            for entry in UIDs:
                subgrid = get_cage_cells(entry)
                
                # Constraint saying the cells are unique
                self.Model.AddAllDifferent(subgrid)
                print(f"Custom Subgrid with UID {entry} added.")
        
        # The sum of all cages is given
        # example: https://www.youtube.com/watch?v=PaRzV3EAa44
        if SumOfAllCagesGiven:
            all_cells = [cell for entry in UIDs for cell in get_cage_cells(entry)]
            self.Model.Add(sum(all_cells) == SumOfAllCages)
        
        # There are groups of cages having the same sum
        # example: https://www.youtube.com/watch?v=M7H0mpeYW00
        if SameSumCageGroups:
            for group in map(tuple, SameSumCageGroupIDs):  # Ensure groups are tuples
                for ID1, ID2 in combinations(group, 2):
                    self.Model.Add(sum(get_cage_cells(ID1)) == sum(get_cage_cells(ID2)))
        
        # There are groups of killer cages having unique sums
        # That is, there are many cages separated into different groups
        # based on same sums. However, all the groups have unique sums
        # example: https://www.youtube.com/watch?v=M7H0mpeYW00
        if UniqueCageGroupSums:
            group_sum_vars = []
            for group in SameSumCageGroupIDs:
                first_cage_id = group[0]  # Pick one cage ID from the group
                cage_cells = get_cage_cells(first_cage_id)
                group_sum_var = self.Model.NewIntVar(1, self.SumOfNumbers, f"GroupSum_{first_cage_id}")  # Adjust range if needed
                self.Model.Add(group_sum_var == sum(cage_cells))
                group_sum_vars.append(group_sum_var)

            # Enforce all group sums are unique
            self.Model.AddAllDifferent(group_sum_vars)
        
        # Equal Sum Cages
        # All the cages have the same sum - sum unknown
        # eg: https://www.youtube.com/watch?v=le1pe4WMGZY
        if EqualSumCages:
            for ID1, ID2 in combinations(UIDs, 2):
                self.Model.Add(sum(get_cage_cells(ID1)) == sum(get_cage_cells(ID2)))
                
        print("Partial/Full Killer Cage with unknown sums Constraints added.")
