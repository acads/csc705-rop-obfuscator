#!/usr/bin/python

#
# File: rop-gadget-categorizer.py 
# Desc: Categorize the gadgets found by ROPgadget.py tool based on the 
#       original ROP paper.
#
# Author: Aravindhan Dhanasekaran <adhanas@ncsu.edu>
#


import sys
import os
import os.path
import getopt

# Constants
NUM_ARGS    = 2
SCRIPT_NAME = "rop-gadget-categorizer.py"

# Globals
g_file_name             = None
g_count_only_flag       = False
g_print_gadgets_flag    = False

#
# Instructions to look for while categorizing the gadgets. This is based on
# the original ROP paper titled "Return-Oriented Programming: Systems, 
# Languages, and Applications"
#
CATEGORY_MEM    = ['pop', 'mov']
CATEGORY_ARITH  = ['add', 'sub', 'mul', 'div']
CATEGORY_LOGIC  = ['xor', 'ror', 'roll', 'and', 'or', 'not']
CATEGORY_CTRL   = ['lcall', 'call', 'jmp', 'je']

# Counters to hold the number of categories in each category.
category_num_mem    = 0  
category_num_arith  = 0
category_num_logic  = 0
category_num_ctrl   = 0
category_num_other  = 0
category_num_total  = 0


#
# Name: print_usage
# Desc: Prints a friendly help text on how to use this tool.
# Args: None
def print_usage():
    print "Usage: %s OPTIONS" % (SCRIPT_NAME) 
    print "Categorizes the ROP gadgets and prints the summary (or summary and gadgets) to a file."
    print " "
    print "OPTIONS"
    print " -f, --gadget-file <ROP-Gadget-File> file containing the actual ROP gadgets"
    print " -p, --print-gadgets                 print the gadget category summary along with the gadgets"
    print " -h, --help                          prints this help text"
    return


#
# Name: validate_args
# Desc: Validates the user passed arguments and sets the globals.
# Args: None.
#
def validate_args():
    global g_file_name, g_count_only_flag, g_print_gadgets_flag

    if (len(sys.argv) < NUM_ARGS):
        print "ERROR: At least %s arguments are required. See usage." \
                % (NUM_ARGS)
        print " "
        print_usage()
        exit()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:p", ["help, gadget-file, print-gadgets"])
    except getopt.GetoptError as err:
        print "ERROR: %s. See usage." % (err)
        print " "
        print_usage()
        exit()
    for opt, arg in opts:
        if (opt in ("-h", "--help")):
            print_usage()
            exit()
        elif (opt in ("-p", "--print-gadgets")):
            g_print_gadgets_flag = True
        elif (opt in ("-f", "--gadget-file")):
            g_file_name = str(arg)
            if (False == (os.path.isfile(g_file_name))):
                print "ERROR: Please enter a valid file name. See usage."
                print " "
                print_usage()
                exit()
            if (False == (os.access(g_file_name, os.R_OK))):
                print "ERROR: FIle \"%s\" is not readable. See usage." %(g_file_name)
                print " "
                print_usage()
                exit()
        else:
            print "ERROR: Invalid options. See usage."
            print " "
            print_usage()
            exit()


    return


#
# Name: categorize_gadget
# Desc: Categories the incoming gadget based on the instructions present in
#       the gadget string.
# Args: gadget string from the file
#
def categorize_gadget(gadget_str):
    global category_num_mem, category_num_arith, category_num_logic, \
            category_num_ctrl, category_num_other

    if any(inst in gadget_str for inst in CATEGORY_MEM):
        category_num_mem += 1
        gadget_type = "Memory: "
    elif any(inst in gadget_str for inst in CATEGORY_ARITH):
        category_num_arith += 1
        gadget_type = "Arithmetic: "
    elif any(inst in gadget_str for inst in CATEGORY_LOGIC):
        category_num_logic += 1
        gadget_type = "Logic: "
    elif any(inst in gadget_str for inst in CATEGORY_CTRL):
        category_num_ctrl += 1
        gadget_type = "Control-flow: "
    else:
        category_num_other += 1
        gadget_type = "Others: "

    if (g_print_gadgets_flag):
        print "%s%s" % (gadget_type, gadget_str)

    return


#
# Main program.
# Reads the passed in gadget file line by line and categorize them 
# individually. Finally, prints the categorized gadget counts.
#
validate_args()

fr = open(g_file_name, "r")
for each_line in fr:
    each_line = each_line.strip()
    category_num_total += 1
    categorize_gadget(each_line)

print "Categorized gadget count for \"%s\"." %(os.path.basename(g_file_name))
print "Total gadgets        : %4u" %(category_num_total)
print "Memory gadgets       : %4u" %(category_num_mem)
print "Arithmetic gadgets   : %4u" %(category_num_arith)
print "Logic gadgets        : %4u" %(category_num_logic)
print "Control flow gadgets : %4u" %(category_num_ctrl)
print "Other gadgets        : %4u" %(category_num_other)

