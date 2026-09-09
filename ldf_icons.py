"""
Vector glyphs for the seven LDF levels, mapped from the NZDF Leadership
Development System poster's icon set:

  Lead Self                  one figure wearing the L badge
  Lead Teams                 twelve figures in a diamond lattice
  Lead Leaders               four L-badged figures in a diamond
  Lead Systems               a circuit: right-angled traces ending in nodes
  Lead Capability            a lit bulb with an L-badged figure inside
  Lead Integrated Capability nine small bulbs, joined as a wheel and rim
  Lead Organisation          a stepped tower block with an L on the roof

Drawn with PyMuPDF shapes inside a circular badge, so they print crisply.

    badge(page, cx, cy, radius, level_index, color, fill)
"""

import math
import os

import pymupdf

# Glyphs taken directly from photographs of the poster, where a clean
# straight-on close-up exists: level index -> (RGBA file, disc radius as a
# fraction of the image half-width).  These override the drawn glyph.
RASTER = {
    3: ("./assets/ldf-icon-lead-systems.png", 0.965),
    5: ("./assets/ldf-icon-lead-integrated-capability.png", 0.965),
}


# ----------------------------------------------------------------- figure --
def _figure(sh, x, y, s, color):
    """The poster's figure: round head, broad torso, narrower legs block.
    Centred on (x, y); overall height about 1.25 * s."""
    sh.draw_circle((x, y - 0.46 * s), 0.15 * s)
    sh.finish(color=None, fill=color)
    torso = pymupdf.Rect(x - 0.26 * s, y - 0.27 * s, x + 0.26 * s, y + 0.2 * s)
    sh.draw_rect(torso, radius=(0.2, 0.12))
    sh.finish(color=None, fill=color)
    legs = pymupdf.Rect(x - 0.17 * s, y + 0.18 * s, x + 0.17 * s, y + 0.66 * s)
    sh.draw_rect(legs)
    sh.finish(color=None, fill=color)


def _L(page, x, y, size, color):
    """A bold L, centred at (x, y)."""
    w = pymupdf.get_text_length("L", fontname="helvetica-bold", fontsize=size)
    page.insert_text((x - w / 2, y + size * 0.36), "L", fontsize=size, fontname="Arial-Bold", color=color)


def _bulb(sh, x, y, s, color, white, lw):
    """Bulb outline centred at (x, y): circle plus a screw base."""
    sh.draw_circle((x, y - 0.12 * s), 0.46 * s)
    sh.finish(color=color, fill=white, width=lw)
    base = pymupdf.Rect(x - 0.17 * s, y + 0.3 * s, x + 0.17 * s, y + 0.62 * s)
    sh.draw_rect(base, radius=(0.15, 0.25))
    sh.finish(color=None, fill=color)
    for k in (0.4, 0.48):
        sh.draw_line((x - 0.17 * s, y + k * s), (x + 0.17 * s, y + k * s))
        sh.finish(color=white, width=lw * 0.6)


def _rounded_path(sh, pts, rr):
    """A polyline whose interior corners are rounded with radius rr."""
    if len(pts) < 3:
        sh.draw_polyline(pts)
        return
    cur = pts[0]
    for k in range(1, len(pts) - 1):
        a, b, c = pts[k - 1], pts[k], pts[k + 1]
        d1 = math.hypot(b[0] - a[0], b[1] - a[1])
        d2 = math.hypot(c[0] - b[0], c[1] - b[1])
        rk = min(rr, d1 / 2, d2 / 2)
        p_in = (b[0] - (b[0] - a[0]) / d1 * rk, b[1] - (b[1] - a[1]) / d1 * rk)
        p_out = (b[0] + (c[0] - b[0]) / d2 * rk, b[1] + (c[1] - b[1]) / d2 * rk)
        sh.draw_line(cur, p_in)
        sh.draw_curve(p_in, b, p_out)
        cur = p_out
    sh.draw_line(cur, pts[-1])


# ------------------------------------------------------------------ icons --
def icon_self(page, sh, cx, cy, r, color, white):
    _figure(sh, cx, cy, 1.35 * r, color)
    sh.commit()
    _L(page, cx - 0.06 * r, cy - 0.02 * r, 0.62 * r, white)


