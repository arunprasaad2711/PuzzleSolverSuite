extends Node3D
class_name Cubelet

@onready var mesh: MeshInstance3D = $Mesh

var data: CubeletData

const FACE_NORMALS := {
	"R": Vector3.RIGHT,
	"L": Vector3.LEFT,
	"U": Vector3.UP,
	"D": Vector3.DOWN,
	"F": Vector3.FORWARD,
	"B": Vector3.BACK
}



func face_to_surface(face: String) -> int:
	match face:
		"R":
			return 0
		"L":
			return 1
		"U":
			return 2
		"D":
			return 3
		"F":
			return 4
		"B":
			return 5
		_:
			return -1


func create_cube_mesh() -> ArrayMesh:
	var array_mesh := ArrayMesh.new()

	var faces := [
		# +X (Right)
		{
			"normal": Vector3.RIGHT,
			"verts": [
				Vector3(0.5, -0.5,  0.5),
				Vector3(0.5,  0.5,  0.5),
				Vector3(0.5,  0.5, -0.5),
				Vector3(0.5, -0.5, -0.5)
			]
		},
		# -X (Left)
		{
			"normal": Vector3.LEFT,
			"verts": [
				Vector3(-0.5, -0.5, -0.5),
				Vector3(-0.5,  0.5, -0.5),
				Vector3(-0.5,  0.5,  0.5),
				Vector3(-0.5, -0.5,  0.5)
			]
		},
		# +Y (Up)
		{
			"normal": Vector3.UP,
			"verts": [
				Vector3(-0.5, 0.5,  0.5),
				Vector3( 0.5, 0.5,  0.5),
				Vector3( 0.5, 0.5, -0.5),
				Vector3(-0.5, 0.5, -0.5)
			]
		},
		# -Y (Down)
		{
			"normal": Vector3.DOWN,
			"verts": [
				Vector3(-0.5, -0.5, -0.5),
				Vector3( 0.5, -0.5, -0.5),
				Vector3( 0.5, -0.5,  0.5),
				Vector3(-0.5, -0.5,  0.5)
			]
		},
		# +Z (Front)
		{
			"normal": Vector3.FORWARD,
			"verts": [
				Vector3(-0.5, -0.5, 0.5),
				Vector3(-0.5,  0.5, 0.5),
				Vector3( 0.5,  0.5, 0.5),
				Vector3( 0.5, -0.5, 0.5)
			]
		},
		# -Z (Back)
		{
			"normal": Vector3.BACK,
			"verts": [
				Vector3( 0.5, -0.5, -0.5),
				Vector3( 0.5,  0.5, -0.5),
				Vector3(-0.5,  0.5, -0.5),
				Vector3(-0.5, -0.5, -0.5)
			]
		}
	]

	for face in faces:
		var arrays := []
		arrays.resize(Mesh.ARRAY_MAX)

		var vertices := PackedVector3Array(face["verts"])
		var normals := PackedVector3Array([
			face["normal"],
			face["normal"],
			face["normal"],
			face["normal"]
		])

		var indices := PackedInt32Array([0, 1, 2, 0, 2, 3])

		arrays[Mesh.ARRAY_VERTEX] = vertices
		arrays[Mesh.ARRAY_NORMAL] = normals
		arrays[Mesh.ARRAY_INDEX] = indices

		array_mesh.add_surface_from_arrays(
			Mesh.PRIMITIVE_TRIANGLES,
			arrays
		)

	return array_mesh


#func normal_to_surface(normal: Vector3) -> int:
	#var n := normal.normalized()
#
	#if abs(n.x) > 0.9:
		#return 0 if n.x > 0 else 1
	#if abs(n.y) > 0.9:
		#return 2 if n.y > 0 else 3
	#if abs(n.z) > 0.9:
		#return 4 if n.z > 0 else 5
#
	#return -1



func setup(cubelet_data: CubeletData):
	data = cubelet_data
	mesh.mesh = create_cube_mesh()
	update_transform()
	update_materials()


func update_transform():
	position = Vector3(
		data.position.x,
		data.position.y,
		data.position.z
	)

	#basis = data.orientation
	scale = Vector3(0.95, 0.95, 0.95)
	#scale = Vector3.ONE

#func update_materials() -> void:
	#mesh.mesh = mesh.mesh.duplicate()
#
	#for i in range(6):
		#var mat := StandardMaterial3D.new()
		#mat.albedo_color = Color.BLACK
		#mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_DISABLED
		#mesh.set_surface_override_material(i, mat)
#
	#for face_key in data.faces.keys():
		#var local_normal :Vector3 = FACE_NORMALS[face_key]
		#var world_normal :Vector3 = basis * local_normal
#
		#var surface := normal_to_surface(world_normal)
		#if surface == -1:
			#continue
