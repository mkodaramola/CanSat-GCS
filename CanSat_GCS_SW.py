import sys
from PyQt5.QtWidgets import QApplication, QWidget,QInputDialog ,QComboBox,QScrollArea ,QTimeEdit,QVBoxLayout, QFrame, QHBoxLayout, QGridLayout,QLabel,QLineEdit, QPushButton,QTextEdit,QTableWidget, QTableWidgetItem
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
import time
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import serial
from PyQt5.QtGui import QPixmap
from datetime import datetime

PACKET_COUNT = 2
ALTITUDE = 5
AIR_SPEED = 6
TEMPERATURE = 9
VOLTAGE = 10
PRESSURE = 11
TILT_X = 12
TILT_Y = 13 
ROT_Z = 14


arduinoData_string = ""

current_image_index = 0
image_path = "dotu.jpg"


# Create the Qt application
app = QApplication(sys.argv)

# Create the main window
window = QWidget()
window.setWindowTitle('CanSat FUTA | 2082')
#window.setStyleSheet("background-color: rgb(245,245,255);")
window.setStyleSheet(f"background-image: url({image_path});")

port_not_Ready = True


while port_not_Ready:
    port, ok = QInputDialog.getText(None, 'CanSat FUTA', 'Enter XBEE Port Number:')
    if ok and port.isdigit():
        port = f"COM{port}"
        try:
            ser = serial.Serial(port,9600)
            time.sleep(1)
        except:
            continue
        port_not_Ready = False
    else:
        continue


# ser = serial.Serial(port,9600)
# time.sleep(1)


tel_data = ""

x_data = []
temperatureY_data = []
altitudeY_data = []
airspeedY_data = []
voltageY_data = []
pressureY_data = []
tiltxY_data = []	
tiltyY_data = []
rotzY_data = []




main_layout = QVBoxLayout()

#content_layout = QStackedWidget()


scroll_area = QScrollArea()

widget = QWidget()

# Create a QGridLayout
layout = QGridLayout()
widget.setLayout(layout)


# Create the plot items
plot_widget_AirSp = pg.GraphicsLayoutWidget()
plot_widget_AirSp.setFixedSize(300, 150)
plot_item_AirSp = plot_widget_AirSp.addPlot(title="Air Speed")
#plot_item_AirSp.getViewBox().setBackgroundColor('w')
plot_item_AirSp.setTitle('Air Speed', color='w')
plot_item_AirSp.getAxis('bottom').setLabel('Packet_count', color='w')
plot_item_AirSp.getAxis('left').setLabel('AirSpeed (m/s)', color='w')
plot_item_AirSp.getAxis('bottom').setPen(color='w')
plot_item_AirSp.getAxis('left').setPen(color='w')
plot_item_AirSp.getAxis('bottom').setTextPen(color='w')
plot_item_AirSp.getAxis('left').setTextPen(color='w')
plot_item_AirSp.getViewBox().setBackgroundColor('w')
plot_curve_AirSp = plot_item_AirSp.plot([], [], pen='k')

plot_widget_pressure = pg.GraphicsLayoutWidget()
plot_widget_pressure.setFixedSize(300, 150)
plot_item_pressure = plot_widget_pressure.addPlot(title="Pressure")
plot_item_pressure.setTitle('Pressure', color='w')
plot_item_pressure.getAxis('bottom').setLabel('Packet_count', color='w')
plot_item_pressure.getAxis('left').setLabel('Pressure (kPa)', color='w')
plot_item_pressure.getAxis('bottom').setPen(color='w')
plot_item_pressure.getAxis('left').setPen(color='w')
plot_item_pressure.getAxis('bottom').setTextPen(color='w')
plot_item_pressure.getAxis('left').setTextPen(color='w')
plot_item_pressure.getViewBox().setBackgroundColor('w')
plot_curve_pressure = plot_item_pressure.plot([], [], pen='k')



