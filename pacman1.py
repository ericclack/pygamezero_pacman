WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE*BLOCK_SIZE
HEIGHT = WORLD_SIZE*BLOCK_SIZE
SPEED = 2

# An array containing the world tiles
world = []

# Our sprites
pacman = Actor('pacman_o.png', anchor=('left', 'top'))
pacman.x = pacman.y = 1*BLOCK_SIZE
# Direction that we're going in
pacman.dx, pacman.dy = 0,0

ghosts = []

# Your level will contain characters, they map
# to the following images
char_to_image = {
    '.': 'dot.png',
    '=': 'wall.png',
    '*': 'power.png',
    'g': 'ghost1.png',
    'G': 'ghost2.png',
}

def load_level(number):
    file = "level-%s.txt" % number
    with open(file) as f:
        for line in f:
            row = []
            for block in line:
                row.append(block)
            world.append(row)

def draw():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE))
    pacman.draw()

def update():
    pacman.x += pacman.dx
    pacman.y += pacman.dy

def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        pacman.dx = 0
    if key in (keys.UP, keys.DOWN):
        pacman.dy = 0

def on_key_down(key):
    if key == keys.LEFT:
        pacman.dx = -1
    if key == keys.RIGHT:
        pacman.dx = 1
    if key == keys.UP:
        pacman.dy = -1
    if key == keys.DOWN:
        pacman.dy = 1

load_level(1)