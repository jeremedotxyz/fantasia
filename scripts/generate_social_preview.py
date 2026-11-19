"""Render Ghostty-grade social preview share artwork for Fantasia CLI.

Generates 1280 x 640 PNG and vector SVG matching the aesthetic of
The NeverEnding Story and modern GPU terminals (Ghostty).

Run:
    /tmp/fantasia-env/bin/python3 scripts/generate_social_preview.py
"""

import math
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

W, H, SCALE = 1280, 640, 2

# Palette
BG = (12, 14, 20)            # #0c0e14
PANEL_BG = (18, 22, 32)      # #121620
BORDER = (46, 54, 72)        # #2e3648
INK = (235, 240, 248)        # #ebf0f8
MUTED = (125, 138, 156)      # #7d8a9c
GOLD = (218, 175, 55)        # #daaf37
GOLD_LIGHT = (245, 230, 170) # #f5e6aa
CYAN = (72, 201, 176)        # #48c9b0
ORACLE_BLUE = (0, 210, 255)  # #00d2ff
NOTHING_VOID = (224, 86, 253)# #e056fd
GREEN = (74, 222, 128)       # #4ade80
RED = (248, 113, 113)        # #f87171
AMBER = (251, 191, 36)       # #fbbf24

# Helpers
image = Image.new("RGB", (W * SCALE, H * SCALE), BG)
draw = ImageDraw.Draw(image)

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<title>FANTASIA / CLI — Ghostty-grade terminal AI operator</title>',
    '<desc>Modelled after The NeverEnding Story: AURYN token governor, Southern Oracle, and bounded context against The Nothing.</desc>',
    f'<rect width="{W}" height="{H}" fill="#0c0e14"/>',
]


def c2hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def line(points, color=BORDER, width=1.0):
    if len(points) < 2:
        return
    draw.line([(x * SCALE, y * SCALE) for x, y in points], fill=color, width=max(1, round(width * SCALE)))
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    svg.append(f'<polyline points="{coords}" fill="none" stroke="{c2hex(color)}" stroke-width="{width}"/>')


def rect(x, y, w, h, color=BORDER, fill_color=None, width=1.0, rx=0):
    if fill_color:
        draw.rectangle(
            [(x * SCALE, y * SCALE), ((x + w) * SCALE, (y + h) * SCALE)],
            fill=fill_color,
            outline=color if width > 0 else None,
            width=max(1, round(width * SCALE)) if width > 0 else 0,
        )
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c2hex(fill_color)}" stroke="{c2hex(color)}" stroke-width="{width}"/>')
    else:
        line([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], color, width)


def circle(cx, cy, r, fill_color):
    draw.ellipse([(cx - r) * SCALE, (cy - r) * SCALE, (cx + r) * SCALE, (cy + r) * SCALE], fill=fill_color)
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c2hex(fill_color)}"/>')


def text(x, y, val, size=13, color=INK, bold=False):
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    font = None
    for cand in candidates:
        try:
            font = ImageFont.truetype(cand, round(size * SCALE), index=1 if bold and cand.endswith(".ttc") else 0)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()

    draw.text((x * SCALE, y * SCALE), val, font=font, fill=color, anchor="la")
    weight = 700 if bold else 400
    svg.append(f'<text x="{x}" y="{y + size}" fill="{c2hex(color)}" font-family="Menlo, Monaco, Consolas, monospace" font-size="{size}" font-weight="{weight}">{escape(val)}</text>')


def draw_auryn_ouroboros(cx, cy, r):
    """Draw symbolic intertwined dual-ouroboros infinity curves."""
    points1 = []
    points2 = []
    steps = 90
    for i in range(steps + 1):
        t = i / steps * 2 * math.pi
        # lemniscate / infinity curve
        denom = 1 + math.sin(t) ** 2
        x = (r * 1.8 * math.cos(t)) / denom
        y = (r * 1.8 * math.sin(t) * math.cos(t)) / denom
        points1.append((cx + x, cy + y - 4))
        points2.append((cx + x, cy + y + 4))

    line(points1, GOLD, 1.8)
    line(points2, GOLD_LIGHT, 1.2)
    circle(cx - r * 1.1, cy - 4, 3, GOLD_LIGHT)
    circle(cx + r * 1.1, cy + 4, 3, GOLD)


# --- Background grid ---
for gx in range(30, W - 29, 32):
    line([(gx, 30), (gx, H - 30)], (22, 26, 38), 0.5)
for gy in range(30, H - 29, 32):
    line([(30, gy), (W - 30, gy)], (22, 26, 38), 0.5)

# Outer Ghostty Window Frame
rect(36, 36, W - 72, H - 72, BORDER, PANEL_BG, 1.2, rx=8)

# Header Bar with window controls
line([(36, 78), (W - 36, 78)], BORDER, 1.0)
circle(56, 57, 5, RED)
circle(72, 57, 5, AMBER)
circle(88, 57, 5, GREEN)

# Tabs
rect(120, 44, 114, 26, GOLD, (26, 32, 46), 1.0, rx=4)
text(130, 50, "IVORY TOWER", 11, GOLD_LIGHT, bold=True)
text(248, 50, "SOUTHERN ORACLE", 11, MUTED)
text(388, 50, "THE VOID", 11, MUTED)