# Code for plot_widget_Altitude
plot_widget_Altitude = pg.GraphicsLayoutWidget()
plot_widget_Altitude.setFixedSize(300, 150)
plot_item_Altitude = plot_widget_Altitude.addPlot(title="Altitude")
plot_item_Altitude.setLabel('bottom', 'Packet_count')
plot_item_Altitude.setLabel('left', 'Altitude (m)')
plot_item_Altitude.setTitle('Altitude', color='w')

plot_item_Altitude.getAxis('left').setPen(color='w')

plot_item_Altitude.getAxis('bottom').setTextPen(color='w')

plot_item_Altitude.getAxis('left').setTextPen(color='w')

plot_item_Altitude.getViewBox().setBackgroundColor('w')

plot_curve_Altitude = plot_item_Altitude.plot([], [], pen='k')

# Code for plot_widget_temp
plot_widget_temp = pg.GraphicsLayoutWidget()
plot_widget_temp.setFixedSize(300, 150)
plot_item_temp = plot_widget_temp.addPlot(title="Temperature")
plot_item_temp.setLabel('bottom', 'Packet_count')
plot_item_temp.setLabel('left', 'Temperature (degree)')
plot_item_temp.setTitle('Temperature', color='w')
plot_item_temp.getAxis('bottom').setPen(color='w')
plot_item_temp.getAxis('left').setPen(color='w')
plot_item_temp.getAxis('bottom').setTextPen(color='w')
plot_item_temp.getAxis('left').setTextPen(color='w')
plot_item_temp.getViewBox().setBackgroundColor('w')
plot_curve_temp = plot_item_temp.plot([], [], pen='k')




# Code for plot_widget_TiltX (similar adjustments)
plot_widget_TiltX = pg.GraphicsLayoutWidget()
plot_widget_TiltX.setFixedSize(300, 150)
plot_item_TiltX = plot_widget_TiltX.addPlot(title="Tilt X (AccelerometerX)")
plot_item_TiltX.setLabel('bottom', 'Time (s)')
plot_item_TiltX.setLabel('left', 'TiltX (degrees)')
plot_item_TiltX.setTitle('Tilt X (AccelerometerX)', color='w')
plot_item_TiltX.getAxis('bottom').setPen(color='w')
plot_item_TiltX.getAxis('left').setPen(color='w')
plot_item_TiltX.getAxis('bottom').setTextPen(color='w')
plot_item_TiltX.getAxis('left').setTextPen(color='w')
plot_item_TiltX.getViewBox().setBackgroundColor('w')
plot_curve_TiltX = plot_item_TiltX.plot([], [], pen='k')

# Code for plot_widget_TiltY (similar adjustments)
plot_widget_TiltY = pg.GraphicsLayoutWidget()
plot_widget_TiltY.setFixedSize(300, 150)
plot_item_TiltY = plot_widget_TiltY.addPlot(title="Tilt Y (AccelerometerY)")
plot_item_TiltY.setLabel('bottom', 'Time (s)')
plot_item_TiltY.setLabel('left', 'TiltY (degrees)')
plot_item_TiltY.setTitle('Tilt Y (AccelerometerY)', color='w')
plot_item_TiltY.getAxis('bottom').setPen(color='w')
plot_item_TiltY.getAxis('left').setPen(color='w')
plot_item_TiltY.getAxis('bottom').setTextPen(color='w')
plot_item_TiltY.getAxis('left').setTextPen(color='w')
plot_item_TiltY.getViewBox().setBackgroundColor('w')
plot_curve_TiltY = plot_item_TiltY.plot([], [], pen='k')

# Code for plot_widget_RotZ (similar adjustments)
plot_widget_RotZ = pg.GraphicsLayoutWidget()
plot_widget_RotZ.setFixedSize(300, 150)
plot_item_RotZ = plot_widget_RotZ.addPlot(title="Rotation Z (AccelerometerZ)")
plot_item_RotZ.setLabel('bottom', 'Time (s)')
plot_item_RotZ.setLabel('left', 'RotZ (degrees/sec)')
plot_item_RotZ.setTitle('Rotation Z (AccelerometerZ)', color='w')
plot_item_RotZ.getAxis('bottom').setPen(color='w')
plot_item_RotZ.getAxis('left').setPen(color='w')
plot_item_RotZ.getAxis('bottom').setTextPen(color='w')
plot_item_RotZ.getAxis('left').setTextPen(color='w')
plot_curve_RotZ = plot_item_RotZ.plot([], [], pen='k')

