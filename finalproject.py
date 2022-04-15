#!/usr/bin/python

"""/**********************************
 * Name: Joshua Bih
 * Email: jbih2@nd.edu
 * File Name: basketball.h
 * Date Created: 4/7/2022
 * File Contents: This file contains the function declarations for the Final Project
 **********************************/"""

#__author__ = "Josh Bih"
#__email__ = "jbih2@nd.edu"

import os
import sys
import pprint

from nba_api.stats.static import players

def usage(exit_code=0):
    progname = os.path.basename(sys.argv[0])
    print(f'''Usage: {progname} [-a ALPHABET -c CORES -l LENGTH -p PATH -s HASHES]
    -a ALPHABET Alphabet to use in permutations
    -c CORES    CPU Cores to use
    -l LENGTH   Length of permutations
    -p PREFIX   Prefix for all permutations
    -s HASHES   Path of hashes file''')
    sys.exit(exit_code)

def main():
    # Basic Request

    # get_teams returns a list of 30 dictionaries, each an NBA team.    
    player_info = players.find_players_by_first_name('james')
    for player in player_info:
        print(player)

    # Parse command line arguments  
    """
    if len(sys.argv) < 2:
        usage(2)

    arguments = sys.argv[1:]

    while (len(arguments) and arguments[0].startswith('-')):
        argument = arguments.pop(0)
        
        if argument == "-h":
            usage()

        elif argument == "-s":
            shorten = True

        elif argument == "-n":
            limit = int(arguments.pop(0))

        elif argument == "-o":
            orderby = arguments.pop(0)

        elif argument == "-t":
            titlelen = int(arguments.pop(0))

        else:
            usage("1")
    """

    # Loads data from HTTP request

# Main Execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
