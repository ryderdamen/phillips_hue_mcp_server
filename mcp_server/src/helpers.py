import colorsys
from typing import Tuple, Dict


def rgb_to_hsb(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Convert RGB values (0-255) to HSB values for Hue lights.
    
    Args:
        r: Red value (0-255)
        g: Green value (0-255) 
        b: Blue value (0-255)
    
    Returns:
        Tuple of (hue, saturation, brightness) where:
        - hue: 0-65535 (Hue's scale)
        - saturation: 0-254 (Hue's scale)
        - brightness: 0-254 (Hue's scale)
    """
    # Normalize RGB to 0-1
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    
    # Convert to HSV (Hue uses HSV, not HSB, but they're the same)
    h, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
    
    # Convert to Hue's scale
    hue = int(h * 65535)  # Hue uses 0-65535
    sat = int(s * 254)    # Hue uses 0-254
    bri = int(v * 254)    # Hue uses 0-254
    
    return hue, sat, bri

def hsb_to_rgb(hue: int, sat: int, bri: int) -> Tuple[int, int, int]:
    """
    Convert HSB values from Hue lights to RGB values.
    
    Args:
        hue: Hue value (0-65535)
        sat: Saturation value (0-254)
        bri: Brightness value (0-254)
    
    Returns:
        Tuple of (r, g, b) where each value is 0-255
    """
    # Normalize to 0-1
    h_norm = hue / 65535.0
    s_norm = sat / 254.0
    v_norm = bri / 254.0
    
    # Convert to RGB
    r, g, b = colorsys.hsv_to_rgb(h_norm, s_norm, v_norm)
    
    # Convert to 0-255 scale
    r_int = int(r * 255)
    g_int = int(g * 255)
    b_int = int(b * 255)
    
    return r_int, g_int, b_int

def rgb_to_hue_state(r: int, g: int, b: int, on: bool = True) -> Dict:
    """
    Convert RGB values to a complete Hue light state dictionary.
    
    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)
        on: Whether the light should be on (default: True)
    
    Returns:
        Dictionary with Hue-compatible state values
    """
    hue, sat, bri = rgb_to_hsb(r, g, b)
    return {
        "on": on,
        "hue": hue,
        "sat": sat,
        "bri": bri
    }
