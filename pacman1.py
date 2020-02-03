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
dx,dy = 0,0


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
            for block in line.strip():
                row.append(block)
            world.append(row)

def draw():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE))
    pacman.draw()

def blocks_at(pixel_pos, delta=(0,0)):
    """Return a list of tiles at this position + delta"""

    x,y = pixel_pos
    dx,dy = delta
    x += dx
    y += dy

    # Integer block pos, using floor
    ix,iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)
    # Remainder
    rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE

    blocks = [ world[iy][ix] ]
    if rx: blocks.append(world[iy][ix+1])
    if ry: blocks.append(world[iy+1][ix])
    if rx and ry: blocks.append(world[iy+1][ix+1])

    return blocks

def update():
    global dx,dy
    # In order to go in direction dx, dy their must be no wall that way
    next_blocks = blocks_at(pacman.pos, (dx,dy))
    if '=' not in next_blocks:
        pacman.x += dx * SPEED
        pacman.y += dy * SPEED

def on_key_up(key):
    global dx,dy
    dx,dy = 0,0

def on_key_down(key):
    global dx,dy
    if key == keys.LEFT:
        dx = -1
    if key == keys.RIGHT:
        dx = 1
    if key == keys.UP:
        dy = -1
    if key == keys.DOWN:
        dy = 1

load_level(1)

def every_second():
    global dx,dy
    print(blocks_at(pacman.pos, (dx,dy)))

clock.schedule_interval(every_second, 0.25)