#!/usr/bin/python

#
# File: generate-gadgets.py
# Desc: Generate gadgets for obfuscated and unobfuscated coreutils binaries
#       using ROPgadget.py tool.
#
# Author: Aravindhan Dhanasekaran <adhanas@ncsu.edu>
#

import os
import os.path
import sys
import time
import getopt
import subprocess

# Constants
NUM_ARGS            = 2
BIN_TYPE_OBFUSC     = "obfusc"
BIN_TYPE_UNOBFUSC   = "unobfusc"
BIN_PATH            = "/home/hpjoshi/projects/csc705-rop-obfuscator/binaries/"
GADGET_PATH         = "/home/hpjoshi/projects/csc705-rop-obfuscator/gadgets/"
SCRIPT_NAME         = "generate-gadgets.py"

# Globals
g_bin_type      = None
g_bin_path      = None
g_gadget_path   = None 


#
# Name: print_usage
# Desc: Prints a friendly help text on how to use the script.
# Args: None
#
def print_usage():
    print "Usage: %s OPTIONS" % (SCRIPT_NAME) 
    print "Generates ROP gadgets for obfuscated/unobfuscated "  \
            "coreutils binaries."
    print " "
    print "OPTIONS"
    print " -t, --bin-type {obfusc | unobfusc}  type of binaries "  \
                    "to be tested for gadgets"
    print " -h, -- help                         prints this help text"
    return


#
# Name: validate_args
# Desc: Validates the user passed arguments and sets the path accordingly.
# Args: None
#
def validate_args():
    global g_bin_type, g_bin_path, g_gadget_path

    if (len(sys.argv) < NUM_ARGS):
        print "ERROR: Incorrect number of arguments. See usage."
        print_usage()
        exit()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:", ["help", "bin-type="])
    except getopt.GetoptError as err:
        print "ERROR: %s. See usage." % (err)
        print_usage()
        exit()
    for opt, arg in opts:
        if (opt in ("-h", "--help")):
            print_usage()
            exit()
        elif (opt in ("-t", "--bin-type")):
            if (BIN_TYPE_OBFUSC == arg):
                g_bin_type = BIN_TYPE_OBFUSC
                g_bin_path = BIN_PATH + BIN_TYPE_OBFUSC + "/"
                g_gadget_path = GADGET_PATH + BIN_TYPE_OBFUSC + "/"
            elif (BIN_TYPE_UNOBFUSC == arg):
                g_bin_type = BIN_TYPE_UNOBFUSC
                g_bin_path = BIN_PATH + BIN_TYPE_UNOBFUSC + "/"
                g_gadget_path = GADGET_PATH + BIN_TYPE_UNOBFUSC + "/"
            else:
                print "ERROR: Incorrect argument. See usage."
                print_usage()
                exit()


#
# Name: find_gadgets_for_bin
# Desc: Finds the list of ROP gadgets for the given binary and stores them in
#       a list in g_gadget_path.
# Args: bin_name (binary file name)
#
def find_gadgets_for_bin(bin_name):
    rop_gadget = "/home/hpjoshi/projects/csc705-rop-obfuscator/rop-gadget.py"
    rop_gadget_options = " --binary "
    cmd = rop_gadget + rop_gadget_options + \
            g_bin_path + bin_name + \
            " > " + \
            g_gadget_path + bin_name + ".gdt"
    os.system(cmd)
    print "Gadget file created for %s binary %s." % (g_bin_type, bin_name)
    return

#
# Name: main
# Desc: Main routine for this script. 
# Args: argv (user passed data)
#
def main(argv):
    num_gadgets = 0
    start_time = time.time()
    validate_args()

    print "Creating gadgets for %s binaries..." % (g_bin_type)
    print "Binaries location: %s" % (g_bin_path)
    print " "

    for each_bin_file in os.listdir(g_bin_path):
        num_gadgets += 1
        find_gadgets_for_bin(each_bin_file)
   
    print " "
    print "Gadgets location: %s" % (g_gadget_path)
    print "Total number of %s binaires' gadgets crated: %u." \
            %(g_bin_type, num_gadgets)

    end_time = time.time()
    exec_seconds = (end_time - start_time)
    m,s = divmod(exec_seconds, 60)
    h, m = divmod(m, 60)
    print "Total time taken: %02uh %02um %02us" % (h, m, s)


# Init code
if __name__ == "__main__":
    main(sys.argv)