# Code for plot_widget_Voltage (similar adjustments)
plot_widget_Voltage = pg.GraphicsLayoutWidget()
plot_widget_Voltage.setFixedSize(300, 150)
plot_item_Voltage = plot_widget_Voltage.addPlot(title="Battery Voltage")
plot_item_Voltage.setLabel('bottom', 'Time (s)')
plot_item_Voltage.setLabel('left', 'Battery Voltage (Volts)')
plot_item_Voltage.setTitle('Battery Voltage', color='w')
plot_item_Voltage.getAxis('bottom').setPen(color='w')
plot_item_Voltage.getAxis('left').setPen(color='w')
plot_item_Voltage.getAxis('bottom').setTextPen(color='w')
plot_item_Voltage.getAxis('left').setTextPen(color='w')
plot_item_Voltage.getViewBox().setBackgroundColor('w')
plot_curve_Voltage = plot_item_Voltage.plot([], [], pen='k')


# Create the main QTableWidget for overwritten data
table_widget = QTableWidget()
table_widget.setColumnCount(15)
table_widget.setFixedSize(900, 70) 
table_widget.setHorizontalHeaderLabels(["TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE", "SPEED", "HS_DEPLOYED", "PC_DEPLOYED", "TEMPERATURE", "VOLTAGE", "PRESSURE", "TILT_X", "TILT_Y", "ROT_Z"])
font = table_widget.font()
font.setBold(True)
table_widget.setFont(font)
table_widget.setMinimumWidth(200)



