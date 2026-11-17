# Linux side (Qualcomm MPU): serves the handwriting page, runs the ONNX model,
# and sends the result to the MCU through Bridge to show on the LED matrix.
import os
from arduino.app_utils import App, Bridge, Frame
from arduino.app_bricks.web_ui import WebUI

from digit_model import DigitModel
from matrix_display import build_frame

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "digit_cnn.onnx")
model = DigitModel(MODEL_PATH)
ui = WebUI()


def show_on_matrix(digit=None, conf=0.0):
    try:
        Bridge.call("draw", Frame(build_frame(digit, conf)).to_board_bytes())
    except Exception as e:
        print(f"[matrix] draw failed: {e}", flush=True)


def predict(payload: dict):
    pixels = payload.get("pixels", [])
    if len(pixels) != 784:
        return {"error": "need 784 pixels"}
    digit, probs, ms = model.predict(pixels)
    print(f"pred={digit} conf={probs[digit]:.3f} infer={ms:.2f}ms", flush=True)
    show_on_matrix(digit, probs[digit])
    return {"digit": digit, "probs": probs, "ms": ms}


def clear():
    show_on_matrix(None)
    return {"ok": True}


ui.expose_api(method="POST", path="/predict", function=predict)
ui.expose_api(method="POST", path="/clear", function=clear)

show_on_matrix(None)
print("Digit Recognizer ready", flush=True)
App.run()
