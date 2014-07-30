'''
=====
Shout
=====
'''

from __future__ import unicode_literals


__author__ = "Dan Bradham"
__version__ = "0.1.0"
__license__ = "MIT"
__all__ = ["HasEars", "Message", "hears", "shout"]


import inspect
from collections import Sequence, defaultdict
import sys


ROOM_DEFL = "void"


class MetaMsg(type):
    '''Metaclass adding a listeners dict to each subclass allowing them to keep
    track of their own listeners.'''

    def __new__(kls, name, bases, members):

        cls = super(MetaMsg, kls).__new__(kls, name, bases, members)
        cls.listeners = defaultdict(set)

        return cls

MetaMetaMsg = MetaMsg(str("MetaMetaMsg"), (), {}) # 2n3 compatible metaclass

class Message(MetaMetaMsg):
    '''Message instances store args and kwargs to shout to their listeners.
    When an instances shout method is called these args and kwargs are passed
    to all the listeners that hear Messages in the appropriate rooms. Rooms
    are nothing more than strings used as keys in a Message object's
    listeners     dictionary. Return values of the listeners are collected in
    the instance's results list. If all listeners run successfully the
    instance's success attribute is set to True. If an Exception is raised
    during a shout, the shout is stopped and the Execution is bound to the
    message's exc attribute.

    :param args: Arguments to shout
    :param kwargs: Keyword Arguments to shout
    :method shout: Passes args and kwargs to all appropriate listeners
    :classmethod new: Dynamically creates a new Message object.
    '''

    def __init__(self, *args, **kwargs):

        try:
            self.room = kwargs.pop("room")
        except KeyError:
            self.room = ROOM_DEFL
        self.args = args
        self.kwargs = kwargs
        self.results = []
        self.exc = None
        self.success = False

    def shout(self):

        listeners = self.listeners[self.room]
        if not listeners:
            self.exc = UserWarning(
                "Nobody is listening in room: {0}".format(self.room))
            return

        for listener in listeners:
            try:
                result = listener(*self.args, **self.kwargs)
                self.results.append(result)
            except:
                self.exc = sys.exc_info()[1]
                return
        self.success = True

    @classmethod
    def add_listener(cls, fn):
        for room in fn.rooms:
            cls.listeners[room].add(fn)
        return cls

    @classmethod
    def rem_listener(cls, fn):
        for room_set in cls.listeners.itervalues():
            cls.listeners.discard(fn)
        return cls

    @staticmethod
    def new(name):
        '''Dynamically create a new Message object.

        :param name: The __class__.__name__ to use.
        '''
        message = type(name, (Message,), {})
        return message


class HasEars(object):
    '''A Mixin baseclass that automatically takes methods decorated with hears
    and adds them as listeners for the specified Messages.
    '''

    def __init__(self, *args, **kwargs):

        members = inspect.getmembers(self.__class__)
        for name, member in members:
            if getattr(member, "has_ears", False):
                method = getattr(self, member.__name__)
                for msg_type in member.msg_types:
                    msg_type.add_listener(method)
        super(HasEars, self).__init__(*args, **kwargs)


def typecheck_args(args):
    '''Ensures all args are of type Message.'''
    if isinstance(args, Sequence):
        for item in args:
            if not issubclass(item, Message):
                raise TypeError(
                    "All arguments passed to hears must be"
                    " subclasses of Message")
        return True

    raise TypeError(
        "Wrong argument signature passed to hears decorator..."
        "Pass a Message subclass or multiple Message subclasses.")


def hears(*args, **kwargs):
    '''Wrap a function or Node method to hear Messages. Pass Node names to the
    rooms keyword to limit the method to hear only Messages from certain
    Node objects.

    :param args: The type of Messages this function should listen to.
    :param rooms: A tuple containing the rooms the function listens to.'''
    def wrapper(fn):

        typecheck_args(args) # Make sure all our args are Message Subclasses

        fn.has_ears = True
        fn.msg_types = args
        fn.rooms = kwargs.get("rooms", (ROOM_DEFL,))

        if isinstance(fn.rooms, basestring):
            fn.rooms = (fn.rooms,)

        argspec = inspect.getargspec(fn)
        if argspec.args and argspec.args[0] == "self":
            return fn

        for msg_type in fn.msg_types:
            msg_type.add_listener(fn)
    return wrapper


def shout(msg_type, *args, **kwargs):
    '''A convenience method for shouting Message instances.

    :param msg_type: The type of Message to shout.
    :param room: The room to shout into.'''
    msg = msg_type(*args, **kwargs)
    msg.shout()
    return msg