def icon_teams(page, sh, cx, cy, r, color, white):
    s = 0.36 * r
    rows = [(-0.92, 1), (-0.55, 2), (-0.18, 3), (0.19, 3), (0.56, 2), (0.93, 1)]
    for dy, n in rows:
        for k in range(n):
            dx = (k - (n - 1) / 2) * 0.5
            _figure(sh, cx + dx * r, cy + dy * r, s, color)
    sh.commit()


def icon_leaders(page, sh, cx, cy, r, color, white):
    s = 0.62 * r
    pts = [(0, -0.6), (-0.58, 0.05), (0.58, 0.05), (0, 0.66)]
    for dx, dy in pts:
        _figure(sh, cx + dx * r, cy + dy * r, s, color)
    sh.commit()
    for dx, dy in pts:
        _L(page, cx + dx * r - 0.03 * s, cy + dy * r - 0.03 * s, 0.3 * s, white)


def icon_systems(page, sh, cx, cy, r, color, white):
    """Circuit: ring nodes spread through the badge, traces that turn at
    rounded right angles, several running out to the badge rim."""
    lw = max(0.6, 0.09 * r)
    R = 1.6                        # beyond the badge rim in glyph units, so rim traces run off the edge
    nodes = [(-0.10, -0.78), (0.22, -0.46), (0.62, -0.46), (0.46, -0.06), (-0.50, 0.00),
             (0.14, 0.22), (-0.70, 0.46), (0.50, 0.56), (0.06, 0.82)]
    traces = [
        [(-0.10, -0.78), (0.62, -0.78), (0.62, -0.46)],                    # top node across and down to C
        [(-R, -0.30), (-0.50, -0.30), (-0.50, 0.00)],                       # in from the left rim to E
        [(0.22, -0.46), (-0.16, -0.46), (-0.16, 0.22), (0.14, 0.22)],       # B round to F
        [(0.62, -0.46), (R, -0.46)],                                        # C out to the right rim
        [(0.46, -0.06), (0.86, -0.06), (0.86, R)],                          # D out to the lower right rim
        [(0.14, 0.22), (0.46, 0.22), (0.46, -0.06)],                        # F up to D
        [(-0.50, 0.00), (-0.50, 0.46), (-0.70, 0.46)],                      # E down to G
        [(-0.70, 0.46), (-0.70, 0.66), (0.06, 0.66), (0.06, 0.82)],         # G along the bottom to I
        [(0.14, 0.22), (0.14, 0.56), (0.50, 0.56)],                         # F down to H
        [(0.50, 0.56), (0.50, R)],                                          # H out to the bottom rim
    ]
    for t in traces:
        _rounded_path(sh, [(cx + x * r, cy + y * r) for x, y in t], 0.14 * r)
        sh.finish(color=color, width=lw, closePath=False, lineJoin=1, lineCap=1)
    for x, y in nodes:
        sh.draw_circle((cx + x * r, cy + y * r), 0.13 * r)
        sh.finish(color=color, fill=white, width=lw)
    sh.commit()


def icon_capability(page, sh, cx, cy, r, color, white):
    lw = max(0.6, 0.085 * r)
    _bulb(sh, cx, cy + 0.02 * r, 1.25 * r, color, white, lw)
    # seven rays: horizontals, upper and lower diagonals, and the top
    for deg in (180, 225, 270, 315, 0, 135, 45):
        a = math.radians(deg)
        x0, y0 = cx + 0.72 * r * math.cos(a), cy - 0.12 * r + 0.72 * r * math.sin(a)
        x1, y1 = cx + 0.95 * r * math.cos(a), cy - 0.12 * r + 0.95 * r * math.sin(a)
        sh.draw_line((x0, y0), (x1, y1))
        sh.finish(color=color, width=lw)
    _figure(sh, cx, cy - 0.1 * r, 0.62 * r, color)
    sh.commit()
    _L(page, cx - 0.03 * r, cy - 0.11 * r, 0.26 * r, white)


