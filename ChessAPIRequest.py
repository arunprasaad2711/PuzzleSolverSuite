import requests

url = "http://127.0.0.1:8000/nqueens"

payload = {
    "Order": 8,
    "NRooks": False,
    "NBishops": False,
    "NBishopsRowConstraint": False,
    "NQueens": True
}

try:
    resp = requests.post(url, json=payload)
    print(f"Status Code: {resp.status_code}")
    
    if resp.text:  # Only try to parse JSON if there's content
        print("JSON Response:")
        print(resp.json())
    else:
        print("Empty response!")
        
except requests.exceptions.ConnectionError:
    print("Connection failed! Is the server running?")
except Exception as e:
    print(f"Other error: {e}")
