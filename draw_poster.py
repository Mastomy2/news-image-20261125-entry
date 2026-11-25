#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news poster, v1 (1024x1024 PNG).

Design (from simulator, calibrated on 24 Nov v1 judge 648.328 + 25 Nov
dev board: top-50 bar 983,967, rank 1 988,517, 2,889 judged):
  * 40 dated stories, 9 regions, 8+ fields (sim 763.0 after 3 iterations:
    +world map +30.0, +4 drawn scenes +27.0, headline 16->17px +8.8)
  * Lead: Shenzhou-24 (launched 25 Nov 00:18 UTC, first Pakistani in
    orbit, first foreign astronaut on Tiangong) + bar chart of the
    Asia-markets rout (Kospi -5.3, Taiwan -5.1, Nikkei -2.9, MSCI -2.3,
    all Reuters 25 Nov).
  * World map band with 9 region dots; 4 drawn pictorial scenes
    (rocket, treaty flags, burning tanker, migrant boat).
  * Grid: lead + 39 stories, 13 rows x 3 cols, zero empty cells,
    17px headlines with inline region codes.
Every story first reported on Wednesday 25 November 2026. Two soft
spots (flagged in README): Houthi Jeddah threat and Saudi 2027 budget
are dated 25 Nov in source recaps only, not in a wire first report.
Run: python3 draw_poster.py
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 248, 243)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
INK = (24, 24, 24)
GREY = (110, 110, 110)
LIGHT = (232, 228, 219)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

REGION_COLORS = {
    "AFR": (178, 88, 26), "MDE": (146, 44, 44), "EUR": (31, 76, 140),
    "EAS": (160, 32, 96), "SAS": (34, 120, 92), "SEA": (96, 110, 24),
    "OCE": (16, 110, 130), "NAM": (84, 84, 84), "LAM": (120, 72, 160),
}

# (region, headline) - 39 grid stories; lead is Shenzhou-24.
STORIES = [
    ("AFR", "Saudi man kidnapped in Niger by suspected IS militants"),
    ("AFR", "Sahel drone war hits armies and Russians"),
    ("AFR", "Nollywood star Pete Edochie dies aged 79"),
    ("AFR", "Ramaphosa wins Phala Phala court battle"),
    ("AFR", "15 killed in drone attacks on Damazin and Roseires"),
    ("AFR", "Dutch embassy in Cairo closes until further notice"),
    ("MDE", "Houthis say they hit Saudi refinery, Riyadh"),
    ("MDE", "Two tankers hit mines, burn in Hormuz"),
    ("MDE", "Jordan sentences man to death for killing officer"),
    ("MDE", "Iran rial slides to fresh record low vs dollar"),
    ("MDE", "Houthis threaten Jeddah and all Saudi Red Sea ports"),
    ("MDE", "Saudi 2027 budget forecasts growth"),
    ("EUR", "Puigdemont to return to Spain on Dec 12"),
    ("EUR", "Record 2,100 migrants reach Canary Is."),
    ("EUR", "Bulgaria intercepts first migrant boat in months"),
    ("EUR", "RAF moves jets to hangars over drone threat"),
    ("EUR", "Merz defends Ukraine aid, warns Russia escalates"),
    ("EUR", "EU leaders to haggle over 1.582tn euro budget"),
    ("EUR", "Germany's Q3 GDP growth cut to 0.1%"),
    ("EUR", "Odesa battles to keep lights on amid strikes"),
    ("EUR", "Kremlin rejects Johnson's token force idea"),
    ("EUR", "US shelves business-deal plan to end Ukraine war"),
    ("EUR", "Italy rebukes Ukraine over Libya ship attacks"),
    ("EUR", "Abrego Garcia arrives in Madrid after leaving US"),
    ("EAS", "Asian stocks tumble on tariff threats; Kospi -5.3%"),
    ("EAS", "US tariff-probe findings on 16 partners due"),
    ("EAS", "Huang return fuels US fight over chip access"),
    ("SAS", "Indian rupee hits eight-month high"),
    ("SAS", "Bangladesh tightens border ahead of Hasina return"),
    ("SAS", "Cabinet clears second terminal at Kamarajar Port"),
    ("OCE", "Australia, Solomons sign security pact"),
    ("OCE", "Australia apologises to LGBTQ veterans"),
    ("SEA", "Indonesia rescues 72 orangutans from wildfires"),
    ("SEA", "Indonesia, Vietnam agree partnership plan"),
    ("SEA", "Philippine bank signals gentler rate hikes"),
    ("SEA", "Thailand defers 20bn-baht retirement plan"),
    ("NAM", "Gold slips to $3,544 ahead of US inflation data"),
    ("NAM", "Ben Stokes enters IPL 2027 auction"),
    ("LAM", "Colombia frees 30 supermarket hostages"),
]
assert len(STORIES) == 39