text(W - 270, 50, "FANTASIA // CLI · v0.1.0", 11, MUTED, bold=True)

# Main Title Area
draw_auryn_ouroboros(96, 126, 26)
text(152, 106, "FANTASIA", 36, INK, bold=True)
text(338, 118, "/ CLI", 22, GOLD, bold=True)
text(154, 148, "DO WHAT THOU WILT — THE TERMINAL IS STILL BECOMING", 12, GOLD_LIGHT, bold=True)
text(W - 480, 114, "GHOSTTY-GRADE TERMINAL AI OPERATOR", 11, CYAN, bold=True)
text(W - 480, 134, "MICHAEL ENDE LORE · BOUNDED CONTEXT ENGINE", 11, MUTED)

line([(56, 182), (W - 56, 182)], BORDER, 0.8)

# Left Panel: Terminal Shell & Oracle Gate
rect(56, 204, 660, 360, BORDER, (14, 17, 24), 1.0, rx=6)
# Window bar inside panel
rect(56, 204, 660, 34, BORDER, (20, 25, 36), 1.0)
text(72, 214, "SESSION: atreyu@ivory-tower: ~", 11, MUTED)
text(630, 214, "[ANSI 24-BIT]", 10, CYAN, bold=True)

# CLI prompt lines
text(76, 252, "❯ fantasia wish \"rebuild the world from a single grain of sand\"", 13, INK, bold=True)
text(76, 280, "  [AURYN] Wish accepted: wish_7f3a9e · Anchor token consumed", 11, GOLD)
text(76, 304, "  [GATE] Passing the First Gate of the Sphinxes...", 11, MUTED)

# Oracle Output Card inside terminal
rect(76, 332, 620, 160, (38, 88, 92), (18, 30, 38), 1.0, rx=4)
text(92, 346, "◉ THE SOUTHERN ORACLE (Die Südliche Orakel)", 12, CYAN, bold=True)
text(92, 374, "\"Every world in Fantasia begins from a single grain of sand", 13, INK)
text(92, 396, " given a name. Construct the boundary first. Keep dependencies zero,", 13, INK)
text(92, 418, " the typography sharp, and the evidence reproducible.\"", 13, INK)
text(92, 452, "Provider: SouthernOracle (Synthetic Sphinx / Zero-Token Fallback)", 11, MUTED)

# Terminal bottom status inside left panel
text(76, 514, "❯ fantasia atreyu --scout --ground-memories", 12, INK)
circle(390, 520, 4, GREEN)
text(402, 514, "Atreyu active on the Grassy Plains", 11, GREEN)

# Right Panel: Telemetry & The Nothing
rect(740, 204, 484, 360, BORDER, (14, 17, 24), 1.0, rx=6)
rect(740, 204, 484, 34, BORDER, (20, 25, 36), 1.0)
text(756, 214, "TELEMETRY & ENTROPY MONITOR", 11, NOTHING_VOID, bold=True)
text(1130, 214, "[MONITOR]", 10, GOLD)

# Radar & Context Budget
text(756, 252, "THE NOTHING (DAS NICHTS) STATUS", 12, INK, bold=True)
text(756, 276, "Context budget: 14,200 / 128,000 tokens (11.1%)", 11, MUTED)

# Visual Gauge
rect(756, 298, 448, 14, BORDER, (20, 22, 30))
rect(756, 298, 50, 14, NOTHING_VOID, NOTHING_VOID)
text(756, 322, "[████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 11.1% VOID", 11, NOTHING_VOID)

line([(756, 350), (1190, 350)], BORDER, 0.6)

text(756, 368, "AURYN TALISMAN GOVERNANCE", 12, GOLD, bold=True)
text(756, 392, "Inscription : DO WHAT THOU WILT", 11, INK)
text(756, 414, "Active Bearer : Bastian Balthazar Bux", 11, MUTED)
text(756, 436, "Anchors Held : 3 human memories preserved", 11, CYAN)

line([(756, 462), (1190, 462)], BORDER, 0.6)

text(756, 480, "FALKOR OPTIMISTIC RESCUE", 12, GREEN, bold=True)
text(756, 504, "\"Never give up, and good luck will find you.\"", 11, MUTED)
text(756, 526, "Status: Airborne · Latency: 0.12ms · Stalls: 0", 11, GREEN)

# Bottom Status Footer
line([(36, H - 76), (W - 36, H - 76)], BORDER, 1.0)
circle(56, H - 56, 4, GREEN)
text(68, H - 62, "AURYN BOUND", 11, GOLD, bold=True)
text(180, H - 62, "ZERO DEPS AT RUNTIME · STDLIB PYTHON 3.10+", 11, MUTED)
text(W - 360, H - 62, "github.com/jeremedotxyz/fantasia", 11, CYAN, bold=True)

svg.append("</svg>")

# Save PNG and SVG
png_path = OUT / "social-preview.png"
svg_path = OUT / "social-preview.svg"

image.save(png_path, "PNG", optimize=True)
svg_path.write_text("\n".join(svg), encoding="utf-8")

print(f"Generated {png_path} ({png_path.stat().st_size:,} bytes)")
print(f"Generated {svg_path} ({svg_path.stat().st_size:,} bytes)")
