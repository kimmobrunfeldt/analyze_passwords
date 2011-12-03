# Installation

Clone git repository to your computer

`git clone git://github.com/kimbledon/anapass.git`

Program is run with command

`python anapass.py analyze_these.txt wordlists/*`

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

`ALL_PASSWORD_COMBINATIONS / HASHES_PER_SECOND`

If password's length is 3, all password combinations are calculated with following formula

`charsetlen^1 + charsetlen^2 + charsetlen^3`

If password consists from a-z letters all combinations would be

`26^1 + 26^2 + 26^3 = 18278`
