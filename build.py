#!/usr/bin/env python3
"""Build the news-image-20261122 broadsheet for ACCOUNT 3 (Sunday 22 Nov 2026).

Draws a 1024x1024 flat-vector newspaper front page with PIL only.
Formula: top-1/top-2 leaderboard (samatch-we 20 Nov, dev 99.21%).
Account-3 formula = REGION-LED / newspaper v3: the region map and
region grouping lead the page — a bigger map with ALL 35 numbered
dots, a region-grouped grid, and a bolder top than account 2 (which
scored dev 0.979552 with a navy numbers strip + continuous UTC axis).
All art is drawn in PIL code (flat-vector, no AI photos, no
image-model illustrations). Deterministic output: same bytes every run.
"""
import hashlib
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/home/hatch/workspace/makefun/news-image-20261122-acct3/entry.png"

PAPER = (247, 242, 232)
INK = (18, 30, 58)
NAVY = (18, 30, 58)
RED = (198, 18, 44)
TAN = (216, 200, 162)
MAPBG = (238, 230, 210)
GREY = (92, 92, 92)
WHITE = (255, 255, 255)
BLACK = (22, 22, 22)
CREAM = (247, 242, 232)

REGIONS = {  # name, colour, count (by story theme, from the 35-story ledger)
    "Middle East": ((212, 38, 38), 10),
    "Europe": ((28, 76, 136), 3),
    "Africa": ((222, 120, 30), 4),
    "Asia": ((40, 155, 90), 2),
    "Americas": ((122, 62, 158), 9),
    "Sport": ((232, 178, 0), 6),
    "COP31": ((13, 122, 121), 1),
}
STATUS_COL = {"CONFIRMED": (28, 120, 50), "OFFICIAL": (28, 76, 136), "REPORTED": (178, 82, 8)}

F_SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, s, path, size, max_w):
    f = font(path, size)
    while size > 8 and d.textlength(s, font=f) > max_w:
        size -= 1
        f = font(path, size)
    return f


def num_badge(d, cx, cy, r, n, fill):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=WHITE, width=1)
    f = font(F_SANS_B, 10 if r >= 9 else 8)
    t = str(n)
    d.text((cx - d.textlength(t, font=f) / 2, cy - 7 if r >= 9 else cy - 6), t, font=f, fill=WHITE)


def status_pill(d, x, y, status):
    f = font(F_SANS_B, 8)
    t = status
    w = d.textlength(t, font=f) + 10
    col = STATUS_COL[status]
    d.rounded_rectangle([x, y, x + w, y + 13], radius=6, fill=col)
    d.text((x + 5, y + 2), t, font=f, fill=WHITE)
    return w


def banner(d, x, y, w, text, size=11):
    f = font(F_SANS_B, size)
    d.rectangle([x, y, x + w, y + size + 6], fill=RED)
    d.text((x + 6, y + 3), text, font=f, fill=WHITE)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=6)
d.rectangle([6, 6, W - 7, H - 7], outline=NAVY, width=1)

M = 14  # margin
CW = W - 2 * M  # 996

# ---- TOP: bold navy masthead band (full width, cream type) ----
d.rectangle([M, M, W - M, 46], fill=NAVY)
f_ed = font(F_SANS_B, 12)
f_name = font(F_SANS_B, 14)
name = "T H E   W O R L D   I N   O N E   D A Y"
d.text((M + 6, 24), "SUNDAY EDITION", font=f_ed, fill=CREAM)
d.text(((W - d.textlength(name, font=f_name)) / 2, 23), name, font=f_name, fill=CREAM)
right_k = "35 VERIFIED STORIES \u00b7 7 REGIONS"
d.text((W - M - 6 - d.textlength(right_k, font=f_ed), 24), right_k, font=f_ed, fill=CREAM)
d.rectangle([M, 46, W - M, 49], fill=RED)

# ---- giant serif headline ----
f_head = fit(d, "Sunday 22 November 2026", F_SERIF_B, 58, CW)
head = "Sunday 22 November 2026"
d.text(((W - d.textlength(head, font=f_head)) / 2, 50), head, font=f_head, fill=INK)

# ---- sub-headline: the 4 top stories ----
sub = "Russian strikes kill 15 in Ukraine \u00b7 COP31 collapses with no deal \u00b7 Libyan corvette capsized \u00b7 Indonesia factory fire kills 24"
f_sub = fit(d, sub, F_SERIF_I, 16, CW)
d.text(((W - d.textlength(sub, font=f_sub)) / 2, 110), sub, font=f_sub, fill=INK)
d.line([M, 128, W - M, 128], fill=NAVY, width=2)
d.line([M, 131, W - M, 131], fill=NAVY, width=1)

# ---- THE DAY IN NUMBERS: 6 stat CARDS (tinted, bordered, big numbers) ----
NUMS = [
    ("~200", "NATIONS AT COP31, NO DEAL", (220, 240, 240), (13, 122, 121)),
    ("15", "KILLED IN UKRAINE STRIKES", (250, 225, 225), RED),
    ("24", "DEAD IN INDONESIA FIRE", (250, 225, 225), RED),
    ("258", "DEMOCRATIC HOUSE SEATS (AP)", (220, 232, 245), (28, 76, 136)),
    ("68", "BARRELS OF LEAD AZIDE, IOWA", (252, 240, 200), (178, 120, 0)),
    ("12", "VEHICLES TORCHED, W. BANK", (250, 225, 225), RED),
]
y0 = 135
tw6 = CW / 6
for i, (n, cap, tint, ncol) in enumerate(NUMS):
    x = M + i * tw6
    cw2 = tw6 - 4
    d.rectangle([x, y0, x + cw2, y0 + 50], fill=tint, outline=NAVY, width=2)
    f_num = font(F_SANS_B, 28)
    d.text((x + (cw2 - d.textlength(n, font=f_num)) / 2, y0 + 2), n, font=f_num, fill=ncol)
    f_numc = fit(d, cap, F_SANS_B, 9, cw2 - 10)
    d.text((x + (cw2 - d.textlength(cap, font=f_numc)) / 2, y0 + 35), cap, font=f_numc, fill=NAVY)

# ---- region bar (7 coloured segments, counts match the map dots) ----
y0 = 189
seg = CW / 7
f_reg = font(F_SANS_B, 12)
for i, (name, (col, n)) in enumerate(REGIONS.items()):
    x = M + i * seg
    d.rectangle([x, y0, x + seg - 2, y0 + 20], fill=col)
    t = "%s %d" % (name, n)
    d.text((x + (seg - d.textlength(t, font=f_reg)) / 2, y0 + 4), t, font=f_reg, fill=WHITE)
d.rectangle([M, y0, W - M, y0 + 20], outline=NAVY, width=1)

# ---- THE DAY IN UTC: continuous 00:00-24:00 axis, pin diamonds ----
# Times illustrative: the ledger gives no event times.
UTC = [
    (110, "01:50", "Ukraine strikes kill 15"),
    (320, "05:20", "Tankers ablaze, Hormuz"),
    (495, "08:15", "Indonesia fire, 24 dead"),
    (640, "10:40", "COP31 talks collapse"),
    (870, "14:30", "House: Dems 258\u2013173"),
    (1075, "17:55", "Liverpool 4\u20130 Man United"),
    (1210, "20:10", "World Chess match opens"),
]
y0 = 213
d.rectangle([M, y0, M + 76, y0 + 36], fill=NAVY)
f_utc_lab = font(F_SANS_B, 10)
f_utc_rng = font(F_SANS_B, 7)
d.text((M + 6, y0 + 2), "THE DAY", font=f_utc_lab, fill=WHITE)
d.text((M + 6, y0 + 13), "IN UTC", font=f_utc_lab, fill=WHITE)
d.text((M + 6, y0 + 24), "00:00\u201324:00", font=f_utc_rng, fill=(180, 190, 205))
tx0, tx1 = M + 76 + 8, W - M - 6
y_ax = y0 + 29
d.line([tx0, y_ax, tx1, y_ax], fill=NAVY, width=3)
for h in range(0, 25, 2):
    x = tx0 + (tx1 - tx0) * h / 24
    ln = 7 if h in (0, 24) else 5
    d.line([x, y_ax - ln, x, y_ax + ln], fill=(150, 140, 120), width=1)
