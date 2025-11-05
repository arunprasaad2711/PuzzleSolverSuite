def ArrowAverage(self, arrow_circles, arrow_bodies):
        
    """
    Arrow Average/Mean Sudoku. The number in the arrow circle is the average
    or mean of the numbers on the arrow body
    
    Example Puzzle: https://www.youtube.com/watch?v=gvi2UEgEjDE
    
    Args:
        arrow_circles (list): List of coordinates (row, col) for the arrow circle cells.
        arrow_bodies (list): List of lists, where each sublist contains coordinates (row, col) 
                            for the arrow body cells.
    """
     
    if len(arrow_circles) != len(arrow_bodies):
        raise ValueError("Mismatch between number of arrow averages and arrow bodies.")
    
    for arrow_id, (arrow_circle, arrow_body) in enumerate(zip(arrow_circles, arrow_bodies)):
        
        # Extract the cells of the arrow body
        Cells_of_Arrow = [self.Cells[row][col] for row, col in arrow_body]
        
        # Extract the cell of the arrow circle
        r, c = arrow_circle
        Cell_of_Arrow_Circle = self.Cells[r][c]
        
        # Debug information
        print(f"Processing Arrow {arrow_id + 1}: Circle at {arrow_circle}, Body length = {len(Cells_of_Arrow)}")

        # Place the average condition
        # average of all the cells of the arrow = cell value of the arrow circle
        # This can be written as sum = n*average
        if len(Cells_of_Arrow) > 0:
            self.Model.Add(sum(Cells_of_Arrow) == len(Cells_of_Arrow) * Cell_of_Arrow_Circle)
            print(f"Arrow Average Condition {arrow_id + 1} added for circle {arrow_circle}")
        else:
            print(f"Warning: Arrow {arrow_id + 1} has no body cells. Skipping.")

def ArrowSum(self, arrow_circles, arrow_bodies):
    
    """
    Arrow Sum Sudoku. The number in the arrow circle is the sum of the numbers on the arrow body
    
    Example Puzzle: https://www.youtube.com/watch?v=gvi2UEgEjDE
    
    Args:
        arrow_circles (list): List of coordinates (row, col) for the arrow circle cells.
        arrow_bodies (list): List of lists, where each sublist contains coordinates (row, col) 
                            for the arrow body cells.
    """
    
    if len(arrow_circles) != len(arrow_bodies):
        raise ValueError("Mismatch between number of arrow circles and arrow bodies.")
    
    for arrow_id, (arrow_circle, arrow_body) in enumerate(zip(arrow_circles, arrow_bodies)):
        
        # Extract the cells of the arrow body
        Cells_of_Arrow = [self.Cells[row][col] for row, col in arrow_body]
        
        # Extract the cell of the arrow circle
        r, c = arrow_circle
        Cell_of_Arrow_Circle = self.Cells[r][c]
        
        # Debug information
        print(f"Processing Arrow {arrow_id + 1}: Circle at {arrow_circle}, Body length = {len(Cells_of_Arrow)}")
        print(f"Arrow Body: {arrow_body}")

        # Place the average condition
        # Sum of cells in arrow = value in arrow circle
        if len(Cells_of_Arrow) > 0:
            self.Model.Add(sum(Cells_of_Arrow) == Cell_of_Arrow_Circle)
            print(f"Arrow Sum Condition {arrow_id + 1} added for circle {arrow_circle}")
        else:
            print(f"Warning: Arrow {arrow_id + 1} has no body cells. Skipping.")

def TwoDigitArrowSum(self, arrow_circles1, arrow_circles2, arrow_bodies):
        
    if len(arrow_circles1) != len(arrow_bodies):
        raise ValueError("Mismatch between number of arrow averages and arrow bodies.")
    
    for arrow_id, (arrow_circle1, arrow_circle2, arrow_body) in enumerate(zip(arrow_circles1, arrow_circles2, arrow_bodies)):
        
        # Extract the cells of the arrow body
        Cells_of_Arrow = [self.Cells[row][col] for row, col in arrow_body]
        
        # Extract the cell of the arrow circle
        r1, c1 = arrow_circle1
        r2, c2 = arrow_circle2
        Cell_of_Arrow_Circle1 = self.Cells[r1][c1]
        Cell_of_Arrow_Circle2 = self.Cells[r2][c2]

        # Place the average condition
        # Sum of cells in arrow = value in arrow circle
        if len(Cells_of_Arrow) > 0:
            self.Model.Add(sum(Cells_of_Arrow) == 10*Cell_of_Arrow_Circle1 + Cell_of_Arrow_Circle2)
        else:
            print(f"Warning: Arrow {arrow_id + 1} has no body cells. Skipping.")
