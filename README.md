# Smart Room Light Monitoring System (ESP32-Light-Monitoring-MQTT)

A real-time IoT monitoring system using an ESP32 microcontroller running MicroPython that converts analog potentiometer inputs to status updates published via MQTT to a public broker, allowing remote clients to monitor light status in real time.

---

## Features

- **MicroPython on ESP32**: Leverages MicroPython firmware for rapid prototyping and clean hardware controller scripting.
- **Analog Input (ADC)**: Translates physical potentiometer rotation to discrete control thresholds using a 12-bit Analog-to-Digital Converter (GPIO35) with 11dB attenuation.
- **State-driven Decision Logic**: Eliminates message flooding by publishing status changes only when transitions (ON/OFF) occur.
- **MQTT Publish/Subscribe Protocol**: Publishes room status messages over TCP/IP to a public Mosquitto broker (`test.mosquitto.org`).
- **PC Dashboard Subscriber**: A lightweight Python monitoring script (`paho-mqtt`) running on a PC to listen and log room lighting status updates in real time.

---

## Tech Stack

| Component | Technology | Description |
|---|---|---|
| **Microcontroller** | ESP32 | High-performance dual-core MCU with built-in Wi-Fi and Bluetooth |
| **Firmware** | MicroPython | Python 3 implementation optimized for microcontrollers |
| **Communication** | MQTT | Lightweight publish-subscribe network protocol (TCP/IP) |
| **MQTT Broker** | Mosquitto | Public test broker hosted at `test.mosquitto.org` |
| **Dashboard Client** | Python (paho-mqtt) | Python PC application utilizing the `paho-mqtt` package |
| **Sensors & Actuators** | Potentiometer & LED | Analog input (GPIO35) and digital state indicator (GPIO2) |

---

## Architecture

The diagram below details the data flow from the hardware sensors to the PC monitoring client:

```mermaid
graph LR
    A[Potentiometer] -->|Analog Voltage 0-3.3V| B[ESP32 ADC GPIO35]
    B -->|Determine Threshold| C{ON/OFF State Change?}
    C -->|Local Control| D[ESP32 Built-in LED GPIO2]
    C -->|Publish message "LIGHT ON/OFF"| E[MQTT Broker: test.mosquitto.org:1883]
    E -->|Forward message| F[PC Dashboard: pc_dashboard.py]
```

---

## Getting Started

### Hardware Requirements & Wiring

- **ESP32 Development Board** (e.g. NodeMCU ESP32)
- **10k Ohm Potentiometer**
- **Jumper wires & Breadboard**

#### Wiring Instructions:
1. Connect the **Potentiometer VCC Pin** to ESP32 **3V3 Pin**.
2. Connect the **Potentiometer GND Pin** to ESP32 **GND Pin**.
3. Connect the **Potentiometer Data Out Pin** to ESP32 **GPIO 35** (ADC1_CH7).
4. The system controls the built-in blue LED on **GPIO 2** to signal the state locally.

---

### Setup & Flashing Instructions

#### 1. ESP32 Microprocessor Configuration
1. Flash the latest **MicroPython firmware** onto your ESP32 board.
2. Connect your ESP32 to your PC using a serial tool like Thonny IDE.
3. Install the standard MicroPython MQTT dependency:
   ```python
   import mip
   mip.install("umqtt.simple")
   ```
4. Open [esp32/esp32_code.py](file:///C:/Users/bb426/.gemini/antigravity-ide/scratch/github_cleanup/ESP32-Light-Monitoring-MQTT/esp32/esp32_code.py) and update the credentials:
   ```python
   SSID = "YOUR_WIFI_NAME"
   PASSWORD = "YOUR_WIFI_PASSWORD"
   ```
5. Save `esp32_code.py` to the ESP32 device as `main.py` so it executes automatically upon boot.

#### 2. PC Dashboard Configuration
1. Install Python 3.x on your workstation.
2. Install the necessary MQTT dependencies:
   ```bash
   pip install paho-mqtt
   ```
3. Run the dashboard subscriber:
   ```bash
   python dashboard/pc_dashboard.py
   ```
4. Rotate your hardware potentiometer all the way up (ON) or down (OFF) to see real-time console printouts!

---

## What I Learned

- **ADC Attenuation & Bit-Width**: Gained hands-on experience setting up 12-bit ADC resolution (0-4095 range) with 11dB attenuation to safely read the full 3.3V analog input range in MicroPython.
- **State-Change Caching**: Implemented a state comparison check (`last_state`) on the microcontroller to avoid flooding the MQTT network. This limits publishing only to instances where the lighting state changes.
- **Asynchronous Decoupled Communication**: Designed and tested a publish-subscribe communication pipeline, separating low-power hardware edge nodes from PC dashboard clients.

---

## Future Improvements

- Replace the analog potentiometer with an actual **Light Dependent Resistor (LDR)** sensor to automate light switching based on real room lux levels.
- Add secure communication parameters utilizing mutual TLS (MQTTS) for encrypted transmissions.
- Migrate the simple console logging client into a web interface (e.g. built with HTML/CSS/JS or Streamlit) for graphical real-time data representation.
