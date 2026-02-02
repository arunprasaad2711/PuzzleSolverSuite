extends RefCounted
class_name CubeState

var cubelets := {} # Vector3i -> CubeletData


func create_solved():
	cubelets.clear()

	for x in [-1, 0, 1]:
		for y in [-1, 0, 1]:
			for z in [-1, 0, 1]:
				var pos = Vector3i(x, y, z)
				var faces = {}

				if y == 1: faces["U"] = Color.WHITE
				if y == -1: faces["D"] = Color.YELLOW
				if z == 1: faces["F"] = Color.GREEN
				if z == -1: faces["B"] = Color.BLUE
				if x == 1: faces["R"] = Color.RED
				if x == -1: faces["L"] = Color.ORANGE

				cubelets[pos] = CubeletData.new(pos, faces)

func get_layer(axis: String, value: int) -> Array:
	var result := []

	for cubelet in cubelets.values():
		match axis:
			"X":
				if cubelet.position.x == value:
					result.append(cubelet)
			"Y":
				if cubelet.position.y == value:
					result.append(cubelet)
			"Z":
				if cubelet.position.z == value:
					result.append(cubelet)

	return result
func rotate_layer(axis: String, value: int, clockwise: bool):
	var affected := get_layer(axis, value)
	var moved := {}

	for cubelet in affected:
		var old_pos :Vector3i = cubelet.position
		var new_pos :Vector3i = old_pos

		match axis:
			"X":
				new_pos.y = (-old_pos.z) if clockwise else old_pos.z
				new_pos.z = (old_pos.y) if clockwise else -old_pos.y
			"Y":
				new_pos.x = (old_pos.z) if clockwise else -old_pos.z
				new_pos.z = (-old_pos.x) if clockwise else old_pos.x
			"Z":
				new_pos.x = (-old_pos.y) if clockwise else old_pos.y
				new_pos.y = (old_pos.x) if clockwise else -old_pos.x

		cubelet.position = new_pos
		moved[old_pos] = cubelet

	for old_pos in moved.keys():
		cubelets.erase(old_pos)

	for cubelet in moved.values():
		cubelets[cubelet.position] = cubelet
