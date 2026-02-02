extends RefCounted
class_name CubeletData

var position: Vector3i
var orientation: Basis
var faces := {}  # Dictionary: face_name -> color

func _init(pos: Vector3i, face_colors: Dictionary):
	position = pos
	#orientation = Basis.IDENTITY
	faces = face_colors.duplicate()
#
#const ROTATE_FACE_MAP := {
	## Rotation around +X axis (right-hand rule)
	#"X": {
		#"U": "F",
		#"F": "D",
		#"D": "B",
		#"B": "U",
		#"R": "R",
		#"L": "L"
	#},
#
	## Rotation around +Y axis
	#"Y": {
		#"F": "L",
		#"L": "B",
		#"B": "R",
		#"R": "F",
		#"U": "U",
		#"D": "D"
	#},
#
	## Rotation around +Z axis
	#"Z": {
		#"U": "L",
		#"L": "D",
		#"D": "R",
		#"R": "U",
		#"F": "F",
		#"B": "B"
	#}
#}



#
#func rotate_faces(axis: String, clockwise: bool) -> void:
	#var new_faces: Dictionary = {}
#
	#for face in faces.keys():
		#var new_face: String = face
#
		#if clockwise:
			#new_face = ROTATE_FACE_MAP[axis][face]
		#else:
			## Counter-clockwise = 3 clockwise turns
			#for i in range(3):
				#new_face = ROTATE_FACE_MAP[axis][new_face]
#
		#new_faces[new_face] = faces[face]
#
	#faces = new_faces
