def KropkiRatioConstraints(self, numerator, denominator):
    """
    Adds the Kropki constraint that two orthogonally adjacent cells 
    cannot be in the ratio of `numerator:denominator`.
    
    Args:
        numerator (int): The numerator of the ratio.
        denominator (int): The denominator of the ratio.
    """
    for i in range(self.Rows):
        for j in range(self.Cols):
            # Check right (if within bounds)
            if j + 1 < self.Cols:
                self.Model.Add(self.Cells[i][j] != numerator * self.Cells[i][j + 1])  # A = numerator * B
                self.Model.Add(self.Cells[i][j + 1] != denominator * self.Cells[i][j])  # B = denominator * A

            # Check down (if within bounds)
            if i + 1 < self.Rows:
                self.Model.Add(self.Cells[i][j] != numerator * self.Cells[i + 1][j])  # A = numerator * B
                self.Model.Add(self.Cells[i + 1][j] != denominator * self.Cells[i][j])  # B = denominator * A

    print(f"Kropki {numerator}:{denominator} ratio constraints added.")

def KropkiOrthogonalAntiSumConstraints(self, kropki_sum, PairExceptions=None):
    """
    Adds the Kropki constraint that two orthogonally adjacent cells 
    cannot add-up to a 'kropki_sum'.
    
    Args:
        kropki_sum (int): the sum the two numbers should not add up to.
        PairExceptions (list of tuples): List of bypassable pairs of cells that DO obey the condition
    """
    for i in range(self.Rows):
        for j in range(self.Cols):
            
            ExceptionFound = False
            if PairExceptions is not None:
                for pair1, pair2 in PairExceptions:
                    if ((i, j) == pair1 and (i, j + 1) == pair2) or ((i, j) == pair1 and (i + 1, j) == pair2):
                        print(f"Found a conflicting exception {pair1} and {pair2}. Excluding it")
                        ExceptionFound = True
                        break
            
            if not ExceptionFound:
                # Check right (if within bounds)
                if j + 1 < self.Cols:
                    self.Model.Add(self.Cells[i][j] + self.Cells[i][j + 1] != kropki_sum)  

                # Check down (if within bounds)
                if i + 1 < self.Rows:
                    self.Model.Add(self.Cells[i][j] + self.Cells[i + 1][j] != kropki_sum)

    print(f"Kropki Anti-Sum condition of {kropki_sum} constraints added.")
