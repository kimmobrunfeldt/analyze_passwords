# Warning

This program is overly optimistic in its approximations! There are many ways to make cracking even faster. 
If your password is bad according to this program, in reality it sucks.

# Installation

Clone git repository to your computer

`git clone git://github.com/kimbledon/anapass.git`

Run with command(wordlists are optional):

`python anapass.py analyze_these.txt [wordlists/*]`

# Main purpose

Main purpose of the program is to analyze how good passwords are. You should believe this analyzer when you give a password in a public site.
The (almost) worst case scenario is that passwords are stored as MD5 hashes to site's database.

# Analyzing

## Known words

There is two wordlists included in source code, english(3262212 words) and finnish(94123 words) wordlist.
Program creates a few additions to the wordlists: original words with ! added in the end and original words where o -> 0 and i -> 1

## Calculations

I looked at newest MD5 cracking tools and their cracking speed. For example: http://hashcat.net/oclhashcat-plus/#tested-gpu
With Ubuntu 10.10, 64 bitCatalyst 11.6 + Stream SDK v2.48x ATI hd6970,
you could create 26122 million MD5 hashes per second.

The program estimates the bruteforcing times with following formula:

`ALL_PASSWORD_COMBINATIONS / HASHES_PER_SECOND / 2`

Time is divided by 2 because on average, testing half of the combinations is enough to crack the password.

If password's length was 3, all password combinations would be calculated with the following formula

`charsetlen^1 + charsetlen^2 + charsetlen^3`

If password consisted from a-z letters, all combinations would be

`26^1 + 26^2 + 26^3 = 18278`

Also the entropy of the password is calculated with the formula given in http://en.wikipedia.org/wiki/Password_strength
