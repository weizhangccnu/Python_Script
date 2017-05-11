set term postscript eps enhanced color dl 2.0 lw 1.5 "Helvetica" 18 
set output "fft_result.eps"
set multiplot layout 1,2 
set origin 0,0
set size 1.0,0.5
set xrange [0:50]
unset yrange
set yrange [0:1]
set xlabel "Frequency [Hz]"
set ylabel "Voltage [V]"
set title ""
plot "./fft_result.dat" u 1:2 w p ps 1 pt 3 lw 2 lt 1 lc 3 t''
set origin 0,0.5
set size 0.983,0.5
set xrange[0:50]
set yrange [-180:180]
set ytics 90
set ylabel "Phase [{/Symbol \260}]"
unset xlabel
plot "./fft_result.dat" u 1:3 w p ps 1 pt 3 lw 2 lt 1 lc 1 t''
unset multiplot
unset output
