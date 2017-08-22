#!/usr/bin/gnuplot 
set terminal postscript eps enhanced color dl 2.0 lw 1.5 "Helvetica" 12
set title "1000000 sapmle point recovered waveform" font ",15"
set output "./h5_output.eps"
set xlabel "Sample point" font ",14"
set ylabel "hdf5 stored number" font ",14"
plot './h5_output.dat' u ($0):1 w l t'' 
#--------------------------------------------------------------------------#
unset output
