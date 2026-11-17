import numpy as np

# 5x7 font for digits 0-9
FONT = {
    0: ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    1: ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    2: ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    3: ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    4: ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    5: ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    6: ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    7: ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    8: ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    9: ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
}

ROWS, COLS = 8, 13
DIGIT_ON = 7   # max brightness (sketch uses 3-bit grayscale: 0~7)
BAR_ON = 3     # dimmer confidence bar


def build_frame(digit=None, conf=0.0):
    """Digit on the left (cols 1-5), confidence bar on the right (cols 9-11, fills from bottom)."""
    f = np.zeros((ROWS, COLS), dtype=np.uint8)
    if digit is None:
        return f
    for r, line in enumerate(FONT[digit]):
        for c, ch in enumerate(line):
            if ch == "1":
                f[r, 1 + c] = DIGIT_ON
    height = int(round(conf * ROWS))
    for r in range(ROWS - height, ROWS):
        f[r, 9:12] = BAR_ON
    return f
