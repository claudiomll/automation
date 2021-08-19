import logging
import schedule
import time
import RPi.GPIO as GPIO

logging.basicConfig(filename='/var/log/plants_watering.log', level=logging.DEBUG)

GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers

RELAYS = [17, 27]
WATERING_TIME = 3


def initialize_relays():
    for relay in RELAYS:
        logging.info("configuring relay %s as OUT mode" % str(relay))
        GPIO.setup(relay, GPIO.OUT)  # GPIO Assign mode
        logging.info("setting default state for relay %s to LOW" % str(relay))
        GPIO.output(relay, GPIO.LOW) # Default state


def watering_job():
    for relay in RELAYS:
        logging.info("activating relay %s" % str(relay))
        GPIO.output(relay, GPIO.HIGH)
        time.sleep(WATERING_TIME)
        logging.info("de-activating relay %s" % str(relay))
        GPIO.output(relay, GPIO.LOW)


try:
    initialize_relays()
    #schedule.every(10).seconds.do(watering_job)
    schedule.every().day.at("21:00").do(watering_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

except KeyboardInterrupt:
    logging.warning("program interrupted")

except Exception as e:
    logging.exception("%s" % str(e))

finally:
    GPIO.cleanup()
