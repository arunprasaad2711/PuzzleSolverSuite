import requests
import json
import os
from datetime import datetime
import re

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(cell) for cell in row))
    print()

url = "http://127.0.0.1:5500/solve"
# PAYLOADS_DIR = "./TestJSONs/OmniSolver"
# PAYLOADS_DIR = "./TestJSONs/Experiments"
PAYLOADS_DIR = "./TestJSONs/ChessSolver"
# PAYLOADS_DIR = "./TestJSONs/PersonalSudokus"

# FName = "AntiRatioAntiConsecutive.json"
FName = "NQueensExperiment_11queens.json"
# FName = "RenbanLinesAsSudoku_MiracleSudoku.json"
# FName = "Tents_HorvathZoltan.json"
# FName = "Tents_StevenScott.json"
# FName = "Dummy.json"

FilePath = os.path.join(PAYLOADS_DIR, FName)
with open(FilePath, 'r') as f:
    payload = json.load(f)

try:
    resp = requests.post(url, json=payload)
    print(f"Status Code: {resp.status_code}")
    result = resp.json()

    # --- Save response ---
    subfolder = os.path.basename(PAYLOADS_DIR)  # e.g. "Experiments"
    results_dir = os.path.join("./TestJSONs_Results", subfolder)
    os.makedirs(results_dir, exist_ok=True)

    result_fname = os.path.splitext(FName)[0] + ".json"
    result_path = os.path.join(results_dir, result_fname)

    # with open(result_path, 'w') as f:
    #     json.dump(result, f, indent=2)
    
    with open(result_path, 'w') as f:
        raw = json.dumps(result, indent=2)
        # Collapse arrays of numbers onto a single line
        compact = re.sub(
            r'\[\s*(\d+(?:,\s*\d+)*)\s*\]',
            lambda m: '[' + ', '.join(re.findall(r'\d+', m.group(1))) + ']',
            raw
        )
        f.write(compact)
    print(f"Response saved to: {result_path}")
    # ---------------------

    if result['success']:
        if "solutions" in result:
            for solution in result["solutions"]:
                print_matrix(solution)
    else:
        print(result)
        print("Something went wrong!")

except requests.exceptions.ConnectionError:
    print("Connection failed! Is the server running?")
except Exception as e:
    print(f"Other error: {e}")