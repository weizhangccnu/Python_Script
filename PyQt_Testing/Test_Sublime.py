#!/usr/bin/python
# -*- coding: utf-8 -*-
import os 
import sys
import time
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#-------------------------------------------------------------#
def Test_PyQt4():
	app = QtGui.QApplication(sys.argv)
	w = QtGui.QWidget()
	w.resize(450, 350)
	w.move(200, 200)
	w.setWindowTitle('Menu')
	w.show()
	#time.sleep(1)
	#w.close()
	sys.exit(app.exec_())
#-------------------------------------------------------------#
def Window():
	app = QApplication(sys.argv)	
	win = QDialog()
	b1 = QPushButton(win)
	b1.setText("Button1")
	b1.move(100, 20)
	b1.clicked.connect(b1_clicked)

	b2 = QPushButton(win)
	b2.setText("Button2")
	b2.move(100, 70)
	QObject.connect(b2, SIGNAL("clicked()"), b2_clicked)

	win.setGeometry(200,200,300,300)
	win.setWindowTitle("PyQt_Test")
	win.show()
	sys.exit(app.exec_())
#-------------------------------------------------------------#
def b1_clicked():
	print "Button 1 clicked"
#-------------------------------------------------------------#
def b2_clicked():
	print "Button 2 clicked"
#-------------------------------------------------------------#
## Print_String function
def Print_String():
	for i in xrange(1000):
		print i, "you are my sunshine!"
		time.sleep(0.001)
#-------------------------------------------------------------#
## Main function
def main():
	Print_String()
	#Test_PyQt4()
	Window()	
#-------------------------------------------------------------#
##execute main function
if __name__ == '__main__':
	#sys.exit(main())
	main()
