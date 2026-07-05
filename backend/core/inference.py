import os
# Force Keras to use PyTorch as its backend
os.environ["KERAS_BACKEND"] = "torch"

import keras
import torch
import numpy as np
import cv2
import threading
import random
from PIL import Image

OPTIMAL_THRESHOLD = 0.5
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.normpath(os.path.join(BASE_DIR, "../custom_cnn/student_cnn.keras"))
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")