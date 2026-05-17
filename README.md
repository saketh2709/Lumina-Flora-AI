#  LuminaFlora AI - Smart Horticulture & Decision Support System

A modern, full-stack IoT and analytics web application that utilizes edge computing and microclimate data metrics to automate plant growth environments and provide real-time agricultural analytics.

Built with a **Flask SaaS frontend/backend**, an **ESP32 MicroPython edge layer**, and an asynchronous cloud-data architecture running on a centralized telemetry schema.

---

##  Features

* **Closed-Loop Automation:** Microcontroller evaluates ambient solar radiation dynamically to deliver supplemental agricultural lighting instantly when $Lux < 500$.
* **Biometric Crop Analytics:** Real-time computation of Vapor Pressure Deficit ($VPD$) and predictive crop health indexes to detect physiological plant stress.
* **Granular Multi-Domain Dashboard:** Secure, role-based user portals separating localized monitoring, analytics tracking, configuration, and secure profile management.
* **Historical Telemetry Logging:** Continuous data stream brokerage parsing edge inputs into relational schemas for localized seasonal planning.
* **Manual Override Protocol:** High-priority cloud-to-device command layer bypassing automation sequences for system maintenance and specialized plant treatments.

---

## 📁 Project Structure

```text
LuminaFlora-AI/
│
├── App/
│   ├── app.py                  # Multi-domain Flask SaaS Application
│   └── main_logger.py          # Background MQTT Cloud Broker Telemetry Listener
│
├── Hardware/
│   └── main.py                 # ESP32 Edge Device MicroPython Core Firmware
│
├── .gitignore                  # Exclusion patterns for untracked database & local venv logs
├── LICENSE                     # MIT Open Source License distribution parameters
└── README.md                   # Core repository technical guide and index


Parameter,Sensor/Engine,Critical Minimum,Optimal Target Range,Critical Maximum,Action Flag
Sunlight,LDR Array,< 500 Lux,500 - 1200 Lux,> 2000 Lux,Supplemental Grow Light Active
Temperature,DHT22 Core,< 18°C,22°C - 28°C,> 32°C,Health Degradation Warning (-30%)
VPD,Magnus-Tetens,< 0.50 kPa,0.80 - 1.20 kPa,> 1.50 kPa,Stomatal Closure / Transpiration Stress

🌐 Cloud API & Telemetry Routes
Telemetry Broadcast (Wokwi $\rightarrow$ Cloud Broker)Publish Topic: horticulture/saketh/dataPayload Format: String ("light,temp,hum,mode")
Command & Control (Dashboard $\rightarrow$ Wokwi Edge)Subscribe Topic: horticulture/saketh/controlControl Commands Handled:
AUTO — Hands device operational control back to the ambient LDR script.
LED_ON — Forces the GPIO-driven grow lamp matrix high (Manual Override).
LED_OFF — Shuts down lighting arrays forcefully for system isolation.


Tech Stack
Edge & Hardware Layer
MicroPython — High-performance microcontroller script executions.
ESP32 Wi-Fi SoC — Integrated localized compute core.
DHT22 & LDR Array — Sensory intake peripherals.

Data Transport & Backend
MQTT (HiveMQ Cloud Broker) — Asynchronous light-footprint messaging platform.
Python / Flask — Multi-threaded administrative backend router.
SQLite3 — Embedded ACID-compliant microclimate storage tracking.

Interface & Graphics
Chart.js — Multi-axis microclimate graphic trajectory mapping.
HTML5 / CSS3 — Modular workspace views layout.

👤 Data Attribution & Ownership
Developer: Kanneluru Saketh
Affiliation: Vellore Institute of Technology - AP (VIT-AP)
Student Identifier: 22MIS7062