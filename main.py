from network import WLAN
from network import ESPNOW
from mqtt import MQTTClient

import machine
import binascii
import time
import gc

def sub_cb(topic, msg):
   print(msg)

wlan = WLAN(mode=WLAN.STA)
wlan.connect("<SSID>", auth=(WLAN.WPA2, "<PASSWORD>"), timeout=5000)

while not wlan.isconnected():
    machine.idle()

print("Connected to WiFi\n")

clientESP = MQTTClient("LoPy-Router", "<IP ADDRESS HERE>", user="mqtt-user", password="<MQTT BROKER PASSWORD>", port=1883)


#gc.collect()
clientESP.set_callback(sub_cb)
clientESP.connect()
time.sleep(2)

#clientLoRa.set_callback(sub_cb)
#clientLoRa.connect()
#time.sleep(2)

clientESP.subscribe(topic="endpoints/outbound")

while True:
    print("Sending ON")
    clientESP.publish(topic="test/feeds", msg="1")
    time.sleep(5)
    print("Sending OFF")
    clientESP.publish(topic="test/feeds", msg="3")
    clientESP.check_msg()

    time.sleep(5)
