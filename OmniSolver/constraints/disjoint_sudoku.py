def DisjointConstraints(self):
    """
    Adds the Disjoint or SuperWindoku constraints to the model. Each of the 9 SuperWindoku
    regions must contain all numbers from 1 to 9 exactly once.
    """
    
    SW0_IDs = []
    BaseList = []
    for i in range(self.OrderRow):
        for j in range(self.OrderCol):
            BaseList.append((i*self.OrderRow, j*self.OrderCol))

    for x in range(self.OrderRow):
        for y in range(self.OrderCol):
            list1 = []
            for ID in BaseList:
                i, j = ID
                list1.append((i + x, j + y))
            SW0_IDs.append(list1)
    
    # SW0_IDs contains the 9 Windoku regions as list of tuples (row, col)
    for region_id, region_cells in enumerate(SW0_IDs):
        # Extract cells based on the given row, col indices in each region
        cells = [self.Cells[row][col] for row, col in region_cells]

        # Add a constraint to ensure all values in the region are distinct
        self.Model.AddAllDifferent(cells)

        print(f"Disjoint/Super Windoku region {region_id + 1} added.")
