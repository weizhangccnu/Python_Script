set terminal postscript eps enhanced color dl 2.0 lw 1.5  "Helvetica" 18
set output "./keysight_oscilloscope.eps"
#--------------------------------------------------------------------------#
set grid
set yrange[-32768:32768]
set xlabel "Time [ms]" 
set ylabel "Voltage [V]" 
plot './data_output.dat' u ((($1)-10000000/2.0)/10000000.0):2 w l t'' 
#--------------------------------------------------------------------------#
unset multiplot
unset output