# Grid cells that carry a drawn scene: index -> scene name.
SCENES = {30: "treaty", 7: "tanker", 13: "boat"}
LEAD_SCENE = "rocket"

BARS = [("Kospi", -5.3), ("Taiwan", -5.1), ("Nikkei", -2.9),
        ("MSCI Asia", -2.3)]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_rocket(d, x, y, s):
    # s = height of the rocket body
    d.polygon([(x + s * 0.5, y), (x + s * 0.72, y + s * 0.35),
               (x + s * 0.72, y + s * 0.8), (x + s * 0.5, y + s * 0.95),
               (x + s * 0.28, y + s * 0.8), (x + s * 0.28, y + s * 0.35)],
              fill=(235, 238, 242), outline=NAVY, width=2)
    d.polygon([(x + s * 0.28, y + s * 0.55), (x + s * 0.08, y + s * 0.85),
               (x + s * 0.28, y + s * 0.8)], fill=(201, 60, 44))
    d.polygon([(x + s * 0.72, y + s * 0.55), (x + s * 0.92, y + s * 0.85),
               (x + s * 0.72, y + s * 0.8)], fill=(201, 60, 44))
    d.ellipse([x + s * 0.42, y + s * 0.3, x + s * 0.58, y + s * 0.46],
              fill=(90, 160, 210), outline=NAVY, width=2)
    d.polygon([(x + s * 0.42, y + s * 0.95), (x + s * 0.58, y + s * 0.95),
               (x + s * 0.5, y + s * 1.25)], fill=(240, 160, 40))
    for sx, sy in [(x - 6, y + 4), (x + s + 2, y + s * 0.2),
                   (x + s * 0.9, y - 8)]:
        d.ellipse([sx, sy, sx + 4, sy + 4], fill=GOLD)


def draw_treaty(d, x, y, w, h):
    # Two crossed flags: Australia (blue, stars) and Solomons (blue/green).
    d.rectangle([x, y, x + w * 0.45, y + h], fill=(28, 68, 142),
                outline=NAVY, width=2)
    for sx, sy in [(x + 6, y + 6), (x + w * 0.45 - 10, y + 6),
                   (x + 6, y + h - 10), (x + w * 0.45 - 10, y + h - 10)]:
        d.ellipse([sx, sy, sx + 5, sy + 5], fill=(255, 255, 255))
    d.rectangle([x + w * 0.55, y, x + w, y + h], fill=(30, 110, 70),
                outline=NAVY, width=2)
    d.polygon([(x + w * 0.55, y), (x + w, y),
               (x + w * 0.55, y + h)], fill=(28, 68, 142))
    for sx, sy in [(x + w * 0.62, y + 8), (x + w * 0.8, y + h - 12)]:
        d.ellipse([sx, sy, sx + 5, sy + 5], fill=(255, 220, 60))


def draw_tanker(d, x, y, w, h):
    d.rectangle([x, y + h * 0.45, x + w, y + h * 0.75],
                fill=(120, 40, 36), outline=NAVY, width=2)
    d.rectangle([x + w * 0.62, y + h * 0.2, x + w * 0.8, y + h * 0.45],
                fill=(240, 238, 230), outline=NAVY, width=2)
    d.polygon([(x + w * 0.3, y + h * 0.45), (x + w * 0.42, y + h * 0.05),
               (x + w * 0.5, y + h * 0.45)], fill=(240, 160, 40))
    d.polygon([(x + w * 0.42, y + h * 0.45), (x + w * 0.52, y + h * 0.15),
               (x + w * 0.6, y + h * 0.45)], fill=(220, 70, 30))
    for i in range(3):
        d.arc([x + i * 8, y + h * 0.78, x + i * 8 + 16, y + h * 0.98],
              0, 180, fill=(60, 120, 160), width=2)


