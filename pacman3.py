import random

WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE*BLOCK_SIZE
HEIGHT = WORLD_SIZE*BLOCK_SIZE

SPEED = 2
GHOST_SPEED = 1

# An array containing the world tiles
world = []

# Our sprites
pacman = Actor('pacman_o.png')
pacman.x = pacman.y = 1.5*BLOCK_SIZE
# Direction that we're going in
pacman.dx, pacman.dy = 0,0
pacman.food_left = None

# An array of ghosts
ghosts = []
# Where do the ghosts start?
ghost_start_pos = []

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
    pacman.food_left = 0

    with open(file) as f:
        for line in f:
            row = []
            for block in line.strip():
                row.append(block)
                if block == '.': pacman.food_left += 1
            world.append(row)

def set_random_dir(sprite, speed):
    sprite.dx = random.choice([-speed, speed])
    sprite.dy = random.choice([-speed, speed])

def make_ghost_actors():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            if block in ['g', 'G']:
                # Make the sprite in the correct position
                g = Actor(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE), anchor=('left', 'top'))
                set_random_dir(g, GHOST_SPEED)

                ghosts.append(g)
                ghost_start_pos.append((x,y))
                # Now we have the ghost sprite we don't need this block
                world[y][x] = None

def draw():
    screen.clear()
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE))
    pacman.draw()
    for g in ghosts: g.draw()

def blocks_ahead_of(sprite, dx, dy):
    """Return a list of tiles at this position + delta"""

    # Here's where we want to move to, bit of rounding to
    # ensure we get the exact pixel position
    x = int(round(sprite.left)) + dx
    y = int(round(sprite.top)) + dy

    # Find integer block pos, using floor (so 4.7 becomes 4)
    ix,iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)
    # Remainder let's us check adjacent blocks
    rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE
    # Keep in bounds of world
    if ix == WORLD_SIZE-1: rx = 0
    if iy == WORLD_SIZE-1: ry = 0

    blocks = [ world[iy][ix] ]
    if rx: blocks.append(world[iy][ix+1])
    if ry: blocks.append(world[iy+1][ix])
    if rx and ry: blocks.append(world[iy+1][ix+1])

    return blocks

def wrap_around(mini, val, maxi):
    if val < mini: return maxi
    elif val > maxi: return mini
    else: return val

def move_ahead(sprite):
    # Record current pos so we can see if the sprite moved
    oldx, oldy = sprite.x, sprite.y

    # In order to go in direction dx, dy there must be no wall that way
    if '=' not in blocks_ahead_of(sprite, sprite.dx, 0):
        sprite.x += sprite.dx
    if '=' not in blocks_ahead_of(sprite, 0, sprite.dy):
        sprite.y += sprite.dy

    # Keep sprite on the screen
    sprite.x = wrap_around(0, sprite.x, WIDTH-BLOCK_SIZE)
    sprite.y = wrap_around(0, sprite.y, HEIGHT-BLOCK_SIZE)

    # Did we move?
    moved = (oldx != sprite.x or oldy != sprite.y)

    # Costume change for pacman
    if moved and sprite == pacman:
        a = 0
        if oldx < sprite.x: a = 0
        elif oldy > sprite.y: a = 90
        elif oldx > sprite.x: a = 180
        elif oldy < sprite.y: a = 270
        sprite.angle = a
    return moved

def eat_food():
    ix,iy = int(pacman.x / BLOCK_SIZE), int(pacman.y / BLOCK_SIZE)
    if world[iy][ix] == '.':
        world[iy][ix] = None
        pacman.food_left -= 1
        print("Food left: ", pacman.food_left)

def lose_life():
    pacman.x = pacman.y = 1.5 * BLOCK_SIZE
    # Move ghosts back to their start pos
    for g, (x, y) in zip(ghosts, ghost_start_pos):
        g.x = x * BLOCK_SIZE
        g.y = y * BLOCK_SIZE

def update():
    move_ahead(pacman)
    eat_food()

    for g in ghosts:
        if not move_ahead(g):
            set_random_dir(g, GHOST_SPEED)
        if g.colliderect(pacman):
            lose_life()

def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        pacman.dx = 0
    if key in (keys.UP, keys.DOWN):
        pacman.dy = 0

def on_key_down(key):
    if key == keys.LEFT:
        pacman.dx = -SPEED
        pacman.angle = 180
    if key == keys.RIGHT:
        pacman.dx = SPEED
        pacman.angle = 0
    if key == keys.UP:
        pacman.dy = -SPEED
        pacman.angle = 90
    if key == keys.DOWN:
        pacman.dy = SPEED
        pacman.angle = 270

# Game set up
load_level(1)
make_ghost_actors()