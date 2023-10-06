import RPi.GPIO as GPIO
import sys
import time
import drivers
from time import sleep

# Motor and PWM pin configuration
ENA = 13  # Motor 1 Enable (ENA) - Pin 13 (PWM)
IN3 = 27  # Motor 1 Input 1 (IN3) - Pin 27
ENB = 12  # Motor 2 Enable (ENB) - Pin 12 (PWM)
IN4 = 22  # Motor 2 Input 4 (IN4) - Pin 22
IN1 = 23  # Motor 1 Input 2 (IN1) - Pin 23
IN2 = 24  # Motor 1 Input 3 (IN2) - Pin 24

# Keypad configuration
COL_PINS = [21, 20, 16, 5]
ROW_PINS = [6, 11, 19, 26]

# KEYS matrix
KEYS = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]





# Initialize LCD and PWM
display = drivers.Lcd()
GPIO.setmode(GPIO.BCM)
GPIO.setup(COL_PINS, GPIO.OUT)
GPIO.setup(ROW_PINS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)


# PWM initialization
pwm_motor1 = GPIO.PWM(ENA, 100)  # PWM frequency = 100 Hz
pwm_motor2 = GPIO.PWM(ENB, 100)  # PWM frequency = 100 Hz

# Start PWM with duty cycle 0 (motors off)
pwm_motor1.start(0)
pwm_motor2.start(0)

# Function to read keypad input and limit to 4 digits
def get_key(limit=4):
    key = None
    last_key = None
    displayed_digits = ""

    while len(displayed_digits) < limit:
        for col_num, col_pin in enumerate(COL_PINS):
            GPIO.output(col_pin, 0)
            for row_num, row_pin in enumerate(ROW_PINS):
                if not GPIO.input(row_pin):
                    key = KEYS[row_num][col_num]

            if key and key != last_key:
                last_key = key
                if key.isdigit():
                    displayed_digits += key
                elif key == '#':
                    return displayed_digits
                
                display.lcd_display_string("Inputs: " + displayed_digits, 1)
                time.sleep(0.1)  # A short delay to avoid multiple key presses
            GPIO.output(col_pin, 1)

    return displayed_digits

try:
    while True:
        display.lcd_clear()
        sleep(1)
        display.lcd_display_string("DR.G.RAMANATHAN", 1)
        display.lcd_display_string("SPIN COATER", 2)
        sleep(10)
        display.lcd_display_string("STARTING.......", 1)
        sleep(10)
        display.lcd_clear()
        sleep(1)
        display.lcd_display_string("ENTER INPUTS", 1)
        display.lcd_display_string("1-RPM,2-TIME", 2)
        sleep(5)
        display.lcd_clear() 
        sleep(1)
        display.lcd_display_string("Press 1st digit", 1)
        display.lcd_display_string("For RPM",2)
        sleep(5)
        display.lcd_clear()
        rpm_input = get_key(4)
        display.lcd_display_string("RPM FIXED: " + rpm_input, 1)
        time.sleep(10)
        display.lcd_clear()
        sleep(1)
        display.lcd_display_string("Press 1st digit", 1)
        display.lcd_display_string("For Time",2)
        sleep(5)
        display.lcd_clear()
        time_input = get_key(4)
        display.lcd_display_string("TIME FIXED: " + time_input, 1)        
        sleep(10)
        display.lcd_clear()
        
        display.lcd_display_string("Vacuum Started..", 1)
        duty_cycle_motor2 = 35  # Default duty cycle for the vacuum motor
        pwm_motor2.ChangeDutyCycle(duty_cycle_motor2)
        GPIO.output(IN4, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        sleep(20)
        pwm_motor2.ChangeDutyCycle(0)
        display.lcd_clear()
        
        display.lcd_display_string("Coating Started", 1)
        display.lcd_display_string("Wait 300s",2)
        sleep(100)
        display.lcd_display_string("Wait 200s",2)
        sleep(100)
        display.lcd_display_string("Wait 100s",2)
        sleep(100)
        display.lcd_display_string("Spinning...",2)
        # Convert RPM input to PWM duty cycle (adjust this conversion factor as needed)
        # Convert RPM input to PWM duty cycle
rpm = int(rpm_input)

# Define duty cycle values based on RPM
if rpm <= 1000:
    duty_cycle_motor1 = 20
elif rpm <= 2000:
    duty_cycle_motor1 = 25
elif rpm <= 3000:
    duty_cycle_motor1 = 30
elif rpm <= 4000:
    duty_cycle_motor1 = 35
elif rpm <= 5000:
    duty_cycle_motor1 = 40
elif rpm <= 6000:
    duty_cycle_motor1 = 45
elif rpm <= 7000:
    duty_cycle_motor1 = 50
elif rpm <= 8000:
    duty_cycle_motor1 = 55
elif rpm <= 9999:
    duty_cycle_motor1 = 60
else:
    print("Invalid RPM input")
    # You may want to add error handling here, such as setting a default duty cycle or exiting the program

# Apply PWM to the motor
pwm_motor1.ChangeDutyCycle(duty_cycle_motor1)
        
        # Run motors for the specified time
        run_time = int(time_input)
        sleep(run_time)
        
        # Stop the motors
        pwm_motor1.ChangeDutyCycle(0)
        
        display.lcd_clear()
        # Clear LCD
        display.lcd_display_string("FILM COATED", 1)
        display.lcd_display_string("TAKE IT OUT", 2)
        sleep(30)
        display.lcd_clear()

except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_display_string("Cleaning up!", 1)
    pwm_motor1.stop()
    pwm_motor2.stop()
    display.lcd_clear()
    GPIO.cleanup()
    sys.exit()
