import serial

with serial.Serial("/dev/cu.usbserial-0001", 115_200, timeout=10) as ser:
    line = ser.readline()
    print (line)