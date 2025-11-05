import numpy as np
import time
from ortools.sat.python import cp_model
from InputJSONClass import Chess

class NQueens:
    
    def __init__(self, Data: Chess):
        
        self.Order = Data.Order
        self.Rows = self.Cols = self.Order
        self.OutputMatrix = np.zeros((self.Rows, self.Cols), np.int32)
        
        # CP Solver Model
        self.Model = cp_model.CpModel()
        
        # CP Solver
        self.Solver = cp_model.CpSolver()
        
        # Create all the variables for the solver and assign possible values
        self.Cells = [
                        [
                            self.Model.NewIntVar(0, 1, name=f"x({i}, {j})")
                            for j in range(self.Cols)
                        ]
                        for i in range(self.Rows)
                    ]

        self.ModelStatus = False

    
    def RowConstraint(self):
        
        # Collect all rows and columns separately.
        for i in range(self.Rows):
            RowCollection = []
            
            for j in range(self.Cols):
                RowCollection.append(self.Cells[i][j])
            
            # Put a condition that you can have only 1 piece in every row
            self.Model.Add(sum(RowCollection) == 1)
        
        print("Row Collections Added")
    
    def ColConstraint(self):
        
        # Collect all rows and columns separately.
        for i in range(self.Rows):
            ColCollection = []
            
            for j in range(self.Cols):
                ColCollection.append(self.Cells[j][i])
            
            # Put a condition that you can have only 1 piece in every column
            self.Model.Add(sum(ColCollection) == 1)
        
        print("Col Rook Collections Added")
    
    def NQueensConstraint(self):
        
        self.RowConstraint()
        self.ColConstraint()
        self.DiagonalAntiDiagonalConstraint()
        
        print(f"{self.Order} Queens Constraints Added.")
    
    def NRooksConstraint(self):
        
        self.RowConstraint()
        self.ColConstraint()
        
        print(f"{self.Order} Rooks Constraints Added.")
    
    def NBishopsConstraint(self, RowConstraint=False):
        
        if RowConstraint:
            self.RowConstraint()
            self.DiagonalAntiDiagonalConstraint()
            
            print(f"{self.Order} Bishops on {self.Order} Rows Constraints Added.")
        else:
            self.ColConstraint()
            self.DiagonalAntiDiagonalConstraint()
            
            print(f"{self.Order} Bishops on {self.Order} Cols Constraints Added.")
    
    def DiagonalAntiDiagonalConstraint(self):
        
        # Get all the Anti-Diagonals and Diagonals and set their sum to be utmost 1
        for i in range(0, self.Order):
            AntiDiagonals = self.DiagonalTRBL_ids(0, i)
            # print(i, AntiDiagonals)
            
            Cells = [self.Cells[r][c] for r, c in AntiDiagonals]
            self.Model.Add(sum(Cells) <= 1)
        
        for i in range(1, self.Order):
            AntiDiagonals = self.DiagonalTRBL_ids(i, self.Order-1)
            # print(i, AntiDiagonals)
            
            Cells = [self.Cells[r][c] for r, c in AntiDiagonals]
            self.Model.Add(sum(Cells) <= 1)
        
        for i in range(self.Order-1, -1, -1):
            Diagonals = self.DiagonalTLBR_ids(i, 0)
            # print(i, Diagonals)
            
            Cells = [self.Cells[r][c] for r, c in Diagonals]
            self.Model.Add(sum(Cells) <= 1)
        
        for i in range(1, self.Order):
            Diagonals = self.DiagonalTLBR_ids(0, i)
            # print(i, Diagonals)
            
            Cells = [self.Cells[r][c] for r, c in Diagonals]
            self.Model.Add(sum(Cells) <= 1)
        
        print("Diagonal/Anti-Diagonal Bishop Collections Added")
    
    def DiagonalTRBL_ids(self, RowID, ColID):
        
        IDs = []
        
        x, y = RowID, ColID
        while x <= self.Rows - 1 and y >= 0:
            IDs.append((x, y))
            x += 1
            y -= 1
        
        return IDs
    
    def DiagonalTLBR_ids(self, RowID, ColID):
        
        IDs = []
        
        x, y = RowID, ColID
        while x <= self.Rows - 1 and y <= self.Cols - 1:
            IDs.append((x, y))
            x += 1
            y += 1
        
        return IDs
    
    def Solve(self):
        
        solution_count = 0
        solutions = []
        
        StartTime = time.time()
        self.ModelStatus = self.Solver.Solve(self.Model)
        EndTime = time.time()
        
        TimeTaken = EndTime - StartTime
        
        print(f"Solving done in {TimeTaken} second(s)")
        
        if self.ModelStatus == cp_model.FEASIBLE or self.ModelStatus == cp_model.OPTIMAL:    
            print("Optimal Solution Found!")
            
            solution = []
            for i in range(self.Order):
                row = []
                for j in range(self.Order):
                    self.OutputMatrix[i, j] = self.Solver.Value(self.Cells[i][j])
                    row.append(self.Solver.Value(self.Cells[i][j]))
                solution.append(row)
            solutions.append(solution)
            solution_count += 1
        else:
            print("Houston, we don't have a solution")
        
        return solutions
    
    def PrintMatrix(self):
        print(self.OutputMatrix)
    
    def PrintSolution(self, solution):
        for row in solution:
            print(row)
    
    def MultiSolutionSolve(self):
        
        StartTime = time.time()
        
        solution_count = 0  # To count the number of solutions
        solutions = []      # To store all solutions

        while True:
            self.ModelStatus = self.Solver.Solve(self.Model)
            
            if self.ModelStatus == cp_model.FEASIBLE or self.ModelStatus == cp_model.OPTIMAL:
                print(f"Solution {solution_count + 1} Found!")
                solution = []
                for i in range(self.Rows):
                    row = []
                    for j in range(self.Cols):
                        value = self.Solver.Value(self.Cells[i][j])
                        self.OutputMatrix[i, j] = value
                        row.append(value)
                    solution.append(row)
                solutions.append(solution)
                solution_count += 1

                # Create a list of Boolean variables to exclude the current solution
                exclusion_constraints = []
                for i in range(self.Rows):
                    for j in range(self.Cols):
                        # Create a unique Boolean variable for each solution using the solution count
                        bool_var = self.Model.NewBoolVar(f"exclusion_{solution_count}_{i}_{j}")
                        self.Model.Add(self.Cells[i][j] != solutions[-1][i][j]).OnlyEnforceIf(bool_var)
                        exclusion_constraints.append(bool_var)
                
                # Add a constraint to ensure that at least one of the inequalities holds
                self.Model.AddBoolOr(exclusion_constraints)
                
            else:
                if solution_count == 0:
                    print("Houston, we don't have a solution")
                else:
                    print(f"No more solutions. Total solutions found: {solution_count}")
                break

        EndTime = time.time()
        TimeTaken = EndTime - StartTime
        print(f"Analysis Done in {TimeTaken:.2f} second(s)")

        return solutions
