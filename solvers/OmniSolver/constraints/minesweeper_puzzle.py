import numpy as np

def ClassicMineSweeperConstraints(self, GridMap, NeighbourMode="King"):

    '''
    
    Similar to the minesweeper game, you have to find all the mines in the field.
    The gridmap tells how many mines are present in the neighbourhood.

    The Neighbour mode tells what cells can be neighbours.
    King mode - both orthogonal and diagonal cells
    Knight mode - cells that are knight's move apart
    Orthogonal mode - purely orthogonal cells
    Diagonal mode - purely diagonal cells

    '''

    GridMap = np.array(GridMap)

    if NeighbourMode == "King":
        Neighbours = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
    elif NeighbourMode == "Knight":
        Neighbours = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]
    elif NeighbourMode == "Orthogonal":
        Neighbours = [
            (-1, 0), (0, -1), (0, 1), (1, 0),
        ]
    elif NeighbourMode == "Diagonal":
        Neighbours = [
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]
    
    # Minesweeper constraints
    for i in range(self.Rows):
        for j in range(self.Cols):

            if GridMap[i, j] > 0 or GridMap[i, j] == self.ZeroMaskingDigit:

                # Constraint 1 - if the GridMap has a number, then there are no mines:
                self.Model.Add(self.Cells[i][j] == 0)

                # Constraint 2 - sum of all the neighbours around the GridMap must be
                # equal to the grid map number.
                ValidNeighbours = []
                for move in Neighbours:
                    ni, nj = i + move[0], j + move[1]
                    if 0 <= ni < self.Rows and 0 <= nj < self.Cols:
                        ValidNeighbours.append(self.Cells[ni][nj])
                
                # Setting up constraint 2. Since zero is valid, adjustment
                # is done for it as well.
                if GridMap[i, j] > 0:
                    self.Model.Add(sum(ValidNeighbours) == GridMap[i, j])
                elif GridMap[i, j] == self.ZeroMaskingDigit:
                    self.Model.Add(sum(ValidNeighbours) == 0)
    
    print(f"MineSweeper Constraints Added")