def icon_integrated(page, sh, cx, cy, r, color, white):
    lw = max(0.5, 0.05 * r)
    grid = [(-0.6, -0.6), (0, -0.6), (0.6, -0.6), (-0.6, 0), (0, 0), (0.6, 0), (-0.6, 0.6), (0, 0.6), (0.6, 0.6)]
    pts = [(cx + x * r, cy + y * r) for x, y in grid]
    rim = [(0, 1), (1, 2), (2, 5), (5, 8), (8, 7), (7, 6), (6, 3), (3, 0)]
    spokes = [(4, k) for k in range(9) if k != 4]
    for a, b in rim + spokes:
        sh.draw_line(pts[a], pts[b])
        sh.finish(color=color, width=lw)
    for x, y in pts:
        _bulb(sh, x, y - 0.02 * r, 0.42 * r, color, white, lw * 1.3)
        sh.draw_circle((x, y - 0.12 * r), 0.045 * r)
        sh.finish(color=None, fill=color)
        sh.draw_rect(pymupdf.Rect(x - 0.035 * r, y - 0.09 * r, x + 0.035 * r, y + 0.03 * r))
        sh.finish(color=None, fill=color)
    sh.commit()


def icon_organisation(page, sh, cx, cy, r, color, white):
    # stepped tower: the left third rises higher and carries the L
    x0, x1 = cx - 0.42 * r, cx + 0.42 * r
    top_l, top_r, bottom = cy - 0.9 * r, cy - 0.62 * r, cy + 0.88 * r
    step_x = x0 + 0.34 * r
    sh.draw_polyline([(x0, top_l), (step_x, top_l), (step_x, top_r), (x1, top_r), (x1, bottom), (x0, bottom)])
    sh.finish(color=None, fill=color, closePath=True)
    # windows: three columns, rows down the block; a door in the bottom middle
    win = 0.15 * r
    cols = [x0 + 0.08 * r, x0 + 0.34 * r, x0 + 0.6 * r]
    rows = [top_r + 0.1 * r + k * 0.24 * r for k in range(6)]
    for i, wx in enumerate(cols):
        for j, wy in enumerate(rows):
            if j == 5 and i == 1:
                sh.draw_rect(pymupdf.Rect(wx, wy, wx + win, bottom))     # door
            else:
                sh.draw_rect(pymupdf.Rect(wx, wy, wx + win, wy + win))
            sh.finish(color=None, fill=white)
    # the L on the roof of the taller part
    lbox = pymupdf.Rect(x0 + 0.06 * r, top_l + 0.06 * r, step_x - 0.06 * r, top_r + 0.02 * r)
    sh.draw_rect(lbox)
    sh.finish(color=None, fill=white)
    sh.commit()
    _L(page, (lbox.x0 + lbox.x1) / 2, (lbox.y0 + lbox.y1) / 2, 0.22 * r, color)


ICONS = [icon_self, icon_teams, icon_leaders, icon_systems, icon_capability, icon_integrated, icon_organisation]
SCALE = [0.7, 0.7, 0.7, 0.6, 0.7, 0.7, 0.7]      # glyph radius as a fraction of the badge radius


def badge(page, cx, cy, radius, level_index, color, fill=(1, 1, 1), ring=True):
    """Circular badge with the level's glyph.  The page must have the
    fonts 'Arial' and 'Arial-Bold' registered."""
    sh = page.new_shape()
    sh.draw_circle((cx, cy), radius)
    sh.finish(color=None, fill=fill)
    sh.commit()
    if level_index in RASTER and os.path.exists(RASTER[level_index][0]):
        path, frac = RASTER[level_index]
        half = radius / frac                       # image half-width so the disc matches the badge
        page.insert_image(pymupdf.Rect(cx - half, cy - half, cx + half, cy + half), filename=path)
    else:
        sh = page.new_shape()
        ICONS[level_index](page, sh, cx, cy, radius * SCALE[level_index], color, fill)
    if ring:
        # the poster's ring, drawn last so it covers the cut edge of a raster glyph
        sh = page.new_shape()
        sh.draw_circle((cx, cy), radius * 0.96)
        sh.finish(color=color, fill=None, width=max(0.8, radius * 0.1))
        sh.commit()
