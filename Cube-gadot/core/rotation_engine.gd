extends Node
class_name RotationEngine

signal move_finished

var cube_state: CubeState
var cube_visual: CubeVisual

var is_rotating: bool = false
var rotation_duration: float = 0.25

func setup(state: CubeState, visual: CubeVisual):
	cube_state = state
	cube_visual = visual

func get_visual_layer(axis: String, layer: int) -> Array:
	var result := []

	for cubelet in cube_visual.cubelets.values():
		match axis:
			"X":
				if cubelet.data.position.x == layer:
					result.append(cubelet)
			"Y":
				if cubelet.data.position.y == layer:
					result.append(cubelet)
			"Z":
				if cubelet.data.position.z == layer:
					result.append(cubelet)

	return result

func apply_move(move):
	if is_rotating:
		return

	is_rotating = true

	for i in range(move.turns):
		await _rotate_once(move.axis, move.layer, move.clockwise)

	is_rotating = false
	move_finished.emit()

func _rotate_once(axis: String, layer: int, clockwise: bool) -> void:
	var cubelets: Array = get_visual_layer(axis, layer)

	# 1️⃣ Compute center of the layer
	var center: Vector3 = Vector3.ZERO
	for c in cubelets:
		center += c.global_position
	center /= float(cubelets.size())

	# 2️⃣ Create pivot at center
	var pivot: Node3D = Node3D.new()
	cube_visual.add_child(pivot)
	pivot.global_position = center

	# 3️⃣ Reparent cubelets to pivot (CORRECTLY)
	for c in cubelets:
		var t: Transform3D = c.global_transform
		cube_visual.remove_child(c)
		pivot.add_child(c)
		c.global_transform = t

	# 4️⃣ Rotation axis
	var axis_vec: Vector3
	match axis:
		"X":
			axis_vec = Vector3.RIGHT
		"Y":
			axis_vec = Vector3.UP
		"Z":
			axis_vec = Vector3.FORWARD

	var angle: float = (-PI / 2.0) if clockwise else (PI / 2.0)

	# 5️⃣ Animate rotation using BASIS
	var start_basis: Basis = pivot.basis
	var target_basis: Basis = Basis(axis_vec, angle) * start_basis

	var tween: Tween = create_tween()
	tween.tween_property(
		pivot,
		"basis",
		target_basis,
		rotation_duration
	)

	await tween.finished

	# 6️⃣ Reparent cubelets back to CubeRoot (CORRECTLY)
	for c in cubelets:
		var t2: Transform3D = c.global_transform
		pivot.remove_child(c)
		cube_visual.add_child(c)
		c.global_transform = t2

	pivot.queue_free()

	# 7️⃣ Update LOGICAL cube state ONLY
	cube_state.rotate_layer(axis, layer, clockwise)
	cube_visual.sync_from_state(cube_state)
