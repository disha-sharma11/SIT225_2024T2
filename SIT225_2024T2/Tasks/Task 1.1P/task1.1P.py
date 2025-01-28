import serial
import random
import time

# set baud rate, same speed as set in your Arduino sketch.
boud_rate = 9600

# set serial port as suits your operating system
s = serial.Serial('/dev/cu.usbmodem101', boud_rate, timeout=5)

while True:
    data_send = random.randint(1, 3)
    s.write(bytes(str(data_send), 'utf-8'))
    print(f"Sent to Arduino >>> {data_send}")

    time.sleep(0.5)

    data_recv = s.readline().decode('utf-8').strip()
    if data_recv.isdigit():
        delay_time = int(data_recv)
        print(f"Received from Arduino <<< {delay_time}")
        time.sleep(delay_time * 2)
