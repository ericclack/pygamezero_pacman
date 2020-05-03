.. _part4:

Part 4
======

Part 4 is a work in progress, so at the moment this page is just a
bunch of notes. Feel free to have a read through and see what you can
discover.

Tell the user what's happening
------------------------------

Let's add a way to tell the user what's just happened by displaying
a big banner on the screen. As well as displaying nice big text
we also need to consider how long we want the banner to be displayed.

If you've completed our other tutorials (Flappy Bird and Candy Crush)
you'll know that we can use :code:`screen.draw.text` to draw text
on the screen.

For example, add this to your :code:`draw` function to see what
happens: ::

  screen.draw.text('Hello!', center=(WIDTH/2, HEIGHT/2), fontsize=120)

That's nice and big isn't it? But it never goes away, how do
we fix this? Well we can add a counter and count down to zero
then remove it.

So we need to add two variables: one to store the message and one
to store the counter. As we've done before let's put these on the
:code:`pacman` sprite. Add these two lines under where you've
created the pacman sprite: ::

  pacman.banner = None
  pacman.banner_counter = 0

Now let's display a big `Ouch!` when Pac-Man loses a life...

Find your :code:`update` function and in the if-statement that tests
for :code:`g.colliderect(pacman)` add this line: ::

  set_banner('Ouch!', 5)

We've not written that function yet, so this won't work, but we write
this line first to think about how we want the function to work. We
don't yet know what 5 means, maybe it is seconds? Maybe some fraction
of seconds? 

Now add the function: ::

  def set_banner(message, count):
    pacman.banner = message
    pacman.banner_counter = count

OK, now we're in business. You can see that the function
:code:`set_banner` is really shorthand for setting those two
variables. Given that we'll probably show a few different banners
this will save a fair bit of typing.

Now we can update the draw function to remove the `Hello` message
and use these variables: ::

  if pacman.banner and pacman.banner_counter > 0: 
      screen.draw.text(pacman.banner, center=(WIDTH/2, HEIGHT/2), fontsize=120)

Time to test. Do you see any bugs?

That's right: the banner never disappears. Let's fix that now.

So we could decrement (programmer speak for 'reduce by one') the
counter in the draw function, but this is executed many times per
second so we'd need to use big numbers to keep the banner visible for
long enough to read it. A better solution is to add a periodic
function, this will be handy later too.


Periodic functions
------------------

A periodic function is called repeatedly at equal intervals. We can
use it to reduce our banner counter, and any others we might create.

Here's how we can use it for our banner counter... add this code
at the end of your program: ::

  def periodic():
    if pacman.banner_counter > 0:
        pacman.banner_counter -= 1

  clock.schedule_interval(periodic, 0.2)

The function is what we want to do every period, and the last line
tells PygameZero to call this function every 0.2 seconds or 5 times
a second. 

Now when you run your game you should see `Ouch!` displayed for a
second and no more.

Score and Lives
---------------

Let's add a score and some lives so that there's a consequence to Pac-Man
hitting a ghost.

First question: we need to store these numbers in variables, but where?

Given that we'll be accessing and updating them in various places we can
put them on the :code:`pacman` object, that'll make our coding easier.

So add these lines just under where you set :code:`pacman.level`: ::

  pacman.score = 0
  pacman.lives = 3

Now we need to draw those numbes on the screen. In the real Pac-Man
we would show one little Pac-Man sprite for each life left, but for now
we're going to use text.

At the end of your :code:`draw` function add these two lines: ::
  
  screen.draw.text("Score: %s" % pacman.score, topleft=(8, 4), fontsize=40)
  screen.draw.text("Lives: %s" % pacman.lives, topright=(WIDTH-8,4), fontsize=40)

Have a play around with the position and size of those until you are happy.

OK, so now we have a score and lives but they never change! Where do you
think we need to make changes to them? Have a think...

...

...

...

