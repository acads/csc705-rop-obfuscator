#
# File: chroot.gp
# Desc: Obfuscated vs unobfuscated categorized ROP gadget count GNUplot graph 
#       file for chroot binary.
#
# Author: Aravindhan Dhanasekaran <adhanas@ncsu.edu>
#

clear
reset

set terminal postscript eps enhanced dashed
set output 'chroot.eps'

set title 'chroot: Categorized ROP Gadget Count for Unobfuscated and Obfuscated chroot Binary'
set key left top

set ylabel 'Number of Unique Gadgets'
set xlabel 'Gadget Categories'
set xtics rotate by -45

set style data histogram
set style histogram clustered gap 1
set style fill pattern border 0

plot for [COL=2:3] 'chroot.gp.dat' using COL:xticlabels(1) title columnheader fs pattern 2

reset

