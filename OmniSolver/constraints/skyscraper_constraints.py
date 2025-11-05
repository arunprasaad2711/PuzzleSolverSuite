def SkyscraperConstraints(self, LeftSkyScrapers=None, RightSkyScrapers=None, TopSkyScrapers=None, BottomSkyScrapers=None):
    """
    Apply skyscraper constraints for all edges (left, right, top, bottom).
    :param LeftSkyScrapers: Clues for the left side of rows.
    :param RightSkyScrapers: Clues for the right side of rows.
    :param TopSkyScrapers: Clues for the top side of columns.
    :param BottomSkyScrapers: Clues for the bottom side of columns.
    """

    def apply_constraints(clues, is_row, reverse=False, direction=""):
        """
        Apply skyscraper constraints for a row or column.
        :param clues: List of clues for the edge.
        :param is_row: True if applying to rows, False for columns.
        :param reverse: True if iterating in reverse direction.
        :param direction: Direction of constraint (left, right, top, bottom).
        """
        for i, v in enumerate(clues):
            if v is None:  # No clue
                continue

            # Define the line of cells
            line = self.Cells[i] if is_row else [self.Cells[j][i] for j in range(self.Rows)]
            if reverse:
                line = line[::-1]

            size = len(line)
            MaxDigit = self.FullOrder

            # Constraint 1: Upper bound on the first cell
            self.Model.Add(line[0] <= MaxDigit - v + 1)

            # Constraint 2: MaxDigit must appear in positions [v-1, size-1]
            is_max_digit = [self.Model.NewBoolVar(f'is_max_digit_{direction}_{i}_{j}') for j in range(size)]
            for j in range(size):
                if j < v - 1 or j >= size:
                    # Positions outside the valid range cannot be MaxDigit
                    self.Model.Add(is_max_digit[j] == 0)
                else:
                    # Enforce that line[j] == MaxDigit only when is_max_digit[j] is true
                    self.Model.Add(line[j] == MaxDigit).OnlyEnforceIf(is_max_digit[j])
                    self.Model.Add(line[j] != MaxDigit).OnlyEnforceIf(is_max_digit[j].Not())

            # Ensure exactly one MaxDigit position is true
            self.Model.Add(sum(is_max_digit) == 1)

            # Constraint 3: Enforce visibility using AddMaxEquality
            is_peak = [self.Model.NewBoolVar(f'is_peak_{direction}_{i}_{j}') for j in range(size)]
            self.Model.Add(is_peak[0] == 1)  # First skyscraper is always visible

            for j in range(1, size):
                # max_peak_in_direction[j] represents the max height in line[:j+1]
                max_peak_in_direction = self.Model.NewIntVar(1, MaxDigit, f'max_peak_in_direction_{direction}_{i}_{j}')
                self.Model.AddMaxEquality(max_peak_in_direction, line[:j+1])

                # A skyscraper at j is a peak if it matches the max height
                self.Model.Add(line[j] == max_peak_in_direction).OnlyEnforceIf(is_peak[j])
                self.Model.Add(line[j] < max_peak_in_direction).OnlyEnforceIf(is_peak[j].Not())

            # The total number of peaks must match the clue
            self.Model.Add(sum(is_peak) == v)

    # Apply constraints for all edges
    if TopSkyScrapers is not None:
        self.TopRowNums = TopSkyScrapers
        apply_constraints(TopSkyScrapers, is_row=False, reverse=False, direction="top")     # Top side (top-to-bottom)
    if BottomSkyScrapers is not None:
        self.BottomRowNums = BottomSkyScrapers
        apply_constraints(BottomSkyScrapers, is_row=False, reverse=True, direction="bottom")  # Bottom side (bottom-to-top)
    if LeftSkyScrapers is not None:
        self.LeftColumnNums = LeftSkyScrapers
        apply_constraints(LeftSkyScrapers, is_row=True, reverse=False, direction="left")    # Left side (left-to-right)
    if RightSkyScrapers is not None:
        self.RightColumnNums = RightSkyScrapers
        apply_constraints(RightSkyScrapers, is_row=True, reverse=True, direction="right")   # Right side (right-to-left)
