#!/usr/bin/env python3
"""THE WORLD — Wednesday 25 November 2026 front page (v2, fixed layout).

Draws a 1024x1024 newspaper front page with PIL. Deterministic: no
randomness, no timestamps, no network. Every run writes identical bytes.
Written from scratch for the make.fun news-image-20261125 competition.

Layout grid (all art confined to its own box; every text block auto-fits
its allotted height, shrinking the font until it fits):
  masthead  18-148 | lead art 158-340 | lead text 350-552 | rule 562
  row 2 art 572-656 | row 2 text 662-790 | rule 796
  row 3 text 806-992 | footer rule 996, footer text 1002
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "entry.png")

PAPER = (248, 244, 233)      # warm newsprint cream
INK = (18, 18, 18)           # near-black ink
RED = (163, 30, 34)          # sober front-page red for kickers
GREY = (90, 86, 78)          # caption grey
RULE = (40, 40, 40)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, path, sizes, max_w, max_lines):
    """Pick the largest size from sizes whose wrap fits in max_lines."""
    for size in sizes:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(path, sizes[-1])
    return fnt, wrap(draw, text, fnt, max_w)


def draw_lines(draw, x, y, lines, fnt, fill, leading=None):
    """Draw pre-wrapped lines; returns the y below the block."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def vgrad(draw, box, top, bottom, steps=48):
    """Vertical gradient fill inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / (steps - 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        yy0 = y0 + int((y1 - y0) * i / steps)
        yy1 = y0 + int((y1 - y0) * (i + 1) / steps)
        draw.rectangle([x0, yy0, x1, yy1], fill=c)


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def starburst(draw, cx, cy, r, fill):
    """Simple 12-point explosion burst."""
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([6, 6, W - 7, H - 7], outline=RULE, width=2)

# ---------------------------------------------------------------- masthead
d.text((W // 2, 18), "THE WORLD", font=font(SERIF_B, 88),
       fill=INK, anchor="ma")
d.text((W // 2, 108), "WEDNESDAY  25  NOVEMBER  2026",
       font=font(SANS_B, 26), fill=INK, anchor="ma")
rule(d, 24, 142, W - 24, 3)
rule(d, 24, 148, W - 24, 1)

# ---------------------------------------------------------------- LEAD PANEL
# Illustration box (24, 158)-(1000, 340): Riyadh skyline at dusk,
# PIF Tower struck, smoke rising. Nothing is drawn outside this box.
LX0, LY0, LX1, LY1 = 24, 158, 1000, 340
vgrad(d, (LX0, LY0, LX1, LY1), (62, 52, 74), (214, 128, 74))
# low sun setting behind the skyline
d.ellipse([610, 250, 770, 330], fill=(232, 150, 84))
# distant skyline silhouettes (bases on LY1)
for (bx, bw, bh) in [(24, 70, 90), (110, 46, 130), (172, 80, 70),
                     (268, 54, 110), (700, 64, 96), (780, 50, 130),
                     (846, 76, 84), (938, 62, 118)]:
    d.rectangle([bx, LY1 - bh, bx + bw, LY1], fill=(52, 44, 58))
# PIF Tower: tall tapering twisted tower, centre-left
d.polygon([(392, LY1), (408, 210), (470, 176), (486, LY1)], fill=(38, 34, 44))
d.polygon([(408, 210), (470, 176), (462, 196), (416, 226)], fill=(58, 52, 64))
# lit windows on the tower
for wy in range(240, 330, 22):
    for wx in (424, 442, 460):
        d.rectangle([wx, wy, wx + 7, wy + 9], fill=(240, 196, 110))
# explosion burst at the tower crown + smoke plume (kept inside the box)
starburst(d, 440, 196, 30, (255, 176, 66))
starburst(d, 440, 196, 16, (255, 224, 130))
for (sx, sy, sr) in [(428, 186, 13), (448, 174, 10), (462, 168, 7)]:
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(96, 88, 92))
# ground line
d.rectangle([LX0, LY1 - 6, LX1, LY1], fill=(30, 28, 34))

# Lead kicker, headline, caption
d.text((24, 350), "RIYADH  •  MIDDLE EAST", font=font(SANS_B, 22), fill=RED)
fnt, lines = fit(d, "HOUTHI STRIKE HITS RIYADH TOWER", SANS_B,
                 [48, 44, 40], 976, 2)
y = draw_lines(d, 24, 376, lines, fnt, INK, leading=int(fnt.size * 1.2))
fnt, lines = fit(d,
                 "Rebels struck the PIF Tower in Riyadh's financial "
                 "district, wounding at least 11 people. The second strike "
                 "on the tower in under a week.",
                 SANS, [22, 20], 976, 2)
y = draw_lines(d, 24, 498, lines, fnt, GREY, leading=int(fnt.size * 1.22))
print("lead headline lines:", len(lines), "bottom:", y)
rule(d, 24, 562, W - 24, 2)

# ---------------------------------------------------------------- ROW 2
# Illustration boxes are 84px tall (572-656); text below them.
COL_W, GAP = 478, 16

# --- Hormuz art, box (24, 572)-(502, 656)
HX0, HY0, HX1 = 24, 572, 502
vgrad(d, (HX0, HY0, HX1, HY0 + 84), (46, 74, 96), (16, 34, 52))
d.ellipse([380, 582, 436, 638], fill=(214, 178, 120))  # moon
d.rectangle([HX0, HY0 + 60, HX1, HY0 + 84], fill=(20, 44, 66))  # sea
d.polygon([(80, 628), (440, 628), (425, 652), (95, 652)],
          fill=(24, 24, 28))  # tanker hull
d.rectangle([330, 604, 395, 628], fill=(200, 200, 196))  # superstructure
d.rectangle([120, 606, 146, 628], fill=(163, 30, 34))  # funnel
starburst(d, 133, 598, 11, (255, 176, 66))  # flame
for (sx, sy, sr) in [(126, 586, 8), (140, 580, 6)]:
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 104, 100))
d.ellipse([452, 632, 470, 650], fill=(10, 10, 12))  # naval mine
for (mx, my) in [(461, 628), (450, 634), (472, 634), (450, 646), (472, 646)]:
    d.line([(461, 641), (mx, my)], fill=(10, 10, 12), width=3)
d.line([(HX0 + 8, 650), (HX1 - 8, 650)], fill=(70, 110, 140), width=2)

d.text((HX0, 662), "STRAIT OF HORMUZ", font=font(SANS_B, 19), fill=RED)
fnt, lines = fit(d, "OIL TANKERS HIT BY MINES IN HORMUZ", SANS_B,
                 [25, 23], COL_W, 2)
y = draw_lines(d, HX0, 686, lines, fnt, INK, leading=int(fnt.size * 1.2))
fnt, lines = fit(d, "Iran claims three tankers hit mines and caught fire. "
                    "Unverified; threat level stays severe.",
                 SANS, [17, 16], COL_W, 2)
y = draw_lines(d, HX0, 750, lines, fnt, GREY, leading=int(fnt.size * 1.2))
print("hormuz caption bottom:", y)

# --- NATO art, box (522, 572)-(1000, 656)
NX0, NY0, NX1 = 522, 572, 1000
vgrad(d, (NX0, NY0, NX1, NY0 + 84), (10, 16, 38), (28, 44, 78))
for (sx, sy) in [(560, 586), (640, 606), (700, 580), (950, 596),
                 (760, 640), (980, 640), (880, 580)]:
    d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(240, 240, 240))
d.ellipse([585, 585, 645, 645], fill=(38, 96, 150))  # planet
d.ellipse([598, 598, 632, 626], fill=(52, 130, 84))
d.arc([700, 582, 950, 656], start=200, end=340, fill=(180, 190, 220),
      width=2)  # orbit
d.rectangle([820, 596, 868, 616], fill=(200, 200, 204))  # satellite
d.rectangle([772, 602, 820, 612], fill=(70, 110, 180))
d.rectangle([868, 602, 916, 612], fill=(70, 110, 180))
d.ellipse([836, 592, 854, 606], fill=(255, 200, 90))

d.text((NX0, 662), "BRUSSELS  •  SPACE", font=font(SANS_B, 19), fill=RED)
fnt, lines = fit(d, "NATO VOWS SPACE DEFENCE", SANS_B,
                 [25, 23], COL_W, 2)
y = draw_lines(d, NX0, 686, lines, fnt, INK, leading=int(fnt.size * 1.2))
fnt, lines = fit(d, "NATO vows to defend space after reports Russia may "
                    "launch a nuclear-armed satellite.",
                 SANS, [17, 16], COL_W, 2)
y = draw_lines(d, NX0, 750, lines, fnt, GREY, leading=int(fnt.size * 1.2))
print("nato caption bottom:", y)

rule(d, 24, 796, W - 24, 2)

# ---------------------------------------------------------------- ROW 3
# No illustrations here: headline + caption only, so nothing can collide.
# Left: Putin.
d.text((24, 806), "MOSCOW", font=font(SANS_B, 19), fill=RED)
fnt, lines = fit(d, "PUTIN: RETALIATION \u201cINEVITABLE\u201d", SANS_B,
                 [25, 23], COL_W, 2)
y = draw_lines(d, 24, 832, lines, fnt, INK, leading=int(fnt.size * 1.2))
fnt, lines = fit(d, "Putin says retaliation is inevitable after Ukraine "
                    "hit Russian oil plants.",
                 SANS, [18, 17], COL_W, 2)
y = draw_lines(d, 24, 896, lines, fnt, GREY, leading=int(fnt.size * 1.22))
print("putin caption bottom:", y)

# Right: Huang mini item, then Myanmar mini item.
SX0 = 24 + COL_W + GAP
d.text((SX0, 806), "MARKETS", font=font(SANS_B, 19), fill=RED)
fnt, lines = fit(d, "HUANG'S $34 BILLION DAY", SANS_B, [22, 20], COL_W, 1)
y = draw_lines(d, SX0, 830, lines, fnt, INK, leading=int(fnt.size * 1.2))
fnt, lines = fit(d, "Nvidia's Jensen Huang recouped nearly $34bn in a day "
                    "after being reinstated as CEO.",
                 SANS, [16, 15], COL_W, 2)
y = draw_lines(d, SX0, 856, lines, fnt, GREY, leading=int(fnt.size * 1.2))
rule(d, SX0, 900, SX0 + COL_W, 1, fill=GREY)
d.text((SX0, 906), "THE HAGUE", font=font(SANS_B, 19), fill=RED)
fnt, lines = fit(d, "UN COURT CONDEMNS MYANMAR", SANS_B, [22, 20], COL_W, 1)
y = draw_lines(d, SX0, 930, lines, fnt, INK, leading=int(fnt.size * 1.2))
fnt, lines = fit(d, "The UN's top court condemned Myanmar over actions "
                    "against the Rohingya.",
                 SANS, [15, 14], COL_W, 2)
y = draw_lines(d, SX0, 956, lines, fnt, GREY, leading=int(fnt.size * 1.2))
print("myanmar caption bottom:", y)

# ---------------------------------------------------------------- footer
rule(d, 24, 996, W - 24, 2)
d.text((W // 2, 1002),
       "THE WORLD  •  WEDNESDAY 25 NOVEMBER 2026  •  ALL THE WORLD'S NEWS IN ONE IMAGE",
       font=font(SANS_B, 13), fill=GREY, anchor="ma")

# ---------------------------------------------------------------- save
os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, format="PNG")
print("wrote", OUT)