OK, here's what you could try for the score: in the code
:code:`eat_food` function, inside the `if-statement` that checks for a
dot, increase the score by one. So this block now reads: ::

  if world[iy][ix] == '.':
      world[iy][ix] = None
      pacman.food_left -= 1
      # Add this line...
      pacman.score += 1

We know where to decrement lives, we just added a banner there. Update
the block inside the if-statement so that it reads: ::

  set_banner("Ouch!", 5)
  pacman.lives -= 1
  reset_sprites()
  
Power-ups
---------

Let's make the power-ups do something interesting. We can spot them
in the :code:`eat_food` function. Add this code to the function
being careful to indent everything properly: ::

  elif world[iy][ix] == '*':
      world[iy][ix] = None
      pacman.score += 5

OK, so now we get an extra 5 points on our score, but we also
want the ghosts to run away from us. We need some way of knowing
that the Pac-Man has a power-up, which should be time limited in
some way -- we can use counters again for this. 

Let's start by adding another variable to the :code:`pacman` sprite.
Near the top of your program add this line: ::

  pacman.powerup = 0

Now we can add this line in the :code:`eat_food` function inside
that if-statement you just changed: ::
  
  pacman.powerup = 25

The last thing we need to do is to make the ghosts change direction. We
need something like this -- this won't work yet, but you get the idea: ::

  for g in ghosts: new_ghost_direction(g)

Now if we can get :code:`new_ghost_direction` to take account of
:code:`pacman.powerup` we can make them follow or run away from
Pac-Man.

Hmmm...

      
Run ghosts, run!
----------------

(Do ghosts actually have legs, can they run? Never mind.)

We already have a function called :code:`set_random_dir` which in
theory works for any sprite, but we only use it for ghosts. It doesn't
consider where Pac-Man is it just sets a random direction.

Let's rename this function to make our intentions clearer, let's call
it :code:`new_ghost_direction` and make it smarter so that ghosts
can run away from Pac-Man if he has a power up.

Here's the new function: ::

  def new_ghost_direction(g):
    if pacman.powerup:
        g.dx = math.copysign(GHOST_SPEED*1.5, g.x - pacman.x)
        g.dy = math.copysign(GHOST_SPEED*1.5, g.y - pacman.y)
    else:
        g.dx = random.choice([-GHOST_SPEED, GHOST_SPEED])
        g.dy = random.choice([-GHOST_SPEED, GHOST_SPEED])

The last bit is the same as before, but the first bit is new. If
Pac-Man has a power up we have some weird maths going on. What does it
mean? Here's what:

* `g.dx` and `g.dy` are the ghost's direction, as before
* `math.copysign` takes two numbers: some value and an expression
  which returns a positive or negative number. It applies the sign of
  that number to the value
* In our function the sign is determined by the relative position
  of Pac-Man and the ghost.
* For example: if the ghost is to the right of Pac-Man the sign will
  be positive so the ghost will move to the right (away from Pac-Man)
* And if the ghost is to the left the sign will be negative and
  the ghost will move to the left (away)
* The value is the speed, which is 1.5 times the original, a bit
  faster than before.

Phew! That's a lot going on in only a few lines. Now that you've
renamed the old function, we need to find where we used it and update
this code to use the new method.

Make the change in :code:`def make_ghost_actors`.

Now we can use the new function for power ups. Plus we can add a
banner to shout it out to the user. Update your :code:`eat_food`
function so that it looks like this: ::

  def eat_food():
    ix,iy = int(pacman.x / BLOCK_SIZE), int(pacman.y / BLOCK_SIZE)
    if world[iy][ix] == '.':
        world[iy][ix] = None
        pacman.food_left -= 1
        pacman.score += 1
    elif world[iy][ix] == '*':
        world[iy][ix] = None
        pacman.powerup = 25
        set_banner("Power Up!", 5)
        for g in ghosts: new_ghost_direction(g)
        pacman.score += 5

Time for a test... what do you think? 

Flashing ghosts
---------------

Coming soon. 

.. _code for part 4: https://github.com/ericclack/pygamezero_pacman/blob/master/pacman4.py
