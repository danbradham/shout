.. _guide:
.. currentmodule:: shout

Guide
=====
This section provides everything you need to know about using Shout.

Creating a Message
------------------
Start by importing the essentials from shout.

::

    from shout import Message, has_ears, hears, shout

Now we can create a new type of :class:`Message`.

::

    class MyMessage(Message):
        pass

Our :class:`Message` type will allow us to :func:`shout` args and kwargs around our application. But, before we can do that...

Who is Listening?
-----------------
Let's make a function that can actually hear us :func:`shout` our :class:`Message` s.

::

    @hears(MyMessage, inside="A")
    def maximum(msg):
        return upper(msg) + "!!"

:func:`max_volume` will hear all :class:`MyMessage` shouts inside room "A". In this case only one type of :class:`Message` will be heard, but multiple :class:`Message` s can be passed as args to :func:`hears`. Additionally multiple rooms can be passed as a tuple to the inside keyword argument. If you don't pass any room names to inside, your function will listen in the default room, "void".

Does your class have ears?
--------------------------
You're every day class doesn't have ears so it's methods won't be able to hear
any shouted :class:`Message` s. It's **super** simple to give a class ears, just decorate it with :func:`has_ears`!

::

    @has_ears
    class Volumes(object):

        @hears(MyMessage)
        def low(msg):
            return lower(msg)

        @hears(MyMessage)
        def med(msg):
            return msg.title()

        @hears(MyMessage)
        def hi(msg):
            return upper(msg)

Shout at the top of your lungs!
-------------------------------
Time to shout some messages!

::

    m = shout(MyMessage, "hello there", inside="A")

Okay, now we've shouted a :class:`Message` and we've got a :class:`Message` instance bound to **m**. :class:`Message` instances have a bunch of useful attributes.

::

    print "args, kwargs: ", m.args, m.kwargs
    print "response: ", m.response
    print "success: ", m.success
    print "excception: ", m.exc

    # args, kwargs: ("hello there", ), {}
    # response: ["HELLO THERE!!"]
    # success: True
    # exception: None

Cool, but, judging from the response, none of our methods in :class:`Volumes` heard us shout. That's because we shouted inside room "A". Let's see what happens if we shout again but this time, not explicitly into a room.

::

    m = shout(MyMessage, "hello again")

    print "args, kwargs: ", m.args, m.kwargs
    print "response: ", m.response
    print "success: ", m.success
    print "excception: ", m.exc

    # args, kwargs: ("hello again", ), {}
    # response: ["hello again", "Hello Again", "HELLO AGAIN"]
    # success: True
    # exception: None

There we go! It's important to note that while we only passed one argument in our shouts, any arg, kwarg signature is supported. :class:`Message` signatures are really set by their listeners. So, if you have multiple listeners for the same type of :class:`Message`, ensure that they all take the same parameters.

Debugging
---------
Shout has extensive logging which is turned off by default.

::

    from shout import shout_logging
    shout_logging(debug=True)

This will set Shouts logger level to logging.DEBUG. Printing out a ton of useful messages! You can also log to a file.

::

    shout_logging(debug=True, filename="shout.log")
