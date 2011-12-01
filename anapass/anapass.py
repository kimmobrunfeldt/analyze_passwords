#!/usr/bin/python
# -*- coding: UTF-8 -*-

# License: CC BY-SA 3.0, http://creativecommons.org/licenses/by-sa/3.0/
# Author: Kimmo Brunfeldt
# 2011

import hashlib
import time
import string
import logger
import sys

# How many hashes can be generated in second
HASH_PER_SEC = 10**6 * 600  # 600 million.
# http://www.elcomsoft.com/lhc.html -> With a few GPUs this cracking speed is possible.

# That's why it is being multiplied by 5 (I bet a group of crackers can do
# even better)
HASH_PER_SEC *= 5


MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24
YEAR = DAY * 365

# Constants to estimate strength of password. Constants are seconds to break
# password with brute force.
# Everything below WEAK_SECS is considered as "useless" password.

WEAK_SECS = DAY * 30                     # 30 days
OK_SECS = DAY * 365 * 10                 # 10 years
STRONG_SECS = DAY * 365 * 1000           # 1000 years
VERYSTRONG_SECS = DAY * 365 * 10 ** 25   # 10^25 years

def secs_readable(secs):
    """Converts seconds to human-readable form."""

    if secs > YEAR:
        return str( int(round(float(secs) / YEAR)) ) + " years"
    
    if secs > DAY:
        return str( int(round(float(secs) / DAY)) ) + " days"
    
    if secs > HOUR:
        return str( int(round(float(secs) / HOUR)) ) + " hours"
    
    if secs > MINUTE:
        return str( int(round(float(secs) / MINUTE)) ) + " minutes"
    
    return str(secs) + "seconds"
    

class PasswordOracle(object):
    """Analyzes passwords' weakness."""

    def __init__(self, wordlist_files):

        self.log = logger.Logger(time.time())
        self.read_wordlists(wordlist_files)
        self.modify_wordlist()
        
        if len(self.password_list) == 0:
            self.log.log('Wordlist is empty!')
        
        else:
            self.log.log('Sorting wordlist.. ')
            self.password_list.sort()
            self.log.log('Sorted.')

    def read_wordlists(self, wordlist_files):
        """Read wordlists to memory"""

        self.password_list = []
        
        self.log.log('Reading wordlist files..')
        
        for filename in wordlist_files:
            self.password_list += open(filename).read().splitlines()
        
        self.log.log('%s words read.'%len(self.password_list))
    
    def modify_wordlist(self):
        
        self.log.log('Modifying wordlists. Adding ! to end.')
        self.password_list += map(lambda x: x + '!', self.password_list)
        
        self.log.log('Changing o -> 0 and i -> 1.')
        self.password_list += map(lambda x: x.replace('o','0').replace('i','1'),
                                   self.password_list)
        
        self.log.log('Wordlist contains now %s words.' % len(self.password_list))
        
    def combinations(self, charsetlen, passwordlen):
        """Returns the amount of different passwords with a certain
        character set and password length. If password's length is 3,
        1 - 3 length password combinations is returned."""
        
        # charsetlen = 26, passlen = 3 returns: 26**1 + 26**2 + 26**3
        return sum([charsetlen ** (x + 1) for x in xrange(passwordlen)])

    def is_known_word(self, password):
        """Checks if password is a common word in wordlists"""
        
        if password in self.password_list:
            return True
        
        return False
    
    def give_grade(self, password):
        """Analyze the strength of password against bruteforce.
        Returns a word to describe password"""
        
        charsetlen = self.charset_len(password)
        
        all_combs = self.combinations(charsetlen, len(password))
        all_secs = all_combs / HASH_PER_SEC
        
        self.log.log('Charset\'s length is %s.'%charsetlen)

        self.log.log('1 - %s length passwords\' combinations: %s.'%(len(password), all_combs))
        self.log.log('1 - %s length\'s bruteforcing time: ~%s'%(len(password), secs_readable(all_secs)))
 
        if all_secs > VERYSTRONG_SECS:
            grade = "very strong"
        
        elif all_secs > STRONG_SECS:
            grade = "strong"
        
        elif all_secs > OK_SECS:
            grade = "just ok"
        
        elif all_secs > WEAK_SECS:
            grade = "weak"
        
        else:
            grade = "useless"

        if len(self.password_list):
            if self.is_known_word(password):
                grade = "useless(COMMON WORD, WAS FOUND IN WORDLIST!)"

        self.log.log('"%s" = %s'%(password, grade.upper()))
    
    def charset_len(self, password):
        """Returns integer of password charsetlen"""
        
        charsets = [
            string.ascii_lowercase,  # len=26
            string.ascii_uppercase,  # len=26
            string.digits,           # len=10
            "!_.?%* ",               # len=7
            "'\"#$@/&()=[]\,+-_",    # len=17
            "öäå",                   # len=3
        ]
        
        used_sets = [False] * len(charsets)  # To determine already added sets.
        
        self.log.log('Charset is: ', False)  # Without endline char.
        charsetlen = 0
        
        # Add charsets to charsetlen.
        # Sort password's characters -> charsets are printed in same order.
        for char in ''.join(sorted(password))[::-1]:
            for index, charset in enumerate(charsets):
                
                if char in charset and not used_sets[index]:
                    charsetlen += len(charset)
                    used_sets[index] = True
                    
                    self.log.stdout(charset)
        
        print('') 
        
        return charsetlen
        
    def analyze_all(self, words):
        """Analyze strength of words against bruteforce and wordlists"""
        
        print('')
        for word in words:

            self.log.log('Analyzing password "%s" (length = %s)'% (word, len(word)))
            self.give_grade(word)    
            
            print('')

if __name__ == '__main__':

    print('Calculations are based on following estimates:')
    print('%s hashes/sec is cracking speed.'% HASH_PER_SEC)

    p = PasswordOracle(sys.argv[2:])
    p.analyze_all(open(sys.argv[1]).read().splitlines())
    
