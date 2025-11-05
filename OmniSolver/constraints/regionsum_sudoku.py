def RegionSumConstraints(self, RegionSums, RegionMap, RegionUniqueness):
        
    '''
    Sudoku constraint in which there are separate regions that add upto a sum.
    They are similar to killer cages, but a single region/group can be two or more
    separate sub-regions that may not be connected to each other.
    The entries in a region can be unique if the uniqueness flag is set to 1.
    
    eg: https://www.youtube.com/watch?v=Bhczfz8WGik
    '''
    
    # First, find all the unique entries in the Killer Cage Map
    UIDs = set()
    for i in range(self.Rows):
        for j in range(self.Cols):
            if RegionMap[i, j] not in UIDs:
                UIDs.add(RegionMap[i, j])
    
    # Remove 0 so that cells with 0 are not clubbed together as another group
    if 0 in UIDs:
        UIDs.remove(0)
        
    for (entry, region_sum, region_uniqueness) in zip(UIDs, RegionSums,
                                                                RegionUniqueness):
        
        region = [ self.Cells[i][j] for i in range(self.Rows) 
                    for j in range(self.Cols) if entry == RegionMap[i, j]]
        
        regionIDs = [(i, j) for i in range(self.Rows) 
                    for j in range(self.Cols) if entry == RegionMap[i, j]]
        
        # Constraint saying the cells are unique - 1 means unique
        if region_uniqueness == 1:
            self.Model.AddAllDifferent(region)
        
        # This is used to tell if a cage sum is given or not
        # -1 implies cage sum is not given.
        if region_sum != -1:
            # Constraint equating the sum of the cells
            self.Model.Add(sum(region) == region_sum)
        
        print(f"Custom Region with UID {entry} added.")
