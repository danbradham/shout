'''
Shout
-----
A loud messaging framework.
'''

from __future__ import unicode_literals


__author__ = "Dan Bradham"
__version__ = "0.1.0"
__license__ = "MIT"
__all__ = ["HasEars", "Message", "hears", "shout"]


import inspect
from collections import Sequence, defaultdict
import sys
from six import add_metaclass


ROOM_DEFL = "void"


class MetaMsg(type):
    '''Metaclass adding a listeners dict allowing subclasses to keep
    track of listeners and their methods.'''

    def __new__(kls, name, bases, members):

        cls = super(MetaMsg, kls).__new__(kls, name, bases, members)
        cls.listeners = defaultdict(set)

        return cls

@add_metaclass(MetaMsg)
class Message(object):

    def __init__(self, *args, **kwargs):

        try:
            self.room = kwargs.pop("to")
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
                "Nobody is listening to room: {0}".format(self.room))
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

        message = type(name, (Message,), {})
        return message


class HasEars(object):

    def __init__(self, *args, **kwargs):

        members = inspect.getmembers(self.__class__)
        for name, member in members:
            if getattr(member, "has_ears", False):
                method = getattr(self, member.__name__)
                for msg_type in member.msg_types:
                    msg_type.add_listener(method)
        super(HasEars, self).__init__(*args, **kwargs)


def typecheck_args(args):
    '''Ensures all objects in sequence are of type Message.'''
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
    Node objects.'''
    def wrapper(fn):

        typecheck_args(args) # Make sure all our args are Message Subclasses

        fn.has_ears = True
        fn.msg_types = args
        fn.rooms = kwargs.get("inside", (ROOM_DEFL,))

        if isinstance(fn.rooms, basestring):
            fn.rooms = (fn.rooms,)

        argspec = inspect.getargspec(fn)
        if argspec.args and argspec.args[0] == "self":
            return fn

        for msg_type in fn.msg_types:
            msg_type.add_listener(fn)
    return wrapper


def shout(msg_type, *args, **kwargs):
    '''A convenience method for shouting Message instances.'''
    msg = msg_type(*args, **kwargs)
    msg.shout()
    return msg
