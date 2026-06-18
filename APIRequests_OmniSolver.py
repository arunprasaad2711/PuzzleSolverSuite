import requests
import json
import os

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(cell) for cell in row))
    print()

url = "http://127.0.0.1:5500/solve"
PAYLOADS_DIR = "./TestJSONs/OmniSolver"
# PAYLOADS_DIR = "./TestJSONs/PersonalSudokus"
FName = "Tents_PuzzleTentHard15x15_ID_4511247.json"
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
