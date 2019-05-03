import sys, subprocess, serial, csv
import os,glob
import datetime as time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QSplitter, QStyleFactory, QFrame, QComboBox, QMessageBox, QGridLayout, QLayout, QGroupBox
#------------------------------------------info---------------------------------------------------------
# subprocess.run("chmod 666 /dev/ttyUSB0")
#dmesg | grep tty -- to list serial ports in linux
# sudo chmod 666 /dev/ttyUSB0)
#-----------------------------------------variables ----------------------------------------------------
result = []
selected = ""
#--------------------------------------initialisation---------------------------------------------------
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
#----------------------------------------------------------------
def admin(password):
    serial_ports()
    command = "sudo chmod 666 "+result[0]
    p = os.system('echo %s|sudo -S %s' % (password, command))
#---------------------------------------GUI Initialisation-----------------------------------------------
class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.l = QLabel("Weight")
        self.l1 = QLabel("select the Port")
        self.btn = QPushButton("Get Weight")
        self.flag = False
        self.init_ui()
        
    def init_ui(self):
        h_box_main = QHBoxLayout()

        self.combo = QComboBox(self)
        for i in result:
            self.combo.addItem(i)

        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.l)
        h_box.addStretch()

        h_box1 = QHBoxLayout()
        h_box1.addStretch()
        h_box1.addWidget(self.combo)
        h_box1.addStretch()

        h_box11 = QHBoxLayout()
        h_box11.addStretch()
        h_box11.addWidget(self.l1)
        h_box11.addStretch()

        h_box2 = QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.btn)
        h_box2.addStretch()

        v_box = QVBoxLayout()
        v_box.addLayout(h_box11)
        v_box.addLayout(h_box1)

        top_left = QFrame(self)
        top_left.setFrameShape(QFrame.StyledPanel)
        # top_left.setFixedSize(240,150)
        top_left.setLayout(v_box)

        top_right = QFrame(self)
        top_right.setFrameShape(QFrame.StyledPanel)
        top_right.setLayout(h_box)
        bottom = QFrame(self)
        bottom.setFrameShape(QFrame.StyledPanel)
        bottom.setLayout(h_box2)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(top_left)
        splitter1.addWidget(top_right)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        h_box_main.addWidget(splitter2)
        self.setLayout(h_box_main)

        self.setLayout(h_box_main)

        self.setWindowTitle("Weight App")
        self.setFixedSize(500, 300)

        self.btn.clicked.connect(self.portSelection)
        self.combo.activated.connect(self.comboActivated)

        self.show()
      
    def portSelection(self):
        if(self.flag):
            self.get_weight()
        else:
            self.l.setText("select the port")

    
    def comboActivated(self):
        selected = self.combo.currentText()
        self.ser = serial.Serial(selected, 2400, timeout=2)
        self.flag = True

    def get_weight(self):
        csv = open("weightdata.csv","a")
        self.ser.flushOutput()
        bytesToRead = self.ser.inWaiting()
        v= str(self.ser.read(bytesToRead))
        x = v.split(" ")
        try:
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
        except:
            pass
#----------------------------------------------------------------
class PreWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.l = QLabel("Enter Password")
        self.le = QLineEdit()
        self.button = QPushButton("Done")
        self.home()
    
    def home(self):
        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.l)
        h_box.addStretch()

        h_box1 = QHBoxLayout()
        h_box1.addStretch()
        h_box1.addWidget(self.le)
        h_box1.addStretch()

        h_box2 = QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.button)
        h_box2.addStretch()

        v_box = QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addLayout(h_box1)
        v_box.addLayout(h_box2)

        self.setLayout(v_box)

        self.button.clicked.connect(self.get_pwd)

        self.show()

    def nextWindow(self):
        self.close()
        self.next = Window()
    
    def get_pwd(self):
        password = self.le.text()
        admin(password)
        self.close()
        self.nw = Window()
        self.nw.show()

#-------------------------------------------Main----------------------------------------------------
serial_ports()
app = QApplication(sys.argv)
a_window = PreWindow()
# b_window = Window()
sys.exit(app.exec_())

    

