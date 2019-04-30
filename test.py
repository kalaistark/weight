import sys, subprocess, serial, csv
import os
import datetime as time
from PyQt5 import QtWidgets

port = "/dev/ttyUSB0"

# subprocess.run("chmod 666 /dev/ttyUSB0")
returned = os.popen("sudo chmod 666 /dev/ttyUSB0").readline()
print(returned)

ser = serial.Serial("/dev/ttyUSB0", 2400, timeout=2)


#dmesg | grep tty -- to list serial ports in linux
# sudo chmod 666 /dev/ttyUSB0)

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.l = QtWidgets.QLabel("Weight")
        self.btn = QtWidgets.QPushButton("Get Weight")
        self.init_ui()

    def init_ui(self):
        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.l)
        h_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addWidget(self.btn)

        self.setLayout(v_box)

        self.setWindowTitle("Weight App")
        self.resize(500, 300)

        self.btn.clicked.connect(self.get_weight)

        self.show()

    def get_weight(self):
        csv = open("weightdata.csv","a")
        ser.flushOutput()
        bytesToRead = ser.inWaiting()
        v= str(ser.read(bytesToRead))
        x = v.split(" ")
        a = x[-3]
        if len(a) == 0:
            print(x[-2])
            x = (x[-2])[11:]
            csv.write(x + "kg" + " time:" + str(time.datetime.now())+ "\n")
            self.l.setText(x)
        else:
            #print(x[-3:])
            print((x[-3])[11:])
            y = (x[-3])[11:]
            csv.write(y +" kg" + " time:" + str(time.datetime.now())+ "\n")
            self.l.setText(x[-3][11:]+" kg")

app = QtWidgets.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())
