import requests
import time
import random
from datetime import datetime

API_URL = "http://localhost:5000/api/sensors"

def send_sensor_data(equip_id):
    base_temp = 72
    base_vibe = 1.5
    
    # normal reading with some randomness
    temp = base_temp + random.uniform(-3, 3)
    vibe = base_vibe + random.uniform(-0.5, 0.5)
    
    # 10% chance of anomaly
    if random.random() < 0.1:
        temp = base_temp + random.uniform(15, 25)
        vibe = base_vibe + random.uniform(2, 3)
        print(f"[ANOMALY] Equip {equip_id}: temp={temp:.1f}, vibe={vibe:.1f}")
    
    data = {
        "equipment_id": equip_id,
        "temperature": round(temp, 2),
        "vibration": round(vibe, 2),
        "runtime_hours": random.randint(4000, 5000)
    }
    
    try:
        resp = requests.post(API_URL, json=data)
        if resp.status_code == 201:
            result = resp.json()
            status = "⚠️ ANOMALY" if result['anomaly_detected'] else "✓"
            print(f"{datetime.now().strftime('%H:%M:%S')} - Equip {equip_id}: {status}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("IoT sensor simulator - sending data every 5sec")
    print("Press Ctrl+C to stop\n")
    
    try:
        import requests
    except:
        import subprocess
        subprocess.check_call(["pip", "install", "requests"])
        import requests
    
    while True:
        for equip_id in range(1, 7):
            send_sensor_data(equip_id)
        print("-" * 40)
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped")