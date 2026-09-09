"""
Vector glyphs for the seven LDF levels, redrawn from the NZDF Leadership
Development System poster's icon set: a person (Lead Self), a team cluster
(Lead Teams), leaders wearing the L badge (Lead Leaders), a circuit (Lead
Systems), a lit bulb with a person inside (Lead Capability), a connected
network of bulbs (Lead Integrated Capability) and a building (Lead
Organisation).  Each is drawn inside a circular badge with PyMuPDF shapes so
it prints crisply at any size.

    badge(page, cx, cy, radius, level_index, color, fill)
"""

import math

import pymupdf


def _person(sh, x, y, s, color, fill_body=True):
    """A simple figure centred at (x, y), height about 1.3 * s."""
    sh.draw_circle((x, y - 0.42 * s), 0.17 * s)
    sh.finish(color=None, fill=color)
    r = pymupdf.Rect(x - 0.24 * s, y - 0.2 * s, x + 0.24 * s, y + 0.62 * s)
    sh.draw_rect(r, radius=(0.35, 0.18))
    sh.finish(color=None, fill=color if fill_body else None)


def _badge_L(page, x, y, size, color):
    page.insert_text((x - size * 0.3, y + size * 0.35), "L", fontsize=size, fontname="Arial-Bold", color=color)


def icon_self(page, sh, cx, cy, r, color, white):
    _person(sh, cx, cy, 1.2 * r, color)
    sh.commit()
    _badge_L(page, cx, cy + 0.2 * r, 0.6 * r, white)


def icon_teams(page, sh, cx, cy, r, color, white):
    s = 0.34 * r
    rows = [(-0.62, 3), (-0.05, 4), (0.52, 3)]
    for dy, n in rows:
        for k in range(n):
            dx = (k - (n - 1) / 2) * 0.46
            _person(sh, cx + dx * r, cy + dy * r, s, color)
    sh.commit()


def icon_leaders(page, sh, cx, cy, r, color, white):
    s = 0.62 * r
    pts = [(0, -0.6), (-0.58, 0.08), (0.58, 0.08), (0, 0.62)]
    for dx, dy in pts:
        _person(sh, cx + dx * r, cy + dy * r, s, color)
    sh.commit()
    for dx, dy in pts:
        _badge_L(page, cx + dx * r, cy + dy * r + 0.2 * s, 0.42 * s, white)


def icon_systems(page, sh, cx, cy, r, color, white):
    nodes = [(-0.62, -0.5), (0.05, -0.62), (0.62, -0.2), (-0.55, 0.25), (0.15, 0.4), (0.6, 0.6), (-0.2, -0.1)]
    traces = [[(-0.62, -0.5), (-0.2, -0.5), (-0.2, -0.1)],
              [(0.05, -0.62), (0.05, -0.1), (-0.2, -0.1)],
              [(0.62, -0.2), (0.3, -0.2), (0.3, 0.4), (0.15, 0.4)],
              [(-0.55, 0.25), (-0.2, 0.25), (-0.2, -0.1)],
              [(0.15, 0.4), (0.15, 0.6), (0.6, 0.6)],
              [(-0.2, 0.25), (-0.2, 0.6), (0.15, 0.6)]]
    for t in traces:
        sh.draw_polyline([(cx + x * r, cy + y * r) for x, y in t])
        sh.finish(color=color, width=max(0.6, 0.09 * r), closePath=False)
    for x, y in nodes:
        sh.draw_circle((cx + x * r, cy + y * r), 0.13 * r)
        sh.finish(color=color, fill=white, width=max(0.6, 0.09 * r))
    sh.commit()


def icon_capability(page, sh, cx, cy, r, color, white):
    bulb_c = (cx, cy - 0.1 * r)
    sh.draw_circle(bulb_c, 0.46 * r)
    sh.finish(color=color, width=max(0.6, 0.09 * r))
    base = pymupdf.Rect(cx - 0.17 * r, cy + 0.36 * r, cx + 0.17 * r, cy + 0.66 * r)
    sh.draw_rect(base)
    sh.finish(color=None, fill=color)
    for k in range(7):
        a = math.pi * (1.0 + k / 6.0)          # rays over the top half
        x0, y0 = bulb_c[0] + 0.6 * r * math.cos(a), bulb_c[1] + 0.6 * r * math.sin(a)
        x1, y1 = bulb_c[0] + 0.82 * r * math.cos(a), bulb_c[1] + 0.82 * r * math.sin(a)
        sh.draw_line((x0, y0), (x1, y1))
        sh.finish(color=color, width=max(0.6, 0.09 * r))
    _person(sh, cx, cy - 0.08 * r, 0.5 * r, color)
    sh.commit()
    _badge_L(page, cx, cy + 0.02 * r, 0.24 * r, white)


def icon_integrated(page, sh, cx, cy, r, color, white):
    grid = [(-0.55, -0.55), (0, -0.55), (0.55, -0.55), (-0.55, 0), (0, 0), (0.55, 0), (-0.55, 0.55), (0, 0.55), (0.55, 0.55)]
    pts = [(cx + x * r, cy + y * r) for x, y in grid]
    links = [(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8), (0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8),
             (0, 4), (4, 8), (2, 4), (4, 6)]
    for a, b in links:
        sh.draw_line(pts[a], pts[b])
        sh.finish(color=color, width=max(0.5, 0.06 * r))
    for x, y in pts:
        sh.draw_circle((x, y - 0.03 * r), 0.13 * r)
        sh.finish(color=color, fill=white, width=max(0.6, 0.08 * r))
        sh.draw_rect(pymupdf.Rect(x - 0.06 * r, y + 0.1 * r, x + 0.06 * r, y + 0.18 * r))
        sh.finish(color=None, fill=color)
    sh.commit()


def icon_organisation(page, sh, cx, cy, r, color, white):
    b = pymupdf.Rect(cx - 0.42 * r, cy - 0.7 * r, cx + 0.42 * r, cy + 0.72 * r)
    sh.draw_rect(b)
    sh.finish(color=None, fill=color)
    cols, rows = 3, 5
    for i in range(cols):
        for j in range(rows):
            if j == 0 and i == 1:
                continue
            x = b.x0 + 0.1 * r + i * 0.26 * r
            y = b.y0 + 0.36 * r + j * 0.24 * r
            sh.draw_rect(pymupdf.Rect(x, y, x + 0.14 * r, y + 0.14 * r))
            sh.finish(color=None, fill=white)
    sh.draw_rect(pymupdf.Rect(cx - 0.12 * r, b.y0 + 0.06 * r, cx + 0.12 * r, b.y0 + 0.3 * r))
    sh.finish(color=None, fill=white)
    sh.commit()
    _badge_L(page, cx, b.y0 + 0.18 * r, 0.26 * r, color)


ICONS = [icon_self, icon_teams, icon_leaders, icon_systems, icon_capability, icon_integrated, icon_organisation]


def badge(page, cx, cy, radius, level_index, color, fill=(1, 1, 1), ring=True):
    """Circular badge with the level's glyph.  Requires the page to have the
    fonts 'Arial' and 'Arial-Bold' registered."""
    sh = page.new_shape()
    sh.draw_circle((cx, cy), radius)
    sh.finish(color=color if ring else None, fill=fill, width=max(0.7, radius * 0.07))
    sh.commit()
    sh = page.new_shape()
    ICONS[level_index](page, sh, cx, cy, radius * 0.72, color, fill)
