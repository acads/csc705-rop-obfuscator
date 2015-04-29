#!/usr/bin/python

#
# File: categorize-gadgets.py 
# Desc: Categorize obfuscated and unobfuscated corteutils gadgets using
#       rop-gadget-categorizer.py tool.
#
# Author: Aravindhan Dhanasekaran <adhanas@ncsu.edu>
#

import os
import os.path
import sys
import time
import getopt

# Constants
NUM_ARGS            = 2
BIN_TYPE_OBFUSC     = "obfusc"
BIN_TYPE_UNOBFUSC   = "unobfusc"
OBFUSC_TYPE_BCF     = "bcf"
OBFUSC_TYPE_FLA     = "fla"
OBFUSC_TYPE_SUB     = "sub"
GADGET_PATH         = "/home/hpjoshi/projects/csc705-rop-obfuscator/gadgets/"
SCRIPT_NAME         = "categorize-gadgets.py"

# Globals
g_gadget_type   = None
g_gadget_path   = None 


#
# Name: print_usage
# Desc: Prints a friendly help text on how to use the script.
# Args: None
#
def print_usage():
    print "Usage: %s OPTIONS" % (SCRIPT_NAME) 
    print "Categorize obfuscated and unobfuscated coreutils gadgets."
    print " "
    print "OPTIONS"
    print " -t, --gadget-type {obfusc | unobfusc}   type of gadgets to be categorized"
    print " -o, --obfusc-type {bcf | fla | sub}     type of obfuscated binary, default is all types"
    print " -h, -- help                             prints this help text"
    print " "
    print "EXAMPLES"
    print " \"%s --gadget-type obfusc --obfusc-type fla\" categorizes fla type gadgets for obfuscated coretutils binaries"
    print " \"%s --gadget-type unobfusc\" categorizes gadgets unobfuscated coretutils binaries"
    return


#
# Name: validate_args
# Desc: Validates the user passed arguments and sets the path accordingly.
# Args: None
#
def validate_args():
    global g_gadget_type, g_gadget_path

    if (len(sys.argv) < NUM_ARGS):
        print "ERROR: Incorrect number of arguments. See usage."
        print " "
        print_usage()
        exit()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:o:", \
                ["help", "gadget-type=", "obfusc-type="])
    except getopt.GetoptError as err:
        print "ERROR: %s. See usage." % (err)
        print " "
        print_usage()
        exit()
    for opt, arg in opts:
        if (opt in ("-h", "--help")):
            print_usage()
            exit()
        elif (opt in ("-t", "--gadget-type")):
            if (BIN_TYPE_OBFUSC == arg):
                g_gadget_type = BIN_TYPE_OBFUSC
                g_gadget_path = GADGET_PATH + BIN_TYPE_OBFUSC + "/"
            elif (BIN_TYPE_UNOBFUSC == arg):
                g_gadget_type = BIN_TYPE_UNOBFUSC
                g_gadget_path = GADGET_PATH + BIN_TYPE_UNOBFUSC + "/"
        elif (opt in ("-o", "--obfusc-type")):
            if (BIN_TYPE_UNOBFUSC == g_gadget_type):
                print "ERROR: Unobfuscated binaries cannot be used with obfusc-type. See usage."
                print " "
                print_usage()
                exit()
            if (OBFUSC_TYPE_BCF == arg):
                g_gadget_path = g_gadget_path + OBFUSC_TYPE_BCF + "/"
            elif (OBFUSC_TYPE_FLA == arg):
                g_gadget_path = g_gadget_path + OBFUSC_TYPE_FLA + "/"
            elif (OBFUSC_TYPE_SUB == arg):
                g_gadget_path = g_gadget_path + OBFUSC_TYPE_SUB + "/"
            else:
                print "ERROR: Invalid obufsc-type. See usage."
                print " "
                print_usage()
                exit()
        else:
            print "ERROR: Incorrect option(s). See usage."
            print " "
            print_usage()
            exit()


#
# Name: categorize_gadgets
# Desc: Categorizes the gadgets of the given gadget file and writes the 
#       results in ".cnt" file of the same name as the gadget.
# Args: gadget_name (gadget file name)
#
def categorize_gadgets(gadget_file):
    categorizer = \
            "/home/hpjoshi/projects/csc705-rop-obfuscator/scripts/rop-gadget-categorizer.py"
    cmd = categorizer + " -f " + \
            g_gadget_path + gadget_file + \
            " > " + \
            g_gadget_path + gadget_file + ".cnt"
    os.system(cmd)
    print "%s %s gadget categorized." % (gadget_file, g_gadget_type)


#
# Name: main
# Desc: Main routine for this script. 
# Args: argv (user passed data)
#
def main(argv):
    num_gadgets = 0
    start_time = time.time()
    validate_args()

    print "Categorizing %s gadgets..." % (g_gadget_type)
    print " "

    for each_gadget_file in os.listdir(g_gadget_path):
        if each_gadget_file.endswith(".gdt"):
            num_gadgets += 1
            categorize_gadgets(each_gadget_file)
   
    print " "
    print "Gadgets location: %s" % (g_gadget_path)
    print "Total number of %s gadgets categorized: %u." \
            %(g_gadget_type, num_gadgets)

    end_time = time.time()
    exec_seconds = (end_time - start_time)
    m,s = divmod(exec_seconds, 60)
    h, m = divmod(m, 60)
    print "Total time taken: %02uh %02um %02us" % (h, m, s)


# Init code
if __name__ == "__main__":
    main(sys.argv)

