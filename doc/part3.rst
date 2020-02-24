.. _part3:

Part 3
======

In part 3 we're going to get Pac-Man eating the food on the screen,
make him turn properly as we move him about the world, and add
collision detection for the ghosts.

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
the :code:`pacman` actor: ::

    pacman.food_left = None

Now add these lines in the function :code:`load_level`: ::

    pacman.food_left = 0

And then inside the :code:`for block` loop we need to spot food blocks like this: ::
  
    if block == '.': pacman.food_left += 1

Now let's add a new method to spot and eat food. Add this new method: ::
    
    def eat_food():
        ix,iy = int(pacman.x / BLOCK_SIZE), int(pacman.y / BLOCK_SIZE)
        if world[iy][ix] == '.':
            world[iy][ix] = None
            pacman.food_left -= 1
            print("Food left: ", pacman.food_left)

Finally, call this new method in the :code:`update` function after the
line :code:`move_ahead(pacman)`: ::

    eat_food()

Now go and test and check that it works. You should see in your
console (in the Mu editor at the bottom of the screen) an update of
how much food is left each time you eat some.

Better Pac-Man when moving around
---------------------------------

Pac-Man always looks to the right, even when moving down or to the
left, let's fix this using the rotation feature on actors.

But first we need to change Pac-Man's anchor point, as if we stick
with top-left when we rotate him he'll won't stay in place, but move
into other blocks.

So near the top of your code replace these two lines: ::
  
    pacman = Actor('pacman_o.png', anchor=('left', 'top'))
    pacman.x = pacman.y = 1*BLOCK_SIZE

with these two: ::
  
    pacman = Actor('pacman_o.png')
    pacman.x = pacman.y = 1.5*BLOCK_SIZE

Now we've changed Pac-Man's centre of placement and rotation we need
to change a bit of maths to keep the collision detection working. In
function :code:`blocks_ahead_of` replace these lines: ::

    # Here's where we want to move to
    x = sprite.x + dx
    y = sprite.y + dy

with these: ::

    # Here's where we want to move to, bit of rounding to
    # ensure we get the exact pixel position
    x = int(round(sprite.left)) + dx
    y = int(round(sprite.top)) + dy

Now we can rotate Pac-Man based on which direction he's moving. In
function :code:`move_ahead` replace this line at the end of the
function: ::
  
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

Right now nothing happens when Pac-Man hits a ghost, let's fix that. Also,
what should happen after a collision? Let's move the ghosts back to where
they started.

To record the ghosts' start positions add these lines just under
:code:`ghosts = []` near the top of your code: ::

    # Where do the ghosts start?
    ghost_start_pos = []

Next in function :code:`make_ghost_actors` add this just under
:code:`ghosts.append(g)`: ::

    ghost_start_pos.append((x,y))

Now we have a list that records the :code:`(x, y)` co-ordinates of
each ghost. Let's add the collision decetion.
    
Add this test in the :code:`update` function inside the :code:`for g
in ghosts` loop: ::

    if g.colliderect(pacman):
        lose_life()

Finally add this new function: ::

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

Let's have a play in the REPL to see how it works...

Click *New* to open a new script and set the *Mode* to Python 3, then
open a RPEL and enter these lines of code (don't type the prompt
:code:`>>>` and there's no need to type in the comments that start
with a :code:`#` character): ::

  # Make some lists
  >>> names = [ 'fred', 'bill', 'amy', 'martha' ]
  >>> ages = [ 25, 29, 21, 52 ]

  # Display the lists
  >>> print(names)
  ['fred', 'bill', 'amy', 'martha']
  >>> print(ages)
  [ 25, 29, 21, 52 ]

So far, no surprises (hopefully!). Now let's try the :code:`zip`
function: ::

  # First try of zip
  >>> print(zip(names, ages)
  <zip object at 0x10b699d88>

What's that all about?! Well that's an iterator, which means we need
to use a :code:`for` loop to use it: ::

  # Try zip with a loop
  >>> for i in zip(names, ages): print(i)
  ('fred', 25)
  ('bill', 29)
  ('amy', 21)
  ('martha', 52)

OK! So zip has merged the two lists together and paired up the
elements. We can extend this a bit further by capturing the name and
age at the same time: ::

  >>> for name, age in zip(names, ages): print(name, "is", age, "years old")
  fred is 25 years old
  bill is 29 years old
  amy is 21 years old
  martha is 52 years old

Make sense? OK :) Don't forget to change your game *Mode* back to
PygameZero.
        
Next up...
----------

 * tbc

.. _code for part 3: https://github.com/ericclack/pygamezero_pacman/blob/master/pacman3.py
