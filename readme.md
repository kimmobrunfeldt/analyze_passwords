# Installation

Clone git repository to your computer

`git clone `

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

I looked at newest MD5 cracking tools and their cracking speed. For example: http://www.elcomsoft.com/lhc.html
With NVIDIA 9800GX2, you could create 608 million MD5 hashes per second.

The program estimates the bruteforcing times with following formula:

`ALL_PASSWORD_COMBINATIONS / HASHES_PER_SECOND`

If password's length is 3, all password combinations are calculated with following formula

`charsetlen^1 + charsetlen^2 + charsetlen^3`

If password consists from a-z letters all combinations would be

`26^1 + 26^2 + 26^3 = 18278`
