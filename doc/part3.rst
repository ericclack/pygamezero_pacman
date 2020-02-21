.. _part3:

Part 3
======

This part is in note form at the moment. Feel free to try the code out
to see what happens...

Food for Pac-Man
----------------

Add this code as directed by the comments

.. code:: python

    # At the top          
    pacman.food_left = None

    # In `load_level`
    pacman.food_left = 0

    # In `for block` loop
    if block == '.': pacman.food_left += 1

    # New method
    
    def eat_food():
        ix,iy = int(pacman.x / BLOCK_SIZE), int(pacman.y / BLOCK_SIZE)
        if world[iy][ix] == '.':
            world[iy][ix] = None
            pacman.food_left -= 1
            print("Food left: ", pacman.food_left)

    # Call this new method in `update` function after `move_ahead(pacman)`
    eat_food()

Better Pac-Man when moving around
---------------------------------

.. code:: python

    # Replace these two lines:
    pacman = Actor('pacman_o.png', anchor=('left', 'top'))
    pacman.x = pacman.y = 1*BLOCK_SIZE

    # With these two
    pacman = Actor('pacman_o.png')
    pacman.x = pacman.y = 1.5*BLOCK_SIZE

    # Replace these lines

    # Here's where we want to move to
    x = sprite.x + dx
    y = sprite.y + dy


    # With these

    # Here's where we want to move to, bit of rounding to
    # ensure we get the exact pixel position
    x = int(round(sprite.left)) + dx
    y = int(round(sprite.top)) + dy

    # Did we move?

    # Replace this line:
    return oldx != sprite.x or oldy != sprite.y

    # With these
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
    

What happens when Pac-Man hits a ghost?
---------------------------------------

.. code:: python

    # At the top

    # Where do the ghosts start?
    ghost_start_pos = []

    # In `make_ghost_actors` just under `ghosts.append(g)`
    ghost_start_pos.append((x,y))

    # New function

    def lose_life():
        pacman.x = pacman.y = 1.5 * BLOCK_SIZE
        # Move ghosts back to their start pos
        for g, (x, y) in zip(ghosts, ghost_start_pos):
            g.x = x * BLOCK_SIZE
            g.y = y * BLOCK_SIZE

    # In `update` function inside `for g in ghosts` loop:

    if g.colliderect(pacman):
        lose_life()
            
Next up...
----------

 * a
 * b
 * b
  

.. _code for part 3: https://github.com/ericclack/pygamezero_pacman/blob/master/pacman3.py
