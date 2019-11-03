## This Readme file introduces how to develope a Qt GUI program.

### 1. Install PyQt5 developement tools at Windows docs command line or Linux terminal with the command as below.
```python
pip install Pyqt5-tools
```
### 2. Lanuch *Qt Designer* application and develope your GUI. The **Qt Designer** application picture is shown as below figure.
![Qt Desiger GUI](https://github.com/weizhangccnu/Python_Script/blob/master/PyQt_Testing/Img/QT_Designer_GUI.PNG)
  - According to your requirement, you can develope your GUI freely and save file with name `xxx.ui`.

### 3. Convert `xxx.ui` file into `xxx.py` file with the command `pyuic5 -x xxx.ui -o xxx.py`
  - The script `pyuic5` locates in the directroy of `./Python/Python37/Scripts`
