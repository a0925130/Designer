import pyfirmata
import time

print("Connecting to Arduino...")
board = pyfirmata.Arduino('COM3')
it = pyfirmata.util.Iterator(board)
board.digital[6].mode = pyfirmata.INPUT
it.start()
print("Running Arduino...")

while True:
    # board.digital[8].write(1)
    time.sleep(0.5)
    # board.digital[8].write(0)
    # time.sleep(1)
    r = board.digital[6].read()
    print(int(r))
# board.digital[8].write(1)
# time.sleep(0.1)
    # else:
    #     board.digital[8].write(1)
    #     time.sleep(0.1)
# board.digital[10].mode = pyfirmata.INPUT
# led = board.get_pin('d:13:o')
# sw = True
#
# while True:
#     # sw = board.digital[10].read()
#     print(sw)
#     if sw is True:
#         led.write(1)
#         sw = False
#         time.sleep(1)
#     else:
#         led.write(0)
#         sw = True
#         time.sleep(1)
#     print(led.read())
