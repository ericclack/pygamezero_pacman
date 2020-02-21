.. _part3:

Part 3
======

This part is in note form at the moment. Feel free to try the code out
to see what happens...

Food for Pac-Man
----------------

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

    # In `update` function after `move_ahead(pacman)`
    eat_food()

            
Next up...
----------

 * a
 * b
 * b
  

.. _code for part 3: https://github.com/ericclack/pygamezero_pacman/blob/master/pacman3.py
