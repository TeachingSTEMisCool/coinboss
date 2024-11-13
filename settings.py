import random

WIDTH, HEIGHT = 800, 640
tile_size = 32

floor_map = [
    ['055', '057', '055', '055', '055', '055', '059', '055', '055', '055', '055', '055', '056', '055', '055', '055', '055', '059', '055', '055', '055', '055', '055', '055', '055'],
    ['055', '055', '055', '055', '055', '059', '055', '055', '055', '055', '055', '055', '055', '058', '058', '055', '057', '055', '055', '055', '055', '055', '055', '055', '055'],
    ['055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '059', '057', '055', '056', '055', '055', '055', '055', '057', '055', '055', '055', '057'],
    ['055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '057', '055', '055', '055', '055', '055', '055', '055', '055'],
    ['055', '055', '055', '055', '055', '055', '055', '055', '055', '056', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055'],
    ['055', '055', '055', '055', '055', '058', '055', '055', '055', '055', '055', '059', '055', '055', '055', '056', '055', '055', '055', '055', '055', '055', '055', '055', '055'],
    ['055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '059', '055', '055', '058', '055', '055'],
    ['055', '055', '055', '055', '055', '055', '055', '055', '055', '059', '055', '058', '055', '055', '055', '055', '057', '055', '059', '058', '055', '057', '055', '055', '056'],
    ['055', '055', '055', '055', '055', '059', '055', '057', '055', '055', '055', '055', '055', '055', '059', '055', '055', '055', '055', '055', '055', '055', '055', '055', '057'],
    ['055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055'],
    ['055', '055', '055', '055', '055', '055', '055', '056', '055', '055', '055', '055', '055', '055', '055', '055', '059', '055', '057', '055', '055', '055', '055', '055', '057'],
    ['055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '057', '055', '058', '055', '055', '055', '055', '055', '055', '055', '055', '055', '059'],
    ['055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '056', '055', '058', '055', '055', '055', '055', '055', '055', '055'],
    ['055', '057', '056', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055'],
    ['055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055'],
    ['055', '055', '055', '055', '055', '058', '055', '055', '055', '055', '055', '055', '055', '058', '055', '055', '055', '056', '056', '055', '055', '055', '055', '058', '055'],
    ['055', '055', '058', '055', '055', '055', '057', '056', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055'],
    ['055', '055', '055', '055', '055', '055', '058', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055'],
    ['055', '058', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '059', '055', '055', '055', '057', '055', '056', '055', '055'],
    ['055', '057', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '055', '058', '055']
]

detail_map = [
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'E', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, 'bush', None, None, None, None, None, None, 'E', None, None, None, 'tree', None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, 'tree', None, None, None, None, None, None, None, None, None, None, None, None, 'E', None],
    [None, None, None, None, None, 'E', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'tree', None, None, None, None, None, None, None, None, None, None, 'sm_rock', None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, 'med_rock', None, None, 'P', None, None, None, None, None, None, 'bush', None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ['E', None, None, None, None, None, None, None, None, None, None, None, None, 'lg_rock', None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'E', None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, 'sm_rock', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'tree', None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, 'tree', None, None, None, None, None, None, None, 'E', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'bush', None, None, None, None, None, None, None, None, None, None],
    [None, None, 'E', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'E', None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
]

"""
with open('detail.txt', 'w') as f:
    # Iterates through rows
    for i in range(HEIGHT // tile_size):
        detail_map.append([])
        # Iterates through cols
        for j in range(WIDTH // tile_size):
            #coin_toss = random.randint(0, 10)
            #random_tile = '0' + str(random.randint(0, 3) + 56) if coin_toss == 0 else '055'
            #floor_map[i].append(random_tile)
            detail_map[i].append(None)
        f.write(str(detail_map[i]))
        f.write(",\n")
"""
