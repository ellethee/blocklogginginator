# -*- coding: utf-8 -*-
"""
A silly class to logging blocks execution time.
"""
__file_name__ = "blocklogginginator.py"
__author__ = "ellethee <ellethee@altervista.org>"
__version__ = "1.0.2"
__date__ = "2013-01-15"

import time
import datetime


def lbprint(message):
    """
    A default to print a message.
    """
    print message

"""
We use the _<NAME> to keep track of the original value.
"""
#: elapsed time format string
_ET_FORMAT = ET_FORMAT = "%2.3f"
#: String to print when the block starts.
_START_BLOCK_STRING = START_BLOCK_STRING = (
    'Block "%(name)s" started at %(start_date)s')
#: String to print when the block ends.
_END_BLOCK_STRING = END_BLOCK_STRING = (
    'Block "%(name)s" ended at %(end_date)s (%(et_formatted)s)')
#: The default block name.
_DEFAULT_BLOCK_NAME = DEFAULT_BLOCK_NAME = "n°%(counter)d"
#: Too soon string.
_TOO_SOON = TOO_SOON = 'not yet compiled'
#: The default log function
_DEFAULT_LOG_FUNC = DEFAULT_LOG_FUNC = lbprint
#: The default indent char
_DEFAULT_INDENT_CHAR = DEFAULT_INDENT_CHAR = '\t'
#: The default indent state
_DEFAULT_INDENT_STATE = DEFAULT_INDENT_STATE = False
#: The global counter.
_BLOCK_COUNTER = 1
_INDENT_COUNTER = 1


def reset_to_defaults():
    global ET_FORMAT, START_BLOCK_STRING, END_BLOCK_STRING, DEFAULT_BLOCK_NAME
    global TOO_SOON, DEFAULT_LOG_FUNC, DEFAULT_INDENT_CHAR
    global DEFAULT_INDENT_STATE
    ET_FORMAT = _ET_FORMAT
    START_BLOCK_STRING = _START_BLOCK_STRING
    END_BLOCK_STRING = _END_BLOCK_STRING
    DEFAULT_BLOCK_NAME = _DEFAULT_BLOCK_NAME
    TOO_SOON = _TOO_SOON
    DEFAULT_LOG_FUNC = _DEFAULT_LOG_FUNC
    DEFAULT_INDENT_CHAR = _DEFAULT_INDENT_CHAR
    DEFAULT_INDENT_STATE = _DEFAULT_INDENT_STATE


class BlockLoggingInator(object):

    """
    the logblock context manager, which prints when the block begins and when
    it ends.

    :params log_func: Function to use for print informations
        (default *DEFAULT_LOG_FUNC*).
    :params name: Name of the block (default *DEFAULT_BLOCK_NAME*)
    :params indent: Tells if a block with a counter has to be indented
        (default *DEFAULT_INDENT_STATE*).

    The returned context manager can be used to write directly into the
    log function and the message can contains logblock properties.

    example::

        import time
        import logging
        logging.basicConfig(level=logging.DEBUG)

        #: start out context manager as lb
        with logblock(logging.debug, "my block") as lb:

            #: use lb to log to the logger
            lb("%(name)s as already started")

            #: wait a little
            time.sleep(1)

        #: the block is ended now.
        lb("%(name)s has finish time arrival: %(et_formatted)s")

    result::

        DEBUG:root:Block "my block" started 2013-01-15 18:12:57.518049
        DEBUG:root:my block as already started
        DEBUG:root:Block "my block" ended 2013-01-15 18:12:58.519445 (1.001)
        DEBUG:root:my block has finish time arrival: 1.001

    """

    def __init__(
            self, name=None, start=None, end=None, log_func=None,
            et_format=None, too_soon=None, indent=None):
        global _BLOCK_COUNTER, _INDENT_COUNTER
        self.counter = 0
        self.indent = ''
        self._INDENT_COUNTER = _INDENT_COUNTER
        if indent or DEFAULT_INDENT_STATE:
            self.indent = DEFAULT_INDENT_CHAR * (self._INDENT_COUNTER - 1)
        self.log_func = log_func or DEFAULT_LOG_FUNC
        self.start_block_string = (
            start if start is not None else START_BLOCK_STRING)
        self.end_block_string = end if end is not None else END_BLOCK_STRING
        self.et_format = et_format or ET_FORMAT
        self.too_soon = too_soon or TOO_SOON
        self.start_date = self.end_date = self.start_time = self.end_time = \
            self.elapsed_time = self.too_soon
        """
        Ok, if we don't have a block name passed we will create one using the
        DEFAULT_BLOCK_NAME and we wil use the counter.
        """
        if name is None:
            self.counter = _BLOCK_COUNTER
            name = DEFAULT_BLOCK_NAME % vars(self)
            """
            We can indent the blocks respecting the counter.
            """
        self.name = name
        """
        Store our vars and the property to format elapsed time.
        """
        self.__vars = vars(self)
        self.__vars['et_formatted'] = self.et_formatted

    def __call__(self, message, *args, **kwargs):
        """
        Well let's make the class "callable" so we can use it directly to call
        the log function with some vars and args etc.
        """
        return self.log_func(message % self.__vars, *args, **kwargs)

    @property
    def et_formatted(self):
        """
        This will return the elapsed_time formatted.
        """
        if self.elapsed_time == self.too_soon:
            return self.too_soon
        return self.et_format % self.elapsed_time

    def __enter__(self):
        """
        The magic __enter__
        """
        """
        Increment the global counter if we have an instance counter.
        """
        global _BLOCK_COUNTER, _INDENT_COUNTER
        if self.counter:
            _BLOCK_COUNTER += 1
        _INDENT_COUNTER += 1
        """
        Let's set some vars.
        """
        self.start_time = time.time()
        self.start_date = datetime.datetime.fromtimestamp(self.start_time)
        """
        Refresh the __vars dict.
        """
        self.__vars = vars(self)
        self.__vars['et_formatted'] = self.et_formatted
        """
        Log the Start event.
        """
        if len(self.start_block_string):
            self(self.indent + self.start_block_string)
        """
        return self object for the with.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        The Magic __exit__.
        """
        global _BLOCK_COUNTER, _INDENT_COUNTER
        """
        We will decrement the global counter if we need.
        """
        if self.counter > 0:
            _BLOCK_COUNTER -= 1
        _INDENT_COUNTER -= 1
        """
        Let's set some vars.
        """
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        self.end_date = datetime.datetime.fromtimestamp(self.end_time)
        """
        Refresh the __vars dict.
        """
        self.__vars = vars(self)
        self.__vars['et_formatted'] = self.et_formatted
        """
        Log the End event.
        """
        if len(self.end_block_string):
            self(self.indent + self.end_block_string)

#: Alias
logblock = BlockLoggingInator
