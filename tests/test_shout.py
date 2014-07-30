from shout import Message, HasEars, hears, shout, typecheck_args
from nose.tools import *


class GetClasses(Message):
    pass


class GetException(Message):
    pass


class Greet(Message):
    pass


class SendArgsKwargs(Message):
    pass


class A(HasEars):

    @hears(Greet)
    def a_class_method(self):
        return "Hi from a!"

    @hears(GetClasses)
    def give_class(self):
        return self.__class__


class B(HasEars):

    @hears(Greet, rooms=("B", "C"))
    def b_class_method(self):
        return "Hi from b!"

    @hears(GetClasses)
    def give_class(self):
        return self.__class__


@hears(Greet, rooms=("Unbound",))
def module_level_fn():
    return "Hi from module_level_fn!"


@hears(SendArgsKwargs)
def module_level_fn_args_kwargs(*args, **kwargs):
    return args, kwargs


@hears(GetException)
def module_level_fn_raises_exc(*args, **kwargs):
    raise AttributeError("Bad error!")


class Test_Shout(object):

    @classmethod
    def setup_class(cls):
        cls.a = A()
        cls.b = B()

    def test_shout(self):
        msg = shout(Greet)
        assert msg.results == ['Hi from a!']


    def test_room(self):
        msg = shout(Greet, room="Unbound")
        assert msg.results == ["Hi from module_level_fn!"]


    def test_rooms(self):

        msg_b = shout(Greet, room="B")
        msg_c = shout(Greet, room="C")
        assert msg_b.results == ["Hi from b!"]
        assert msg_c.results == ["Hi from b!"]


    def test_exc(self):
        msg_e = shout(GetException)
        assert isinstance(msg_e.exc, AttributeError)


    def test_results(self):
        msg = shout(GetClasses)
        assert A in msg.results
        assert B in msg.results


    def test_args_kwargs(self):
        msg = shout(SendArgsKwargs, "oh yes", kwarg="right")
        assert (("oh yes", ), {"kwarg": "right"}) in msg.results


    @raises(TypeError)
    def test_typecheck_args(self):
        args = (Greet, GetClasses, SendArgsKwargs)
        assert typecheck_args(args)

        args = ("A", Greet)
        typecheck_args(args)

        args = "A"
        typecheck_args(args)