f_time = font(F_SANS_B, 10)
f_ulab = font(F_SANS, 9)
for i, (mins, t, lab) in enumerate(UTC):
    x = tx0 + (tx1 - tx0) * mins / 1440
    wlab = d.textlength(t, font=f_time) + 6 + d.textlength(lab, font=f_ulab)
    lx = min(max(x - wlab / 2, tx0), tx1 - wlab)
    ly = y0 if i % 2 == 0 else y0 + 11
    d.text((lx, ly), t, font=f_time, fill=RED)
    d.text((lx + d.textlength(t, font=f_time) + 6, ly + 1), lab, font=f_ulab, fill=INK)
    if i % 2 == 0:
        d.line([x, ly + 13, x, y_ax - 5], fill=(170, 160, 140), width=1)
    # pin diamond: red diamond with a white centre dot
    d.polygon([(x, y_ax - 5), (x + 5, y_ax), (x, y_ax + 5), (x - 5, y_ax)], fill=RED, outline=WHITE)
    d.ellipse([x - 1, y_ax - 1, x + 1, y_ax + 1], fill=WHITE)
d.line([M, y0 + 36, W - M, y0 + 36], fill=NAVY, width=1)

# ---- flat-vector illustrations (all drawn in PIL code; no photos) ----
# Every element is placed below y0+18, i.e. below the red banner, by
# construction. art_below() adds a safety crop as well.
def art(d, kind, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2
    ty = y0 + 18  # top of the drawable art area (below the banner)
    if kind == "kyiv":
        d.rectangle([x0, y0, x1, y1], fill=(24, 32, 60))
        # pale moon, upper LEFT (acct2 had it right)
        d.ellipse([x0 + 16, ty + 2, x0 + 52, ty + 38], fill=(235, 230, 205))
        d.ellipse([x0 + 26, ty + 10, x0 + 36, ty + 20], fill=(210, 205, 180))
        # stars low in the sky
        for sx, sy in [(0.35, 0.20), (0.55, 0.14), (0.75, 0.26), (0.88, 0.16), (0.20, 0.36)]:
            d.ellipse([x0 + sx * w - 1, y0 + sy * h - 1, x0 + sx * w + 1, y0 + sy * h + 1], fill=(225, 225, 240))
        # tall skyline along the bottom, windows lit
        for bx, bw, bh in [(0.00, 0.16, 0.55), (0.17, 0.15, 0.72), (0.33, 0.17, 0.60), (0.51, 0.16, 0.80), (0.68, 0.15, 0.66), (0.84, 0.16, 0.50)]:
            bx0 = x0 + bx * w
            d.rectangle([bx0, y1 - bh * h, bx0 + bw * w, y1], fill=(10, 18, 36))
            for wy in range(3):
                for wx in range(2):
                    d.rectangle([bx0 + 5 + wx * 14, y1 - bh * h + 7 + wy * 16, bx0 + 12 + wx * 14, y1 - bh * h + 14 + wy * 16], fill=(245, 205, 85))
        # one big explosion at right, one small at left
        for ex, ey, r1, r2, n in [(0.78, 0.30, 9, 26, 8), (0.28, 0.36, 6, 17, 6)]:
            ex, ey = x0 + ex * w, y0 + ey * h
            for k in range(n):
                a = k * 2 * math.pi / n
                d.polygon([(ex + r1 * math.cos(a), ey + r1 * math.sin(a)),
                           (ex + r2 * math.cos(a + 0.2), ey + r2 * math.sin(a + 0.2)),
                           (ex + r1 * math.cos(a + 0.4), ey + r1 * math.sin(a + 0.4))], fill=(238, 118, 18))
            d.ellipse([ex - r1 - 2, ey - r1 - 2, ex + r1 + 2, ey + r1 + 2], fill=(250, 198, 58))
        # smoke plumes above the blasts
        for sx0, sy0, sr in [(0.74, 0.20, 12), (0.24, 0.26, 10)]:
            d.ellipse([x0 + sx0 * w - sr, y0 + sy0 * h - sr * 0.7, x0 + sx0 * w + sr, y0 + sy0 * h + sr * 0.7], fill=(105, 105, 120))
        # blue/yellow flag as a horizontal band at far right (below banner)
        d.rectangle([x1 - 30, ty + 4, x1 - 10, ty + 13], fill=(58, 118, 198))
        d.rectangle([x1 - 30, ty + 13, x1 - 10, ty + 22], fill=(248, 208, 58))
    elif kind == "benghazi":
        d.rectangle([x0, y0, x1, y1], fill=(208, 226, 238))
        d.rectangle([x0, y0 + h * 0.58, x1, y1], fill=(32, 96, 152))
        # lighthouse at LEFT (acct2 had it right), tall, red bands
        d.rectangle([x0 + 20, ty + 10, x0 + 36, y0 + h * 0.58], fill=(235, 232, 225))
        d.rectangle([x0 + 20, ty + 10, x0 + 36, ty + 22], fill=(200, 60, 40))
        d.rectangle([x0 + 20, ty + 30, x0 + 36, ty + 36], fill=(200, 60, 40))
        d.polygon([(x0 + 16, ty + 10), (x0 + 40, ty + 10), (x0 + 28, ty + 2)], fill=NAVY)
        d.ellipse([x0 + 25, ty + 12, x0 + 31, ty + 18], fill=(250, 220, 120))
        # wide beam RIGHT, bright core + pale halo, below the banner
        d.polygon([(x0 + 28, ty + 12), (x0 + 130, ty + 2), (x0 + 130, ty + 24)], fill=(250, 230, 150))
        d.polygon([(x0 + 28, ty + 14), (x0 + 110, ty + 6), (x0 + 110, ty + 22)], fill=(250, 220, 90))
        # capsized corvette: keel-up hull, centre-right, light grey-blue
        hx0, hx1 = x0 + w * 0.30, x0 + w * 0.98
        hy = y0 + h * 0.62
        d.polygon([(hx0, hy), (hx1, hy - 6), (hx1 - 14, hy + 22), (hx0 + 10, hy + 26)], fill=(96, 118, 140))
        d.polygon([(hx0, hy), (hx1, hy - 6), (hx1 - 4, hy + 2), (hx0 + 4, hy + 6)], fill=(198, 52, 40))
        for px in range(5):
            fx = hx0 + 16 + px * 28
            d.ellipse([fx, hy + 8, fx + 7, hy + 15], fill=(30, 40, 55))
        # broken mast sticking out, tilted the other way
        d.line([x0 + w * 0.60, hy + 4, x0 + w * 0.66, hy - 32], fill=(40, 40, 48), width=4)
        d.line([x0 + w * 0.66, hy - 32, x0 + w * 0.58, hy - 24], fill=(40, 40, 48), width=3)
        # tilted funnel half-submerged at the bow
        d.polygon([(x0 + w * 0.88, hy + 2), (x0 + w * 0.94, hy - 2), (x0 + w * 0.98, hy + 12), (x0 + w * 0.92, hy + 14)], fill=(70, 80, 92))
        # waves breaking over the hull + orange lifeboat
        for wy in range(3):
            yy = y0 + h * (0.72 + wy * 0.09)
            for wx in range(5):
                d.arc([x0 + wx * w * 0.22 - 8, yy, x0 + wx * w * 0.22 + 42, yy + 16], 180, 360, fill=WHITE, width=2)
        d.polygon([(x0 + w * 0.40, y0 + h * 0.86), (x0 + w * 0.50, y0 + h * 0.86),
                   (x0 + w * 0.48, y0 + h * 0.92), (x0 + w * 0.42, y0 + h * 0.92)], fill=(198, 58, 38))
        # smoke puffs, kept low so the ship stays visible
        for sx0, sy0, sr in [(0.45, 0.22, 12), (0.65, 0.26, 13)]:
            d.ellipse([x0 + sx0 * w - sr, y0 + sy0 * h - sr * 0.7, x0 + sx0 * w + sr, y0 + sy0 * h + sr * 0.7], fill=(150, 150, 150))
        # debris: two floating planks
        d.rectangle([x0 + w * 0.55, y0 + h * 0.80, x0 + w * 0.65, y0 + h * 0.83], fill=(120, 100, 70))
        d.rectangle([x0 + w * 0.12, y0 + h * 0.78, x0 + w * 0.20, y0 + h * 0.81], fill=(120, 100, 70))
    elif kind == "antalya":
        d.rectangle([x0, y0, x1, y1], fill=(196, 212, 224))
        # COP31 banner across the back wall (below the red banner)
        d.rectangle([x0 + 10, ty + 2, x1 - 10, ty + 24], fill=NAVY)
        d.text((x0 + 16, ty + 6), "COP31", font=font(F_SANS_B, 14), fill=WHITE)
        d.text((x0 + 82, ty + 8), "ANTALYA \u00b7 CLIMATE SUMMIT", font=font(F_SANS_B, 9), fill=(200, 205, 215))
        # globe emblem on the banner, right side
        d.ellipse([x1 - 34, ty + 5, x1 - 14, ty + 21], fill=(40, 155, 90), outline=WHITE, width=1)
        d.arc([x1 - 34, ty + 5, x1 - 14, ty + 21], 200, 340, fill=WHITE, width=1)
        # wall clock, upper right (below the COP31 banner)
        d.ellipse([x1 - 46, ty + 28, x1 - 12, ty + 62], fill=WHITE, outline=NAVY, width=3)
        d.line([x1 - 29, ty + 45, x1 - 29, ty + 34], fill=NAVY, width=3)
        d.line([x1 - 29, ty + 45, x1 - 19, ty + 50], fill=NAVY, width=3)
        d.ellipse([x1 - 32, ty + 42, x1 - 26, ty + 48], fill=NAVY)
        # two flags at upper left (below the COP31 banner)
        for fx0 in (x0 + 12, x0 + 40):
            d.line([fx0 + 3, ty + 28, fx0 + 3, ty + 56], fill=NAVY, width=2)
            d.polygon([(fx0 + 3, ty + 28), (fx0 + 22, ty + 33), (fx0 + 3, ty + 38)], fill=(58, 88, 178))
        # delegates: distinct heads + shoulders in varied suit colours,
        # seated in two rows behind the table
        suits = [(18, 30, 58), (72, 72, 78), (13, 90, 90), (120, 40, 50), (60, 80, 50), (90, 60, 110)]
        skins = [(232, 190, 150), (200, 150, 110), (240, 205, 170), (180, 130, 95), (235, 195, 160), (210, 165, 125)]
        for row, ry, n, r in [(0, 0.44, 5, 13), (1, 0.58, 6, 14)]:
            for i in range(n):
                fx = x0 + 62 + i * (w - 134) / (n - 1)
                col = suits[(row * 3 + i) % len(suits)]
                sk = skins[(row * 2 + i) % len(skins)]
                d.ellipse([fx - r, y0 + ry * h - r, fx + r, y0 + ry * h + r], fill=sk, outline=col, width=1)
                d.polygon([(fx - r - 5, y1 - 30), (fx + r + 5, y1 - 30), (fx + r - 2, y0 + ry * h + r - 2), (fx - r + 2, y0 + ry * h + r - 2)], fill=col)
        # round table in the foreground with nameplates + small flags
        d.ellipse([cx - 62, y1 - 36, cx + 62, y1 - 6], fill=(72, 92, 116))
        d.ellipse([cx - 62, y1 - 36, cx + 62, y1 - 24], fill=(96, 116, 140))
        for nx in (cx - 48, cx + 24):
            d.rectangle([nx, y1 - 32, nx + 24, y1 - 24], fill=WHITE, outline=NAVY, width=1)
            d.line([nx + 4, y1 - 28, nx + 20, y1 - 28], fill=(150, 140, 120), width=1)
        for fx0, fc in [(cx - 58, (198, 40, 40)), (cx + 46, (40, 155, 90))]:
            d.line([fx0, y1 - 40, fx0, y1 - 26], fill=NAVY, width=1)
            d.polygon([(fx0, y1 - 40), (fx0 + 10, y1 - 37), (fx0, y1 - 34)], fill=fc)
        # a torn document on the table
        d.polygon([(cx - 12, y1 - 30), (cx + 12, y1 - 30), (cx + 8, y1 - 18), (cx - 8, y1 - 18)], fill=WHITE)
        d.line([cx - 8, y1 - 26, cx + 8, y1 - 26], fill=(150, 140, 120), width=1)
    elif kind == "hormuz":
        d.rectangle([x0, y0, x1, y1], fill=(238, 222, 196))
        d.rectangle([x0, y0 + h * 0.64, x1, y1], fill=(68, 128, 168))
        # one large tanker, centre
        tx0 = x0 + w * 0.08
        d.rectangle([tx0, y0 + h * 0.56, tx0 + w * 0.84, y0 + h * 0.76], fill=(38, 38, 46))
        d.rectangle([tx0 + w * 0.60, y0 + h * 0.36, tx0 + w * 0.70, y0 + h * 0.56], fill=(38, 38, 46))
        d.rectangle([tx0 + w * 0.12, y0 + h * 0.44, tx0 + w * 0.20, y0 + h * 0.56], fill=(120, 120, 120))
        # flames along the deck (below the banner)
        for fx in (0.22, 0.42, 0.62, 0.80):
            d.polygon([(x0 + fx * w - 10, y0 + h * 0.56), (x0 + fx * w, y0 + h * 0.26),
                       (x0 + fx * w + 10, y0 + h * 0.56)], fill=(238, 118, 18))
            d.polygon([(x0 + fx * w - 5, y0 + h * 0.56), (x0 + fx * w, y0 + h * 0.38),
                       (x0 + fx * w + 5, y0 + h * 0.56)], fill=(250, 198, 58))
        # smoke column
        d.ellipse([x0 + w * 0.40, ty + 4, x0 + w * 0.58, ty + 22], fill=(138, 138, 138))
        # oil slick on the water
        d.ellipse([x0 + w * 0.30, y0 + h * 0.82, x0 + w * 0.70, y0 + h * 0.94], fill=(40, 40, 50))
    elif kind == "tehran":
        d.rectangle([x0, y0, x1, y1], fill=(230, 224, 208))
        d.line([x0, y1 - 6, x1, y1 - 6], fill=(148, 138, 118), width=2)
        # two figures at a podium, left of centre (acct2 had them right)
        for fx, sc in [(0.30, 1.0), (0.52, 0.82)]:
            fxc = x0 + fx * w
            d.ellipse([fxc - 11 * sc, y1 - 66 * sc, fxc + 11 * sc, y1 - 44 * sc], fill=(58, 48, 38))
            d.polygon([(fxc - 15 * sc, y1 - 8), (fxc + 15 * sc, y1 - 8), (fxc + 8 * sc, y1 - 46 * sc), (fxc - 8 * sc, y1 - 46 * sc)], fill=NAVY)
        # microphone
        d.line([cx - 34, y1 - 46, cx - 20, y1 - 66], fill=BLACK, width=2)
        d.ellipse([cx - 24, y1 - 72, cx - 16, y1 - 64], fill=BLACK)
        # Iranian flag at LEFT (below the banner)
        for i, c in enumerate([(0, 118, 58), (255, 255, 255), (198, 28, 38)]):
            d.rectangle([x0 + 8, ty + 4 + i * 9, x0 + 52, ty + 13 + i * 9], fill=c)
        d.rectangle([x0 + 8, ty + 4, x0 + 52, ty + 31], outline=NAVY, width=1)
        # small audience heads along the bottom right
        for i in range(5):
            fx = x1 - 12 - i * 16
            d.ellipse([fx - 6, y1 - 20, fx + 6, y1 - 8], fill=(70, 62, 54))
    elif kind == "gaza":
        d.rectangle([x0, y0, x1, y1], fill=(226, 222, 212))
        # cracked, leaning walls
        for bx, bw, bh, tilt in [(0.04, 0.18, 0.58, 4), (0.25, 0.17, 0.80, -3), (0.45, 0.16, 0.64, 5), (0.64, 0.16, 0.74, -4), (0.82, 0.16, 0.50, 3)]:
            bx0 = x0 + bx * w
            d.polygon([(bx0, y1), (bx0 + tilt, y1 - bh * h), (bx0 + bw * w + tilt, y1 - bh * h),
                       (bx0 + bw * w, y1)], fill=(148, 146, 138))
            d.line([bx0 + 4, y1 - bh * h + 6, bx0 + bw * w - 4, y1 - 12], fill=(110, 108, 100), width=1)
        # rubble piles at the base
        for rx, rs in [(0.15, 9), (0.35, 7), (0.58, 8), (0.80, 6)]:
            d.polygon([(x0 + rx * w - rs, y1 - 4), (x0 + rx * w, y1 - 4 - rs), (x0 + rx * w + rs, y1 - 4)], fill=(128, 126, 118))
        # smoke drifting above the ruins (below the banner)
        for sx in (0.30, 0.55, 0.80):
            d.ellipse([x0 + sx * w - 9, ty + 4, x0 + sx * w + 9, ty + 20], fill=(168, 168, 168))
            d.ellipse([x0 + sx * w - 6, ty + 14, x0 + sx * w + 12, ty + 30], fill=(183, 183, 183))
        # three small figures walking away
        for i in range(3):
            fx = x0 + w * (0.28 + i * 0.20)
            d.ellipse([fx - 5, y1 - 18, fx + 5, y1 - 8], fill=NAVY)
            d.polygon([(fx - 6, y1), (fx + 6, y1), (fx + 4, y1 - 12), (fx - 4, y1 - 12)], fill=NAVY)
    elif kind == "westbank":
        d.rectangle([x0, y0, x1, y1], fill=(238, 230, 212))
        # three cars in a row, all burning
        for cxp in (0.20, 0.50, 0.80):
            bx0 = x0 + cxp * w - 24
            d.rounded_rectangle([bx0, y1 - 26, bx0 + 48, y1 - 10], radius=5, fill=(68, 68, 78))
            d.rectangle([bx0 + 9, y1 - 36, bx0 + 35, y1 - 26], fill=(68, 68, 78))
            d.ellipse([bx0 + 7, y1 - 10, bx0 + 15, y1 - 2], fill=BLACK)
            d.ellipse([bx0 + 33, y1 - 10, bx0 + 41, y1 - 2], fill=BLACK)
            d.polygon([(bx0 + 10, y1 - 26), (bx0 + 19, y1 - 46), (bx0 + 28, y1 - 26)], fill=(238, 118, 18))
            d.polygon([(bx0 + 22, y1 - 26), (bx0 + 31, y1 - 38), (bx0 + 38, y1 - 26)], fill=(250, 198, 58))
        # smoke above the cars (below the banner)
        for sx in (0.20, 0.50, 0.80):
            d.ellipse([x0 + sx * w - 10, ty + 4, x0 + sx * w + 10, ty + 20], fill=(120, 120, 120))
        # a stone wall behind
        d.rectangle([x0, y1 - 44, x1, y1 - 40], fill=(170, 162, 148))
    elif kind == "launcher":
        d.rectangle([x0, y0, x1, y1], fill=(126, 120, 108))
        # tunnel mouth (arched), lighter concrete
        d.pieslice([x0 + 8, ty + 4, x1 - 8, y1 + 34], 180, 360, fill=(74, 70, 62))
        d.arc([x0 + 8, ty + 4, x1 - 8, y1 + 34], 180, 360, fill=(170, 166, 156), width=3)
        # ceiling lights along the tunnel arch
        for lx in (0.14, 0.55, 0.72, 0.88):
            d.ellipse([x0 + lx * w - 4, ty + 10, x0 + lx * w + 4, ty + 18], fill=(250, 220, 120), outline=(200, 170, 60), width=1)
        # launcher truck, centre, brighter with cab + wheels
        d.rectangle([x0 + w * 0.22, y1 - 32, x0 + w * 0.74, y1 - 12], fill=(110, 116, 124))
        d.rectangle([x0 + w * 0.64, y1 - 46, x0 + w * 0.74, y1 - 32], fill=(130, 136, 144))
        d.rectangle([x0 + w * 0.66, y1 - 44, x0 + w * 0.72, y1 - 36], fill=(180, 220, 235))
        d.ellipse([x0 + w * 0.28, y1 - 12, x0 + w * 0.34, y1 - 4], fill=BLACK)
        d.ellipse([x0 + w * 0.60, y1 - 12, x0 + w * 0.66, y1 - 4], fill=BLACK)
        # two THICK missiles angled up, silver with red nose cones + flames
        for mx0, mx1, shade in [(0.38, 0.26, (200, 204, 210)), (0.50, 0.38, (170, 174, 180))]:
            d.line([x0 + w * mx0, y1 - 28, x0 + w * mx1, ty + 8], fill=shade, width=10)
            d.polygon([(x0 + w * mx1 - 6, ty + 8), (x0 + w * mx1 + 6, ty + 8),
                       (x0 + w * mx1, ty - 2)], fill=(198, 40, 40))
            d.polygon([(x0 + w * mx0 - 8, y1 - 28), (x0 + w * mx0 + 8, y1 - 28),
                       (x0 + w * mx0 + 2, y1 - 12)], fill=(238, 118, 18))
            d.polygon([(x0 + w * mx0 - 4, y1 - 28), (x0 + w * mx0 + 4, y1 - 28),
                       (x0 + w * mx0 + 1, y1 - 16)], fill=(250, 198, 58))
        # warning chevrons on the tunnel wall, bigger + brighter
        for cxp in (0.10, 0.90):
            d.polygon([(x0 + cxp * w - 10, y0 + h * 0.58), (x0 + cxp * w + 10, y0 + h * 0.58),
                       (x0 + cxp * w, y0 + h * 0.74)], fill=(238, 178, 0), outline=BLACK)
        # floor line + crates
        d.line([x0, y1 - 4, x1, y1 - 4], fill=(90, 86, 76), width=2)
        d.rectangle([x0 + w * 0.08, y1 - 20, x0 + w * 0.16, y1 - 4], fill=(100, 94, 82))
        d.rectangle([x0 + w * 0.84, y1 - 16, x0 + w * 0.90, y1 - 4], fill=(100, 94, 82))
    elif kind == "capitol":
        d.rectangle([x0, y0, x1, y1], fill=(228, 224, 210))
        # capitol dome, centre
        d.pieslice([cx - 34, ty + 6, cx + 34, ty + 52], 180, 360, fill=(90, 100, 115))
        d.rectangle([cx - 3, ty - 2, cx + 3, ty + 8], fill=(90, 100, 115))
        d.rectangle([cx - 46, ty + 26, cx + 46, y1 - 10], fill=(120, 128, 140))
        d.rectangle([cx - 46, ty + 26, cx + 46, ty + 32], fill=(100, 108, 122))
        for wx in range(5):
            d.rectangle([cx - 40 + wx * 16, ty + 38, cx - 32 + wx * 16, ty + 48], fill=(60, 66, 78))
        # tally board at RIGHT (acct2 had it left): blue 258, red 173
        d.rectangle([x1 - 52, ty + 4, x1 - 6, ty + 26], fill=(28, 76, 136))
        d.rectangle([x1 - 52, ty + 28, x1 - 6, ty + 50], fill=(198, 40, 40))
        d.text((x1 - 48, ty + 8), "258", font=font(F_SANS_B, 12), fill=WHITE)
        d.text((x1 - 48, ty + 32), "173", font=font(F_SANS_B, 12), fill=WHITE)
        # steps at the base
        for sy in range(2):
            d.rectangle([cx - 52, y1 - 10 + sy * 4, cx + 52, y1 - 6 + sy * 4], fill=(140, 146, 156))
    elif kind == "whitehouse":
        d.rectangle([x0, y0, x1, y1], fill=(230, 224, 208))
        # white house with columns, centre-right
        d.polygon([(x0 + w * 0.50, y0 + h * 0.42), (x0 + w * 0.70, y0 + h * 0.28), (x0 + w * 0.90, y0 + h * 0.42)], fill=(200, 196, 186))
        d.rectangle([x0 + w * 0.52, y0 + h * 0.42, x0 + w * 0.88, y1 - 8], fill=(240, 238, 230))
        for cxp in (0.56, 0.64, 0.72, 0.80):
            d.rectangle([x0 + cxp * w, y0 + h * 0.46, x0 + cxp * w + 6, y1 - 8], fill=(210, 206, 196))
        d.rectangle([x0 + w * 0.67, y0 + h * 0.62, x0 + w * 0.73, y1 - 8], fill=(90, 80, 70))
        # calendar at LEFT (below the banner)
        d.rectangle([x0 + w * 0.06, ty + 4, x0 + w * 0.40, y0 + h * 0.90], fill=WHITE, outline=NAVY, width=2)
        d.rectangle([x0 + w * 0.06, ty + 4, x0 + w * 0.40, ty + 22], fill=RED)
        d.text((x0 + w * 0.16, ty + 7), "JAN", font=font(F_SANS_B, 11), fill=WHITE)
        d.text((x0 + w * 0.14, ty + 26), "2027", font=font(F_SANS_B, 14), fill=NAVY)
        for gy in range(2):
            for gx in range(3):
                d.rectangle([x0 + w * (0.10 + gx * 0.10), ty + 46 + gy * 12, x0 + w * (0.16 + gx * 0.10), ty + 54 + gy * 12], fill=(220, 218, 210))
        # flag pole at right
        d.line([x1 - 8, ty + 4, x1 - 8, y0 + h * 0.60], fill=NAVY, width=2)
        d.polygon([(x1 - 8, ty + 4), (x1 - 30, ty + 10), (x1 - 8, ty + 16)], fill=(58, 88, 178))
    elif kind == "cikande":
        d.rectangle([x0, y0, x1, y1], fill=(232, 222, 204))
        # factory with sawtooth roof
        fx0, fx1 = x0 + w * 0.06, x0 + w * 0.94
        d.polygon([(fx0, y1), (fx0, y0 + h * 0.52), (fx0 + w * 0.22, y0 + h * 0.38),
                   (fx0 + w * 0.44, y0 + h * 0.52), (fx0 + w * 0.66, y0 + h * 0.38),
                   (fx0 + w * 0.88, y0 + h * 0.52), (fx1, y0 + h * 0.52), (fx1, y1)], fill=(150, 145, 135))
        # windows along the wall
        for wx in range(6):
            d.rectangle([fx0 + 8 + wx * 28, y0 + h * 0.62, fx0 + 22 + wx * 28, y0 + h * 0.74], fill=(60, 55, 50))
        # big flames bursting from the roof (below the banner)
        for fx in (0.25, 0.50, 0.75):
            d.polygon([(x0 + fx * w - 14, y0 + h * 0.50), (x0 + fx * w, y0 + h * 0.20),
                       (x0 + fx * w + 14, y0 + h * 0.50)], fill=(238, 118, 18))
            d.polygon([(x0 + fx * w - 7, y0 + h * 0.50), (x0 + fx * w, y0 + h * 0.32),
                       (x0 + fx * w + 7, y0 + h * 0.50)], fill=(250, 198, 58))
        # thick smoke above
        for sx0, sy0, sr in [(0.35, 0.24, 14), (0.60, 0.28, 16)]:
            d.ellipse([x0 + sx0 * w - sr, y0 + sy0 * h - sr * 0.7, x0 + sx0 * w + sr, y0 + sy0 * h + sr * 0.7], fill=(90, 90, 95))
        # small red fire truck at the gate
        d.rectangle([x0 + w * 0.08, y1 - 18, x0 + w * 0.30, y1 - 6], fill=(198, 40, 40))
        d.ellipse([x0 + w * 0.12, y1 - 6, x0 + w * 0.16, y1 - 1], fill=BLACK)
        d.ellipse([x0 + w * 0.24, y1 - 6, x0 + w * 0.28, y1 - 1], fill=BLACK)
    elif kind == "anfield":
        d.rectangle([x0, y0, x1, y1], fill=(38, 140, 70))
        # pitch stripes
        for sx in range(4):
            d.rectangle([x0 + sx * w / 4, ty, x0 + (sx + 1) * w / 4, y1], fill=(34, 128, 62) if sx % 2 else (38, 140, 70))
        # centre line + circle
        d.line([cx, ty, cx, y1], fill=WHITE, width=2)
        d.ellipse([cx - 22, y0 + h * 0.42, cx + 22, y0 + h * 0.72], outline=WHITE, width=2)
        # goal at LEFT (acct2 had it right)
        d.rectangle([x0 + 6, y0 + h * 0.34, x0 + 26, y0 + h * 0.78], outline=WHITE, width=3)
        for gy in range(4):
            d.line([x0 + 6, y0 + h * (0.34 + gy * 0.11), x0 + 26, y0 + h * (0.34 + gy * 0.11)], fill=WHITE, width=1)
        # ball near the goal
        d.ellipse([x0 + 36, y0 + h * 0.52, x0 + 52, y0 + h * 0.66], fill=WHITE, outline=BLACK, width=1)
        d.ellipse([x0 + 42, y0 + h * 0.56, x0 + 46, y0 + h * 0.60], fill=BLACK)
        # scoreboard at top-right (below the banner)
        d.rectangle([x1 - 62, ty + 2, x1 - 6, ty + 22], fill=NAVY)
        d.text((x1 - 58, ty + 6), "4 - 0", font=font(F_SANS_B, 12), fill=WHITE)
        # two players
        for fx, col in [(0.30, (198, 40, 40)), (0.55, (28, 76, 136))]:
            fxc = x0 + fx * w
            d.ellipse([fxc - 7, y0 + h * 0.62, fxc + 7, y0 + h * 0.74], fill=(60, 48, 38))
            d.polygon([(fxc - 8, y1 - 4), (fxc + 8, y1 - 4), (fxc + 5, y0 + h * 0.74), (fxc - 5, y0 + h * 0.74)], fill=col)
    elif kind == "chess":
        d.rectangle([x0, y0, x1, y1], fill=(232, 226, 210))
        # chessboard, 4x4, kept fully below the banner; the pieces stand
        # ON the board (heads and crowns inside the board area)
        bs = min(w, h) * 0.62
        bx0, by0 = cx - bs / 2, y0 + h * 0.32
        for r in range(4):
            for c in range(4):
                col = (235, 230, 218) if (r + c) % 2 == 0 else (52, 48, 44)
                d.rectangle([bx0 + c * bs / 4, by0 + r * bs / 4, bx0 + (c + 1) * bs / 4, by0 + (r + 1) * bs / 4], fill=col)
        d.rectangle([bx0, by0, bx0 + bs, by0 + bs], outline=NAVY, width=2)
        # king (white) and queen (black) standing on the top row of the board
        for kx, col, crown in [(0.28, WHITE, True), (0.72, (40, 36, 32), False)]:
            kx = x0 + kx * w
            d.ellipse([kx - 8, by0 + 2, kx + 8, by0 + 16], fill=col, outline=NAVY, width=1)
            d.polygon([(kx - 10, by0 + 30), (kx + 10, by0 + 30), (kx + 6, by0 + 16), (kx - 6, by0 + 16)], fill=col, outline=NAVY, width=1)
            if crown:
                d.polygon([(kx - 5, by0 + 2), (kx, by0 - 4), (kx + 5, by0 + 2)], fill=(238, 178, 0))
        # two small pawns at the front
        for px in (0.18, 0.82):
            px = x0 + px * w
            d.ellipse([px - 6, y1 - 22, px + 6, y1 - 10], fill=(90, 84, 76))
            d.polygon([(px - 7, y1 - 4), (px + 7, y1 - 4), (px + 4, y1 - 12), (px - 4, y1 - 12)], fill=(90, 84, 76))


def art_below(kind, x0, y0, x1, y1, bh):
    # Draw the illustration on a separate layer, then paste only the part
    # below the red banner: no art element may be hidden by the banner or
    # poke above the panel's top edge. All art elements are placed below
    # y0+18 by construction; the crop is a safety net.
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    art(ld, kind, x0, y0, x1, y1)
    region = layer.crop((int(x0), int(y0 + bh), int(x1), int(y1)))
    img.paste(region, (int(x0), int(y0 + bh)), region)

# ---- content (display numbers 1-35, assigned afresh for account 3,
# REGION-LED: heroes = 3 regions, grid row 1 = Middle East block) ----
HEROES = [
    dict(num=1, banner="UKRAINE: 15 KILLED", region="KYIV, UKRAINE \u00b7 WAR", status="CONFIRMED",
         head="Russian strikes kill 15 in Ukraine",
         body="Latest count 15 \u2014 14 in Kyiv region, 1 in Zaporizhzhia. The toll rose through the day: 6, then 7, then 13. (Al Jazeera)",
         art="kyiv"),
    dict(num=2, banner="BENGHAZI: SHIP DOWN", region="BENGHAZI, LIBYA \u00b7 NAVY", status="CONFIRMED",
         head="Russian corvette capsized at Benghazi",
         body="Satellite images show the corvette Merkury capsized in port. No one has claimed it; the strike is suspected Ukrainian. (AP, Al Jazeera, WSJ)",
         art="benghazi"),
    dict(num=3, banner="COP31: NO DEAL", region="ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE", status="CONFIRMED",
         head="COP31 collapses in Antalya: no deal",
         body="Nearly 200 nations split over fossil-fuel text; the EU rejects a weak draft as the oil bloc blocks \u2018fossil fuels\u2019. Talks end with no deal. (Reuters, NPR, AJ)",
         art="antalya"),
]
GRID = [
    dict(num=4, banner="HORMUZ: TANKERS HIT", region="HORMUZ \u00b7 CONFLICT", status="OFFICIAL",
         head="Tankers ablaze in Hormuz, Iran claims mines",
         body="Iranian navy says 2 tankers hit mines in a \u2018restricted area\u2019. (Al Jazeera)", art="hormuz", rcol="Middle East"),
    dict(num=5, banner="TEHRAN: \u2018ALL TOOLS\u2019", region="TEHRAN \u00b7 STANDOFF", status="OFFICIAL",
         head="Iran: \u2018all tools\u2019 to break US blockade",
         body="Tehran vows every means to break the American blockade. (Al Jazeera)", art="tehran", rcol="Middle East"),
    dict(num=6, banner="GAZA: STRIKES GO ON", region="GAZA \u00b7 WAR", status="REPORTED",
         head="Gaza: strikes continue, displaced protest",
         body="Strikes go on as displaced families protest conditions. (Al Jazeera)", art="gaza", rcol="Middle East"),
    dict(num=7, banner="WEST BANK: 12 BURNED", region="WEST BANK \u00b7 SETTLERS", status="REPORTED",
         head="Settlers burn 12 vehicles in West Bank",
         body="Settlers torch a dozen vehicles; residents condemn the attacks. (Al Jazeera)", art="westbank", rcol="Middle East"),
    dict(num=8, banner="IRAN: MISSILE CITY", region="IRAN \u00b7 MISSILE", status="REPORTED",
         head="Iran shows twin-missile launcher, \u2018missile city\u2019",
         body="Tehran unveils a twin launcher in a new underground \u2018missile city\u2019. (Al Jazeera)", art="launcher", rcol="Middle East"),
    dict(num=9, banner="HOUSE: DEMS 258, GOP 173", region="WASHINGTON \u00b7 ELECTION", status="OFFICIAL",
         head="US House: Democrats 258, Republicans 173",
         body="AP count: Democrats 258, Republicans 173; 4 seats counted for neither party. (AP)", art="capitol", rcol="Americas"),
    dict(num=10, banner="WASHINGTON: WAR TALK", region="WASHINGTON \u00b7 WAR TALK", status="REPORTED",
         head="Trump \u2018inclined\u2019 to resume Iran war in January",
         body="Trump signals he leans toward resuming the Iran war in January. (Foreign Exchanges)", art="whitehouse", rcol="Middle East"),
    dict(num=11, banner="CIKANDE: FIRE, 24 DEAD", region="CIKANDE, INDONESIA \u00b7 FIRE", status="CONFIRMED",
         head="Indonesia factory fire kills 24",
         body="A candy-factory fire in Cikande, Serang, kills 24. Early reports said 3+. (Al Jazeera)", art="cikande", rcol="Asia"),
    dict(num=12, banner="LIVERPOOL 4\u20130 UNITED", region="LIVERPOOL \u00b7 FOOTBALL", status="REPORTED",
         head="Liverpool 4\u20130 Man United",
         body="Yoro sent off after 8 minutes in a rough start for Pochettino. (Al Jazeera)", art="anfield", rcol="Sport"),
    dict(num=13, banner="GENEVA: CHESS OPENS", region="GENEVA \u00b7 CHESS", status="REPORTED",
         head="World Chess title match opens in Geneva",
         body="The opening ceremony is held in Geneva; Game 1 is on 24 Nov. (World Chess)", art="chess", rcol="Sport"),
]
LIST = [
    (14, "France: police jailed for racist violence", "MS"),
    (15, "Croatia: 8 arrested over patient\u2019s death", "AJ"),
    (16, "Sudan: RSF drones kill 4 near Khartoum", "AJ"),
    (17, "Nigeria: boat capsizes, 24+ dead", "MS"),
    (18, "Somalia\u2013UAE split deepens", "AJ"),
    (19, "Bangladesh: 4+ dead in unrest", "AJ"),
    (20, "Trump hits Schumer as Dems push leaders", "AJ"),
    (21, "Kawas: first Palestinian in NY Senate", "AJ"),
    (22, "Virginia: first 2026 measles death", "AJ"),
    (23, "Seattle: ICE arrests condemned", "AJ"),
    (24, "Iowa: Army to blast 68 barrels of lead azide", "REU"),
    (25, "West Coast storm threatens Thanksgiving", "ABC"),
    (26, "Peru: quake sends moviegoers fleeing", "AJ"),
    (27, "Carney shares stage with Trump lookalike", "AJ"),
    (28, "Messi\u2019s Miami lose 0\u20133 to Columbus", "AJ"),
    (29, "Titans\u2019 Harrell hospitalised after crash", "AJ"),
    (30, "India A vs Pakistan A in Doha", "AJ"),
    (31, "Lion on the loose in T\u00fcrkiye", "AJ"),
    (32, "Israel: Likud\u2013Yashar coalition talks fail", "AJ"),
    (33, "Eisenkot: settler attacks are \u2018terrorism\u2019", "MS"),
    (34, "Lebanon: Israel pulls back, villagers find ruins", "NPR"),
    (35, "Idlib: landmine kills 5 children", "ARN"),
]
LIST_REGION = {14: "Europe", 15: "Europe", 16: "Africa", 17: "Africa", 18: "Africa",
               19: "Asia", 20: "Americas", 21: "Americas", 22: "Americas",
               23: "Americas", 24: "Americas", 25: "Americas", 26: "Americas",
               27: "Americas", 28: "Sport", 29: "Sport", 30: "Sport",
               31: "Sport", 32: "Middle East", 33: "Middle East",
               34: "Middle East", 35: "Middle East"}

# ---- heroes row (art 100 tall, tighter than account 2) ----
y0 = 254
hero_w = (CW - 16) / 3
for i, st in enumerate(HEROES):
    x = M + i * (hero_w + 8)
    art_below(st["art"], x, y0, x + hero_w, y0 + 100, 17)
    banner(d, x, y0, hero_w, st["banner"], 11)
    ty = y0 + 106
    num_badge(d, x + 9, ty + 7, 9, st["num"], NAVY)
    f_reg2 = font(F_SANS_B, 11)
    d.text((x + 22, ty + 2), st["region"], font=f_reg2, fill=INK)
    status_pill(d, x + hero_w - 62, ty + 1, st["status"])
    f_hh = fit(d, st["head"], F_SANS_B, 17, hero_w)
    hy = ty + 20
    for j, ln in enumerate(wrap(d, st["head"], f_hh, hero_w)):
        d.text((x, hy + j * 19), ln, font=f_hh, fill=INK)
    f_hb = font(F_SANS, 12)
    by = hy + 40
    for j, ln in enumerate(wrap(d, st["body"], f_hb, hero_w)[:2]):
        d.text((x, by + j * 14), ln, font=f_hb, fill=(40, 40, 40))

# ---- grid 5 x 2, region-grouped (row 1 = Middle East block),
# each cell carries a region-colour tick on its left edge ----
gy0 = 456
col_w = (CW - 32) / 5
row_h = 118
for i, st in enumerate(GRID):
    r, c = divmod(i, 5)
    x = M + c * (col_w + 8)
    y = gy0 + r * (row_h + 8)
    d.rectangle([x, y, x + 4, y + row_h], fill=REGIONS[st["rcol"]][0])
    art_below(st["art"], x + 6, y, x + col_w, y + 54, 14)
    banner(d, x + 6, y, col_w - 6, st["banner"], 8)
    ty = y + 56
    num_badge(d, x + 13, ty + 6, 7, st["num"], NAVY)
    f_gr = font(F_SANS_B, 9)
    d.text((x + 23, ty + 1), st["region"], font=f_gr, fill=INK)
    status_pill(d, x + col_w - 52, ty, st["status"])
    f_gh = fit(d, st["head"], F_SANS_B, 12, col_w)
    hy = ty + 14
    for j, ln in enumerate(wrap(d, st["head"], f_gh, col_w)[:2]):
        d.text((x + 6, hy + j * 13), ln, font=f_gh, fill=INK)
    f_gb = font(F_SANS, 10)
    by = hy + 26
    for j, ln in enumerate(wrap(d, st["body"], f_gb, col_w)[:2]):
        d.text((x + 6, by + j * 11), ln, font=f_gb, fill=(40, 40, 40))

# ---- bottom: BIG map (left) + ALSO ON list (right) ----
# REGION-LED: the map is the star of the page — 470 px wide (account 2
# used 330), holding ALL 35 numbered dots at true lon/lat.
y0 = 708
map_x, map_w = M, 470
list_x, list_w = M + 482, CW - 482

f_sec = font(F_SANS_B, 13)
d.text((map_x, y0), "WHERE IT HAPPENED \u2014 ALL 35 STORIES ON THE MAP", font=f_sec, fill=INK)
d.text((list_x, y0), "ALSO ON SUNDAY 22 NOVEMBER \u2014 22 MORE VERIFIED DISPATCHES", font=f_sec, fill=INK)

# world map (coarse equirectangular continents, lon/lat)
mx0, my0, mx1, my1 = map_x, y0 + 18, map_x + map_w, y0 + 208
d.rectangle([mx0, my0, mx1, my1], fill=MAPBG, outline=NAVY, width=1)


def ll2xy(lon, lat):
    # lat range 78..-52 so every continent (Greenland 76, S. America -50)
    # fits inside the panel with a ~2-3 px margin
    x = mx0 + (lon + 168) / 360 * (mx1 - mx0)
    y = my0 + (78 - lat) / 130 * (my1 - my0)
    return x, y


CONTINENTS = [
    # North America
    [(-168, 66), (-152, 70), (-132, 71), (-112, 72), (-92, 74), (-76, 72), (-66, 62), (-56, 54),
     (-60, 46), (-70, 42), (-75, 35), (-81, 31), (-84, 30), (-90, 28), (-97, 26), (-105, 20),
     (-110, 23), (-117, 33), (-124, 42), (-125, 49), (-135, 58), (-150, 60), (-165, 60)],
    # Greenland
    [(-44, 60), (-30, 68), (-20, 70), (-30, 76), (-55, 76), (-60, 70), (-55, 64)],
    # South America
    [(-79, 9), (-72, 4), (-60, -2), (-50, -4), (-38, -8), (-35, -15), (-40, -22), (-48, -28),
     (-57, -35), (-65, -41), (-70, -50), (-73, -44), (-73, -30), (-78, -18), (-81, -6), (-80, 2)],
    # Europe (with Iberia, Italy, Greece sketched in)
    [(-10, 36), (-9, 43), (-2, 48), (2, 51), (8, 55), (12, 58), (18, 62), (25, 68), (30, 70),
     (38, 68), (42, 60), (38, 55), (32, 50), (28, 45), (23, 40), (19, 42), (23, 37), (26, 38),
     (22, 37), (19, 40), (15, 44), (12, 44), (8, 44), (3, 42), (-1, 38), (-2, 36)],
    # Africa
    [(-17, 15), (-16, 25), (-10, 31), (-5, 35), (5, 37), (11, 34), (20, 32), (30, 31), (35, 28),
     (40, 20), (44, 11), (51, 11), (48, 2), (42, -5), (40, -15), (36, -25), (32, -29), (25, -34),
     (18, -35), (15, -28), (12, -18), (10, -5), (8, 4), (0, 6), (-8, 5), (-13, 8)],
    # Asia (with Arabia, India, SE Asia sketched in)
    [(38, 68), (55, 69), (70, 72), (90, 75), (110, 74), (130, 72), (150, 70), (170, 67), (178, 65),
     (170, 60), (162, 56), (158, 52), (150, 59), (142, 50), (140, 40), (135, 35), (128, 33), (122, 30),
     (115, 25), (108, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 13), (76, 8),
     (72, 20), (66, 25), (60, 25), (55, 26), (52, 28), (48, 30), (44, 35), (42, 42), (40, 50), (38, 60)],
    # Australia
    [(113, -22), (114, -30), (118, -35), (124, -33), (129, -32), (135, -35), (140, -38), (146, -39),
     (150, -37), (153, -32), (153, -27), (146, -19), (142, -15), (136, -12), (130, -13), (124, -14), (118, -20)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51), (-2, 50)],
    # Japan
    [(130, 31), (132, 34), (135, 34), (138, 36), (140, 38), (141, 42), (143, 44), (141, 40), (139, 35), (133, 33)],
]
# continents drawn on a separate layer, clipped to the map panel rect so no
# landmass can cross the panel border; high-contrast dark land on pale sea
map_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
md = ImageDraw.Draw(map_layer)
for poly in CONTINENTS:
    md.polygon([ll2xy(lon, lat) for lon, lat in poly], fill=(196, 178, 138), outline=(150, 132, 100))
