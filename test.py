import irsdk
import time
ir = irsdk.IRSDK()
ir.startup()
while(True):
    print(ir['Speed']) 
    time.sleep(0.05)