import cube

my_cube = cube.Cube()
my_cube.parse_move_notation("U")
my_cube.x_rotation(1)

print(my_cube.to_string())

