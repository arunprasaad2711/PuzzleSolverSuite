extends Node

func _ready():
	print("=== Move Parser Test ===")

	var parser := MoveParser.new()

	var sequence := "R U R' U' F2 D"
	var moves := parser.parse_sequence(sequence)

	assert(moves.size() == 6)

	for m in moves:
		print(
			"face=", m.face,
			" axis=", m.axis,
			" layer=", m.layer,
			" turns=", m.turns,
			" cw=", m.clockwise
		)

	print("✔ Move Parser Test PASSED")
