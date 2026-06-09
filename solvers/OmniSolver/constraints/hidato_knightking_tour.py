def HidatoConstraints(self, RuleMode="King"):

    '''
    Hidato puzzle.

    Place numbers in a grid such that all the numbers from the shortest to the
    largest are connected by a single line. Consecutive numbers must be 
    "adjacent" to each other.

    King variant is the standard Hidado game wherein the consecutive numbers must
    be orthogonally or diagonally adjacent to each other.

    Knight variant is the variation wherein the consecutive numbers must be adjacent
    to each other by a chess knight's move.

    eg: https://www.youtube.com/watch?v=fdUZBiBqLJQ
    '''

    if RuleMode == "King":
        Neighbours = [
            (-1, -1), (-1,  0), (-1,  1),
            ( 0, -1),           ( 0,  1),
            ( 1, -1), ( 1,  0), ( 1,  1),
        ]
    elif RuleMode == "Knight":
        Neighbours = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]
    
    # All Different Condition
    self.Model.AddAllDifferent([self.Cells[i][j] for i in range(self.Rows) 
                                for j in range(self.Cols)])

    for i in range(self.Rows):
        for j in range(self.Cols):

            IsLowerBound = self.Model.NewBoolVar(f"Is_Hidato_LowerBound_{i}_{j}")
            IsUpperBound = self.Model.NewBoolVar(f"Is_Hidato_UpperBound_{i}_{j}")

            # Bi-directional linking
            self.Model.Add(self.Cells[i][j] == self.LowerBound).OnlyEnforceIf(IsLowerBound)
            self.Model.Add(self.Cells[i][j] != self.LowerBound).OnlyEnforceIf(IsLowerBound.Not())
            self.Model.Add(self.Cells[i][j] == self.UpperBound).OnlyEnforceIf(IsUpperBound)
            self.Model.Add(self.Cells[i][j] != self.UpperBound).OnlyEnforceIf(IsUpperBound.Not())

            # Set conditions that any number is either an extreme or within range.
            IsExtreme = self.Model.NewBoolVar(f"Is_Hidato_Extreme_{i}_{j}")
            # IsExtreme ↔ (IsLowerBound OR IsUpperBound)
            self.Model.AddBoolOr([IsLowerBound, IsUpperBound]).OnlyEnforceIf(IsExtreme)
            self.Model.AddBoolAnd([IsLowerBound.Not(), IsUpperBound.Not()]).OnlyEnforceIf(IsExtreme.Not())
            self.Model.AddBoolOr([IsExtreme, IsLowerBound.Not()])   # if lower → extreme
            self.Model.AddBoolOr([IsExtreme, IsUpperBound.Not()])   # if upper → extreme

            # check if the number is jousting with a neighbour - a neighbouring cell is
            # consecutive.
            IsJoustingArray = []
            for move in Neighbours:
                ni, nj = i + move[0], j + move[1]
                if 0 <= ni < self.Rows and 0 <= nj < self.Cols:

                    IsJousting1 = self.Model.NewBoolVar(f"Cell_{i}_{j}_Hidato_jousting1_{ni}_{nj}")
                    IsJousting2 = self.Model.NewBoolVar(f"Cell_{i}_{j}_Hidato_jousting2_{ni}_{nj}")
                    IsJousting  = self.Model.NewBoolVar(f"Cell_{i}_{j}_Hidato_jousting_{ni}_{nj}")

                    self.Model.Add(self.Cells[i][j] == self.Cells[ni][nj] + 1).OnlyEnforceIf(IsJousting1)
                    self.Model.Add(self.Cells[i][j] == self.Cells[ni][nj] - 1).OnlyEnforceIf(IsJousting2)
                    self.Model.AddBoolOr([IsJousting1, IsJousting2]).OnlyEnforceIf(IsJousting)
                    self.Model.AddBoolAnd([IsJousting1.Not(), IsJousting2.Not()]).OnlyEnforceIf(IsJousting.Not())

                    IsJoustingArray.append(IsJousting)

            # Ensure that if the number is an extreme, there is only one neighbour
            # Otherwise, there are two
            self.Model.Add(sum(IsJoustingArray) == 1).OnlyEnforceIf(IsExtreme)
            self.Model.Add(sum(IsJoustingArray) == 2).OnlyEnforceIf(IsExtreme.Not())
    
    print(f"Initialized Hidato Constraint with {RuleMode} mode")
