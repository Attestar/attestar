"""Emit the Attestar brand assets (logo, icon, banner) from one palette.

Run from the repository root:

    python3 assets/generate.py

Rasters are exported separately from the SVGs (1024px logo, 256px icon).
"""

import math
import random

# ---- Attestar palette: cyan on deep space -------------------------------
GROUND  = "#05070F"   # near-black navy
DEEP    = "#0A1024"   # panel
PRIMARY = "#22D3EE"   # electric cyan
BRIGHT  = "#67E8F9"   # cyan light
DIM     = "#0891B2"   # cyan deep
WHITE   = "#FFFFFF"
MUTED   = "#7C8BA8"
TEXT    = "#A9BBD4"

FONT = "Inter,'Segoe UI',Helvetica,Arial,sans-serif"

def hexagon(cx, cy, r, rot=-90):
    """Pointy-top hexagon vertices."""
    return [(cx + r*math.cos(math.radians(rot + 60*i)),
             cy + r*math.sin(math.radians(rot + 60*i))) for i in range(6)]

def pts(v):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in v)

def sparkle(ro, q):
    """4-point sparkle centred on the origin."""
    return (f"M0,{-ro} Q{q},{-q} {ro},0 Q{q},{q} 0,{ro} "
            f"Q{-q},{q} {-ro},0 Q{-q},{-q} 0,{-ro} Z")

def starfield(seed, n, w, h, rmin=0.8, rmax=2.4, op=0.55):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.uniform(rmin, rmax)
        o = rnd.uniform(0.15, op)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{WHITE}" opacity="{o:.2f}"/>')
    return "\n    ".join(out)

def defs(idp, clip=False):
    """Shared gradient defs, id-prefixed so logo+banner can coexist inline."""
    clipdef = (f'    <clipPath id="{idp}clip">\n'
               f'      <rect width="512" height="512" rx="112"/>\n'
               f'    </clipPath>\n') if clip else ""
    return f'''  <defs>
    <linearGradient id="{idp}cyan" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{BRIGHT}"/>
      <stop offset="55%" stop-color="{PRIMARY}"/>
      <stop offset="100%" stop-color="{DIM}"/>
    </linearGradient>
    <linearGradient id="{idp}star" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0%" stop-color="{WHITE}"/>
      <stop offset="45%" stop-color="{BRIGHT}"/>
      <stop offset="100%" stop-color="{PRIMARY}"/>
    </linearGradient>
    <linearGradient id="{idp}ground" x1="0" y1="0" x2="0.7" y2="1">
      <stop offset="0%" stop-color="{DEEP}"/>
      <stop offset="100%" stop-color="{GROUND}"/>
    </linearGradient>
    <radialGradient id="{idp}glow">
      <stop offset="0%" stop-color="{PRIMARY}" stop-opacity="0.45"/>
      <stop offset="55%" stop-color="{PRIMARY}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{PRIMARY}" stop-opacity="0"/>
    </radialGradient>
{clipdef}    <radialGradient id="{idp}core">
      <stop offset="0%" stop-color="{WHITE}" stop-opacity="0.95"/>
      <stop offset="38%" stop-color="{BRIGHT}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{BRIGHT}" stop-opacity="0"/>
    </radialGradient>
  </defs>'''

