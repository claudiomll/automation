import schedule
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

RELAYS = [17, 27]


def initialize_relays():
    GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers

    for relay in RELAYS:
        GPIO.setup(relay, GPIO.OUT)  # GPIO Assign mode
        GPIO.output(relay, GPIO.LOW)


def job():
    for relay in RELAYS:
        print("+ activating %s" % str(relay))
        GPIO.output(relay, GPIO.HIGH)
        client.publish("switch/water_valve_1", "ON")
        time.sleep(3)
        print("- de-activating %s" % str(relay))
        GPIO.output(relay, GPIO.LOW)
        client.publish("switch/water_valve_1", "OFF")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


schedule.every(10).seconds.do(job)

client.connect("ha.home", 1883, 60)
client.loop_start()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
while True:
    schedule.run_pending()
    time.sleep(1)
