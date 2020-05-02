.. _part4:

Part 4
======

Part 4 is a work in progress, so at the moment this page is just a
bunch of notes. Feel free to have a read through and see what you can
discover.

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

OK, here's what you could try: in the code :code:`eat_food` function,
inside the `if-statement` that checks for a dot, increase the score
by one. So this block now reads: ::

  if world[iy][ix] == '.':
      world[iy][ix] = None
      pacman.food_left -= 1
      # Add this line...
      pacman.score += 1

  
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
some way.

Let's start by adding another variable to the :code:`pacman` sprite.
Near the top of your program add this line: ::

  pacman.powerup = False

Now we can add this line in the :code:`eat_food` function: ::
  
  pacman.powerup = True

The last thing we need to do is to make the ghosts change direction. We
need something like this -- this won't work yet, but you get the idea: :: 

  for g in ghosts: new_ghost_direction(g)

Now if we can get :code:`new_ghost_direction` to take account of
:code:`pacman.powerup` we can make them follow or run away from Pac-Man.

Hmmm...

      
Ghosts running away
-------------------




.. _code for part 4: https://github.com/ericclack/pygamezero_pacman/blob/master/pacman4.py
