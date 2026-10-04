#!/usr/bin/env python3
"""Generate kerfwork logo SVGs: icon-only + Bricolage Grotesque wordmark lockup."""

import hashlib

BROWN      = "#5C3B2A"
TAN        = "#D0B284"
BLUE       = "#52748E"
DOT_COLOR  = "#C99E6B"
SQ_COLOR   = "#BE8F58"
DASH_COLOR = "#C0905A"

SQ_SIZE = 200.0
TAN_W, TAN_H = 42.0, 92.0
BLUE_W, BLUE_H = TAN_W, 22.0
GRID_N = 8
CELL = SQ_SIZE / GRID_N
MARK_H = SQ_SIZE + BLUE_H  # 222


def mark_type(row, col):
    """Deterministically pick a mark for each grid cell."""
    h = int(hashlib.md5(f"kerfwork-{row}-{col}".encode()).hexdigest(), 16)
    return {0: "dot", 1: "square", 2: "dash"}.get(h % 6)


def mark_body(sq_x, sq_y):
    """SVG lines for the full mark with square top-left at (sq_x, sq_y)."""
    L = []
    L.append(f'    <rect x="{sq_x:.1f}" y="{sq_y:.1f}" width="{SQ_SIZE}" height="{SQ_SIZE}" fill="{BROWN}"/>')
    L.append('    <g id="data-grid">')
    for row in range(GRID_N):
        for col in range(GRID_N):
            cx = sq_x + col * CELL + CELL / 2
            cy = sq_y + row * CELL + CELL / 2
            m = mark_type(row, col)
            if m == "dot":
                L.append(f'      <circle cx="{cx:.1f}" cy="{cy:.1f}" r="3" fill="{DOT_COLOR}"/>')
            elif m == "square":
                L.append(f'      <rect x="{cx-3:.1f}" y="{cy-3:.1f}" width="6" height="6" fill="{SQ_COLOR}"/>')
            elif m == "dash":
                L.append(f'      <rect x="{cx-5:.1f}" y="{cy-1.5:.1f}" width="10" height="3" fill="{DASH_COLOR}"/>')
    L.append('    </g>')
    # Tan kerf slot
    tan_x = sq_x + SQ_SIZE / 2 - TAN_W / 2
    L.append(f'    <rect x="{tan_x:.1f}" y="{sq_y:.1f}" width="{TAN_W}" height="{TAN_H}" fill="{TAN}"/>')
    # Blue saw cap above the square
    blue_x = sq_x + SQ_SIZE / 2 - BLUE_W / 2
    L.append(f'    <rect x="{blue_x:.1f}" y="{sq_y - BLUE_H:.1f}" width="{BLUE_W}" height="{BLUE_H}" fill="{BLUE}"/>')
    return L


# ── Icon only (400×400, mark vertically centred) ──
ICON = 400.0
sq_x = (ICON - SQ_SIZE) / 2
sq_y = (ICON - MARK_H) / 2 + BLUE_H
icon = [f'<svg width="{ICON:.0f}" height="{ICON:.0f}" viewBox="0 0 {ICON:.0f} {ICON:.0f}" xmlns="http://www.w3.org/2000/svg">',
        '  <g id="kerfwork-icon">']
icon += mark_body(sq_x, sq_y)
icon += ['  </g>', '</svg>']
with open("/Users/sjanes/work26/kerfwork-icon.svg", "w") as f:
    f.write("\n".join(icon))

# ── Lockup (icon + Bricolage wordmark) ──
W, H = 900, 400
sq_x = 60.0
sq_y = (H - MARK_H) / 2 + BLUE_H
lock = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
        '  <g id="kerfwork-mark">']
lock += mark_body(sq_x, sq_y)
lock += ['  </g>',
         '  <g id="wordmark">',
         '    <text x="330" y="200" font-family="Bricolage Grotesque" font-size="58" '
         'font-weight="700" fill="' + BROWN + '" dominant-baseline="middle" '
         'style="font-variation-settings: \'opsz\' 96, \'wdth\' 100, \'wght\' 700;">kerfwork</text>',
         '  </g>', '</svg>']
with open("/Users/sjanes/work26/kerfwork-lockup.svg", "w") as f:
    f.write("\n".join(lock))

print("Wrote kerfwork-icon.svg and kerfwork-lockup.svg")