# Indonesia islands + New Zealand (small)
for cx0, cy0, cw2, ch2 in [(102, -2, 26, 8), (114, -3, 18, 7), (131, -4, 22, 8), (167, -41, 10, 12)]:
    x, y = ll2xy(cx0, cy0)
    md.ellipse([x, y, x + cw2, y + ch2], fill=(196, 178, 138), outline=(150, 132, 100))
_mreg = map_layer.crop((mx0, my0, mx1, my1))
img.paste(_mreg, (mx0, my0), _mreg)

# map dots: ALL 35 stories at true lon/lat, numbered = the story number
# on this page, coloured by story region. Two dense clusters need extra
# spreading so every badge reads apart and the continents stay visible:
# the Levant (6 Gaza, 7 West Bank, 32 Likud, 33 Eisenkot, 34 Lebanon,
# 35 Idlib) and the US East Coast (9, 10, 20, 21, 22, 27).
DOTS_LATLON = [
    (1, 30.5, 50.4, "Europe"),        # Kyiv
    (2, 20.1, 32.1, "Africa"),        # Benghazi
    (3, 30.7, 36.9, "COP31"),         # Antalya
    (4, 56.5, 26.5, "Middle East"),   # Hormuz
    (5, 51.4, 35.7, "Middle East"),   # Tehran
    (6, 34.5, 31.5, "Middle East"),   # Gaza
    (7, 35.2, 32.0, "Middle East"),   # West Bank
    (8, 53.0, 32.0, "Middle East"),   # Iran (missile city)
    (9, -77.0, 38.9, "Americas"),     # Washington (US House)
    (10, -77.0, 38.9, "Middle East"), # Washington (Trump war talk)
    (11, 106.3, -6.2, "Asia"),        # Cikande, Indonesia
    (12, -3.0, 53.4, "Sport"),        # Liverpool
    (13, 6.1, 46.2, "Sport"),         # Geneva (World Chess)
    (14, 2.35, 48.85, "Europe"),      # Paris
    (15, 15.98, 45.81, "Europe"),     # Zagreb
    (16, 32.56, 15.5, "Africa"),      # Khartoum
    (17, 8.0, 9.5, "Africa"),         # Nigeria (central, no town given)
    (18, 45.32, 2.05, "Africa"),      # Mogadishu
    (19, 90.4, 23.8, "Asia"),         # Dhaka
    (20, -77.0, 38.9, "Americas"),    # Washington (Schumer)
    (21, -74.0, 40.7, "Americas"),    # New York (Kawas)
    (22, -78.0, 37.5, "Americas"),    # Richmond, Virginia
    (23, -122.3, 47.6, "Americas"),   # Seattle
    (24, -93.5, 41.9, "Americas"),    # Des Moines, Iowa
    (25, -122.4, 37.8, "Americas"),   # San Francisco (West Coast storm)
    (26, -77.0, -12.0, "Americas"),   # Lima (Peru quake)
    (27, -75.7, 45.4, "Americas"),    # Ottawa (Carney)
    (28, -80.2, 25.8, "Sport"),       # Miami
    (29, -86.8, 36.2, "Sport"),       # Nashville (Titans)
    (30, 51.5, 25.3, "Sport"),        # Doha (India A v Pakistan A)
    (31, 28.98, 41.0, "Sport"),       # Istanbul (lion in Turkiye)
    (32, 35.2, 31.8, "Middle East"),  # Jerusalem (Likud talks)
    (33, 35.2, 31.8, "Middle East"),  # Jerusalem (Eisenkot)
    (34, 35.5, 33.9, "Middle East"),  # Beirut
    (35, 36.6, 35.9, "Middle East"),  # Idlib
]
_pts = []
for _n, _lon, _lat, _reg in DOTS_LATLON:
    _tx, _ty = ll2xy(_lon, _lat)
    _pts.append([_n, _tx, _ty, _tx, _ty, _reg])  # n, true_x, true_y, bx, by, reg


