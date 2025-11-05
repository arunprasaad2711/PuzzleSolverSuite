import pandas as pd

class PocketCubeSolver:
    
    def __init__(self):
        self.InputFile = "PocketCubeAtlas.csv"
    
    def Solve(self, InputHashes):
        
        DF = pd.read_csv(self.InputFile)
        
        filteredDF = DF[DF['hash'].isin(InputHashes)]
        
        SolvingSequenceString = list(filteredDF['inverse_sequence'].values)
        ScrambleSequenceString = list(filteredDF['scramble_sequence'].values)
        Depth = list(filteredDF['depth'].values)
        
        if len(SolvingSequenceString) == 1:
            return Depth, ScrambleSequenceString, SolvingSequenceString
        else:
            return -1, "FAIL", "FAIL"