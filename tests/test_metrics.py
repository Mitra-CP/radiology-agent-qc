import numpy as np
from src.common.metrics import entropy_focus_criterion, fber

def test_metrics_shapes():
    img = np.random.rand(64,64)
    bg = np.random.rand(64,64)*0.1
    assert entropy_focus_criterion(img) > 0
    assert fber(img, bg) > 1e-6
