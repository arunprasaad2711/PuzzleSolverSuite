import requests

url = "http://127.0.0.1:8000/solve"

payload = {
    "Matrix": [ [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0] ],
    "AntiKnight": True,
    "AntiKing": True,
    "OrthogonalNonConsec": True
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
