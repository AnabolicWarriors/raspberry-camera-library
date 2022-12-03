import serial

ser = serial.Serial(
    port='COM4',\
    baudrate=38400,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.SEVENBITS)
print(ser)

while True:
    # e = ser.readline(100);
    # print(e)
    line = ser.readline(100)
    line = line.strip();
    # print(line)
    line = line.decode('utf-8');
    data = str(line);
    # 데이터 파싱의 끝!
    key = data[1:6].strip('-');
    # print(data)
    
    

ser.close()
print("Close")
