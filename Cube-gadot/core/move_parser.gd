extends RefCounted
class_name MoveParser

const FACE_MAP := {
	"R": { "axis": "X", "layer":  1 },
	"L": { "axis": "X", "layer": -1 },
	"U": { "axis": "Y", "layer":  1 },
	"D": { "axis": "Y", "layer": -1 },
	"F": { "axis": "Z", "layer":  1 },
	"B": { "axis": "Z", "layer": -1 }
}

class Move:
	var face: String
	var axis: String
	var layer: int
	var turns: int
	var clockwise: bool

	func _init(f: String, a: String, l: int, t: int, cw: bool):
		face = f
		axis = a
		layer = l
		turns = t
		clockwise = cw

func parse_token(token: String) -> Move:
	if token.length() == 0:
		push_error("Empty move token")
		return null

	var face := token[0]
	if not FACE_MAP.has(face):
		push_error("Invalid face: %s" % face)
		return null

	var axis :String = FACE_MAP[face]["axis"]
	var layer :int = FACE_MAP[face]["layer"]

	var turns := 1
	var clockwise := true

	if token.length() > 1:
		if token[1] == "'":
			clockwise = false
		elif token[1] == "2":
			turns = 2
		else:
			push_error("Invalid modifier in token: %s" % token)
			return null

	return Move.new(face, axis, layer, turns, clockwise)

func parse_sequence(sequence: String) -> Array:
	var moves := []
	var tokens := sequence.strip_edges().split(" ", false)

	for token in tokens:
		var move := parse_token(token)
		if move == null:
			push_error("Failed to parse move: %s" % token)
			return []
		moves.append(move)

	return moves
