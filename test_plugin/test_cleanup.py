"""
Demonstration of how to write a plugin which simulates the addCleanup behavior
of unitest.TestCase.

Run as:

    python test_cleanup.py --with-cleanup

"""
import nose
from nose.plugins.base import Plugin


class CleanupPlugin(Plugin):
    """This plugin provides test timings

    """
    name = 'cleanup'

    def options(self, parser, env):
        """Sets additional command line options."""
        super(CleanupPlugin, self).options(parser, env)

    def configure(self, options, config):
        """Configures the test timer plugin."""
        super(CleanupPlugin, self).configure(options, config)

    def afterTest(self, test):
        test.test.inst.doCleanup()


class TestCase(object):
    def __init__(self):
        self._cleanups = []

    def addCleanup(self, f, *args, **kwargs):
        self._cleanups.append((f, args, kwargs))

    def doCleanup(self):
        while self._cleanups:
            function, args, kwargs = self._cleanups.pop()
            function(*args, **kwargs)


xs = []


class TestCustom(TestCase):
    def setUp(self):
        global xs
        self.addCleanup(xs.pop)
        print xs
        if not xs:
            xs.append(1)
            xs.append(2)
            xs.append(3)
            print xs
            raise ValueError()

    # expected to fail
    def test_a(self):
        assert not xs

    def test_b(self):
        assert len(xs) == 2

    def test_c(self):
        assert len(xs) == 1


if __name__ == '__main__':
    nose.main(addplugins=[CleanupPlugin()])
