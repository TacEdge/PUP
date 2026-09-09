#!/usr/bin/env python3
"""
Lift an LDF level glyph from a straight-on photograph of the Leadership
Development System poster.  The badge is a white disc inside a black ring;
we fit that ring, threshold the glyph against the local background so
glare gradients cancel, cut on the fitted circle, drop specks, and write a
black-on-transparent PNG whose disc radius is 0.965 of the half-width.

    python3 extract_ldf_badge.py photo.jpg cx cy r out.png
        cx, cy, r: rough badge centre and radius in the photo's own pixels
"""

import math
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps

DISC_FRACTION = 0.965


def extract(photo, cx, cy, r, out):
    im = Image.open(photo)
    R = int(r * 1.25)
    crop = im.crop((int(cx - R), int(cy - R), int(cx + R), int(cy + R)))
    g = np.asarray(ImageOps.grayscale(crop)).astype(np.float32)
    h, w = g.shape
    cx0, cy0 = w / 2, h / 2
    solid = g < 105
    # the ring's inner edge along 360 rays, scanning inward from outside the
    # ring: the ring is the first dark band met, so glyph parts cannot mislead
    pts = []
    for k in range(360):
        a = math.radians(k)
        run = 0
        for rr in range(int(r * 1.24), int(r * 0.7), -1):
            x = int(round(cx0 + rr * math.cos(a)))
            y = int(round(cy0 + rr * math.sin(a)))
            inside = 0 <= x < w and 0 <= y < h
            if inside and solid[y, x]:
                run += 1
            else:
                if run >= 15:
                    pts.append((cx0 + (rr + 1) * math.cos(a), cy0 + (rr + 1) * math.sin(a)))
                    break
                run = 0
    pts = np.array(pts)

    def fit(p):
        A = np.c_[2 * p[:, 0], 2 * p[:, 1], np.ones(len(p))]
        b = (p ** 2).sum(1)
        sol, *_ = np.linalg.lstsq(A, b, rcond=None)
        return sol[0], sol[1], math.sqrt(sol[2] + sol[0] ** 2 + sol[1] ** 2)

    fx, fy, fr = fit(pts)
    good = np.abs(np.hypot(pts[:, 0] - fx, pts[:, 1] - fy) - fr) < 6
    fx, fy, fr = fit(pts[good])
    print(f"ring: centre offset ({fx - cx0:.1f}, {fy - cy0:.1f}) radius {fr:.1f} from {good.sum()} rays")

    blur = np.asarray(ImageOps.grayscale(crop).filter(ImageFilter.GaussianBlur(25))).astype(np.float32)
    dark = (g < blur - 28) | (g < 110)      # local contrast, plus absolute dark beside the ring
    mask = np.asarray(Image.fromarray((dark * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7))) > 127
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.hypot(xx - fx, yy - fy)
    cut = fr * DISC_FRACTION
    mask &= d < cut

    # drop specks: connected components under 400 px
    lab = np.zeros(mask.shape, dtype=np.int32)
    n = 0
    sizes = {}
    for y0 in range(h):
        for x0 in range(w):
            if mask[y0, x0] and lab[y0, x0] == 0:
                n += 1
                lab[y0, x0] = n
                stack = [(y0, x0)]
                c = 0
                while stack:
                    y, x = stack.pop()
                    c += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        y2, x2 = y + dy, x + dx
                        if 0 <= y2 < h and 0 <= x2 < w and mask[y2, x2] and lab[y2, x2] == 0:
                            lab[y2, x2] = n
                            stack.append((y2, x2))
                sizes[n] = c
    keep = np.isin(lab, [k for k, v in sizes.items() if v >= 400])
    print(f"components kept {sum(1 for v in sizes.values() if v >= 400)} of {n}")

    soft = Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    a = np.clip((np.asarray(soft).astype(np.float32) - 90) * 2.2, 0, 255).astype(np.uint8)
    side = int(round(cut * 2 / DISC_FRACTION))
    half = side / 2
    out_a = np.zeros((side, side), dtype=np.uint8)
    ox, oy = int(round(fx - half)), int(round(fy - half))
    src = a[max(oy, 0):oy + side, max(ox, 0):ox + side]
    out_a[max(-oy, 0):max(-oy, 0) + src.shape[0], max(-ox, 0):max(-ox, 0) + src.shape[1]] = src
    rgba = np.zeros((side, side, 4), dtype=np.uint8)
    rgba[..., 3] = out_a
    Image.fromarray(rgba, "RGBA").save(out)
    prev = Image.new("L", (side, side), 255)
    prev.paste(0, mask=Image.fromarray(out_a))
    prev.save(out.replace(".png", "-preview.png"))
    print(f"wrote {out} ({side}px)")


if __name__ == "__main__":
    photo, cx, cy, r, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    extract(photo, cx, cy, r, out)
