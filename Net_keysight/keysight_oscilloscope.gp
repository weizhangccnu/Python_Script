set terminal postscript eps enhanced color dl 2.0 lw 1.0  "Helvetica" 18
set output "./keysight_oscilloscope.eps"
#--------------------------------------------------------------------------#
set grid
set title "KEYSIGHT DSOS054A 500MHz 20GSa/s 10-bit ADC" offset 0,-0.8 font ",15"
set object rectangle from screen 0,0 to screen 1,1 behind fillcolor rgb '#b3b3b3' fillstyle solid noborder
#set yrange[-40000:40000]
#set yrange[-32768:32768]
set mxtics 5 
set mytics 5
set xlabel "Time [ms]" 
set ylabel "Voltage [V]" 
plot './data_output.dat' u 1:2 w l lc 1 t'' 
#--------------------------------------------------------------------------#
unset multiplot
unset output
