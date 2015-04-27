#!/usr/bin/python

#
# File: aggregate-gadget-count.py 
# Desc: Aggregates the ROP gadget categories for coreutils and writes the
#       gadgets binary-wise to different category files.
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
DATA_PATH           = "/home/hpjoshi/projects/csc705-rop-obfuscator/data/"
DATA_FILE           = "coretutils-aggregate.dat"
GADGET_PATH         = "/home/hpjoshi/projects/csc705-rop-obfuscator/gadgets/"
SCRIPT_NAME         = "aggregate-gadget-count.py"
STR_TOTAL           = "Total gadgets"
STR_MEMORY          = "Memory gadgets"
STR_ARITH           = "Arithmetic gadgets"
STR_LOGIC           = "Logic gadgets"
STR_CTRL            = "Control flow gadgets"
STR_OTHERS          = "Other gadgets"

# Globals
g_gadget_obfusc_path    = None 
g_gadget_unobfusc_path  = None 
g_data_path     = None
g_bin_name      = None
g_bin_flag      = False
g_cat_total     = 0
g_cat_memory    = 0
g_cat_arith     = 0
g_cat_logic     = 0
g_cat_ctrl      = 0
g_cat_others    = 0


#
# Name: print_usage
# Desc: Prints a friendly help text on how to use the script.
# Args: None
#
def print_usage():
    print "Usage: %s OPTIONS" % (SCRIPT_NAME) 
    print "Aggregates the ROP gadget category counts for coreutils binaries."
    print " "
    print "OPTIONS"
    print " -a, --aggregate-counts          aggregate gadget category " \
            "counts for obfuscated and unobfuscated coreutils binaries"
    print " -b, --binary-file <Binary-File> aggregate gadget category " \
            "counts for obfuscated and unobfuscated for given binary"
    print " -h, -- help                     prints this help text"
    return


#
# Name: validate_args
# Desc: Validates the user passed arguments and sets the path accordingly.
# Args: None
#
def validate_args():
    global g_gadget_obfusc_path, g_gadget_unobfusc_path, \
            g_bin_flag, g_bin_file_name

    if (len(sys.argv) < NUM_ARGS):
        print "ERROR: Incorrect number of arguments. See usage."
        print_usage()
        exit()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hab:", \
                ["help", "aggregate-counts"])
    except getopt.GetoptError as err:
        print "ERROR: %s. See usage." % (err)
        print_usage()
        exit()
    for opt, arg in opts:
        if (opt in ("-h", "--help")):
            print_usage()
            exit()
        elif (opt in ("-a", "--aggregate-counts")):
            g_gadget_obfusc_path = GADGET_PATH + BIN_TYPE_OBFUSC + "/"
            g_gadget_unobfusc_path = GADGET_PATH + BIN_TYPE_UNOBFUSC + "/"
        elif (opt in ("-b", "--binary-file")):
            g_bin_flag = True
            g_gadget_obfusc_path = GADGET_PATH + BIN_TYPE_OBFUSC + "/"
            g_gadget_unobfusc_path = GADGET_PATH + BIN_TYPE_UNOBFUSC + "/"
            g_bin_file_name = str(arg)

            bin_file_path = g_gadget_unobfusc_path + \
                    g_bin_file_name + ".gdt.cnt"
            if (False == (os.path.isfile(bin_file_path))):
                print "ERROR: Unobfuscated gadget count file for given binary is invalid. See usage."
                print_usage()
                exit()
            if (False == (os.access(bin_file_path, os.R_OK))):
                print "ERROR: Unobfuscated gadget count file for given binary is not readable. See usage."
                print_usage()
                exit()

            bin_file_path = g_gadget_unobfusc_path + \
                    g_bin_file_name + ".gdt.cnt"
            if (False == (os.path.isfile(bin_file_path))):
                print "ERROR: Obfuscated gadget count file for given binary is invalid. See usage."
                print_usage()
                exit()
            if (False == (os.access(bin_file_path, os.R_OK))):
                print "ERROR: Obfuscated gadget count file for given binary is not readable. See usage."
                print_usage()
                exit()

        else:
            print "ERROR: Incorrect argument. See usage."
            print_usage()
            exit()
    return


#
# Name: aggregate_gadgets
# Desc: Aggregates the category count of gadgets to a global running sum. For
#       every line read in the "*.gdt.cnt" file, this routine categorizes the
#       lines based on the keywords (total, memory, arith, logic, control flow
#       and others) and adds it to the running sum in respective globals.
# Args: gadget_name (gadget counters file name)
#
def aggregate_gadgets(gadget_file):
    global g_cat_total, g_cat_memory, g_cat_arith, g_cat_logic, \
            g_cat_ctrl, g_cat_others
    
    fr_gadget = open(gadget_file, "r")
    print "Aggregating gadgets for file %s" %(gadget_file)
    
    for each_line in fr_gadget:
        each_line = each_line.strip()
        if STR_TOTAL in each_line:
            tmp = str(each_line[each_line.index(':') + 1: len(each_line)])
            tmp = tmp.lstrip()
            g_cat_total += int(tmp)
        elif STR_MEMORY in each_line:
            tmp = str(each_line[each_line.index(':') + 1: len(each_line)])
            tmp = tmp.lstrip()
            g_cat_memory += int(tmp)
        elif STR_ARITH in each_line:
            tmp = str(each_line[each_line.index(':') + 1: len(each_line)])
            tmp = tmp.lstrip()
            g_cat_arith += int(tmp)
        elif STR_LOGIC in each_line:
            tmp = str(each_line[each_line.index(':') + 1: len(each_line)])
            tmp = tmp.lstrip()
            g_cat_logic += int(tmp)
        elif STR_CTRL in each_line:
            tmp = str(each_line[each_line.index(':') + 1: len(each_line)])
            tmp = tmp.lstrip()
            g_cat_ctrl += int(tmp)
        elif STR_OTHERS in each_line:
            tmp = str(each_line[each_line.index(':') + 1: len(each_line)])
            tmp = tmp.lstrip()
            g_cat_others += int(tmp)

    fr_gadget.close()
    return


