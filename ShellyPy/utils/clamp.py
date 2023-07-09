from ..base.hints import byte, temperaur

def clamp(val: int, min_val: int, max_val: int) -> int:
    return max(min(val, max_val), min_val)

def clamp_percent(val: int) -> int:
    return clamp(val, 0, 100)

def clamp_byte(val: byte) -> int:
    return clamp(val, 0, 255)

def clamp_temp(val: temperaur) -> int:
    return clamp(val, 3000, 6500)