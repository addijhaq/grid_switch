import time
import board
from adafruit_ina3221 import INA3221
import gpiod
from gpiod.line import Direction, Value

i2c = board.I2C()
ina3221 = INA3221(i2c)
chip_path = "/dev/gpiochip4"


line18 = gpiod.request_lines(
        chip_path,
        consumer="get-line-value",
        config={18: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.ACTIVE)},) 
voltageMap = {}
try:
    while True:
        for channel in range(3):
            voltage = round(ina3221[channel].bus_voltage,2)
            if(channel not in voltageMap):
                voltageMap[channel] = 0.00
                
            # if (voltage - .6) > 0:
            #         voltage -= .65
                    
            if(voltageMap[channel] != voltage):
                voltageMap[channel] = voltage
                print(f"Channel {channel+1}: Voltage {voltage:.2f} V")
                
            line18.set_value(18, Value.ACTIVE)
            print("MOSFET ON")
            time.sleep(5)
            line18.set_value(18, Value.INACTIVE)
            print("MOSFET OFF")
        
except KeyboardInterrupt:
    print("Exiting...")
finally:
    line18.release()