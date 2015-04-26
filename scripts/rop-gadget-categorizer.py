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

# Constants
NUM_ARGS    = 2
FILE_NAME   = None

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
    print " "
    print "Usage: %s <Gadget-File>" %(str(sys.argv[0]))
    print "<Gadget-File>: Output of ROPgadget.py in a text file."
    return


#
# Name: check_args
# Desc: Validates the arguments passed by the user.
#
def check_args():
    global FILE_NAME

    if (len(sys.argv) != NUM_ARGS):
        print "ERROR: %s arguments are required. See usage." %(NUM_ARGS)
        print_usage()
        exit()

    FILE_NAME = str(sys.argv[1])
    if (False == (os.path.isfile(FILE_NAME))):
        print "ERROR: Please enter a valid file name. See usage."
        print_usage()
        exit()

    if (False == (os.access(FILE_NAME, os.R_OK))):
        print "ERROR: FIle \"%s\" is not readable. See usage." %(FILE_NAME)
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
    elif any(inst in gadget_str for inst in CATEGORY_ARITH):
        category_num_arith += 1
    elif any(inst in gadget_str for inst in CATEGORY_LOGIC):
        category_num_logic += 1
    elif any(inst in gadget_str for inst in CATEGORY_CTRL):
        category_num_ctrl += 1
    else:
        category_num_other += 1
    
    return


#
# Main program.
# Reads the passed in gadget file line by line and categorize them 
# individually. Finally, prints the categorized gadget counts.
#
check_args()

fr = open(FILE_NAME, "r")
for each_line in fr:
    category_num_total += 1
    categorize_gadget(each_line)

print "Categorized gadget count for \"%s\"." %(os.path.basename(FILE_NAME))
print "Total gadgets        : %4u" %(category_num_total)
print "Memory gadgets       : %4u" %(category_num_mem)
print "Arithmetic gadgets   : %4u" %(category_num_arith)
print "Logic gadgets        : %4u" %(category_num_logic)
print "Control flow gadgets : %4u" %(category_num_ctrl)
print "Other gadgets        : %4u" %(category_num_other)