#
		#var mat := StandardMaterial3D.new()
		#mat.albedo_color = data.faces[face_key]
		#mat.cull_mode = BaseMaterial3D.CULL_DISABLED
		#mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_OPAQUE_ONLY
		#mesh.set_surface_override_material(surface, mat)

# 1. Relax the threshold. On a cube, 0.5 is sufficient separation.
#func normal_to_surface(normal: Vector3) -> int:
	#var n := normal.normalized()
	## Lower threshold from 0.9 to 0.5 to catch slightly drifted rotations
	#if abs(n.x) > 0.5:
		#return 0 if n.x > 0 else 1
	#if abs(n.y) > 0.5:
		#return 2 if n.y > 0 else 3
	#if abs(n.z) > 0.5:
		#return 4 if n.z > 0 else 5
	#return -1

# 2. Fix the "Drift" by snapping the rotation after every move
func update_materials() -> void:
	# Ensure the mesh is unique so we don't affect other instances
	mesh.mesh = mesh.mesh.duplicate()

	# 1. Reset all faces to Black (Plastic color)
	for i in range(6):
		var mat := StandardMaterial3D.new()
		mat.albedo_color = Color.BLACK
		mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_DISABLED
		mesh.set_surface_override_material(i, mat)

	# 2. Apply colors based on STATIC local definition
	# If data says "R" is Red, we paint the Right Surface (0) Red.
	# We do NOT care about world rotation here. The Engine handles that.
	for face_key in data.faces.keys():
		var surface_index := face_to_surface(face_key)
		
		if surface_index == -1:
			continue

		var mat := StandardMaterial3D.new()
		mat.albedo_color = data.faces[face_key]
		mat.cull_mode = BaseMaterial3D.CULL_DISABLED
		# OPAQUE_ONLY helps preventing transparency sorting issues
		mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_OPAQUE_ONLY 
		
		mesh.set_surface_override_material(surface_index, mat)

# Helper to snap a vector to exactly (1,0,0), (0,1,0), etc.
func _snap_vector(v: Vector3) -> Vector3:
	if abs(v.x) > abs(v.y) and abs(v.x) > abs(v.z):
		return Vector3(sign(v.x), 0, 0)
	elif abs(v.y) > abs(v.z):
		return Vector3(0, sign(v.y), 0)
	else:
		return Vector3(0, 0, sign(v.z))

#
#func update_materials() -> void:
	#mesh.mesh = mesh.mesh.duplicate()
#
	## 1️⃣ Reset all faces to INTERNAL (not visible, no depth write)
	#for i in range(6):
		#var mat: StandardMaterial3D = StandardMaterial3D.new()
		#mat.albedo_color = Color.BLACK
		#mat.transparency = BaseMaterial3D.TRANSPARENCY_DISABLED
		#mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_DISABLED
		##mat.cull_mode = BaseMaterial3D.CULL_BACK
		#mesh.set_surface_override_material(i, mat)
#
	## 2️⃣ Apply sticker faces based on orientation
	#for face_key in data.faces.keys():
		#var local_normal: Vector3 = FACE_NORMALS[face_key]
		##var world_normal: Vector3 = data.orientation * local_normal
		#var world_normal: Vector3 = basis * local_normal
		##var world_normal: Vector3 = global_basis * local_normal
#
#
		#var surface: int = normal_to_surface(world_normal)
		#if surface == -1:
			#continue
#
		#var mat: StandardMaterial3D = StandardMaterial3D.new()
		#mat.albedo_color = data.faces[face_key]
		#mat.transparency = BaseMaterial3D.TRANSPARENCY_DISABLED
		##mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_OPAQUE_ONLY
		#mat.cull_mode = BaseMaterial3D.CULL_DISABLED
		#mat.roughness = 0.4
		#mat.metallic = 0.0
		#mat.albedo_color.a = 1.0
		#mesh.set_surface_override_material(surface, mat)
#




#func update_materials():
	## First: make ALL faces invisible (internal faces)
	#for i in range(6):
		#var mat := StandardMaterial3D.new()
		#mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		#mat.albedo_color = Color(0, 0, 0, 0)
		#mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_DISABLED
		#mesh.set_surface_override_material(i, mat)
#
	## Then: apply visible sticker faces
	#for face in data.faces.keys():
		#var surface := face_to_surface(face)
		#if surface == -1:
			#continue
#
		#var mat := StandardMaterial3D.new()
		#mat.transparency = BaseMaterial3D.TRANSPARENCY_DISABLED
		#mat.albedo_color = data.faces[face]
		#mat.albedo_color.a = 1.0
		#mat.roughness = 0.4
		#mat.metallic = 0.0
		#mat.cull_mode = BaseMaterial3D.CULL_DISABLED
		##mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_OPAQUE_ONLY
		#mesh.set_surface_override_material(surface, mat)
#
