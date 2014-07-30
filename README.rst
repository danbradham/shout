.. highlight:: python
.. currentmodule:: shout

======
Shout!
======
Loud python messaging! Shout is a single module providing elegant messaging syntax for small applications. Take a look...

::

    from shout import Message, hears, shout


    class Greeting(Message):
        pass


    @hears(Greeting)
    def listener_a(msg):
        print("listener_a heard:", msg)


    @hears(Greeting)
    def listener_b(msg):
        print("listener_b heard:", msg)


    shout(Greeting, "Hey There!")
