#
# File: coretutils-aggregate.gp
# Desc: Obfuscated vs unobfuscated categorized ROP gadget count GNUplot graph 
#       file for all coreutils binaries.
#
# Author: Aravindhan Dhanasekaran <adhanas@ncsu.edu>
#

clear
reset

set terminal postscript eps enhanced dashed
set output 'coretutils-aggregate.eps'

set title 'coreutils: Categorized ROP Gadget Count for Unobfuscated and Obfuscated coreutils Binaries'
set key left top

set ylabel 'Number of Unique Gadgets'
set xlabel 'Gadget Categories'
set xtics rotate by -45

set style data histogram
set style histogram clustered gap 1
set style fill pattern border 0

plot for [COL=2:3] 'coretutils-aggregate.gp.dat' using COL:xticlabels(1) title columnheader fs pattern 2

reset