# Create the appended QTableWidget
table_widget_appended = QTableWidget()
table_widget_appended.setColumnCount(15)
table_widget_appended.setFixedSize(900, 350)
table_widget_appended.setHorizontalHeaderLabels(["TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "MODE", "STATE", "ALTITUDE", "SPEED", "HS_DEPLOYED", "PC_DEPLOYED", "TEMPERATURE", "VOLTAGE", "PRESSURE","TILT_X", "TILT_Y", "ROT_Z",])
font2 = table_widget.font()
font2.setBold(True)
table_widget_appended.setFont(font2)
table_widget_appended.setMinimumWidth(200)



# Function to populate the overwritten table with data
def update_table(data):
    fields = data.split(',')
    table_widget.setRowCount(1)
    for i, field in enumerate(fields):
        table_widget.setItem(0, i, QTableWidgetItem(field))

num_columns = table_widget.columnCount()
adjCol = [0,3,4,5,6,10,11,12,16,17,18,19,21]
# Set the width for all columns
for col in range(num_columns):
    if col in adjCol:
        table_widget.setColumnWidth(col, 65)
    else:
        pass

    

# Function to append data to the appended table
def append_to_table(data):
    fields = data.split(',')
    row_position = table_widget_appended.rowCount()
    table_widget_appended.insertRow(row_position)
    for i, field in enumerate(fields):
        table_widget_appended.setItem(row_position, i, QTableWidgetItem(field))

# Set the width for all columns
for col in range(num_columns):
    if col in adjCol:
        table_widget_appended.setColumnWidth(col, 65)
    else:
        pass



# Update the table with initial data
update_table(tel_data)
append_to_table(tel_data)



def keyPressEvent(event):
    if event.modifiers() == Qt.ControlModifier:
        if event.key() == Qt.Key_1:
            # Scroll to horizontal level 1
            scroll_area.horizontalScrollBar().setValue(0)  # Adjust the value as needed
            scroll_area.verticalScrollBar().setValue(0)
        elif event.key() == Qt.Key_2:
            # Scroll to horizontal level 2
            scroll_area.horizontalScrollBar().setValue(0)  # Adjust the value as needed
            scroll_area.verticalScrollBar().setValue(680)
        # elif event.key() == Qt.Key_3:
        #     # Scroll to vertical level 1
        #     scroll_area.verticalScrollBar().setValue(800)  # Adjust the value as needed
            scroll_area.horizontalScrollBar().setValue(0)
        elif event.key() == Qt.Key_3:
            # Scroll to vertical level 2
            scroll_area.verticalScrollBar().setValue(1500)  # Adjust the value as needed
            scroll_area.horizontalScrollBar().setValue(0)
    else:
        pass




# Create Label
LBTname = QLabel("CanSat FUTA")
LBTname.setStyleSheet("color: #FFA500; background-color: white; font-size: 35px; font-weight: bold;")
LBTname.setAlignment(QtCore.Qt.AlignCenter)

LBtelBox = QLabel('Telemetry')
LBtelBox.setStyleSheet("color: black; font-size: 25px; font-weight: bold;")

tel = QTextEdit()
tel.setStyleSheet("color: black; background-color: rgb(250,250,250); font-size: 11px;")
tel.setFixedWidth(500)  # Set the width to 200 pixels
tel.setFixedHeight(300) 
tel.setReadOnly(True)
tel.append("")

LBtel = QLabel('Telemetry [ON/OFF]')
LBtel.setStyleSheet("color: black; font-size: 15px; font-weight: bold;")

LBsimE = QLabel('Simulation Mode [ENABLE/DISABLE]')
LBsimE.setStyleSheet("color: black; font-size: 15px; font-weight: bold;")

LBsimA = QLabel('Simulation Mode [ACTIVATE/DIACTIVATE]')
LBsimA.setStyleSheet("color: black; font-size: 15px; font-weight: bold;")

LBtime = QLabel('Set Time')
LBtime.setStyleSheet("color: black; font-size: 15px; font-weight: bold;")

LBsimp = QLabel('Simulated Pressure Data')
LBsimp.setStyleSheet("color: black; font-size: 15px; font-weight: bold;")

LBCAL = QLabel('Calibration')
LBCAL.setStyleSheet("color: black; font-size: 15px; font-weight: bold;")

LBBCN = QLabel('Audio Beacon')
LBBCN.setStyleSheet("color: black; font-size: 15px; font-weight: bold;")


label1 = QLabel('           ')
label1.setStyleSheet("color: black; font-size: 25px; font-weight: bold;")




LBImage = QLabel()
LBImage.setFixedSize(300,300)
#LBImage.setStyleSheet("QLabel { padding: 20px; border: 1px solid black; }") 

LBLogo = QLabel()
LBLogo.setFixedSize(50,50)
Lpixmap = QPixmap()
LBLogo.setPixmap(Lpixmap)






# Create the button
bTel = QPushButton('Send')
bTel.setCheckable(True)
bTel.setChecked(False)
bTel.setFixedWidth(50) 
bTel.setFixedHeight(30)
bTel.setStyleSheet("background-color: lightgreen;")

bTime = QPushButton('Send')
bTime.setCheckable(True)
bTime.setChecked(False)
bTime.setFixedWidth(50) 
bTime.setFixedHeight(30)
bTime.setStyleSheet("background-color: lightgreen;")

bSimE = QPushButton('Send')
bSimE.setCheckable(True)
bSimE.setChecked(False)
bSimE.setFixedWidth(50) 
bSimE.setFixedHeight(30)
bSimE.setStyleSheet("background-color: lightgreen;")

bSimA = QPushButton('Send')
bSimA.setCheckable(True)
bSimA.setChecked(False)
bSimA.setFixedWidth(50) 
bSimA.setFixedHeight(30)
bSimA.setStyleSheet("background-color: lightgreen;")

bSimp = QPushButton('Send')
bSimp.setCheckable(True)
bSimp.setChecked(False)
bSimp.setFixedWidth(50) 
bSimp.setFixedHeight(30)
bSimp.setStyleSheet("background-color: lightgreen;")

bCAL = QPushButton('Send')
bCAL.setCheckable(True)
bCAL.setChecked(False)
bCAL.setFixedWidth(50) 
bCAL.setFixedHeight(30)
bCAL.setStyleSheet("background-color: lightgreen;")

bBCN = QPushButton('Send')
bBCN.setCheckable(True)
bBCN.setChecked(False)
bBCN.setFixedWidth(50) 
bBCN.setFixedHeight(30)
bBCN.setStyleSheet("background-color: lightgreen;")



def sim_E_D():
    simEVal = simE_cmd.currentText()
    print(simEVal)
bSimE.clicked.connect(sim_E_D)

def sim_A_D():
    simAVal = simA_cmd.currentText()
    print(simAVal)
bSimA.clicked.connect(sim_A_D)

def setTime():
    timeVal = time_cmd.time().toString("hh:mm:ss")
    print(timeVal)
bTime.clicked.connect(setTime)

def tel_ON_OFF():
    telVal = tel_cmd.currentText()
    print(telVal)
bTel.clicked.connect(tel_ON_OFF)

def simp_E_D():
    simpVal = simp_cmd.text()
    print(simpVal)
bSimp.clicked.connect(simp_E_D)


def BCN_ON_OFF():
    bcn_val = bcn_cmd.currentText()
    print(bcn_val)
bBCN.clicked.connect(BCN_ON_OFF)


def cal_():
    calVal = cal_cmd.text()
    print(calVal)
    s_d = f"cal{calVal}"
    send_data(s_d)
bCAL.clicked.connect(cal_)


image_paths = ['f1.png', 'f2.png', 'f3.png','f4.png','f5.png','f6.png']





# Function to change the image
def change_image(n):
    if n > 5:
        n = 5
    pixmap = QPixmap(image_paths[n])
    LBImage.setPixmap(pixmap)
    

#change_image(current_image_index)

counter = 0
# Animation parameters
start_time = time.time()


def getPos(t,c,n):
    i = 0
    ti = 0
    for ec in t:
        if ec == c:
            i += 1
        ti +=1
        if i == n:
            return ti-1;
        
    return -1

def getValue(t,n):
    return t[getPos(t,',',n)+1:getPos(t,',',n+1)]


def update():
    global arduinoData_string, x_data, temperatureY_data, altitudeY_data, voltageY_data, airspeedY_data, pressureY_data, tiltxY_data, tiltyY_data, rotzY_data
     

    if ser.in_waiting != 0:
        data = ser.readline().decode('utf-8')
        tel.insertPlainText(data)
        arduinoData_string = data
        update_table(data)
        append_to_table(data)
        table_widget_appended.scrollToBottom()   
        

        with open('Flight_2082.csv', 'a') as file:
            
            file.write(data)

    #ser.write(b'g')
     

    x_s = getValue(arduinoData_string, PACKET_COUNT)
    temperature = getValue(arduinoData_string,TEMPERATURE)
    altitude = getValue(arduinoData_string,ALTITUDE)
    airspeed = getValue(arduinoData_string,AIR_SPEED)
    voltage = getValue(arduinoData_string,VOLTAGE)
    pressure = getValue(arduinoData_string,PRESSURE)
    tiltx = getValue(arduinoData_string,TILT_X)
    tilty = getValue(arduinoData_string,TILT_Y)
    rotz = getValue(arduinoData_string,ROT_Z)

    print(x_s)

    try:
        x = float(x_s)
        temperatureY = float(temperature)
        altitudeY = float(altitude)
        airspeedY = float(airspeed)
        voltageY = float(voltage)
        pressureY = float(pressure)
        tiltxY = float(tiltx)
        tiltyY = float(tilty)
        rotzY = float(rotz)
        x_a = x+1
        global counter
        if x_a%15 == 0 and x_a != 0:
            counter+=1
        change_image(counter)
        if counter >= 5:  # Adjust the limit based on your image paths
            counter = 0
        x_data.append(x)
        temperatureY_data.append((temperatureY))
        altitudeY_data.append((altitudeY))
        airspeedY_data.append((airspeedY))
        voltageY_data.append((voltageY))
        pressureY_data.append((pressureY))
        tiltxY_data.append((tiltxY))
        tiltyY_data.append((tiltyY))
        rotzY_data.append((rotzY))
    except:
        pass



    if len(x_data) > 50:
        x_data = x_data[-50:]
        temperatureY_data = temperatureY_data[-50:]
        altitudeY_data = altitudeY_data[-50:]
        voltageY_data = voltageY_data[-50:]
        airspeedY_data = airspeedY_data[-50:]
        pressureY_data = pressureY_data[-50:]
        tiltxY_data = tiltxY_data[-50:]
        tiltyY_data = tiltyY_data[-50:]
        rotzY_data = rotzY_data[-50:]     
    
    

    # Update plot curve for Container
    try:
    	plot_curve_temp.setData(x_data, temperatureY_data)
    except valErr:
    	print(valErr)
    plot_curve_Altitude.setData(x_data, altitudeY_data)
    plot_curve_Voltage.setData(x_data, voltageY_data)
    plot_curve_AirSp.setData(x_data, airspeedY_data)
    plot_curve_pressure.setData(x_data, pressureY_data)
    plot_curve_TiltX.setData(x_data, tiltxY_data)
    plot_curve_TiltY.setData(x_data, tiltyY_data)
    plot_curve_RotZ.setData(x_data, rotzY_data)

    #Telemetry box autoscroll
    cursor = tel.textCursor()
    cursor.movePosition(cursor.End)
    tel.setTextCursor(cursor)


def send_data(data):
    if ser.is_open:
        ser.write(data.encode())  # Encode string to bytes and send
        print(f"{data}")
    else:
        print("Serial port is not open")



# Start the update timer
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1100)

layout.setColumnStretch(3, 2)  # Increase the stretch factor of column 1
layout.setColumnStretch(4, 2)




# Create 4 combo boxes with 2 options each
tel_cmd = QComboBox()
tel_cmd.addItems(["Telemetry ON", "Telemetry OFF"])
tel_cmd.setStyleSheet("background-color: white;")
tel_cmd.setFixedWidth(150) 
tel_cmd.setFixedHeight(30)  

gbox = QGridLayout()
gbox.addWidget(LBtel,0,0)
gbox.addWidget(tel_cmd,1,0)
gbox.addWidget(bTel,1,1)
    


simE_cmd = QComboBox()
simE_cmd.addItems(["Enable", "Disable"])
simE_cmd.setStyleSheet("background-color: white;")
simE_cmd.setFixedWidth(80) 
simE_cmd.setFixedHeight(30)
gbox.addWidget(LBsimE,2,0)
gbox.addWidget(simE_cmd,3,0)
gbox.addWidget(bSimE,3,1)



simA_cmd = QComboBox()
simA_cmd.addItems(["Activate", "Deactivate"])
simA_cmd.setStyleSheet("background-color: white; margin-left:0px;")
simA_cmd.setFixedWidth(80) 
simA_cmd.setFixedHeight(30)
gbox.addWidget(LBsimA,4,0)
gbox.addWidget(simA_cmd,5,0)
gbox.addWidget(bSimA,5,1)



 # Create a QTimeEdit widget for setting the time
time_cmd = QTimeEdit()
time_cmd.setFixedWidth(80) 
time_cmd.setStyleSheet("background-color: white;")
gbox.addWidget(LBtime,6,0)
gbox.addWidget(time_cmd,7,0)
gbox.addWidget(bTime,7,1)


# Create TextBox
simp_cmd = QLineEdit()
simp_cmd.setStyleSheet("background-color: white;")
simp_cmd.setFixedWidth(80) 
simp_cmd.setFixedHeight(20)
gbox.addWidget(LBsimp,8,0)
gbox.addWidget(simp_cmd,9,0)
gbox.addWidget(bSimp,9,1)


cal_cmd = QLineEdit()
cal_cmd.setFixedWidth(80) 
cal_cmd.setFixedHeight(20)
cal_cmd.setStyleSheet("background-color: white;")
gbox.addWidget(LBCAL,10,0)
gbox.addWidget(cal_cmd,11,0)
gbox.addWidget(bCAL,11,1)


bcn_cmd = QComboBox()
bcn_cmd.addItems(["ON", "OFF"])
bcn_cmd.setStyleSheet("background-color: white; margin-left:0px;")
bcn_cmd.setFixedWidth(80) 
bcn_cmd.setFixedHeight(30)
gbox.addWidget(LBBCN,12,0)
gbox.addWidget(bcn_cmd,13,0)
gbox.addWidget(bBCN,13,1)



#---------------------


# Add the plot widget, textbox, and button to the layout

frame1 = QFrame()
frame1.setFrameShape(QFrame.Box) 
frame1.setFrameShadow(QFrame.Raised)

frame2 = QFrame()
frame2.setFrameShape(QFrame.Box) 
frame2.setFrameShadow(QFrame.Raised)

frame3 = QFrame()
frame3.setFrameShape(QFrame.Box) 
frame3.setFrameShadow(QFrame.Raised)

frame4 = QFrame()
frame4.setFrameShape(QFrame.Box) 
frame4.setFrameShadow(QFrame.Raised)

	

GR1 = QGridLayout()
GR1.addWidget(LBTname,0,0)
GR1.setContentsMargins(0, 0, 0, 0)
GR1.setSpacing(0)

	

GR2 = QGridLayout()
GR2.addWidget(LBImage,0,0)
GR2.addWidget(plot_widget_Altitude,0,1)
GR2.addWidget(plot_widget_AirSp,0,2)
GR2.addWidget(plot_widget_temp,1,0)
GR2.addWidget(plot_widget_pressure,1,1)
GR2.addWidget(plot_widget_Voltage,1,2)
GR2.addWidget(plot_widget_TiltX,2,0)
GR2.addWidget(plot_widget_TiltY,2,1)
GR2.addWidget(plot_widget_RotZ,2,2)
GR1.setContentsMargins(0, 0, 0, 0)
GR1.setSpacing(0)



GR3 = QGridLayout()
GR3.addWidget(LBtelBox,0,0)
GR3.addWidget(table_widget,1,0)
GR3.addWidget(label1,2,0)
GR3.addWidget(table_widget_appended,3,0)



r1 = QWidget()
r1.setLayout(GR1)
frame1.setLayout(GR1)
frame1.setLineWidth(1)
frame1.setFrameShape(QFrame.NoFrame)

r2 = QWidget()
r2.setLayout(GR2)
frame2.setLayout(GR2)
frame2.setLineWidth(1)
frame2.setFrameShape(QFrame.NoFrame)

r3 = QWidget()
r3.setLayout(GR3)
frame3.setLayout(GR3)
frame3.setLineWidth(1)
frame3.setFrameShape(QFrame.NoFrame)

r4 = QWidget()
r4.setLayout(gbox)
frame4.setLayout(gbox)
frame4.setLineWidth(1)
frame4.setFrameShape(QFrame.NoFrame)




layout.addWidget(frame1,0,0)
layout.addWidget(frame2,1,0)
layout.addWidget(frame3,2,0)
#layout.addWidget(frame4,3,0)
layout.setHorizontalSpacing(5)
layout.setVerticalSpacing(5)
layout.setContentsMargins(0, 0, 0, 0)
layout.setSpacing(0)


#--------------------

scroll_area.setWidget(widget)
main_layout.addWidget(scroll_area)

window.setLayout(main_layout)


# Show the window
window.show()

print("Running")


window.keyPressEvent = keyPressEvent


# Start the Qt event loop
sys.exit(app.exec_())