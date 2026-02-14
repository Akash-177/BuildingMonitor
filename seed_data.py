import random
import requests

BASE_URL = "http://localhost:5000/api"


def quick_seed():
    print("seeding sample data...")

    buildings = [
        {"name": "Cork HQ", "location": "Cork, Ireland"},
        {"name": "Dublin Office", "location": "Dublin, Ireland"},
        {"name": "Galway Data Center", "location": "Galway, Ireland"},
    ]

    for b in buildings:
        r = requests.post(f"{BASE_URL}/buildings", json=b)
        r.raise_for_status()
    print("buildings ok")

    equipment = [
        {"building_id": 1, "name": "HVAC Unit 1", "type": "HVAC", "model": "Carrier 5000"},
        {"building_id": 1, "name": "Chiller A", "type": "Chiller", "model": "Trane CH530"},
        {"building_id": 2, "name": "Elevator 1", "type": "Elevator", "model": "Otis Gen2"},
        {"building_id": 2, "name": "HVAC Unit 2", "type": "HVAC", "model": "Daikin VRV"},
        {"building_id": 3, "name": "Lighting System", "type": "Lighting", "model": "Philips"},
        {"building_id": 3, "name": "Cooling Tower", "type": "Chiller", "model": "BAC"},
    ]

    for e in equipment:
        r = requests.post(f"{BASE_URL}/equipment", json=e)
        r.raise_for_status()
    print("equipment ok")

    # keep it small: just enough to make health endpoint interesting
    for equip_id in range(1, 7):
        for _ in range(6):
            payload = {
                "equipment_id": equip_id,
                "temperature": round(72 + random.uniform(-3, 3), 2),
                "vibration": round(1.5 + random.uniform(-0.3, 0.3), 2),
                "runtime_hours": random.randint(4000, 5000),
            }
            requests.post(f"{BASE_URL}/sensors", json=payload)

    print("sensor readings ok")
    print("done.")


if __name__ == "__main__":
    quick_seed()
