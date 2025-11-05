import pandas as pd

colourCode = "OGRBWY"
FaceOrders = [
	# White Top - Yellow Bottom
	"LFRBUD", "FRBLUD", "RBLFUD", "BLFRUD",
	# Yellow Top - White Bottom
	"RFLBDU", "FLBRDU", "LBRFDU", "BRFLDU",
	# Green Top - Blue Bottom
	"LDRUFB", "DRULFB", "RULDFB", "ULDRFB",
	# Blue Top - Green Bottom
	"DLURBF", "LURDBF", "URDLBF", "RDLUBF",
	# Orange Top - Red Bottom
	"FUBDLR", "UBDFLR", "BDFULR", "DFUBLR",
	# Red Top - Orange Bottom
	"UFDBRL", "FDBURL", "DBUFRL", "BUFDRL",
]

symbol_map = {'U': 0, 'D': 1, 'L': 2, 'R': 3, 'F': 4, 'B': 5}

def cube_string_to_integer(cube_str):
    base = len(symbol_map)
    num = 0
    for ch in cube_str:
        num = num * base + symbol_map[ch]
    return num