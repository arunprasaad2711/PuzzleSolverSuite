extends Node3D

@onready var cube_visual: CubeVisual = $CubeRoot
@onready var rotation_engine: RotationEngine = $RotationEngine

var cube_state: CubeState

#func _ready():
	#cube_state = CubeState.new()
	#cube_state.create_solved()
#
	#cube_visual.build(cube_state)
	#rotation_engine.setup(cube_state, cube_visual)


func _ready():
	cube_state = CubeState.new()
	cube_state.create_solved()

	cube_visual.build(cube_state)
	rotation_engine.setup(cube_state, cube_visual)

	var parser := MoveParser.new()
	var moves := parser.parse_sequence("U R' U")

	for move in moves:
		await rotation_engine.apply_move(move)
