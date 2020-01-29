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
    TITLE = 'Pac Man'

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
        pac.draw()

Horay! We should now have your map on the screen ready to add our
pacman charater.
 
Wait! Did you get an error? Why do you think this is? Remember, look
at the last line of the error message first.

Can you fix the error yourself? Try first before scrolling down.

...

...

...

OK, so you should have added this to the top of your program:

.. code:: python

   BLOCK_SIZE = 32

  
Next up...
----------

.. :ref:`part2`.
