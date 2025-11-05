from itertools import product

def WindokuConstraints(self, visualize=True):
    """
    Adds the Windoku constraints to the model. Each of the 9 Windoku regions must contain all numbers 
    from 1 to 9 exactly once.
    This is HARD-CODED only for 9x9 sudokus.
    """
    
    w0_IDs = []
    w0_IDs.append(list(product([1, 2, 3], [1, 2, 3])))
    w0_IDs.append(list(product([1, 2, 3], [5, 6, 7])))
    w0_IDs.append(list(product([5, 6, 7], [1, 2, 3])))
    w0_IDs.append(list(product([5, 6, 7], [5, 6, 7])))
    w0_IDs.append(list(product([1, 2, 3], [0, 4, 8])))
    w0_IDs.append(list(product([5, 6, 7], [0, 4, 8])))
    w0_IDs.append(list(product([0, 4, 8], [1, 2, 3])))
    w0_IDs.append(list(product([0, 4, 8], [5, 6, 7])))
    w0_IDs.append(list(product([0, 4, 8], [0, 4, 8])))
    
    # w0_IDs contains the 9 Windoku regions as list of tuples (row, col)
    for region_id, region_cells in enumerate(w0_IDs):
        # Extract cells based on the given row, col indices in each region
        cells = [self.Cells[row][col] for row, col in region_cells]

        # Add a constraint to ensure all values in the region are distinct
        self.Model.AddAllDifferent(cells)

        print(f"Windoku region {region_id + 1} added.")