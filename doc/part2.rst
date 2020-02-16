.. _part2:

Part 2
======

In part 2 we're going to get the ghosts moving, first by making Actor
objects for them (sprites), then by adding code to move them
intelligently (well, sort of) around the screen.

Making ghost sprites
--------------------

We can see the ghosts on the screen, but they don't move yet. That's
because they are just part of the background and drawn in place in the
:code:`draw` function.

So let's pick them out of the world and make them into actors. We can
use a similar method to iterate through the world as we did in the
:code:`draw` function. Add this code...

.. code:: python

    ghosts = []
          
    def make_ghost_actors():
        for y, row in enumerate(world):
            for x, block in enumerate(row):
                if block == 'g' or block == 'G':
                    g = Actor(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE), anchor=('left', 'top'))
                    ghosts.append(g)
                    # Now we have the ghost sprite we don't need this block
                    world[y][x] = None          

And then right at the end of your program add a line to call this new
function, right under your :code:`load_level(1)` line:

.. code:: python

    make_ghost_actors()
                    
You can see from the code above that we are looking for two letters in
the world: a lower case and upper case G. If we find it we create an
actor in the correct place, using x and y from the :code:`for` loops,
then finally we remove the block from the world as otherwise we'd have
two ghosts: one that moves and one that stays in place.

Do run your code now to check that you've not made any typos. If it runs
without any syntax errors you'll notice that now we have no ghosts :(
Let's fix that...

We need to add code to draw the ghost actors, we do this in the
:code:`draw` function. Add these lines to the end:

.. code:: python

    for g in ghosts: g.draw()

Now we have our ghosts back, but they are not moving yet.

Moving the ghosts
-----------------

We can use similar logic to move our ghosts as we use to move Pac-Man,
after all we don't want ghosts to move through the walls.

First let's add some constants to the top of our code, plus we need to use the
random library:

.. code:: python

    import random
          
    SPEED = 2
    GHOST_SPEED = 1

Now when we create a ghost let's set a random speed. Just under this line:

.. code:: python

   g = Actor(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE), anchor=('left', 'top'))

Add these lines, making sure that you match the indentation. 

.. code:: python

   # Random direction
   g.dx = random.choice([-GHOST_SPEED,GHOST_SPEED])
   g.dy = random.choice([-GHOST_SPEED,GHOST_SPEED])

OK, so what we've done just there is to record an x-direction and
y-direction for each ghost, picking at random from 4 combinations:
(-2,-2), (-2,2), (2,-2), (2,2).

So now we need to use these to actually move each ghost. Let's add
code to the :code:`update` function to do this... Add these lines to
the end of the function:

.. code:: python

    for g in ghosts:
        g.x += g.dx
        g.y += g.dy          

Press *Play* to test. Hmmm... not great, the ghosts can move through
the walls. Maybe that's what ghosts do in real life, but not in
Pac-Man!


Next up...
----------

Let a mentor know what you want to see next.

