.. highlight:: python
.. currentmodule:: shout

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
    def listener_a(msg):
        print("listener_a heard:", msg)


    msg = shout(Greeting, "Hello")


Why you'd use Shout
===================

* Decoupling of a GUI and it's behavior

  * PySide/PyQt signals are bound to widgets making it harder to decouple widgets. You have to explicitly connect each widget's signals with their slots which could live deep in a hierarchy of widgets.

  * Shout Messages are classes themselves, existing outside the scope of any individual widgets. Making them usable anywhere and everywhere in your app.

* It's easy and fun to use and incorporates well existing code.


.. toctree::
   :maxdepth: 2