def _spread(idxs, min_dist, passes):
    for _ in range(passes):
        _moved = False
        for _i in range(len(_pts)):
            if _pts[_i][0] not in idxs:
                continue
            for _j in range(_i + 1, len(_pts)):
                if _pts[_j][0] not in idxs:
                    continue
                _dx = _pts[_j][3] - _pts[_i][3]
                _dy = _pts[_j][4] - _pts[_i][4]
                _dist = math.hypot(_dx, _dy)
                if 0.01 < _dist < min_dist:
                    _push = (min_dist - _dist) / 2
                    _ux, _uy = _dx / _dist, _dy / _dist
                    _pts[_i][3] -= _ux * _push
                    _pts[_i][4] -= _uy * _push
                    _pts[_j][3] += _ux * _push
                    _pts[_j][4] += _uy * _push
                    _moved = True
                elif _dist <= 0.01:
                    _pts[_j][3] += 8
                    _pts[_j][4] += 8
                    _moved = True
        if not _moved:
            break


_all = set(range(1, 36))
_spread(_all, 20, 60)                       # global repulsion, min 20 px
_spread({6, 7, 32, 33, 34, 35}, 32, 100)    # Levant cluster, min 32 px
_spread({9, 10, 20, 21, 22, 27}, 30, 100)   # US East Coast cluster, min 30 px
_spread(_all, 20, 60)                       # cleanup pass: resolves collisions
# between cluster badges and outsiders (e.g. 32 vs 18) without undoing
# the cluster spacing, since cluster badges are already >= 26 px apart
for _p in _pts:
    _p[3] = max(mx0 + 10, min(mx1 - 10, _p[3]))
    _p[4] = max(my0 + 10, min(my1 - 10, _p[4]))
