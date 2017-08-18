#!/usr/bin/gnuplot 
set terminal postscript eps enhanced color dl 2.0 lw 1.5 "Helvetica" 12
set output "./keysight_oscilloscope.eps"
#--------------------------------------------------------------------------#
set grid xtics y2tics front lw 1.5  lc rgb "0xffffff" 
set title "KEYSIGHT DSOS054A 500MHz 20GSa/s 10-bit ADC CH1" offset 0,-0.3 font ",15"
set object 1 rectangle from graph 0,0 to graph 1,1 back fillcolor rgb '#333333' fillstyle solid noborder
#set object 2 rectangle from screen 0,0 to screen 1,1 back fillcolor rgb '#cccccc' fillstyle solid noborder
set y2range [-y_var:y_var]
set y2tics 2*y_var/8.0
print y_var
print offset
print (-y_var+offset),(y_var-offset)
set xrange [-x_var:x_var]
set xtics 2*x_var/10.0

set ytics nomirror
unset yrange
unset ytics
set yzeroaxis 
set mxtics 10 
set y2tics
set my2tics 10
set mytics 5
set xlabel "Time [ms]" font "Helvetica,15"  
set y2label "Voltage [V]" font "Helvetica,15"
plot './data_output.dat' u 1:2 w l axes x1y2 lw 0.5 lc 6 t'' 
#--------------------------------------------------------------------------#
unset multiplot
unset output
