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
think we need to make changes to them?

...

...

...


  
  
Power-ups
---------

Ghosts running away
-------------------




.. _code for part 4: https://github.com/ericclack/pygamezero_pacman/blob/master/pacman4.py
