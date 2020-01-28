WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE*BLOCK_SIZE
HEIGHT = WORLD_SIZE*BLOCK_SIZE

# An array containing the world tiles
world = []

pac = Actor('pacman_o.png', anchor=('left', 'top'))
pac.x = pac.y = 1 * BLOCK_SIZE

# Your level will contain characters, they map
# to the following images
char_to_image = {
    '.': 'dot.png',
    '=': 'wall.png',
    '*': 'power.png',
}

def load_level(number):
    file = "level-%s.txt" % number
    with open(file) as f:
        for line in f:
            row = []
            for block in line.strip():
                row.append(block)
            world.append(row)

def draw():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE))
    pac.draw()

load_level(1)
print(world)