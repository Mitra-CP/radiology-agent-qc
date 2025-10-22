import numpy as np
from skimage.filters import laplace
from skimage.util import img_as_float
from typing import Dict

def entropy_focus_criterion(img) -> float:
    # simplified EFC proxy
    F = img_as_float(img)
    F = F / (np.sqrt((F**2).sum()) + 1e-8)
    eps = 1e-12
    E = -(F * np.log(F + eps)).sum()
    N = F.size
    return float(E / np.sqrt(N))

def fber(foreground: np.ndarray, background: np.ndarray) -> float:
    fg = np.median(np.abs(foreground)**2) + 1e-6
    bg = np.median(np.abs(background)**2) + 1e-6
    return float(fg / bg)

def contrast_per_pixel(img: np.ndarray) -> float:
    return float(laplace(img, ksize=3).mean())

def simple_motion_likelihood(img: np.ndarray) -> float:
    # very naive proxy using EFC normalized
    efc = entropy_focus_criterion(img)
    return float(min(1.0, max(0.0, efc)))