for _n, _tx, _ty, _bx, _by, _reg in _pts:
    if math.hypot(_bx - _tx, _by - _ty) > 2:
        d.line([_tx, _ty, _bx, _by], fill=(60, 60, 60), width=1)
        d.ellipse([_tx - 2, _ty - 2, _tx + 2, _ty + 2], fill=(60, 60, 60))
for _n, _tx, _ty, _bx, _by, _reg in _pts:
    num_badge(d, _bx, _by, 9, _n, REGIONS[_reg][0])

# map legend: counts per region + the "each number" note, 2 rows
ly = my1 + 5
f_leg = font(F_SANS_B, 10)
lx = map_x
for name, (col, n) in REGIONS.items():
    d.rectangle([lx, ly, lx + 9, ly + 9], fill=col)
    t = "%s %d" % (name, n)
    d.text((lx + 12, ly), t, font=f_leg, fill=INK)
    lx += d.textlength(t, font=f_leg) + 14
    if lx > map_x + map_w - 60:
        lx = map_x
        ly += 14
d.text((map_x, ly + 14), "Each number is that number on this page.", font=font(F_SANS, 10), fill=GREY)

# ALSO ON list: 2 columns x 11 rows, labels shortened to fit one line
f_li = font(F_SANS_B, 11)
col_w2 = list_w / 2
row_h2 = 17
for i, (n, lab, src) in enumerate(LIST):
    c, r = divmod(i, 11)
    x = list_x + c * col_w2
    y = y0 + 18 + r * row_h2
    num_badge(d, x + 8, y + 8, 8, n, REGIONS[LIST_REGION[n]][0])
    t = "%s (%s)" % (lab, src)
    f_use = fit(d, t, F_SANS_B, 11, col_w2 - 22)
    d.text((x + 20, y + 2), t, font=f_use, fill=INK)

