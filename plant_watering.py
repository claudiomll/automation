import schedule
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers

RELAYS = [17, 27]


def initialize_relays():
    for relay in RELAYS:
        GPIO.setup(relay, GPIO.OUT)  # GPIO Assign mode
        GPIO.output(relay, GPIO.LOW)


def job():
    for relay in RELAYS:
        print("+ activating %s" % str(relay))
        GPIO.output(relay, GPIO.HIGH)
        time.sleep(3)
        print("- de-activating %s" % str(relay))
        GPIO.output(relay, GPIO.LOW)


schedule.every(10).seconds.do(job)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)

except Exception:
    pass

finally:
    GPIO.cleanup()
