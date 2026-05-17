import paho.mqtt.client as mqtt
import sqlite3
import datetime

# --- CONFIGURATION (Must match Wokwi) ---
MQTT_BROKER = "broker.hivemq.com"
TOPIC = "horticulture/saketh/data"  # Updated to match your Saketh channel

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Successfully connected to HiveMQ Cloud Broker!")
        client.subscribe(TOPIC)
        print(f"📡 Now listening on topic: {TOPIC}")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        # Decode the incoming data string
        data_str = msg.payload.decode()
        print(f"📩 Data Received: {data_str}")
        
        # Data format from Wokwi: "light,temp,hum,mode"
        parts = data_str.split(',')
        if len(parts) == 4:
            light = float(parts[0])
            temp = float(parts[1])
            hum = float(parts[2])
            mode = parts[3]
            
            # Save to SQLite Database
            conn = sqlite3.connect('garden.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sensor_data (timestamp, sunlight, temperature, humidity, system_mode)
                VALUES (datetime('now', 'localtime'), ?, ?, ?, ?)
            ''', (light, temp, hum, mode))
            conn.commit()
            conn.close()
            print(f"💾 Saved to DB: {light} Lux | {temp}°C | {mode}")
            
    except Exception as e:
        print(f"⚠️ Error processing message: {e}")

# Setup MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("🚀 Starting Main Logger...")
print("Connecting to Broker...")

try:
    client.connect(MQTT_BROKER, 1883, 60)
    # Start the loop to listen forever
    client.loop_forever()
except KeyboardInterrupt:
    print("\n🛑 Logger stopped by user.")
except Exception as e:
    print(f"💥 Fatal Error: {e}")