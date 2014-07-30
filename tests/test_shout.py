from shout import Message, HasEars, hears, shout, typecheck_args
from nose.tools import *


class MsgResults(Message):
    pass


class MsgException(Message):
    pass


class Msg(Message):
    pass


class MsgArgsKwargs(Message):
    pass


class A(HasEars):

    @hears(Msg)
    def a_class_method(self):
        return "Hi from a!"

    @hears(MsgResults)
    def give_class(self):
        return self.__class__


class B(HasEars):

    @hears(Msg, rooms=("B", "C"))
    def b_class_method(self):
        return "Hi from b!"

    @hears(MsgResults)
    def give_class(self):
        return self.__class__


@hears(Msg, rooms=("Unbound",))
def module_level_fn():
    return "Hi from module_level_fn!"


@hears(Msg, rooms=("RemoveMe",))
def module_level_fn_for_removal():
    return "Hi from module_level_fn!"


@hears(MsgArgsKwargs)
def module_level_fn_args_kwargs(*args, **kwargs):
    return args, kwargs


@hears(MsgException)
def module_level_fn_raises_exc(*args, **kwargs):
    raise AttributeError("Bad error!")


class Test_Shout(object):

    @classmethod
    def setup_class(cls):
        cls.a = A()
        cls.b = B()

    def test_shout(self):
        msg = shout(Msg)
        assert msg.results == ['Hi from a!']


    def test_room(self):
        msg = shout(Msg, room="Unbound")
        assert msg.results == ["Hi from module_level_fn!"]


    def test_rooms(self):

        msg_b = shout(Msg, room="B")
        msg_c = shout(Msg, room="C")
        assert msg_b.results == ["Hi from b!"]
        assert msg_c.results == ["Hi from b!"]


    def test_exc(self):
        msg_e = shout(MsgException)
        assert isinstance(msg_e.exc, AttributeError)


    def test_results(self):
        msg = shout(MsgResults)
        assert A in msg.results
        assert B in msg.results


    def test_args_kwargs(self):
        msg = shout(MsgArgsKwargs, "oh yes", kwarg="right")
        assert (("oh yes", ), {"kwarg": "right"}) in msg.results

    def test_no_listeners(self):
        msg = shout(Msg, room="XYZ")
        assert isinstance(msg.exc, UserWarning)

    def test_rem_listener(self):
        assert module_level_fn_for_removal in Msg.listeners["RemoveMe"]
        Msg.rem_listener(module_level_fn_for_removal)
        assert (not Msg.listeners["RemoveMe"])

    def test_dynamic_message_creation(self):
        NewMessage = Message.create("NewMessage")

        @hears(NewMessage, rooms="NewRoom")
        def nm_listener():
            return True

        msg = shout(NewMessage, room="NewRoom")
        assert msg.results == [True]

    def test_typecheck_args(self):
        args = (Msg, MsgResults, MsgArgsKwargs)
        assert typecheck_args(args)

    @raises(TypeError)
    def test_typecheck_mixed(self):
        args = ("A", Msg)
        typecheck_args(args)

    @raises(TypeError)
    def test_typecheck_str(self):
        args = "A"
        typecheck_args(args)

    @raises(TypeError)
    def test_typecheck_not_seq(self):
        args = 1
        typecheck_args(args)
