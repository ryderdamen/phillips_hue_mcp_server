lights = {
    # Kitchen
    "1": {"name": "Kitchen Overhead 1", "state": {"on": True, "hue": 45000, "bri": 180, "sat": 180}},
    "2": {"name": "Kitchen Overhead 2", "state": {"on": True, "hue": 45000, "bri": 180, "sat": 180}},
    "3": {"name": "Kitchen Floor Lamp", "state": {"on": False, "hue": 10000, "bri": 120, "sat": 100}},
    "4": {"name": "Kitchen Table Lamp", "state": {"on": True, "hue": 50000, "bri": 200, "sat": 150}},
    # Living Room
    "5": {"name": "Living Room Overhead", "state": {"on": True, "hue": 10000, "bri": 254, "sat": 200}},
    "6": {"name": "Living Room Floor Lamp", "state": {"on": False, "hue": 20000, "bri": 180, "sat": 180}},
    "7": {"name": "Living Room Table Lamp", "state": {"on": True, "hue": 30000, "bri": 150, "sat": 120}},
    "8": {"name": "Living Room Wall Sconce", "state": {"on": False, "hue": 40000, "bri": 100, "sat": 100}},
    # Bedroom
    "9": {"name": "Bedroom Overhead", "state": {"on": True, "hue": 30000, "bri": 200, "sat": 180}},
    "10": {"name": "Bedroom Floor Lamp", "state": {"on": False, "hue": 35000, "bri": 120, "sat": 110}},
    "11": {"name": "Bedroom Table Lamp", "state": {"on": True, "hue": 25000, "bri": 180, "sat": 130}},
    "12": {"name": "Bedroom Wall Sconce", "state": {"on": False, "hue": 15000, "bri": 90, "sat": 90}},
}

groups = {
    "1": {
        "name": "Kitchen",
        "type": "Room",
        "class": "Kitchen",
        "lights": ["1", "2", "3", "4"],
        "action": {"on": True, "hue": 45000, "bri": 180, "sat": 180}
    },
    "2": {
        "name": "Living Room",
        "type": "Room",
        "class": "Living room",
        "lights": ["5", "6", "7", "8"],
        "action": {"on": True, "hue": 10000, "bri": 254, "sat": 200}
    },
    "3": {
        "name": "Bedroom",
        "type": "Room",
        "class": "Bedroom",
        "lights": ["9", "10", "11", "12"],
        "action": {"on": True, "hue": 30000, "bri": 200, "sat": 180}
    }
} 