#
# Name: main
# Desc: Main routine for this script. 
# Args: argv (user passed data)
#
def main(argv):
    global g_cat_total, g_cat_memory, g_cat_arith, g_cat_logic, \
            g_cat_ctrl, g_cat_others

    num_gadgets = 0
    start_time = time.time()
    validate_args()

    if (g_bin_flag):
        bin_data_file_name = g_bin_file_name + ".dat"
        fw_data = open(DATA_PATH + bin_data_file_name, "w")
        fw_data.write("Aggregated gadget counts for unobfuscated and obfuscated \"%s\" binary" \
                % (g_bin_file_name))
    else:
        fw_data = open(DATA_PATH + DATA_FILE, "w")
        fw_data.write("Aggregated gadget counts for unobfuscated and obfuscated coreutils binaries")

    # Write table headers
    fw_data.write("\n")
    fw_data.write("gadget/category\t\t%7s\t\t%7s\t\t%7s\t\t%7s\t\t%7s\t\t%7s" \
            % ("total", "memory", "arith", "logic", "ctrl", "other"))
    fw_data.write("\n")

    if (g_bin_flag):
        # Write 'unobfuscated' binaries' data in row 1
        fw_data.write("unobfuscated\t\t")
        print "Aggregating unobfuscated \"%s\" binary's gadgets.." \
                % (g_bin_file_name)
        print " "
        aggregate_gadgets(g_gadget_unobfusc_path + g_bin_file_name + ".gdt.cnt")
        fw_data.write("%7u\t\t%7u\t\t%7u\t\t%7u\t\t%7u\t\t%7u" \
            % (g_cat_total, g_cat_memory, g_cat_arith, g_cat_logic, \
            g_cat_ctrl, g_cat_others))
        fw_data.write("\n")
        g_cat_total = g_cat_memory = g_cat_arith = \
            g_cat_logic = g_cat_ctrl = g_cat_others = 0
        print "Aggregated data file location: %s" \
                % (g_gadget_unobfusc_path + g_bin_file_name + ".dat")

        # Write 'obfuscated' binaries' data in row 2
        fw_data.write("obfuscated\t\t")
        print "Aggregating obfuscated \"%s\" binary's gadgets.." \
                % (g_bin_file_name)
        print " "
        aggregate_gadgets(g_gadget_obfusc_path + g_bin_file_name + ".gdt.cnt")
        fw_data.write("%7u\t\t%7u\t\t%7u\t\t%7u\t\t%7u\t\t%7u" \
            % (g_cat_total, g_cat_memory, g_cat_arith, g_cat_logic, \
            g_cat_ctrl, g_cat_others))
        fw_data.write("\n")
        g_cat_total = g_cat_memory = g_cat_arith = \
            g_cat_logic = g_cat_ctrl = g_cat_others = 0
        print "Aggregated gadget count data file location: %s" \
                % (DATA_PATH + g_bin_file_name + ".dat")
    else:
        num_gadgets = 0
        fw_data.write("unobfuscated\t\t")
        print "Aggregating unobfuscated binaries' gadgets.."
        print " "

        # Go over all unobfuscated gdt.cnt files in the directory and aggregate
        for each_gadget_file in os.listdir(g_gadget_unobfusc_path):
            if each_gadget_file.endswith(".cnt"):
                num_gadgets += 1
                aggregate_gadgets(g_gadget_unobfusc_path + each_gadget_file)

        fw_data.write("%7u\t\t%7u\t\t%7u\t\t%7u\t\t%7u\t\t%7u" \
            % (g_cat_total, g_cat_memory, g_cat_arith, g_cat_logic, \
            g_cat_ctrl, g_cat_others))
        fw_data.write("\n")
        g_cat_total = g_cat_memory = g_cat_arith = \
            g_cat_logic = g_cat_ctrl = g_cat_others = 0
        print "Aggregated %u unobfuscated binaries' gadgets." % (num_gadgets)


        # Write 'obfuscated' binaries' data in row 2
        num_gadgets = 0
        fw_data.write("obfuscated\t\t")
        print "Aggregating obfuscated binaries' gadgets.."
        print " "

        # Go over all obfuscated gdt.cnt files in the directory and aggregate
        for each_gadget_file in os.listdir(g_gadget_obfusc_path):
            if each_gadget_file.endswith(".cnt"):
                num_gadgets += 1
                aggregate_gadgets(g_gadget_obfusc_path + each_gadget_file)

        fw_data.write("%7u\t\t%7u\t\t%7u\t\t%7u\t\t%7u\t\t%7u" \
            % (g_cat_total, g_cat_memory, g_cat_arith, g_cat_logic, \
            g_cat_ctrl, g_cat_others))
        fw_data.write("\n")
        g_cat_total = g_cat_memory = g_cat_arith = \
                g_cat_logic = g_cat_ctrl = g_cat_others = 0
        print "Aggregated %u obfuscated binaries' gadgets." % (num_gadgets)
        print " "
        print "Aggregated gadget count data file location: %s" \
                % (DATA_PATH + DATA_FILE)

    fw_data.close()

    end_time = time.time()
    exec_seconds = (end_time - start_time)
    m,s = divmod(exec_seconds, 60)
    h, m = divmod(m, 60)
    print "Total time taken: %02uh %02um %02us" % (h, m, s)


# Init code
if __name__ == "__main__":
    main(sys.argv)

