./TMS1mmSingleCSAOut1.gp                #execute gnuplot file
eps2png -resolution 400 h5_output.eps   #convert eps file to png
xdg-open h5_output.png                  #invoke xdg-open command open .png file
echo "OK"
