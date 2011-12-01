#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

"""
Simple logger module.
"""

import time
import sys

__all__ = ['Logger']

class Logger(object):
    """Logs everything with timestamp"""
    
    def __init__(self, start_time):
        self.start_time = start_time
        
    def log(self, line, end_line=True):
        
        timestamp = time.strftime('[%.6f]'% (time.time() - self.start_time))
        
        if line[-1] == '\n': # Remove '\n'
            line = line[-1]

        if end_line:
            print('%s %s' %(timestamp, line))
        
        else:
            sys.stdout.write('%s %s'%(timestamp, line))
    
    def stdout(self, text):
        """Write straight to stdout without timestamps"""
        sys.stdout.write(text)
    
        