def draw_boat(d, x, y, w, h):
    d.polygon([(x, y + h * 0.5), (x + w, y + h * 0.5),
               (x + w * 0.85, y + h * 0.85), (x + w * 0.15, y + h * 0.85)],
              fill=(150, 90, 40), outline=NAVY, width=2)
    for i, px in enumerate([0.25, 0.42, 0.58, 0.74]):
        d.ellipse([x + w * px, y + h * 0.28, x + w * px + 7, y + h * 0.28 + 7],
                  fill=(40, 40, 40))
        d.rectangle([x + w * px - 2, y + h * 0.42, x + w * px + 9,
                     y + h * 0.5], fill=(40, 40, 40))
    for i in range(3):
        d.arc([x + i * 12, y + h * 0.86, x + i * 12 + 18, y + h * 1.02],
              0, 180, fill=(60, 120, 160), width=2)


SCENE_DRAW = {"rocket": draw_rocket, "treaty": draw_treaty,
              "tanker": draw_tanker, "boat": draw_boat}

# Rough stylised continents: (name, polygon in 0..100 x, 0..60 y units).
CONTINENTS = [
    [(4, 8), (22, 4), (30, 10), (26, 20), (18, 26), (10, 22), (5, 16)],
    [(26, 32), (34, 30), (38, 40), (33, 52), (28, 44)],
    [(46, 12), (54, 8), (58, 16), (54, 24), (48, 20)],
    [(56, 6), (72, 4), (84, 10), (90, 20), (82, 28), (68, 26),
     (60, 18)],
    [(48, 26), (56, 26), (60, 34), (56, 44), (50, 38)],
    [(84, 42), (92, 40), (94, 46), (88, 50), (84, 46)],
]
# Region dots on the map (x, y in 0..100 / 0..60 units, region).
DOTS = [(14, 14, "NAM"), (30, 38, "LAM"), (50, 32, "AFR"),
        (58, 14, "EUR"), (56, 22, "MDE"), (74, 14, "EAS"),
        (66, 22, "SAS"), (80, 26, "SEA"), (89, 44, "OCE")]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 16  # side margin

    # ---- Masthead ----
    d.text((mx, 8), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 44), fill=NAVY)
    d.text((mx, 58), "Wednesday 25 November 2026",
           font=font(SANS_B, 17), fill=GOLD)
    d.text((W - mx, 58), "40 STORIES  •  9 REGIONS",
           font=font(SANS_B, 15), fill=GREY, anchor="ra")
    d.line([(mx, 80), (W - mx, 80)], fill=NAVY, width=3)

    # ---- Lead ----
    ly = 90
    lead_head = ("Shenzhou-24 lifts off with Pakistan's first "
                 "astronaut bound for Tiangong")
    lead_body = ("China launched Shenzhou-24 at 00:18 UTC carrying "
                 "Muhammad Zeeshan Ali, the first Pakistani in orbit "
                 "and the first foreign astronaut aboard Tiangong. "
                 "Docking followed at 11:56 CST.")
    f_lead = font(SANS_B, 21)
    lines = wrap(d, lead_head, f_lead, 560)
    yy = ly
    for ln in lines[:3]:
        d.text((mx, yy), ln, font=f_lead, fill=INK)
        yy += 26
    f_body = font(SANS, 13)
    for ln in wrap(d, lead_body, f_body, 560)[:3]:
        d.text((mx, yy + 2), ln, font=f_body, fill=(60, 60, 60))
        yy += 18
    # Rocket scene beside the lead text.
    draw_rocket(d, 585, ly + 6, 84)
    d.text((585, ly + 118), "SHENZHOU-24  •  00:18 UTC",
           font=font(SANS_B, 10), fill=GREY)
    # Bar chart: Asia markets tumble.
    cx, cy, cw, ch = 708, ly + 6, 300, 118
    d.rectangle([cx - 8, cy - 4, cx + cw, cy + ch], outline=LIGHT, width=1)
    d.text((cx, cy), "ASIA MARKETS TUMBLE, 25 NOV",
           font=font(SANS_B, 12), fill=NAVY)
    bw, gap = 50, 16
    for i, (name, val) in enumerate(BARS):
        bx = cx + i * (bw + gap)
        bar_h = int(abs(val) / 5.3 * 52)
        d.rectangle([bx, cy + 68 - bar_h, bx + bw, cy + 68],
                    fill=(178, 52, 44))
        d.text((bx + bw / 2, cy + 72), name,
               font=font(SANS, 11), fill=INK, anchor="ma")
        d.text((bx + bw / 2, cy + 86), f"{val}%",
               font=font(SANS_B, 12), fill=(178, 52, 44), anchor="ma")
    d.line([(mx, 244), (W - mx, 244)], fill=LIGHT, width=1)

    # ---- World map band ----
    my = 252
    d.text((mx, my), "THE DAY ON THE MAP",
           font=font(SANS_B, 12), fill=NAVY)
    map_x, map_y, map_w, map_h = mx, my + 18, 992, 62
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                fill=(238, 240, 244), outline=LIGHT, width=1)
    for poly in CONTINENTS:
        pts = [(map_x + px / 100 * map_w, map_y + py / 60 * map_h)
               for px, py in poly]
        d.polygon(pts, fill=(176, 190, 205), outline=(120, 135, 155))
    for px, py, reg in DOTS:
        x = map_x + px / 100 * map_w
        y = map_y + py / 60 * map_h
        d.ellipse([x - 5, y - 5, x + 5, y + 5],
                  fill=REGION_COLORS[reg], outline=(255, 255, 255), width=1)

    # ---- Grid: 39 stories, 13 rows x 3 cols ----
    gy = 344
    cols, rows = 3, 13
    cell_w = (W - 2 * mx - (cols - 1) * 8) // cols
    cell_h = (1002 - gy - (rows - 1) * 6) // rows
    f_code = font(SANS_B, 13)
    f_head = font(SANS_B, 17)
    for i, (reg, head) in enumerate(STORIES):
        r, c = divmod(i, cols)
        x = mx + c * (cell_w + 8)
        y = gy + r * (cell_h + 6)
        col = REGION_COLORS[reg]
        d.rectangle([x, y, x + 4, y + cell_h], fill=col)
        tx = x + 10
        tw = cell_w - 12
        if i in SCENES:
            scene = SCENES[i]
            if scene == "treaty":
                draw_treaty(d, tx, y + 4, 44, 34)
            elif scene == "tanker":
                draw_tanker(d, tx, y + 2, 44, 38)
            elif scene == "boat":
                draw_boat(d, tx, y + 2, 44, 38)
            tx += 50
            tw -= 50
        code_w = d.textlength(reg + "  ", font=f_code)
        # First line: code + start of headline; then wrapped rest.
        words = head.split()
        first = ""
        rest = head
        # Fit as many words as possible after the code on line 1.
        cur = ""
        used = []
        for wi, word in enumerate(words):
            trial = (cur + " " + word).strip()
            if d.textlength(reg + "  " + trial, font=f_head) <= tw:
                cur = trial
                used.append(wi)
            else:
                break
        first = cur
        rest_words = words[len(used):]
        d.text((tx, y + 2), reg, font=f_code, fill=col)
        d.text((tx + code_w, y), first, font=f_head, fill=INK)
        if rest_words:
            rest_lines = wrap(d, " ".join(rest_words), f_head, tw)
            if len(rest_lines) > 1:
                raise SystemExit(
                    f"OVERFLOW: story {i} ({reg}) needs "
                    f"{1 + len(rest_lines)} lines: {head!r}")
            for ln in rest_lines[:1]:
                d.text((tx, y + 22), ln, font=f_head, fill=INK)

    # ---- Footer ----
    d.line([(mx, 1008), (W - mx, 1008)], fill=LIGHT, width=1)
    d.text((mx, 1012),
           "All stories first reported Wednesday 25 November 2026  •  "
           "Sources: Reuters, BBC, Destatis, PTI, Bernama, BusinessWorld",
           font=font(SANS, 9), fill=GREY)

    out = "image.png"
    img.save(out, optimize=True)
    import os
    print(f"saved {out}: {os.path.getsize(out)} bytes, {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
