.. _part1:

Part 1
======

In part 1 we're going to create a game world in a text file, read and
process it in python, then draw it on the screen.

Getting Started
---------------

- Press the **New** button in Mu to open a new file and enter the following lines:

.. code:: python

    WIDTH = 640
    HEIGHT = 640
    TITLE = 'Pac-Man'

- Press **Save** and save the file as :code:`pacman.py`

- press **Play** to see what this code does.

You should see a new, empty window appear.

Making a game world
-------------------

We're going to store a game world in a text file. This means you can
design your own levels and also you'll get to learn about working with
files in Python - a really useful skill.

Creating the text file
......................

So create a text file in your favourite editor and use the equals sign
to draw some walls, for example: ::

  ====================
  =                  =
  ==========         =
  =                  =
  =    ===============
  =                  =
  ====================

Save this file in the same directory as where you saved :code:`pacman.py`. Call the
file :code:`level-1.txt`.

Now let's try reading that file in your python code. Add this empty array to contain the world:

.. code:: python

   world = []

Now add this function to your code underneath that:

.. code:: python

   def load_level(number):
       file = "level-%s.txt" % number
       with open(file) as f:
           for line in f:
               row = []
               for block in line.strip():
                   row.append(block)
               world.append(row)

Let's test that this works, add the following two lines to the end of
your code:

.. code:: python

          load_level(1)
          print(world)

If you typed the code in correctly then you'll see something like this
in your console: ::

  [['=', '=', '=', '=', '=', '=', '=', '=', '=', ' ', ' ', '=', '=', '=', '=', '=', '=', '=', '=', '='], ['=', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '='],
  ...

That's python's way of printing a list and it means that your code
loaded your world from the text file. Each element in the list is a
character at a specific location in your world. The next step is to
draw this on the screen.

Drawing the world
-----------------

As the moment you just have '=' characters in your world. Go back and
put in some dots and stars (:code:`.` and :code:`*`) to represent food
and power-ups.

So now we need a way to map these characters in your text file to
images in on the screen. Let's use a dictionary to do this. A
dictionary is a map from one value to another, in our case we will map
a single character to a file name of the image to use on screen.

Add this code near the top of your game:

.. code:: python

    char_to_image = {
        '.': 'dot.png',
        '=': 'wall.png', 
        '*': 'power.png', 
    }
    
Trying out dictionaries in the REPL
...................................

Let's switch to the REPL to see how this dictionary works. First
change your game mode to Python3--click the Mode icon to do this--then
click the Run button and you'll get a :code:`>>>` prompt at the bottom
of the screen.

Try typing the following and see if you understand what's going on (don't type the :code:`>>>` characters) ...

.. code:: python

   >>> char_to_image['=']
   'wall.png'
   >>> char_to_image['*']
   'power.png'
   >>> char_to_image['!']
   Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
   KeyError: '!'
          

:code:`KeyError` means that '!' is not found in the dictionary, it is
not a valid key because we've not set it in the definition of
:code:`char_to_image`.

OK, make sense? Switch the game mode back to PygameZero, then
continue...

From characters to images
.........................

Add the method below to draw the world. It iterates through the rows
in the world, then the blocks in each row and draws the right image
for the character it finds.

We use :code:`enumerate` so that we get each item in the world *and*
its index in the array, which gives us the right x and y co-ordinates
for the screen position.

.. code:: python
    
    def draw():
        for y, row in enumerate(world):
            for x, block in enumerate(row):
                image = char_to_image.get(block, None)
                if image:
                    screen.blit(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE))

Hooray! We should now have your map on the screen ready to add our
Pac-Man character.
 
Wait! Did you get an error? Why do you think this is? Remember, look
at the last line of the error message first.

Can you fix the error yourself? Try first before scrolling down.

...

...

...

OK, so you should have added this to the top of your program:

.. code:: python

   BLOCK_SIZE = 32

Adding the Pac-Man
------------------

OK, time to add our Pac-Man sprite. Let's start with an Actor to draw
the sprite. Add this code just under the set of capitalised constants
(e.g.  :code:`WORLD_SIZE`):

.. code:: python
          
    # Our sprites
    pacman = Actor('pacman_o.png', anchor=('left', 'top'))
    pacman.x = pacman.y = 1*BLOCK_SIZE

And add this line to the end of your :code:`draw` function:

.. code:: python

    pacman.draw()

This places Pac-Man at the top left of the screen. Now let's think about movement.
We've seen code similar to this in previous tutorials:

