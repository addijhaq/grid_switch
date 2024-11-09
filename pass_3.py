import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

# Initialize the ADC (ADS1115)
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
selected_battery = 0
# GPIO setup
RELAY_PIN = 17  # GPIO pin connected to the relay
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Function to read voltage from the ADC
def read_voltage(channel):
    value = adc.read_adc(channel, gain=GAIN)
    return value * (4.096 / 32767.0)  # Convert ADC value to voltage

# Main loop
try:
    while True:
        primary_voltage = read_voltage(0)  # Read from ADC channel 0 for primary battery
        secondary_voltage = read_voltage(1)  # Read from ADC channel 1 for secondary battery
        print(f"Primary Battery Voltage: {primary_voltage:.2f} V")
        print(f"Secondary Battery Voltage: {secondary_voltage:.2f} V")
        
        if primary_voltage < 12.1 and secondary_voltage >= 12.1:
            if(selected_battery != 1):
                print("Setting selected_battery to secondary battery: 1")
                selected_battery = 1
                GPIO.output(RELAY_PIN, GPIO.HIGH)  # Switch to secondary battery
                print("Switched to secondary battery")
        else:
            if(selected_battery != 0):
                print("Setting selected_battery to primary battery: 0")
                selected_battery = 0
                GPIO.output(RELAY_PIN, GPIO.LOW)  # Use primary battery
                print("Using primary battery")

        time.sleep(1)  # Delay for 1 second

except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()