======
Shout!
======
*Loud* python messaging.

.. image:: https://travis-ci.org/danbradham/shout.svg?branch=master
  :target: https://travis-ci.org/danbradham/shout

.. image:: https://coveralls.io/repos/danbradham/shout/badge.png?branch=master
  :target: https://coveralls.io/r/danbradham/shout?branch=master

Shout is a single module providing simple messaging vocabulary for small applications. Shout is NOT a distributed messaging framework.

::

    from shout import Message, hears, shout


    class WhoAreYou(Message):
        pass


    @hears(WhoAreYou)
    def lucky_day():
        return "We are..."


    @hears(WhoAreYou)
    def dusty_bottoms():
        return "The threeee..."


    @hears(WhoAreYou)
    def ned_nederlander():
        return "Amigos!!"


    msg = shout(WhoAreYou)
    print("".join(msg.results))

    # We are...The threeee...Amigos!!


Why Shout
=========

* Decoupling of a GUI and it's behavior

  * PySide/PyQt signals are bound to widgets making it harder to decouple widgets. You have to explicitly connect each widget's signals with their slots which could live deep in a hierarchy of widgets.

  * Shout Messages are classes themselves, readily available to all other objects in their scope. Shout from inside, outside, top, or bottom of a widget hierarchy, Messages will still get to where they need to go!

* It's easy and fun to use.


For more information visit the `docs <http://shout.readthedocs.org>`_.
