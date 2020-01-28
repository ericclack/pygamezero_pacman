.. _part1:

Part 1
======

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

Creating a text game world
..........................

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

If you typed the code in correctly then you'll see something like this in your console: ::

  [['=', '=', '=', '=', '=', '=', '=', '=', '=', ' ', ' ', '=', '=', '=', '=', '=', '=', '=', '=', '='], ['=', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '='],
  ...

That's python's way of printing a list and it means that your code loaded your world from the text file.

Drawing the world
.................

We need a way to map the characters in your text file to images in on the screen. Let's use a dictionary to do this. (explain). Add this code near the top of your code:

.. code:: python

    char_to_image = {
        '.': 'dot.png',
        '=': 'wall.png', 
        '*': 'power.png', 
    }

Now add this method to draw the world (explain):
    
.. code:: python
    
    def draw():
        for y, row in enumerate(world):
            for x, block in enumerate(row):
                image = char_to_image.get(block, None)
                if image:
                    screen.blit(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE))
        pac.draw()

  
Next up...
----------

.. :ref:`part2`.