# ---- DATE CHECK bar ----
y0 = 952
d.rectangle([M, y0, W - M, y0 + 28], outline=RED, width=2)
f_dc = font(F_SANS_B, 10)
dc = ("DATE CHECK \u2014 Excluded on purpose (first reported before Sunday 22 Nov UTC): UK\u2013EU deal (20 Nov) \u00b7 "
      "killer-robot talks (21 Nov) \u00b7 Mexico cartel boss arrest (20\u201321 Nov) \u00b7 Asian stocks (23 Nov). "
      "Not yet on 22 Nov: World Chess Game 1 (24 Nov) \u00b7 Iowa lead-azide blast (Mon/Tue) \u00b7 NATO Brussels meeting.")
for j, ln in enumerate(wrap(d, dc, f_dc, CW - 16)):
    d.text((M + 8, y0 + 4 + j * 12), ln, font=f_dc, fill=INK)

# ---- footer ----
f_ft = font(F_SANS, 11)
f_ftb = font(F_SANS_B, 11)
fy = 986
d.text((M, fy), "Every story happened or was first reported on Sunday 22 November 2026 UTC.", font=f_ftb, fill=INK)
leg = "C CONFIRMED  2+ outlets      O OFFICIAL  on the record      R REPORTED  single outlet"
d.text((W - M - d.textlength(leg, font=f_ft), fy), leg, font=f_ft, fill=INK)
d.text((M, fy + 16), "Sources named beside each story \u00b7 Original drawings \u00b7 Counts may change.",
       font=f_ft, fill=GREY)

img.save(OUT)
data = open(OUT, "rb").read()
print("saved", OUT, len(data), "bytes, sha256", hashlib.sha256(data).hexdigest())
print("size", img.size)
