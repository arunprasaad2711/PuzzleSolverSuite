from ortools.sat.python import cp_model
import time
import numpy as np
import sys
from pathlib import Path
import importlib.util
from InputJSONClass import Omni

class OmniPuzzleSolver:
    
    def __init__(self, Data: Omni, SolversDirectory="./OmniSolver/constraints"):
        
        print(f"Initializing OmniPuzzleSolver with data {Data}")
        
        # Sudoku Puzzle Variables
        self.OrderRow = Data.OrderRow
        self.OrderCol = Data.OrderCol
        
        # Input Matrix
        self.InputMatrix = np.array(Data.Matrix, dtype=np.int32)
        
        self.Rows, self.Cols = self.InputMatrix.shape
        self.FullOrder = max(self.Rows, self.Cols)
        
        # number of unique numbers
        self.nuns = self.FullOrder
        
        # Sum of all the numbers in a row/col/subgrid
        self.SumOfNumbers = self.FullOrder * (self.FullOrder + 1) // 2
        
        # Variables for formatting output
        self.max_digits = len(str(self.nuns))
        self.border = "-"*(self.nuns*(self.max_digits + 1) + 2*self.OrderRow + 1)
        
        # Solution Matrix
        self.OutputMatrix = np.zeros_like(self.InputMatrix, dtype=np.int32)
        
        # CP Solver Model
        self.Model = cp_model.CpModel()
        
        # CP Solver
        self.Solver = cp_model.CpSolver()
        
        self.Solver.parameters.num_search_workers = 1
        # self.Solver.parameters.log_search_progress = True
        
        self.LowerBound = Data.LowerBound if Data.LowerBound is not None else 1
        self.UpperBound = Data.UpperBound if Data.UpperBound is not None else self.FullOrder
        
        # Create all the variables for the sudoku and assign possible value
        self.Cells = [ 
                        [
                            self.Model.NewIntVar(self.LowerBound, self.UpperBound, f"x({i}, {j})")
                            for j in range(self.Cols)
                        ]
                        for i in range(self.Rows)
                    ]
    
        self.PrintNumber = True

        self.ModelStatus = False
        
        self.solvers_directory = Path(SolversDirectory)
        self._load_solver_methods()
        
        ## Parameters for different sudoku and puzzle solvers
        
        self.KillerCageMaps = []
        self.KillerCageSums = []
        
        self.TLBR_Diagonal = False
        self.TRBL_Diagonal = False
        self.ArgyleSudoku = False
        
        self.ColouredCells = []
        self.ColouredCellsColours = []
        
        self.Lines = []
        self.LineColours = []
        
        self.ArrowCircles = []
        self.ArrowBodies = []
        
        self.RatioPairsPoints = []
        self.DifferencePairsPoints = []
        self.AdditionPairsPoints = []
        self.AdditionPairsSums = []
        self.CosmeticPairsPoints = []
        self.CosmeticPairsSymbols = []
        
        self.Thermometers = []
        
        self.OddEvenMap = []
        
        self.QuadsIDs = []
        self.QuadsVals = []
        
        self.TopRowNums = []
        self.BottomRowNums = []
        self.LeftColumnNums = []
        self.RightColumnNums = []
        
        self.RegionSum = False
        self.RegionSumMap  = []
        self.RegionSumSums = []
        self.RegionSumColours = []
        
        self.StarBattlePuzzle = False
        self.NoriNoriPuzzle = False
        self.SumpletePuzzle = False
        self.KakurasuPuzzle = False
        
        self.CloneRegionSudoku = False
        self.CloneRegionsSet1 = []
        self.CloneRegionsSet2 = []
        self.CloneRegionColours = []
        
        self.MultiAdditionPairsSudoku = False
        self.MultiAdditionPairsPoints = []
    
    def _load_solver_methods(self):
        """Dynamically load all solver methods from separate files"""
        if not self.solvers_directory.exists():
            return
            
        for file_path in self.solvers_directory.glob("*.py"):
            if file_path.name.startswith("_"):
                continue  # Skip private files
                
            # Load the module
            spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Add all public functions to this instance
            for attr_name in dir(module):
                if not attr_name.startswith("_"):
                    attr = getattr(module, attr_name)
                    
                    if hasattr(attr, '__get__') and callable(attr):
                        setattr(self, attr_name, attr.__get__(self, type(self)))
                    else:
                        setattr(self, attr_name, attr)  # Just set it directly
    
    def PrintConstraints(self):
        print(self.Model)
    
    def get_symmetries(self, grid):
        
        """Generate all 8 symmetries (rotations and reflections) of the 9x9 Sudoku grid."""
        symmetries = []

        # 0° (original)
        symmetries.append(grid)

        # 90° rotation
        symmetries.append([list(row) for row in zip(*grid[::-1])])  # Transpose + reverse rows

        # 180° rotation
        symmetries.append([list(row) for row in zip(*symmetries[1][::-1])])

        # 270° rotation
        symmetries.append([list(row) for row in zip(*symmetries[2][::-1])])

        # Horizontal reflection
        symmetries.append(grid[::-1])

        # Vertical reflection
        symmetries.append([row[::-1] for row in grid])

        # Diagonal reflection (main diagonal)
        symmetries.append([list(row) for row in zip(*grid)])

        # Anti-diagonal reflection
        symmetries.append([list(row) for row in zip(*grid[::-1])])

        return symmetries
    
    def MultiSolutionSymmetryRemovedSolve(self):
        
        StartTime = time.time()
    
        solution_count = 0  # To count the number of solutions
        solutions = []      # To store all solutions
        iteration_count = 0
        
        while True:
            self.ModelStatus = self.Solver.Solve(self.Model)
            
            if self.ModelStatus == cp_model.FEASIBLE or self.ModelStatus == cp_model.OPTIMAL:
                print(f"Solution {solution_count + 1} Found! Iteration {iteration_count + 1}")
                solution = []
                for i in range(self.Rows):
                    row = []
                    for j in range(self.Cols):
                        value = self.Solver.Value(self.Cells[i][j])
                        self.OutputMatrix[i, j] = value
                        row.append(value)
                    solution.append(row)
                
                # Find all symmetries of the current solution
                symmetries = self.get_symmetries(solution)
                
                # Create a list of Boolean variables to exclude the symmetries
                for symmetry_index, symmetry in enumerate(symmetries):
                    exclusion_constraints = []
                    for i in range(self.Rows):
                        for j in range(self.Cols):
                            # Create a unique Boolean variable for each symmetry
                            bool_var = self.Model.NewBoolVar(f"exclusion_{solution_count}_{symmetry_index}_{i}_{j}")
                            self.Model.Add(self.Cells[i][j] != symmetry[i][j]).OnlyEnforceIf(bool_var)
                            exclusion_constraints.append(bool_var)
                
                    # Add a constraint to ensure that at least one of the inequalities holds (exclude the symmetries)
                    self.Model.AddBoolOr(exclusion_constraints)
                
                iteration_count += 1

                # Store the new solution
                solutions.append(solution)
                solution_count += 1
            
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
    
    def Solve(self):
        
        solution_count = 0  # To count the number of solutions
        solutions = []      # To store all solutions
        
        StartTime = time.time()
        self.ModelStatus = self.Solver.Solve(self.Model)
        EndTime = time.time()
        
        TimeTaken = EndTime - StartTime
        
        print(f"Solving done in {TimeTaken} second(s)")
        
        if self.ModelStatus == cp_model.FEASIBLE or self.ModelStatus == cp_model.OPTIMAL:    
            print("Optimal Solution Found!")
            
            solution = []
            for i in range(self.Rows):
                row = []
                for j in range(self.Cols):
                    self.OutputMatrix[i, j] = self.Solver.Value(self.Cells[i][j])
                    row.append(self.Solver.Value(self.Cells[i][j]))
                solution.append(row)
            solutions.append(solution)
            solution_count += 1
        else:
            print("Houston, we don't have a solution")
        
        return solutions
        
    def PrintProblem(self, file=sys.stdout):
        
        for i in range(0, self.Rows):
            if i % self.OrderRow == 0:
                print(self.border, file=file)
            line = "|"
            for j in range(0, self.Cols):
                line += f" {self.InputMatrix[i, j]:{self.max_digits}}"
                if (j + 1) % self.OrderCol == 0:
                    line += " |"
            print(line, file=file)
            
        print(self.border, file=file)
    
    def PrintSolution(self, file=sys.stdout):
        
        for i in range(0, self.Rows):
            if i % self.OrderRow == 0:
                print(self.border, file=file)
            line = "|"
            for j in range(0, self.Cols):
                line += f" {self.OutputMatrix[i, j]:{self.max_digits}}"
                if (j + 1) % self.OrderCol == 0:
                    line += " |"
            print(line, file=file)
            
        print(self.border, file=file)
    
    def PrintMatrix(self, Solution, file=sys.stdout):
        
        Matrix = np.array(Solution, dtype=np.int32)
        
        for i in range(0, self.Rows):
            if i % self.OrderRow == 0:
                print(self.border, file=file)
            line = "|"
            for j in range(0, self.Cols):
                line += f" {Matrix[i, j]:{self.max_digits}}"
                if (j + 1) % self.OrderCol == 0:
                    line += " |"
            print(line, file=file)
            
        print(self.border, file=file)