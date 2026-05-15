def ExtendedSudokuRowConstraint(self):

    TotalNoOfVals = list(range(self.LowerBound, self.UpperBound + 1))
    Base = self.UpperBound - self.LowerBound + 1
    # print(Base)
    # print(TotalNoOfVals)

    NoOfExtendedCells = len(TotalNoOfVals) - self.Rows
    # print(NoOfExtendedCells)

    Extra = []
    
    for i in range(self.Rows):
        RowCollection = []
        ExtendedRowCollection = []
        
        for j in range(self.Cols):
            RowCollection.append(self.Cells[i][j])

        for k in range(NoOfExtendedCells):
            Entry = self.Model.NewIntVar(self.LowerBound, self.UpperBound,
                    f"ExtendedRowEntry_{i}_{k}")
            RowCollection.append(Entry)
            ExtendedRowCollection.append(Entry)
        
        # This ensures that even the extended row elements
        # are unique since the main puzzle elements will be unique
        # due to constraints
        self.Model.AddAllDifferent(RowCollection)

        # Make sure that the row entries are sorted in ascending order
        for l in range(0, NoOfExtendedCells - 1):
            self.Model.Add(ExtendedRowCollection[l] < ExtendedRowCollection[l + 1])

        ExtendedRowEntryValues = []
        for k in range(NoOfExtendedCells):
            Entry = self.Model.NewIntVar(self.LowerBound, (Base ** NoOfExtendedCells),
                    f"ExtendedRowEntryValue_{i}_{k}")
            self.Model.Add(Entry == ExtendedRowCollection[k] * (Base ** k))
            ExtendedRowEntryValues.append(Entry)
        
        Extra.append(sum(ExtendedRowEntryValues))
    
    self.Model.AddAllDifferent(Extra)

    print("Extended Row Constraints Added")

def ExtendedSudokuColConstraint(self):

    TotalNoOfVals = list(range(self.LowerBound, self.UpperBound + 1))
    Base = self.UpperBound - self.LowerBound + 1
    # print(Base)

    NoOfExtendedCells = len(TotalNoOfVals) - self.Cols
    
    Extra = []
    
    for j in range(self.Cols):
        ColCollection = []
        ExtendedColCollection = []
        
        for i in range(self.Rows):
            ColCollection.append(self.Cells[i][j])

        for k in range(NoOfExtendedCells):
            Entry = self.Model.NewIntVar(self.LowerBound, self.UpperBound,
                    f"ExtendedColEntry_{j}_{k}")
            ColCollection.append(Entry)
            ExtendedColCollection.append(Entry)
        
        # This ensures that even the extended col elements
        # are unique since the main puzzle elements will be unique
        # due to constraints
        self.Model.AddAllDifferent(ColCollection)

        # Make sure that the col entries are sorted in ascending order
        for l in range(0, NoOfExtendedCells - 1):
            self.Model.Add(ExtendedColCollection[l] < ExtendedColCollection[l + 1])

        ExtendedColEntryValues = []
        for k in range(NoOfExtendedCells):
            Entry = self.Model.NewIntVar(self.LowerBound, (Base ** NoOfExtendedCells),
                    f"ExtendedColEntryValue_{j}_{k}")
            self.Model.Add(Entry == ExtendedColCollection[k] * (Base ** k))
            ExtendedColEntryValues.append(Entry)
        
        Extra.append(sum(ExtendedColEntryValues))
    
    self.Model.AddAllDifferent(Extra)

    print("Extended Col Constraints Added")

def ExtendedSudokuSubGridConstraint(self):

    TotalNoOfVals = list(range(self.LowerBound, self.UpperBound + 1))
    Base = self.UpperBound - self.LowerBound + 1
    # print(Base)

    # SubGrid has OrderRow * OrderCol cells
    SubGridSize = self.OrderRow * self.OrderCol
    NoOfExtendedCells = len(TotalNoOfVals) - SubGridSize

    Extra = []

    for I in range(self.OrderCol):
        for J in range(self.OrderRow):
            SubGridCollection = [ self.Cells[I * self.OrderRow + i][J * self.OrderCol + j]
                                  for i in range(self.OrderRow) for j in range(self.OrderCol) ]
            ExtendedSubGridCollection = []

            for k in range(NoOfExtendedCells):
                Entry = self.Model.NewIntVar(self.LowerBound, self.UpperBound,
                        f"ExtendedSubGridEntry_{I}_{J}_{k}")
                SubGridCollection.append(Entry)
                ExtendedSubGridCollection.append(Entry)

            # This ensures that even the extended subgrid elements
            # are unique since the main puzzle elements will be unique
            # due to constraints
            self.Model.AddAllDifferent(SubGridCollection)

            # Make sure that the subgrid entries are sorted in ascending order
            for l in range(0, NoOfExtendedCells - 1):
                self.Model.Add(ExtendedSubGridCollection[l] < ExtendedSubGridCollection[l + 1])

            ExtendedSubGridEntryValues = []
            for k in range(NoOfExtendedCells):
                Entry = self.Model.NewIntVar(self.LowerBound, (Base ** NoOfExtendedCells),
                        f"ExtendedSubGridEntryValue_{I}_{J}_{k}")
                self.Model.Add(Entry == ExtendedSubGridCollection[k] * (Base ** k))
                ExtendedSubGridEntryValues.append(Entry)

            Extra.append(sum(ExtendedSubGridEntryValues))

    self.Model.AddAllDifferent(Extra)

    print("Extended SubGrid Constraints Added")