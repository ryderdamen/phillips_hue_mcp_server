import os
import requests
from typing import Optional, List, Dict

HUE_BRIDGE_IP = os.environ.get("HUE_BRIDGE_IP")
HUE_USERNAME = os.environ.get("HUE_USERNAME")

if not HUE_BRIDGE_IP or not HUE_USERNAME:
    raise RuntimeError("HUE_BRIDGE_IP and HUE_USERNAME must be set as environment variables.")

BASE_URL = f"http://{HUE_BRIDGE_IP}/api/{HUE_USERNAME}"

def get_lights() -> Dict:
    resp = requests.get(f"{BASE_URL}/lights")
    resp.raise_for_status()
    return resp.json()

def get_groups() -> Dict:
    resp = requests.get(f"{BASE_URL}/groups")
    resp.raise_for_status()
    return resp.json()

def set_light_state(light_id: str, state: dict) -> dict:
    resp = requests.put(f"{BASE_URL}/lights/{light_id}/state", json=state)
    resp.raise_for_status()
    return resp.json()

def set_group_action(group_id: str, action: dict) -> dict:
    resp = requests.put(f"{BASE_URL}/groups/{group_id}/action", json=action)
    resp.raise_for_status()
    return resp.json() 