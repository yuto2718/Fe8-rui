import serial

path = '/dev/ttyACM0'

robot = serial.Serial(path, 115200)
print("open port")

head = 255

tilt = 60 #0-180
pan  = 230 #0-180


robot.write(head.to_bytes(1,'big'))
robot.write(tilt.to_bytes(1,'big'))
robot.write(pan.to_bytes(1,'big'))

while(True):
    if(robot.inWaiting() > 0):
        data = robot.readline()
        print(data)
robot.close();
