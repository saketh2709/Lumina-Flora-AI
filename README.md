# 🌿 LuminaFlora AI - Smart Horticulture Hub

A modern, full-stack IoT and telemetry analytics application built to automate microclimate greenhouse environments and deliver predictive crop health insights using full-stack SaaS architecture.

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
├── .gitignore                  # Exclusion patterns for database & local files
├── LICENSE                     # MIT Open Source License distribution parameters
└── README.md                   # Core repository technical guide and index

📊 Analytics Threshold Matrix
Parameter,Sensor/Engine,Critical Minimum,Optimal Target Range,Critical Maximum,Action Flag
Sunlight,LDR Array,< 500 Lux,500 - 1200 Lux,> 2000 Lux,Supplemental Grow Light Active
Temperature,DHT22 Core,< 18°C,22°C - 28°C,> 32°C,Health Degradation Warning (-30%)
VPD,Magnus-Tetens,< 0.50 kPa,0.80 - 1.20 kPa,> 1.50 kPa,Stomatal Closure / Transpiration Stress

Cloud API & Telemetry Routes
Telemetry Broadcast (Wokwi ➔ Cloud Broker)
Publish Topic: horticulture/saketh/data
Payload Format: String ("light,temp,hum,mode")

Command & Control (Dashboard ➔ Wokwi Edge)
Subscribe Topic: horticulture/saketh/control
Control Commands Handled:
AUTO — Hands device operational control back to the ambient LDR script.
LED_ON — Forces the GPIO-driven grow lamp matrix high (Manual Override).
LED_OFF — Shuts down lighting arrays forcefully for system isolation.

🛠️ Tech Stack
Edge & Hardware Layer
MicroPython — High-performance microcontroller script executions.
ESP32 Wi-Fi SoC — Integrated localized compute core.
DHT22 & LDR Array — Sensory intake peripherals.

Data Transport & Backend
MQTT (HiveMQ Cloud Broker) — Asynchronous light-footprint messaging platform.
Python / Flask — Multi-threaded administrative backend router.
SQLite3 — Embedded database for secure microclimate telemetry storage.

Interface & Graphics
Chart.js — Multi-axis microclimate graphic trajectory mapping.
HTML5 / CSS3 — Modular workspace views layout with full dashboard personalization.

⚙️ Installation & Setup
Prerequisites
Python 3.8+ installed
Git installed locally
1. Clone the Repository
git clone https://github.com/saketh2709/LuminaFlora-AI.git
cd LuminaFlora-AI
2. Set Up the Data Engine & Dashboard
Bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install required dependencies
pip install paho-mqtt flask

# Run the background telemetry data logger
python App/main_logger.py

# Run the Flask SaaS platform (Open a separate terminal tab)
python App/app.py
Your local development dashboard will now be securely running at http://127.0.0.1:5000/

⚠️ Disclaimer
This application is an educational prototype built for smart horticulture demonstration. It simulates real greenhouse environments and industrial agricultural automation loops using simulated hardware profiles.

👨‍💻 Author & Attribution
Developer: Kanneluru Saketh
Affiliation: Vellore Institute of Technology - AP (VIT-AP)
Student Identifier: 22MIS7062
GitHub Profile: @saketh2709

📄 License
This project is open-source and distributed under the terms of the MIT License.

🤝 Contributing
Feedback, issue logs, and optimizations for plant growth algorithms are welcome! Feel free to open a ticket on the repo's issues page.

🔮 Future Enhancements
[ ] Integrate hardware automated cooling relays using 5V DC fans linked to critical heat thresholds.
[ ] Deploy the Flask application to a cloud production pipeline (AWS/GCP) for global dashboard routing.
[ ] Introduce multi-crop target profile presets (e.g., Succulents vs. Leafy Greens) to alter threshold matrices dynamically.
[ ] Implement an automated SMS alert system using Twilio APIs for real-time critical environment warnings.