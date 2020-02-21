.. _part3:

Part 3
======

This part is in note form at the moment. Feel free to try the code out
to see what happens...

Food for Pac-Man
----------------

Add this code just under where you create the :code:`pacman` actor: ::

    pacman.food_left = None

Now add these lines in the function :code:`load_level`: ::

    pacman.food_left = 0

Inside the :code:`for block` loop: ::
  
    if block == '.': pacman.food_left += 1

Add this new method: ::
    
    def eat_food():
        ix,iy = int(pacman.x / BLOCK_SIZE), int(pacman.y / BLOCK_SIZE)
        if world[iy][ix] == '.':
            world[iy][ix] = None
            pacman.food_left -= 1
            print("Food left: ", pacman.food_left)

Finally, call this new method in the :code:`update` function after the
line :code:`move_ahead(pacman)`: ::

    eat_food()

Better Pac-Man when moving around
---------------------------------

Near the top of your code replace these two lines: ::
  
    pacman = Actor('pacman_o.png', anchor=('left', 'top'))
    pacman.x = pacman.y = 1*BLOCK_SIZE

With these two: ::
  
    pacman = Actor('pacman_o.png')
    pacman.x = pacman.y = 1.5*BLOCK_SIZE

In function :code:`blocks_ahead_of` replace these lines: ::

    # Here's where we want to move to
    x = sprite.x + dx
    y = sprite.y + dy

With these: ::

    # Here's where we want to move to, bit of rounding to
    # ensure we get the exact pixel position
    x = int(round(sprite.left)) + dx
    y = int(round(sprite.top)) + dy

In function :code:`move_ahead` replace this line at the end of the function: ::
  
    return oldx != sprite.x or oldy != sprite.y

With these lines: ::
  
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

At these lines just under :code:`ghosts = []`: ::

    # Where do the ghosts start?
    ghost_start_pos = []


In function :code:`make_ghost_actors` add this just under :code:`ghosts.append(g)`: ::

    ghost_start_pos.append((x,y))

Add this new function: ::

    def lose_life():
        pacman.x = pacman.y = 1.5 * BLOCK_SIZE
        # Move ghosts back to their start pos
        for g, (x, y) in zip(ghosts, ghost_start_pos):
            g.x = x * BLOCK_SIZE
            g.y = y * BLOCK_SIZE


In :code:`update` function inside :code:`for g in ghosts` loop: ::

    if g.colliderect(pacman):
        lose_life()
            
Next up...
----------

 * tbc

.. _code for part 3: https://github.com/ericclack/pygamezero_pacman/blob/master/pacman3.py
