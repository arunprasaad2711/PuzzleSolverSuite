extends Node

func _ready():
	print("Running CubeState tests...")

	var cube := CubeState.new()
	cube.create_solved()

	# Store original state
	var original_positions := {}
	for pos in cube.cubelets.keys():
		original_positions[pos] = cube.cubelets[pos].position

	# Apply move + inverse
	cube.rotate_layer("Y", 1, true)   # U
	cube.rotate_layer("Y", 1, false)  # U'

	# Validate positions
	for pos in original_positions.keys():
		assert(cube.cubelets.has(pos))
		assert(cube.cubelets[pos].position == pos)

	print("✔ Rotation reversible test PASSED")
