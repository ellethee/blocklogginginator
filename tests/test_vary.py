# -*- coding: utf-8 -*-
"""
    Simple test
"""

import unittest
import time
from blocklogginginator import logblock


class TestBlocklogginginator(unittest.TestCase):
    """
    UnitTest
    """
    def test_simple(self):
        """
        Simple test.
        """
        print ("#" * 5, "Simple example", "#" * 5)
        with logblock(name='one second'):
            time.sleep(1)

    def test_nested(self):
        """
        Nested blocks
        """
        print ("#" * 5, "Nested blocks", "#" * 5)
        with logblock(name='first blcok'):
            time.sleep(0.5)
            with logblock(name='second block'):
                time.sleep(0.5)
                with logblock(name='third block'):
                    time.sleep(0.5)

    def test_recoursive(self):
        """
        Recursive.
        """
        print ("#" * 5, "Recursive blocks with logging", "#" * 5)
        import logging
        import blocklogginginator
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(message)s',
            datefmt='%F %R',
        )
        # change the default logging function
        blocklogginginator.DEFAULT_LOG_FUNC = logging.info
        # as default we want that the blocks will be indent .
        blocklogginginator.DEFAULT_INDENT_STATE = True
        # and as default indenti 2 spaces will be fine.
        blocklogginginator.DEFAULT_INDENT_CHAR = '  '
        # we don't care time and date for the start string, just the name.
        blocklogginginator.START_BLOCK_STRING = 'Block "%(name)s" started'
        # at the end we need to know the elapsed time.
        blocklogginginator.END_BLOCK_STRING = (
            'Block "%(name)s" ended: %(et_formatted)s')

        def recursive(number):
            """
            A silly recursive function.
            """
            # block with all the defaults.
            with logblock():
                if number == 0:
                    return 0
                """
                We want a different name and a different end string,
                we don't need the start block string.
                """
                with logblock(
                    'The number is %d' % number, start='',
                        end='Block "%(name)s": %(et_formatted)s.'):
                    time.sleep(number / 100.0)
                    return recursive(number - 1)
        recursive(5)
        blocklogginginator.reset_to_defaults()


if __name__ == '__main__':
    unittest.main()
