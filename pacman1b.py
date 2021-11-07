WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE*BLOCK_SIZE
HEIGHT = WORLD_SIZE*BLOCK_SIZE

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

def blocks_ahead_of_pacman(dx, dy):
    """Return a list of tiles at this position + delta"""

    # Here's where we want to move to
    x = pacman.x + dx
    y = pacman.y + dy

    # Find integer block pos, using floor (so 4.7 becomes 4)
    ix,iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)
    # Remainder let's us check adjacent blocks
    rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE

    blocks = [ world[iy][ix] ]
    if rx: blocks.append(world[iy][ix+1])
    if ry: blocks.append(world[iy+1][ix])
    if rx and ry: blocks.append(world[iy+1][ix+1])

    return blocks

def update():
    # In order to go in direction dx, dy there must be no wall that way
    if '=' not in blocks_ahead_of_pacman(pacman.dx, 0):
        pacman.x += pacman.dx
    if '=' not in blocks_ahead_of_pacman(0, pacman.dy):
        pacman.y += pacman.dy

    #if '=' not in blocks_ahead_of_pacman(pacman.dx, pacman.dy):
    #    pacman.x += pacman.dx
    #    pacman.y += pacman.dy

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

def every_second():
    print(blocks_ahead_of_pacman(pacman.dx, pacman.dy))

clock.schedule_interval(every_second, 0.25)