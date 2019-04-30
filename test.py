import sys, subprocess, serial, csv
import os,glob
import datetime as time
from PyQt5 import QtWidgets


result = []
# subprocess.run("chmod 666 /dev/ttyUSB0")
def serial_ports():
   if sys.platform.startswith('win'):
       ports = ['COM%s' % (i + 1) for i in range(256)]
   elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
       # this excludes your current terminal "/dev/tty"
       ports = glob.glob('/dev/tty[A-Za-z]*')
   elif sys.platform.startswith('darwin'):
       ports = glob.glob('/dev/tty.*')
   else:
       raise EnvironmentError('Unsupported platform')

   for port in ports:
       try:
           s = serial.Serial(port)
           s.close()
           result.append(port)
       except (OSError, serial.SerialException):
           pass
   return result



def admin():
    serial_ports()
    returned = os.popen("sudo chmod 666 "+result[0]).readline()
    print(returned)

admin()
ser = serial.Serial(result[0], 2400, timeout=2)


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
