extends Node3D
class_name CubeVisual

@export var cubelet_scene: PackedScene
var cube_state: CubeState
var cubelets : Dictionary[Vector3i, Cubelet] = {} # Vector3i -> Cubelet

func build(cube: CubeState):
	cube_state = cube
	clear()

	for pos in cube.cubelets.keys():
		var cubelet_data :CubeletData = cube.cubelets[pos]
		var cubelet := cubelet_scene.instantiate() as Cubelet
		add_child(cubelet)

		cubelet.setup(cubelet_data)
		cubelets[pos] = cubelet

func clear():
	for child in get_children():
		child.queue_free()
	cubelets.clear()

func sync_from_state(state: CubeState) -> void:
	for cubelet in cubelets.values():
		cubelet.update_transform()
		#cubelet.update_materials()
