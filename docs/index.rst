.. highlight:: python

======
Shout!
======
*Loud* python messaging!

Shout is a single module providing simple messaging vocabulary for small applications. Shout is NOT a distributed messaging framework.

::

    from shout import Message, hears, shout


    class Greeting(Message):
        pass


    @hears(Greeting)
    def responder(msg):
        return '{0} {0}!'.format(msg)


    msg = shout(Greeting, 'Hello')
    print(msg.results, msg.success)

    # ['Hello Hello'] True


Why Shout
=========

* Decoupling of a GUI and it's behavior

  * PySide/PyQt signals are bound to widgets making it harder to decouple widgets. You have to explicitly connect each widget's signals with their slots which could live deep in a hierarchy of widgets.

  * Shout Messages are classes themselves, readily available to all other objects in their scope. Shout from inside, outside, top, or bottom of a widget hierarchy, Messages will still get to where they need to go!

* It's easy and fun to use.


API Documentation
=================

.. toctree::
   :maxdepth: 2

   api
