#!/usr/bin/python

#
# File: batch-rename.py
# Desc: Adds the given extension to all the files in the given direectory.
#
# Author: Aravindhan Dhanasekaran <adhanas@ncsu.edu>
#

import os
import sys

# Constants
NUM_ARGS    = 3
SCRIPT_NAME = "batch-rename.py"

# Globals
g_extn      = None
g_dir       = None


#
# Name: print_usage
# Desc: Prints a friendly text on how to use this tool.
# Args: None
#
def print_usage():
    print "Usage: %s OPTIONS" % (SCRIPT_NAME)
    print "Adds the given extension to all the files in the given direectory."
    print " "
    print "OPTIONS"
    print " -e, --extn <Extension-Name>     the extension to be added without the period"    
    print " -d, --dir <Path-to-Directory>   path of the directory whose files are to be renamed"
    print " -h, --help                      prints this help text"
    print " "
    print "EXAMPLE"
    print "\"%s -e txt -d ~/test/directory\" would add \".txt\" extension to all the files in \"~/test/directory\" directory." \
            % (SCRIPT_NAME)

#
# Name: validate_args
# Desc: Validates the user passed arguments and sets the path accordingly.
# Args: None
#
def validate_args():
    global g_dir, g_extn

    if (len(sys.argv) < NUM_ARGS):
        print "ERROR: Incorrect number of arguments. See usage."
        print_usage()
        exit()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:e:", ["help", "dir=", "extn="])
    except getopt.GetoptError as err:
        print "ERROR: %s. See usage." % (err)
        print_usage()
        exit()
    for opt, arg in opts:
        if (opt in ("-h", "--help")):
            print_usage()
            exit()
        elif (opt in ("-d", "--dir")):
            g_dir = str(arg)
        elif (opt in ("-e", "--extn")):
            g_extn = str(arg)
        else:
            print "ERROR: Incorret options. See usage."
            print " "
            print_usage()
            exit()

#
# Name: main
# Desc: Main routine. Add the given extension to all the files in the user
#       given directory.
# Args: argv (user passed data)
#
def main(argv):
    validate_args()

    for each_file in os.listdir(g_dir):
        os.rename(each_file, each_file + "." + g_extn)


# Init code
if __name__ == "__main__":
    main(sys.argv)

