# -*- coding: utf8 -*-
"""
Utilities for common Unix shell issues
"""

from __future__ import print_function
import signal
import sys
 

def register_sigint_handler(handler=None):
    """
    Provides an interruption handler mechanism
    """
    if handler is None:
        def handler(signal, frame):
            print('\nYou pressed Ctrl+C. Exiting...')
            sys.exit(0)
    signal.signal(signal.SIGINT, handler)
