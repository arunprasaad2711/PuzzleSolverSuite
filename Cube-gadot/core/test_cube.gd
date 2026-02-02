var cube := CubeState.new()
cube.create_solved()
cube.rotate_layer("Y", 1, true) # U move
cube.rotate_layer("Y", 1, false) # U'