Moving through the maze
.......................

.. code:: python

    def on_key_down(key):
        if key == keys.LEFT:
            pacman.x += -BLOCK_SIZE
        if key == keys.RIGHT:
            pacman.x += BLOCK_SIZE
        if key == keys.UP:
            pacman.y += -BLOCK_SIZE
        if key == keys.DOWN:
            pacman.y += BLOCK_SIZE

Try this out. You'll see that our Pac-Man moves very jerkily across the
screen, and has no regard for walls. We can do better than this.

If we change :code:`BLOCK_SIZE` to a smaller value such as 1, then our
character certainly moves slower, but you have to tap the arrow key so
movement is still a problem.

We can fix this by adding another key event function:
:code:`on_key_up` so that we track key presses *and* releases. Change
your :code:`on_key_down` function and add the new function underneath:

.. code:: python

    def on_key_down(key):
        if key == keys.LEFT:
            pacman.dx = -1
        if key == keys.RIGHT:
            pacman.dx = 1
        if key == keys.UP:
            pacman.dy = -1
        if key == keys.DOWN:
            pacman.dy = 1          

    def on_key_up(key):
        if key in (keys.LEFT, keys.RIGHT):
            pacman.dx = 0
        if key in (keys.UP, keys.DOWN):
            pacman.dy = 0

You might be wondering what :code:`dx` and :code:`dy` are. These are
two new variables that we've added to our pacman character that will
track direction in x and y (-1 is up or left, 1 is down or right). We
need to initialise these so add these two lines just under where we
set :code:`pacman.x` and :code:`pacman.y`:

.. code:: python

    # Direction that we're going in
    pacman.dx, pacman.dy = 0,0          

Right, now press Play to test. You should be a bit disappointed --
our pacman no longer moves. We are tracking which direction the
player wants to move in but we are not using this information
anywhere.

It's time to add an :code:`update` function to fix this.

.. code:: python

    def update():
        pacman.x += pacman.dx
        pacman.y += pacman.dy

Yay! Now it moves, and smoothly, and diagonally if you hold down two
arrow keys!

OK, time to add some collision detection...

Collision detection
...................

We need to spot when moving Pac-Man would cause a collision with a
wall. This is a bit trickier than in other games because whilst the
game world is a series of blocks, Pac-Man can move in pixels. This
means that he could potentially collide with up to four blocks at any
one time, and we need to check all of them.

Let's add a new function to check what's ahead of Pac-Man:

.. code:: python

    def blocks_ahead_of_pacman(dx, dy):
        """Return a list of tiles at this position + (dx,dy)"""

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

There's a lot going on in that function! Let's break it down:

 * First we need to determine where Pac-Man wants to go, we add his
   direction :code:`dx,dy` to his :code:`x,y` position.
 * Then we need to convert this destination :code:`x,y` position into
   a block position in our world array, simply by dividing by BLOCK_SIZE.
 * However, arrays always take integers indexes -- we can't look up
   world[1.6][1.0] as that doesn't make any sense to Python -- so we
   set array indexes :code:`ix,iy` to the integer part of the division
   and round down, so (1.6, 1.0) would become (1, 1).
 * We determine any remainder so that we check adjacent blocks, in the
   example above, :code:`rx` would be a positive number and :code:`ry`
   would be zero.
 * Now we can check the blocks, always the one at
   :code:`world[iy][ix]` and then those to the right, below and
   diagonally right/below depending upon the remainders.

That's quite a complex algorithm. Let's see if it works. Change your
:code:`update` function to the following:

.. code:: python

    def update():
        # To go in direction (dx, dy) check for no walls
        if '=' not in blocks_ahead_of_pacman(pacman.dx, 0):
            pacman.x += pacman.dx
        if '=' not in blocks_ahead_of_pacman(0, pacman.dy):
            pacman.y += pacman.dy          

You might be wondering why we check in two stages: x then y. This
enables you to hold down two arrow keys (say right and down) and have
Pac-Man move through a gap without stopping -- handy for escaping
ghosts!

You can see how the single step update with this code, which I think
you'll agree is worse -- do try it:

.. code:: python

    def update():
        if '=' not in blocks_ahead_of_pacman(pacman.dx, pacman.dy):
            pacman.x += pacman.dx
            pacman.y += pacman.dy
            
Next up...
----------

In part two of this tutorial we'll get the ghosts moving.
Move on to :ref:`part2`.

