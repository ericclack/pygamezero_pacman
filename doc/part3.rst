.. _part3:

Part 3
======

In part 3 we're going to let Pac-Man eat the food on the screen, make
him turn properly as we move him about the world, and add collision
detection for the ghosts. Finally we'll add code to move the next
level when all of the food is eaten. 

Food for Pac-Man
----------------

Pac-Man currently ignores the food as he moves about. Let's fix that.

There are a few steps to this:

* Count how much food there is, so that we know when Pac-Man has
  finished eating and we can move to the next level
* Spot when Pac-Man moves over some food
* Eat it by removing it from the world and decrementing the food counter.

Later, we'll move to the next level when all of the food is gone. 

Let's record how much food is left by adding a variable to the
:code:`pacman` actor object. Add this code just under where you create
the :code:`pacman` actor:

.. code:: python
          
   pacman.food_left = None

Now add these lines in the function :code:`load_level`:

.. code:: python
          
    pacman.food_left = 0

And then inside the :code:`for block` loop in the function
:code:`load_level` we need to spot food blocks like this:
  
.. code:: python

   if block == '.': pacman.food_left += 1

Your function should now look like this:

.. code:: python

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
   
Now let's add a new method to spot and eat food:

.. code:: python
    
    def eat_food():
        ix,iy = int(pacman.x / BLOCK_SIZE), int(pacman.y / BLOCK_SIZE)
        if world[iy][ix] == '.':
            world[iy][ix] = None
            pacman.food_left -= 1
            print("Food left: ", pacman.food_left)

Finally, call this new method in the :code:`update` function after the
line :code:`move_ahead(pacman)`:

.. code:: python
          
    eat_food()

Now go and test and check that it works. You should see in your
console (in the Mu editor at the bottom of the screen) an update of
how much food is left each time you eat some.

Rotate Pac-Man when moving around
---------------------------------

Pac-Man always looks to the right, even when moving down or to the
left, let's fix this using the rotation feature on actors.

But first we need to change Pac-Man's anchor point, as if we stick
with top-left when we rotate him he'll won't stay in place, but move
into other blocks.

So near the top of your code replace these two lines:

.. code:: python
  
    pacman = Actor('pacman_o.png', anchor=('left', 'top'))
    pacman.x = pacman.y = 1*BLOCK_SIZE

with these two:

.. code:: python
  
    pacman = Actor('pacman_o.png')
    pacman.x = pacman.y = 1.5*BLOCK_SIZE

Now we've changed Pac-Man's centre of placement and rotation we need
to change a bit of maths to keep the collision detection working. In
function :code:`blocks_ahead_of` replace these lines:

.. code:: python

    # Here's where we want to move to
    x = sprite.x + dx
    y = sprite.y + dy

with these:

.. code:: python

    # Here's where we want to move to, bit of rounding to
    # ensure we get the exact pixel position
    x = int(round(sprite.left)) + dx
    y = int(round(sprite.top)) + dy

Now we can rotate Pac-Man based on which direction he's moving. In
function :code:`move_ahead` replace this line at the end of the
function:

.. code:: python
  
    return oldx != sprite.x or oldy != sprite.y

with these lines:

.. code:: python
  
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

Right now nothing happens when Pac-Man hits a ghost, let's fix that. Also,
what should happen after a collision? Let's move the ghosts back to where
they started.

To record the ghosts' start positions add these lines just under
:code:`ghosts = []` near the top of your code:

.. code:: python      

    # Where do the ghosts start?
    ghost_start_pos = []

Next in function :code:`make_ghost_actors` add this just under
:code:`ghosts.append(g)`:

.. code:: python      

    ghost_start_pos.append((x,y))

Now we have a list that records the :code:`(x, y)` co-ordinates of
each ghost. Let's add the collision decetion.
    
Add this test in the :code:`update` function inside the :code:`for g
in ghosts` loop:

.. code:: python

    if g.colliderect(pacman):
        lose_life()

Finally add this new function:

.. code:: python

    def lose_life():
        pacman.x = pacman.y = 1.5 * BLOCK_SIZE
        # Move ghosts back to their start pos
        for g, (x, y) in zip(ghosts, ghost_start_pos):
            g.x = x * BLOCK_SIZE
            g.y = y * BLOCK_SIZE

This function resets Pac-Man's position to the top left corner, then
resets each of the ghost positions. Do you notice something new in the
:code:`for` loop? We use a function called :code:`zip`, but what does
it do?

Introducing zip
...............

Let's have a play in the REPL to see how it works...

Click *New* to open a new script and set the *Mode* to Python 3, then
open a REPL and enter these lines of code (don't type the prompt
:code:`>>>` and there's no need to type in the comments that start
with a :code:`#` character):

.. code:: python

  # Make some lists
  >>> names = [ 'fred', 'bill', 'amy', 'martha' ]
  >>> ages = [ 25, 29, 21, 52 ]

  # Display the lists
  >>> print(names)
  ['fred', 'bill', 'amy', 'martha']
  >>> print(ages)
  [ 25, 29, 21, 52 ]

So far, no surprises (hopefully!). Now let's try the :code:`zip`
function:

.. code:: python

  # First try of zip
  >>> print(zip(names, ages)
  <zip object at 0x10b699d88>

What's that all about?! Well that's an iterator, which means we need
to use a :code:`for` loop to use it:

.. code:: python

  # Try zip with a loop
  >>> for i in zip(names, ages): print(i)
  ('fred', 25)
  ('bill', 29)
  ('amy', 21)
  ('martha', 52)

OK! So zip has merged the two lists together and paired up the
elements. We can extend this a bit further by capturing the name and
age at the same time:

.. code:: python

  >>> for name, age in zip(names, ages): print(name, "is", age, "years old")
  fred is 25 years old
  bill is 29 years old
  amy is 21 years old
  martha is 52 years old

Make sense? OK :) Don't forget to change your game *Mode* back to
PygameZero.
        
Next Level
----------

Earlier we added code to track how much food was left. Let's use this
to move to the next level when all of the food is gone.

One other thing to consider: we need to test our game and it will take
ages if we have to actually eat all of the food each time we want
to get to the next level, so let's add a *test mode* to the game. Add
this line at the top of your code:

.. code:: python

   TEST_MODE = True

Now let's do the work of moving to the next level. Have a think about
what we need to do to acheive this... there are actually quite a few
steps. See if you can come up with them before reading on further.

...

...

...

OK, here's the list, how does it compare with yours?

1. Record the level we're on, starting at 1
2. Create the next world text file :code:`level-2.txt`
3. Check when all of the food is gone
4. Increment the level by 1
5. Load in the next world text file
6. Capture the ghost positions
7. Reset all the sprites

We can store the current level on the :code:`pacman` sprite as we
did for :code:`food_left`. Add this line just after you've created
the Pac-Man sprite:

.. code:: python

    pacman.level = 1
   
Now let's put the rest of the next-level work in a new functin called :code:`next_level`:

.. code:: python

    def next_level():
        global world, ghosts, ghost_start_pos

        world = []
        ghosts = []
        ghost_start_pos = []

        pacman.level += 1
        load_level(pacman.level)
        make_ghost_actors()

        reset_sprites()

Finally we just need to determine when to call this new
function. There are two places. In :code:`update` add these lines just
under the call to :code:`eat_food()`:

.. code:: python

    if pacman.food_left == 0:
        next_level()

And for our test mode, add these lines at the end of the function
:code:`on_key_up`:

.. code:: python

    if TEST_MODE:
        # Put special key commands here
        if key == keys.N:
            next_level()

Now as long as :code:`TEST_MODE` is :code:`True` we can press N to go
to the next level.

Enjoy your game
---------------

Congratulations for getting this far! You've worked hard and we have
covered a lot of new techniques, so take a bit of time to relax and
enjoy playing your game ... which is beginning to be quite playable
now.


Next up...
----------

* Add a score
* End the game when lives run out
* Power ups and chasing ghosts
* Better animations e.g. when Pac-Man loses a life
* ...

.. _code for part 3: https://github.com/ericclack/pygamezero_pacman/blob/master/pacman3.py