def mark(cx, cy, scale, idp, nodes=True, rays=True):
    """The seal-star: hexagonal seal, converging rays, node vertices, star core."""
    R  = 150 * scale
    v  = hexagon(cx, cy, R)
    sw = 14 * scale
    g  = []
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{196*scale:.1f}" fill="none" '
             f'stroke="{PRIMARY}" stroke-width="{2.5*scale:.1f}" opacity="0.16"/>')
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{170*scale:.1f}" fill="url(#{idp}glow)"/>')
    if rays:
        for x, y in v:
            g.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{cx:.1f}" y2="{cy:.1f}" '
                     f'stroke="{PRIMARY}" stroke-width="{3*scale:.1f}" opacity="0.28"/>')
    g.append(f'<polygon points="{pts(v)}" fill="none" stroke="url(#{idp}cyan)" '
             f'stroke-width="{sw:.1f}" stroke-linejoin="round"/>')
    if nodes:
        for x, y in v:
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{11*scale:.1f}" fill="{GROUND}"/>')
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{11*scale:.1f}" fill="none" '
                     f'stroke="{BRIGHT}" stroke-width="{4*scale:.1f}"/>')
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{120*scale:.1f}" fill="url(#{idp}core)"/>')
    g.append(f'<g transform="translate({cx:.1f},{cy:.1f}) rotate(45) scale({0.70*scale:.3f})">'
             f'<path d="{sparkle(96, 12)}" fill="{PRIMARY}" opacity="0.9"/></g>')
    g.append(f'<g transform="translate({cx:.1f},{cy:.1f}) scale({scale:.3f})">'
             f'<path d="{sparkle(96, 16)}" fill="url(#{idp}star)"/></g>')
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{7*scale:.1f}" fill="{WHITE}"/>')
    return "\n    ".join(g)

# ---- 1. logo.svg (512, app-icon shape) ----------------------------------
logo = f'''<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="t">
  <title id="t">Attestar</title>
{defs("l", clip=True)}
  <rect width="512" height="512" rx="112" fill="url(#lground)"/>
  <g clip-path="url(#lclip)">
    {starfield(7, 44, 512, 512)}
  </g>
  <g>
    {mark(256, 256, 1.0, "l")}
  </g>
</svg>
'''
open("assets/logo.svg", "w").write(logo)

# ---- 2. icon.svg (64, favicon-safe: no rays, no starfield) ---------------
icon = f'''<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="t">
  <title id="t">Attestar icon</title>
{defs("i")}
  <rect width="64" height="64" rx="14" fill="url(#iground)"/>
  <g>
    <circle cx="32" cy="32" r="21" fill="url(#iglow)" opacity="0.75"/>
    <polygon points="{pts(hexagon(32, 32, 21))}" fill="none" stroke="url(#icyan)" stroke-width="4.6" stroke-linejoin="round"/>
    <g transform="translate(32,32) rotate(45) scale(0.105)"><path d="{sparkle(96, 12)}" fill="{PRIMARY}" opacity="0.9"/></g>
    <g transform="translate(32,32) scale(0.150)"><path d="{sparkle(96, 16)}" fill="url(#istar)"/></g>
  </g>
</svg>
'''
open("assets/icon.svg", "w").write(icon)

# ---- 3. banner (2048x576) ------------------------------------------------
W, H = 2048, 576
TX = 620                      # text column x
feats = "Machine Learning  ·  Zero-Knowledge Proofs  ·  Soroban  ·  Stellar"
banner = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="t">
  <title id="t">Attestar — provable ML inference on Stellar</title>
{defs("b")}
  <rect width="{W}" height="{H}" fill="url(#bground)"/>
  <g>
    {starfield(21, 130, W, H)}
  </g>

  <!-- faint constellation motif, right edge -->
  <g opacity="0.5">
    <circle cx="1806" cy="288" r="230" fill="url(#bglow)"/>
    <polygon points="{pts(hexagon(1806, 288, 212))}" fill="none" stroke="{PRIMARY}" stroke-width="2" opacity="0.22"/>
    <polygon points="{pts(hexagon(1806, 288, 154))}" fill="none" stroke="{PRIMARY}" stroke-width="2" opacity="0.30"/>
    <polygon points="{pts(hexagon(1806, 288, 96))}" fill="none" stroke="{BRIGHT}" stroke-width="2" opacity="0.38"/>
    {"".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{BRIGHT}" opacity="0.7"/>' for x, y in hexagon(1806, 288, 212))}
    {"".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{PRIMARY}" opacity="0.6"/>' for x, y in hexagon(1806, 288, 154))}
    <g transform="translate(1806,288) scale(0.38)"><path d="{sparkle(96, 16)}" fill="{BRIGHT}" opacity="0.65"/></g>
  </g>

  <!-- primary mark -->
  <g>
    {mark(330, 288, 0.86, "b")}
  </g>

  <!-- wordmark block -->
  <text x="{TX}" y="188" font-family="{FONT}" font-size="30" font-weight="600"
        letter-spacing="7.5" fill="{BRIGHT}" opacity="0.85">PROVABLE ML INFERENCE ON STELLAR</text>

  <text x="{TX-6}" y="316" font-family="{FONT}" font-size="132" font-weight="800"
        letter-spacing="-2" fill="url(#bstar)">Attestar</text>

  <rect x="{TX}" y="354" width="196" height="5" rx="2.5" fill="url(#bcyan)"/>
  <circle cx="{TX+214}" cy="356.5" r="5" fill="{BRIGHT}"/>

  <text x="{TX}" y="420" font-family="{FONT}" font-size="30" fill="{TEXT}">
    Attested ML inference, verified on-chain with zero-knowledge proofs.</text>

  <text x="{TX}" y="478" font-family="{FONT}" font-size="23" font-weight="600"
        letter-spacing="1.4" fill="{MUTED}">{feats}</text>
</svg>
'''
open("assets/banner-attestar.svg", "w").write(banner)
print("wrote assets/logo.svg, assets/icon.svg, assets/banner-attestar.svg")
