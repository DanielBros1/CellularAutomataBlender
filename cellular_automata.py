import bpy
import random

"""
Proszę napisać program generujący miasto z wykorzystaniem automatu komórkowego. 
W tym celu należy napisać Pythonie skrypt tworzący animację w programie Blender. 
Animacja powinna przedstawiać ewolucję miasta.
Proponowane założenia programu:
- używamy dwuwymiarowego automatu komórkowego, aby wygenerować rozmieszczenie obiektów,
- komórka może mieć kilka różnych stanów w zależności od tego, jaki obiekt ma zostać na niej zbudowany 
(i czy ma zostać zbudowany),
- na dwuwymiarowej siatce ustawiamy obiekty 3D,
- sąsiedztwo może mieć promień większy niż 1 w zależności od potrzeb.
Możliwe są modyfikacje tych założeń po uzgodnieniu ze mną.

Animację proponuję zrobić w następujący sposób:
Tworzymy po jednym prototypie każdego rodzaju obiektu (np. budynku) i ukrywamy go. 
W toku animacji tworzymy kopie obiektów i przesuwamy je na odpowiednie miejsce, a następnie ustawiamy widoczność na True
"""

GRID_SIZE = 15
CELL_SIZE = 2
STEPS = 8
FRAME_INTERVAL = 0

BUILDINGS = {
    0: 'none',
    1: 'house',
    2: 'tree',
    3: 'road',
    4: 'water',
}


# Initialize grid
def init_grid():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Fill grid with zeros

    max_houses = 5
    max_trees = 5

    center_size = 4  # Rozmiar środkowego obszaru (4x4)

    # Oblicz granice środkowego obszaru
    start = (GRID_SIZE - center_size) // 2
    end = start + center_size - 1

    # Generowanie domów w środkowym obszarze 4x4
    for j in range(max_houses):
        house_x = random.randint(start, end)
        house_y = random.randint(start, end)
        grid[house_x][house_y] = 1
    for j in range(max_trees):
        grid[random.randint(0, GRID_SIZE - 1)][random.randint(0, GRID_SIZE - 1)] = 2

    print(grid)
    return grid


# Neighbourhood function
"""
@:return: tuple (house_count, tree_count)
"""


def count_neighbours(grid, x, y):
    house_count = 0
    tree_count = 0
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            if grid[nx][ny] == 1:
                house_count += 1
            elif grid[nx][ny] == 2:
                tree_count += 1

    return house_count, tree_count


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
        if 'house' in obj.name and 'house' != obj.name:
            bpy.data.objects.remove(obj)
        elif 'tree' in obj.name and 'tree' != obj.name:
            bpy.data.objects.remove(obj)


rem()

house = bpy.data.objects['house']
house.hide_set(True)

tree = bpy.data.objects['tree']
tree.hide_set(True)

house.animation_data_clear()
tree.animation_data_clear()

# for i in range(1):
#     bpy.context.scene.frame_set(0)
#     obj_copy = duplicate(house, bpy.context.collection)
#     obj_copy.name = "house" + str(i)
#     obj_copy.location = (0, 0, 2)
#     obj_copy.hide_viewport = True
#     obj_copy.keyframe_insert(data_path="location", index=-1)
#     obj_copy.keyframe_insert(data_path="hide_viewport")

#     bpy.context.scene.frame_set(60)
#     obj_copy.location = (i, 0, 2)
#     obj_copy.hide_viewport = False
#     obj_copy.keyframe_insert(data_path="location", index=-1)
#     obj_copy.keyframe_insert(data_path="hide_viewport")


# WRITE A PROGRAM

# Generate a grid and generate house only on cells with value 1
# Generate a grid and generate tree only on cells with value 2

grid = init_grid()
bpy.context.scene.frame_set(0)
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        if grid[x][y] == 1:
            obj_copy = duplicate(house, bpy.context.collection)
            obj_copy.name = f"house_{x}_{y}"
            obj_copy.location = (x, y, 1)
            obj_copy.hide_viewport = False
            obj_copy.keyframe_insert(data_path="location", index=-1)
            obj_copy.keyframe_insert(data_path="hide_viewport")
        elif grid[x][y] == 2:
            obj_copy = duplicate(tree, bpy.context.collection)
            obj_copy.name = f"tree_{x}_{y}"

            # Set initial position
            obj_copy.location = (x, y, 1)
            obj_copy.keyframe_insert(data_path="location", index=-1)

            # Set initial visibility
            obj_copy.hide_viewport = False
            obj_copy.keyframe_insert(data_path="hide_viewport")

# Print count_neighbours for each cell
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        print(count_neighbours(grid, x, y), end=' ')
    print()
print("DOWN")
# # Make animation. Move houses and trees to new positions (randomly: +/- 1 in x and y)
# for i in range(1, STEPS):
#    bpy.context.scene.frame_set(i * FRAME_INTERVAL)
#    for x in range(GRID_SIZE):
#        for y in range(GRID_SIZE):
#            if grid[x][y] == 1:
#                obj_copy = bpy.data.objects[f"house_{x}_{y}"]
#                obj_copy.location = (x + random.randint(-1, 1), y + random.randint(-1, 1), 1)
#                obj_copy.keyframe_insert(data_path="location", index=-1)
#            elif grid[x][y] == 2:
#                obj_copy = bpy.data.objects[f"tree_{x}_{y}"]
#                obj_copy.location = (x + random.randint(-1, 1), y + random.randint(-1, 1), 1)
#                obj_copy.keyframe_insert(data_path="location", index=-1)

for i in range(0, STEPS):
    neighbours = [[(0, 0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            neighbours[x][y] = count_neighbours(grid, x, y)

    bpy.context.scene.frame_set(i * FRAME_INTERVAL)

    print(neighbours)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            # count_neighbours ---> @return: tuple (house_count, tree_count)
            # if house_count = 3. Generate a house
            house_count = neighbours[x][y][0]
            
            if (house_count == 3 or house_count == 2) and grid[x][y] == 0:
                obj_copy = duplicate(house, bpy.context.collection)
                obj_copy.name = f"house_{x}_{y}"

                # Initial position (outside the grid)
                obj_copy.location = (1, 1, 1)
                obj_copy.hide_viewport = True
                obj_copy.keyframe_insert(data_path="location", index=-1)
                obj_copy.keyframe_insert(data_path="hide_viewport")

                # Set final attributes
                bpy.context.scene.frame_set(bpy.context.scene.frame_current + 60)
                obj_copy.location = (x, y, 1)
                obj_copy.hide_viewport = False
                obj_copy.keyframe_insert(data_path="location", index=-1)
                obj_copy.keyframe_insert(data_path="hide_viewport")

                # Update grid (house is built)
                grid[x][y] = 1

            elif (house_count >= 4 or house_count == 1) and grid[x][y] == 1:

                # Znajdź obiekt po nazwie (zakładając, że został wcześniej dodany)
                house_name = f"house_{x}_{y}"

                if house_name in bpy.context.collection.objects:
                    obj_to_remove = bpy.context.collection.objects[house_name]

                    # Ukryj obiekt w widoku
                    obj_to_remove.hide_viewport = True
                    obj_to_remove.keyframe_insert(data_path="hide_viewport")

                    # Usuń obiekt z kolekcji
                    bpy.context.collection.objects.unlink(obj_to_remove)
                    bpy.data.objects.remove(obj_to_remove)


                    # Aktualizuj siatkę
                    grid[x][y] = 0


print("XD")
