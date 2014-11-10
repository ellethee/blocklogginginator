=============================
BlockLoggingInator
=============================

What is it?
-----------
It's a silly class to logging blocks execution time. 
It started as simple exercise and then i've put on some modify to make it more
flexible.

How to use it
-------------
It's easy just put some code inside a BlockLoggingInator with block,
BlockLoggingInator accepts 3 optional parameters:

 - **name** - String with the block name.
 - **start** - String with the *block start* string.
 - **end** - String with the *block end* string.
 - **log_func** - Function object to use for log/print things.
 - **et_format** - String to format the elapsed time.
 - **too_soon** - String for the *too soon* message.
 - **indent** - Boolean to instruct to indent or not an auto-named block.

**Where no parameter is passed, it uses the defaults:**

 - For the *name*: DEFAULT_BLOCK_NAME = "n°%(counter)d".
 - For the *start*: - START_BLOCK_STRING = 'Block "%(name)s"
 - For the *end*: - END_BLOCK_STRING = 'Block "%(name)s" ended at
    %(end_date)s (%(et_formatted)s)'
 - For the *log_func*: DEFAULT_LOG_FUNC = lbprint.
 - For *et_format* - ET_FORMAT = '%2.3f'
 - For *too_soon* - TOO_SOON = 'not yet compiled'
 - For the *indent*: DEFAULT_INDENT_STATE = False

**There are also other defaults that can be changed**

 - The default *indent char*: DEFAULT_INDENT_CHAR = '\\t'

.. note::
    
    *blocklogginginator.logblock* is the alias for BlockLoggingInator.

    *blocklogginginator.reset_to_defaults()* resets all values to the
    defaults.

Examples:
---------

Simple example:
***************
This is the simplyest case just log a for cycle.

.. code:: python

    import time
    from blocklogginginator import logblock  # logblock is the alias

    with logblock(name='one second'):
        time.sleep(1)

    >> Block "one second" started at 2013-08-02 12:21:33.889992
    >> Block "one second" ended at 2013-08-02 12:21:34.891145 (1.001)


Nested blocks:
**************
A little bit of nesting.

.. code:: python

    import time
    from blocklogginginator import logblock as lb  # logblock is the alias

    with lb(name='first blcok'):
        time.sleep(0.5)
        with lb(name='second block'):
            time.sleep(0.5)
            with lb(name='third block')
                time.sleep(0.5)
    
    >> Block "first blcok" started at 2013-08-02 17:37:20.786033
    >> Block "second block" started at 2013-08-02 17:37:21.286621
    >> Block "third block" started at 2013-08-02 17:37:21.787017
    >> Block "third block" ended at 2013-08-02 17:37:22.287381 (0.500)
    >> Block "second block" ended at 2013-08-02 17:37:22.287506 (1.001)
    >> Block "first blcok" ended at 2013-08-02 17:37:22.287552 (1.502)


More complex:
*************
Ok, let's try something more complex.

We wants to logging the block inside a recursive function.
Obviously we don't want that the blocks have the same name for each recursion.
So we can use the auto naming features. Without a name BlockLoggingInator uses
the DEFAULT_BLOCK_NAME with a counter to create the block name. And to make it
more readable we can decide to indent the result.

.. code:: python
    
    import time
    from blocklogginginator import logblock  # logblock is the alias

    def recursive(n):
        """
        A silly recursive function.
        """
        # block WITHOUT a name with all the defaults .
        with logblock(indent=True):
            if n == 0:
                return 0
            time.sleep(n / 100.0)
            return recursive(n - 1)
    recursive(3)

Our output will be:

.. code::

    >> Block "n°1" started at 2013-08-02 15:44:18.447216
    >>     Block "n°2" started at 2013-08-02 15:44:18.477472
    >>         Block "n°3" started at 2013-08-02 15:44:18.497737
    >>             Block "n°4" started at 2013-08-02 15:44:18.507976
    >>             Block "n°4" ended at 2013-08-02 15:44:18.508083 (0.000)
    >>         Block "n°3" ended at 2013-08-02 15:44:18.508143 (0.010)
    >>     Block "n°2" ended at 2013-08-02 15:44:18.508191 (0.031)
    >> Block "n°1" ended at 2013-08-02 15:44:18.508234 (0.061)

Let's play with the defaults:
*****************************
ok, with the last example we had a lot of information and although the
*indent* has made the thing a little more clear maybe we can do something
better.

.. code:: python

    import time
    from blocklogginginator import logblock  # logblock is the alias
    import blocklogginginator
    # we will use logging facility to logging the blocks
    import logging
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

    def recursive(n):
        """
        A silly recursive function.
        """
        # block with all the defaults.
        with lb():
            if n == 0:
                return 0
            """
            We want a different name and a different end string, we don't need
            the start block string.
            """
            with lb('The number is %d' % n, start='',
                    end='Block "%(name)s": %(et_formatted)s.'):
                time.sleep(n / 100.0)
                return recursive(n-1)
    recursive(5)

And our result is this:

.. code::

    >> 2013-08-02 17:44 Block "n°1" started
    >> 2013-08-02 17:44     Block "n°2" started
    >> 2013-08-02 17:44         Block "n°3" started
    >> 2013-08-02 17:44             Block "n°4" started
    >> 2013-08-02 17:44                 Block "n°5" started
    >> 2013-08-02 17:44                     Block "n°6" started
    >> 2013-08-02 17:44                     Block "n°6" ended: 0.000
    >> 2013-08-02 17:44                   Block "The number is 1": 0.011.
    >> 2013-08-02 17:44                 Block "n°5" ended: 0.011
    >> 2013-08-02 17:44               Block "The number is 2": 0.031.
    >> 2013-08-02 17:44             Block "n°4" ended: 0.032
    >> 2013-08-02 17:44           Block "The number is 3": 0.062.
    >> 2013-08-02 17:44         Block "n°3" ended: 0.063
    >> 2013-08-02 17:44       Block "The number is 4": 0.103.
    >> 2013-08-02 17:44     Block "n°2" ended: 0.103
    >> 2013-08-02 17:44   Block "The number is 5": 0.154.
    >> 2013-08-02 17:44 Block "n°1" ended: 0.154
