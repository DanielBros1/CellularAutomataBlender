import bpy
import random

# SIMULATION PARAMETERS
GRID_SIZE = 20
CELL_SIZE = 2
STEPS = 25
FRAME_INTERVAL = 15

BUILDINGS = {
    0: 'none',
    1: 'house',
    2: 'tree',
    3: 'road',
    4: 'water',
    5: 'devastated-two-turns',
}


def generate_river(grid):
    river_width = 1
    start_x = random.randint(0, GRID_SIZE - 1)
    start_y = 0 if random.choice([True, False]) else GRID_SIZE - 1
    end_y = GRID_SIZE - 1 if start_y == 0 else 0

    current_x = start_x
    current_y = start_y

    direction_choices = [-1, 0, 1]

    while current_y != end_y:
        # Dodaj rzeke do obecnego pola
        for offset in range(-river_width, river_width + 1):
            if 0 <= current_x + offset < GRID_SIZE:
                grid[current_x + offset][current_y] = 4

        current_y += 1 if start_y == 0 else -1

        if random.random() < 0.6:  # Zmienia kierunek ruchu
            current_x += random.choice(direction_choices)

        current_x = max(0, min(GRID_SIZE - 1, current_x))

    # Ostatnie pole
    for offset in range(-river_width, river_width + 1):
        if 0 <= current_x + offset < GRID_SIZE:
            grid[current_x + offset][current_y] = 4


def init_grid():
    initial_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Fill grid with zeros

    max_houses = 5
    center_size = 4  # Rozmiar środkowego obszaru (4x4)

    generate_river(initial_grid)

    # Oblicz granice środkowego obszaru
    start = (GRID_SIZE - center_size) // 2
    end = start + center_size - 1

    # Generowanie domów w środkowym obszarze 4x4
    for _ in range(max_houses):
        house_x = random.randint(start, end)
        house_y = random.randint(start, end)
        initial_grid[house_x][house_y] = 1

    return initial_grid


def count_neighbours(grid_, x_pos, y_pos):
    house_counter = 0
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x_pos + dx, y_pos + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            if grid_[nx][ny] == 1:
                house_counter += 1

    return house_counter


def duplicate(obj, collection, data=True, actions=True):
    ob_copy = obj.copy()
    if data:
        ob_copy.data = ob_copy.data.copy()
    if actions and ob_copy.animation_data:
        ob_copy.animation_data.action = ob_copy.animation_data.action.copy()
    collection.objects.link(ob_copy)
    return ob_copy


def rem():
    for obj in bpy.data.objects:
        if (('house' in obj.name or 'tree' in obj.name or 'water' in obj.name)
                and obj.name != 'house' and obj.name != 'tree' and obj.name != 'water'):
            bpy.context.collection.objects.unlink(obj)
            bpy.data.objects.remove(obj)


def create_and_animate_object(obj, name, location, scale, frame_start, frame_end):
    obj_copy = duplicate(obj, bpy.context.collection)
    obj_copy.name = name
    obj_copy.location = location

    # Początkowe skalowanie na 0 (niewidoczne)
    obj_copy.scale = (0, 0, 0)
    obj_copy.keyframe_insert(data_path="scale", frame=frame_start)

    # Końcowe skalowanie na 1 (widoczne)
    obj_copy.scale = scale
    obj_copy.keyframe_insert(data_path="scale", frame=frame_end)



rem()

house = bpy.data.objects['house']
house.hide_set(True)
tree = bpy.data.objects['tree']
tree.hide_set(True)
water = bpy.data.objects['water']
water.hide_set(True)

house.animation_data_clear()
tree.animation_data_clear()
water.animation_data_clear()

HOUSE_SIZE = (0.30, 0.42, 0.6)
TREE_SIZE = (0.5, 0.6, 0.5)
WATER_SIZE = (0.5, 0.5, 0.1)

HOUSE_Z_LOCATION = 0.6
TREE_Z_LOCATION = 1.93
WATER_Z_LOCATION = 0.1

grid = init_grid()
bpy.context.scene.frame_set(0)



for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        if grid[x][y] == 1:
            create_and_animate_object(house, f"house_{x}_{y}", (x, y, HOUSE_Z_LOCATION), HOUSE_SIZE, 0, FRAME_INTERVAL)
        elif grid[x][y] == 2:
            create_and_animate_object(tree, f"tree_{x}_{y}", (x, y, TREE_Z_LOCATION), TREE_SIZE, 0, FRAME_INTERVAL)
        elif grid[x][y] == 4:
            create_and_animate_object(water, f"water_{x}_{y}", (x, y, WATER_Z_LOCATION), WATER_SIZE, 0, FRAME_INTERVAL)

for i in range(1, STEPS + 1):
    frame = i * FRAME_INTERVAL
    neighbours = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            neighbours[x][y] = count_neighbours(grid, x, y)
            print(neighbours[x][y])

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            # count_neighbours ---> @return: tuple (house_count, tree_count)
            house_count = neighbours[x][y]

            if (house_count == 2) and grid[x][y] == 0:
                # Generate a house
                # print(f'Building house at {x}, {y} at frame {frame}')
                grid[x][y] = 1

                create_and_animate_object(house, f"house_{x}_{y}", (x, y, HOUSE_Z_LOCATION),
                                          HOUSE_SIZE, frame + FRAME_INTERVAL / 4, frame + FRAME_INTERVAL)

            elif (house_count >= 4 or house_count == 1) and grid[x][y] == 1:
                house_name = f"house_{x}_{y}"
                grid[x][y] = 5

                if house_name in bpy.context.collection.objects:

                    obj_to_remove = bpy.context.collection.objects[house_name]

                    # Zmniejsz skalę, zamiast usuwać obiekt
                    obj_to_remove.scale = HOUSE_SIZE
                    obj_to_remove.keyframe_insert(data_path="scale", frame=frame + FRAME_INTERVAL / 4)

                    obj_to_remove.scale = (0, 0, 0)
                    obj_to_remove.keyframe_insert(data_path="scale", frame=frame + FRAME_INTERVAL / 2)

                    print(f'Removing house at {x}, {y} at frame {frame}')

                    if random.random() < 0.15:
                        print(f'Generating tree at {x}, {y} at frame {frame}')
                        grid[x][y] = 2

                        create_and_animate_object(tree, f"tree_{x}_{y}", (x, y, TREE_Z_LOCATION),
                                                  TREE_SIZE, frame + FRAME_INTERVAL / 4, frame + FRAME_INTERVAL)

                        # WYKASUJ CZTERY DOMY WOKÓŁ (x[+1], y), (x[-1], y), (x, y[+1]), (x, y[-1])
                        grid_to_remove = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                        for x_, y_ in grid_to_remove:
                            if 0 <= x_ < GRID_SIZE and 0 <= y_ < GRID_SIZE:
                                house_name = f"house_{x_}_{y_}"
                                if house_name in bpy.context.collection.objects:
                                    obj_to_remove = bpy.context.collection.objects[house_name]

                                    # Zmniejsz skalę do 0, zamiast usuwać obiekt
                                    obj_to_remove.scale = HOUSE_SIZE
                                    obj_to_remove.keyframe_insert(data_path="scale", frame=frame + FRAME_INTERVAL / 4)

                                    obj_to_remove.scale = (0, 0, 0)
                                    obj_to_remove.keyframe_insert(data_path="scale", frame=frame + FRAME_INTERVAL / 2)

                                    grid[x_][y_] = 5
