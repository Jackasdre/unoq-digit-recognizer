import time
import numpy as np
import onnxruntime as ort

MEAN, STD = 0.1307, 0.3081   # same as transforms.Normalize in training


class DigitModel:
    def __init__(self, path):
        self.sess = ort.InferenceSession(path, providers=["CPUExecutionProvider"])

    def predict(self, pixels):
        """pixels: 784 values in 0~1 (white digit on black, 28x28, row-major)"""
        x = np.asarray(pixels, dtype=np.float32).reshape(1, 1, 28, 28)
        x = (x - MEAN) / STD
        t0 = time.perf_counter()
        logits = self.sess.run(None, {"input": x})[0][0]
        ms = (time.perf_counter() - t0) * 1000
        p = np.exp(logits - logits.max())
        p /= p.sum()
        return int(p.argmax()), p.tolist(), ms
