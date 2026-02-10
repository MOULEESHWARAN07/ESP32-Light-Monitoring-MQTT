import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# ---------------- WIFI ----------------
SSID = "NA dhan da"
PASSWORD = "vinil..."

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(0.5)

print("WiFi Connected")
print("IP:", wlan.ifconfig()[0])

# ---------------- MQTT ----------------
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "smartroom/light/status"

client = MQTTClient("esp32_pot_switch", MQTT_BROKER)
client.connect()
print("MQTT Connected")

# ---------------- HARDWARE ----------------
led = Pin(2, Pin.OUT)
led.off()

pot = ADC(Pin(35))
pot.atten(ADC.ATTN_11DB)
pot.width(ADC.WIDTH_12BIT)

last_state = None   # ON / OFF

# ---------------- MAIN LOOP ----------------
while True:
    pot_value = pot.read()
    client.check_msg()

    # Pot = 0 → LIGHT OFF
    if pot_value <= 5:
        if last_state != "OFF":
            led.off()
            client.publish(MQTT_TOPIC, "LIGHT OFF")
            print("Pot =", pot_value, "→ LIGHT OFF")
            last_state = "OFF"

    # Pot = MAX → LIGHT ON
    elif pot_value >= 4090:
        if last_state != "ON":
            led.on()
            client.publish(MQTT_TOPIC, "LIGHT ON")
            print("Pot =", pot_value, "→ LIGHT ON")
            last_state = "ON"

    time.sleep(0.2)
