#!/usr/bin/env python3
"""Genera assets/cover-background.png (2048 x 1152) con los tokens de Terracotta.

Reproduce la EJECUCIÓN del fondo de portada del sistema de Fer (tres paneles verticales, un glow
semicircular en el borde izquierdo de cada panel a media altura, viñeteo vertical a burgundy en los
paneles estrechos y caída radial roja a burgundy en el panel ancho), pero con la paleta de Terracotta
leída de colors_and_type.css (--burgundy, --red, --orange, --yellow). Si la paleta cambia, se vuelve
a ejecutar este script.
"""
import re, pathlib
import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
css = (HERE.parent / "colors_and_type.css").read_text(encoding="utf-8")
def tok(name):
    h = re.search(r"--%s:\s*(#[0-9A-Fa-f]{6})" % name, css).group(1)
    return np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], dtype=float)
BURG, RED, ORANGE, YELLOW = tok("burgundy"), tok("red"), tok("orange"), tok("yellow")

W, H = 2048, 1152
S = W / 2000.0                      # la geometría se definió sobre 2000 x 1125
CY = 560 * S                        # altura del centro de los glows (50% del alto)
X1, X2 = 129 * S, 356 * S           # bordes de los paneles

# rampa de calor: 0 burgundy, 0.45 rojo, 0.75 naranja, 1.0 amarillo (luz)
STOPS = [(0.0, BURG), (0.45, RED), (0.75, ORANGE), (1.0, YELLOW)]
def ramp(t):
    t = np.clip(t, 0, 1)
    out = np.zeros(t.shape + (3,))
    for (t0, c0), (t1, c1) in zip(STOPS[:-1], STOPS[1:]):
        m = (t >= t0) & (t <= t1)
        k = ((t - t0) / (t1 - t0))[m][:, None]
        out[m] = c0 + (c1 - c0) * k
    return out

yy, xx = np.mgrid[0:H, 0:W].astype(float)
t = np.zeros((H, W))

def piece(r, pts):                   # interpolación lineal por tramos de r -> calor
    xs, ys = zip(*pts)
    return np.interp(r, xs, ys)

# panel 3 (ancho): glow centrado en su borde izquierdo, caída circular a burgundy
m3 = xx >= X2
r3 = np.hypot(xx - X2, yy - CY) / S
t3 = piece(r3, [(0, 1.0), (60, .90), (144, .75), (350, .45), (850, 0.0)])
t[m3] = t3[m3]

# panel 2 (medio): glow pequeño sobre campo rojo con viñeteo vertical
m2 = (xx >= X1) & (xx < X2)
r2 = np.hypot(xx - X1, yy - CY) / S
u = 1 - np.abs(yy - CY) / CY
v2 = 0.45 * np.clip(u / 0.54, 0, 1)
t2 = np.maximum(piece(r2, [(0, 1.0), (28, .92), (68, .84), (118, .75), (170, .55), (230, .45), (330, 0.0)]), v2)
t[m2] = t2[m2]

# panel 1 (izquierdo): igual que el 2 con viñeteo más lento
m1 = xx < X1
r1 = np.hypot(xx - 0, yy - CY) / S
v1 = 0.47 * np.clip((u - 0.15) / 0.60, 0, 1)
t1 = np.maximum(piece(r1, [(0, 1.0), (20, .93), (50, .85), (85, .75), (130, .50), (260, 0.0)]), v1)
t[m1] = t1[m1]

img = ramp(t).clip(0, 255).astype(np.uint8)
out = HERE / "assets" / "cover-background.png"
Image.fromarray(img, "RGB").save(out, optimize=True)
print("OK", out, img.shape)
