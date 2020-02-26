.. _part2:

Part 2
======

In part 2 we're going to get the ghosts moving, first by making Actor
objects for them (sprites), then by adding code to move them
intelligently (well, sort of) around the screen.

Making ghost sprites
--------------------

We can see the ghosts on the screen, but they don't move yet. That's
because they are just part of the background and drawn in one place in
the :code:`draw` function.

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
the world: a lower case and upper case G. If we find a match we create an
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

Now when we create a ghost let's set a random direction. Just under this line:

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

Don't move through walls
------------------------

Look at all the code in that :code:`update` function, you can see
we've moving Pac-Man differently to how we're moving each ghost:

.. code:: python
          
    def update():
        # In order to go in direction dx, dy there must be no wall that way
        if '=' not in blocks_ahead_of_pacman(pacman.dx, 0):
            pacman.x += pacman.dx
        if '=' not in blocks_ahead_of_pacman(0, pacman.dy):
            pacman.y += pacman.dy

        for g in ghosts:
            g.x += g.dx
            g.y += g.dy

You can see that with Pac-Man we're checking for walls (the = character) but
not for the ghosts. Let's fix this.

What we want is a general purpose version of
:code:`blocks_ahead_of_pacman` that we can use with ghosts too, then
we can check for walls for any sprite.

So first up, rename the :code:`blocks_ahead_of_pacman` function, add a
new argument so we can pass in the sprite to check and change the two
instances of :code:`pacman` to :code:`sprite`

Let's go through those steps. (1) change the function from: ::

  def blocks_ahead_of_pacman(dx, dy):
  
To: ::

  def blocks_ahead_of(sprite, dx, dy):

Now (2) change these two lines: ::

  x = pacman.x + dx
  y = pacman.y + dy
  
To: ::

  x = sprite.x + dx
  y = sprite.y + dy

Try running your code now. You should see an error, because we've
changed the function but not the places where we use it, which still
refer to the old function.

So in the update function, change the function calls to use the new
method. See if you can figure out how to do this. (You can see the
complete function below if you are stuck).

OK, so we can now use this general purpose function
:code:`blocks_ahead_of` with ghosts too, so change the last few lines
of your :code:`update` function to these:

.. code:: python

    for g in ghosts:
        if '=' not in blocks_ahead_of(g, g.dx, 0):
            g.x += g.dx
        if '=' not in blocks_ahead_of(g, 0, g.dy):
            g.y += g.dy          

So that the complete function looks like this:

.. code:: python

    def update():
        # In order to go in direction dx, dy there must be no wall that way
        if '=' not in blocks_ahead_of(pacman, pacman.dx, 0):
            pacman.x += pacman.dx
        if '=' not in blocks_ahead_of(pacman, 0, pacman.dy):
            pacman.y += pacman.dy

        for g in ghosts:
            if '=' not in blocks_ahead_of(g, g.dx, 0):
                g.x += g.dx
            if '=' not in blocks_ahead_of(g, 0, g.dy):
                g.y += g.dy          

Now we have some good ghost movement, but if you leave it running for
a bit chances are you'll get an error like this (assuming you left
gaps in your walls): ::

  IndexError: list index out of range

Wrapping around
---------------

We get this error because a ghost has gone off the screen and its
(x,y) co-ordinates are outside the range of our world. You'll also
get this error if you move Pac-Man off the screen. 

There's one other problem, not a defect as such, but a violation of
a good coder principle: Don't Repeat Yourself (or DRY). Much of
the code in :code:`update` is repeated. If we fix this first, then
maybe we can fix the out of range error more easily.

Let's create a new function :code:`move_ahead` like so:

.. code:: python
          
    def move_ahead(sprite):
        # In order to go in direction dx, dy there must be no wall that way
        if '=' not in blocks_ahead_of(sprite, sprite.dx, 0):
            sprite.x += sprite.dx
        if '=' not in blocks_ahead_of(sprite, 0, sprite.dy):
            sprite.y += sprite.dy

This contains all the logic we need to move a sprite forward, using (dx,dy)
and avoiding walls. Let's refactor :code:`update` to use this. Replace
the function with this new, much shorter one:

.. code:: python

    def update():
        move_ahead(pacman)
        for g in ghosts:
            move_ahead(g)

Now we have less code, and also just as importantly it's really easy
to see what :code:`update` is actually doing.

Let's look at that :code:`IndexError`. We can see that it's being
generated from inside the :code:`blocks_ahead_of` function. We need
to do two things to fix it.

 1. Wrap the sprites around, so that if they go off one side of the
    screen, they come back on the other side.
 2. Don't check for blocks outside of the world.

For the wrap around we want to keep our sprite's x and y position
in between two values: 0 and the width or height of the screen. If we
go outside this range we want to wrap to the other end of the range.

We can do this with a simple function:

.. code:: python

    def wrap_around(mini, val, maxi):
        if val < mini: return maxi
        elif val > maxi: return mini
        else: return val

You can test this in a Python3 script (in Mu or IDLE) to see how it
works. Here's an example:

.. code:: python
          
    >>> wrap_around(0, 5, 10)
    5                          # No change
    >>> wrap_around(0, 15, 10)
    0                          # 15 is too big, so wrap to 0
    >>> wrap_around(0, -1, 10)
    10                         # -1 is too small, so wrap to 10

OK, let's use this function. Add these lines to the end of
:code:`move_ahead`:

.. code:: python

    # Keep sprite on the screen
    sprite.x = wrap_around(0, sprite.x, WIDTH-BLOCK_SIZE)
    sprite.y = wrap_around(0, sprite.y, HEIGHT-BLOCK_SIZE)          

Finally to stop checking blocks off the world, add these lines to
:code:`blocks_ahead_of` just under the definition of :code:`rx, ry =`

.. code:: python
          
    # Keep in bounds of world
    if ix == WORLD_SIZE-1: rx = 0
    if iy == WORLD_SIZE-1: ry = 0      

Phew! That was quite a bit of work. So how are our ghosts behaving
now? Press *Play* to test them out.

Notice anything odd?

Have any ideas how to fix it?

Keep on moving
--------------

Yes, our ghosts eventually stop, usually in a corner. That's
because we never change their direction.

If we can tell that they've stopped moving we can do something about
it. The function :code:`move_ahead` is the place to start. Here's the
current function:

.. code:: python

    def move_ahead(sprite):
        # In order to go in direction dx, dy there must be no wall that way
        if '=' not in blocks_ahead_of(sprite, sprite.dx, 0):
            sprite.x += sprite.dx
        if '=' not in blocks_ahead_of(sprite, 0, sprite.dy):
            sprite.y += sprite.dy

        # Keep sprite on the screen
        sprite.x = wrap_around(0, sprite.x, WIDTH-BLOCK_SIZE)
        sprite.y = wrap_around(0, sprite.y, HEIGHT-BLOCK_SIZE)

How do we tell if the sprite has moved? We can record the position
at the start of the funciton and compare at the end of the function
like this...

Add these two lines to the start of the function: ::

        # Record current pos so we can see if the sprite moved
        oldx, oldy = sprite.x, sprite.y

And these two lines at the end of the function: ::
        
        # Return whether we moved
        return oldx != sprite.x or oldy != sprite.y

So now anyone that calls this function can find out, if they want,
whether the sprite has moved.

OK, so back in the :code:`update` function we can use this new
information... Change your function to read:

.. code:: python

   def update():
       move_ahead(pacman)

       for g in ghosts:
           if not move_ahead(g):
               set_random_dir(g, GHOST_SPEED)          

There's one more new function here so that we Don't Repeat
Ourselves. Can you spot it? What do you think we should put in it?
Hint: the code is already written, it's just not in a function yet.

If you are completely stuck, have a look at the `code for part 2`_ on
GitHub.
    
Next up...
----------

In the next part of this tutorial we'll work on:

 * Pac-Man eating the food
 * Ghosts killing Pac-Man
 * Power up pills.

Move on to :ref:`part3`.

.. _code for part 2: https://github.com/ericclack/pygamezero_pacman/blob/master/pacman2.py
