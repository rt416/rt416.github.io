"""Lay out the career-journey scene: a trail winding gently but steadily up from left to right, milestone
dots on it, faint scenery (distant range, hills, pines, boulders, birds) and the trail carrying on
past the last milestone, fading out at the edge. Writes data/journey.yaml for the Hugo partial.

Run from the repo root: python3 tools/journey_layout.py data/journey.yaml"""
import math, sys
X0, X1 = 18, 506            # trail start; last milestone
def trail_y(x):
    t = (x - X0) / (X1 - X0)
    return 266 - 192 * t ** 1.18 + 6 * math.sin(2 * math.pi * (x - X0) / 140) * (1 - .35 * t)

def smooth(pts):
    """Catmull-Rom through the points, as cubic Bezier segments."""
    p = [pts[0]] + pts + [pts[-1]]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(p) - 2):
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p[i - 1], p[i], p[i + 1], p[i + 2]
        d += (f" C{x1 + (x2 - x0) / 6:.1f} {y1 + (y2 - y0) / 6:.1f}"
              f" {x2 - (x3 - x1) / 6:.1f} {y2 - (y3 - y1) / 6:.1f} {x2:.1f} {y2:.1f}")
    return d

milestones = [  # label, label_ja, x, era, side
    ("Imperial", "Imperial", 48, 0, "below"),
    ("Cambridge", "Cambridge", 88, 0, "above"),
    ("UCL PhD", "UCL 博士課程", 124, 1, "below"),
    ("ThinkSono", "ThinkSono", 164, 1, "above"),
    ("Butterfly Network", "Butterfly Network", 206, 1, "below"),
    ("InnerEye", "InnerEye", 258, 2, "above"),
    ("T-Detect", "T-Detect", 298, 2, "below"),
    ("Flamingo-CXR", "Flamingo-CXR", 350, 3, "above"),
    ("Med-Gemini", "Med-Gemini", 390, 3, "below"),
    ("AMIE", "AMIE", 428, 3, "above"),
    ("AI co-scientist", "AI co-scientist", 466, 3, "below"),
    ("AI co-clinician", "AI co-clinician", 506, 3, "above"),
]
xs = list(range(X0, X1, 6)) + [X1]
trail = smooth([(x, trail_y(x)) for x in xs])
# Beyond the last milestone the trail keeps climbing and fades out at the edge.
ahead = smooth([(X1, trail_y(X1)), (530, trail_y(X1) - 12), (552, trail_y(X1) - 26), (576, trail_y(X1) - 42), (604, trail_y(X1) - 60)])

# Skyline: an even rhythm of soft crests that rises with the trail; the summit lies beyond the frame.
def far_y(x):
    t = x / 608
    return 150 - 118 * t ** 1.3 - 20 * (.5 + .5 * math.cos(2 * math.pi * (x - 556) / 132))
def mid_y(x):
    # The slope the trail climbs: follows the trail a little above it, without bumps.
    t = (x - X0) / (X1 - X0)
    return 238 - 196 * max(t, 0) ** 1.18 if x <= X1 else mid_y(X1) - (x - X1) * .5
def back_y(x):
    # A paler, farther range behind, offset in rhythm so its crests sit between the near ones.
    t = x / 608
    return 128 - 100 * t ** 1.25 - 15 * (.5 + .5 * math.cos(2 * math.pi * (x - 490) / 118))
ridge = smooth([(x, far_y(x)) for x in range(0, 609, 8)])
far = ridge + " L608 300 L0 300 Z"
back = smooth([(x, back_y(x)) for x in range(0, 609, 8)]) + " L608 300 L0 300 Z"
# Etched contours under the skyline, fainter the further down they go.
contours = "".join(f'<path class="contour c{k}" d="{smooth([(x, far_y(x) + 7 * k) for x in range(0, 609, 8)])}"/>' for k in (1, 2))
mid = smooth([(x, mid_y(x)) for x in range(0, 609, 8)]) + " L608 300 L0 300 Z"
near = smooth([(0, 284), (120, 280), (240, 268), (360, 256), (480, 246), (608, 240)]) + " L608 300 L0 300 Z"

def pine(x, y, h=14):
    # Three tiers, like an ink-drawn pine.
    w, d = h * .42, ""
    for i, (top, bot, ww) in enumerate([(0, .45, .55), (.25, .72, .8), (.5, 1, 1)]):
        yt, yb = y - h + top * (h - 3), y - h + bot * (h - 3)
        d += f"M{x} {yt:.1f}L{x - w * ww:.1f} {yb:.1f}Q{x} {yb - 1.2:.1f} {x + w * ww:.1f} {yb:.1f}Z"
    return f'<path class="tree" d="{d}M{x} {y - 3}V{y}"/>'
def hut(x, y, w=11.5):
    # A tiny hut on the slope beside the trail: walls, pitched roof and a door.
    h = w * .55
    return (f'<path class="hut" d="M{x - w / 2:.1f} {y:.1f}V{y - h:.1f}L{x:.1f} {y - h - w * .45:.1f}L{x + w / 2:.1f} {y - h:.1f}V{y:.1f}Z'
            f'M{x - w * .13:.1f} {y:.1f}V{y - h * .55:.1f}H{x + w * .13:.1f}V{y:.1f}"/>')
def rock(x, y, w=7):
    return f'<path class="rock" d="M{x - w} {y}C{x - w} {y - w * .9:.1f} {x + w * .2:.1f} {y - w * 1.1:.1f} {x + w} {y}Z"/>'
def bird(x, y, s=4.5):
    return f'<path class="bird" d="M{x - s} {y - s * .5:.1f}Q{x - s * .45:.1f} {y - s * .7:.1f} {x} {y}Q{x + s * .45:.1f} {y - s * .7:.1f} {x + s} {y - s * .5:.1f}"/>'

scene = "".join([
    *(pine(x, y, h) for x, y, h in [(378, 266, 13), (391, 270, 17), (404, 265, 12), (440, 254, 15), (453, 258, 19), (467, 253, 13),
                                     (548, 244, 14), (561, 248, 18), (575, 243, 12), (594, 246, 13), (186, 282, 11), (198, 285, 13)]),
    # A small flock heading the way the trail goes.
    bird(168, 62, 4.4), bird(182, 55, 3.8), bird(156, 70, 3.6), bird(196, 49, 3.2), bird(178, 68, 3),
])
def sun_at(x, y, r):
    # A pale disc with a faint ring of glow around it.
    return f'<circle class="sun-glow" cx="{x}" cy="{y}" r="{r + 7}"/><circle class="sun" cx="{x}" cy="{y}" r="{r}"/>'
sun = sun_at(92, 58, 19)

eras = [  # label, label_ja, from, to, year
    ("Maths & Neuroscience", "数学・神経科学", 14, 94, "2010"),
    ("PhD & Start-ups", "博士・スタートアップ", 108, 226, "2015"),
    ("Microsoft Research", "Microsoft Research", 242, 314, "2019"),
    ("Google DeepMind", "Google DeepMind", 332, 520, "2022"),
]

def hut_spot(x0):
    """Place a hut on the slope just beside the trail near x0, clear of the trail and every label."""
    W, H = 11.5, 11.5
    boxes = []
    for _, _, mx, _, side in milestones:
        my, w = trail_y(mx), 5.6 * len(_label_of(mx))
        boxes.append((mx - 5 - w, my - 16, mx - 5, my - 4) if side == "above" else (mx + 5, my + 5, mx + 5 + w, my + 17))
    for dx in (0, -8, 8, -16, 16):
        x = x0 + dx
        xs = [x - W / 2 + k * W / 6 for k in range(7)]
        for off in (7, 10, 13, 16, 19, 22):
            for below in (True, False):
                base = (max(trail_y(t) for t in xs) + off + H) if below else (min(trail_y(t) for t in xs) - off)
                box = (x - W / 2 - 2, base - H - 2, x + W / 2 + 2, base + 2)
                if not any(box[0] < b[2] and b[0] < box[2] and box[1] < b[3] and b[1] < box[3] for b in boxes):
                    return x, base
    return x0, trail_y(x0) + 24
def _label_of(mx):
    return next(m[0] for m in milestones if m[2] == mx)
huts = "".join(hut(*hut_spot(x)) for x in (100, 232, 324))

# ---- Portrait version for phones (340 wide): the trail rises up the screen toward the skyline,
# milestone labels to its left, era names in the left margin between eras.
MW, MH = 340, 560
def m_trail_x(y):
    u = (540 - y) / 444
    return 246 + 16 * math.sin(2 * math.pi * u * 1.6) + 10 * u
m_ys = [516 - i * 38.2 for i in range(len(milestones))]
m_trail = smooth([(m_trail_x(y), y) for y in [540] + [540 - k * 6 for k in range(1, 74)] + [m_ys[-1]] if y >= m_ys[-1]])
yl = m_ys[-1]
m_ahead = smooth([(m_trail_x(yl), yl), (m_trail_x(yl) + 6, yl - 22), (m_trail_x(yl) + 16, yl - 44), (m_trail_x(yl) + 30, yl - 70), (m_trail_x(yl) + 46, 4)])
def m_far_y(x):
    return 118 - 30 * x / MW - 12 * (.5 + .5 * math.cos(2 * math.pi * (x - 262) / 112))
def m_back_y(x):
    return 98 - 28 * x / MW - 10 * (.5 + .5 * math.cos(2 * math.pi * (x - 200) / 96))
m_ridge = smooth([(x, m_far_y(x)) for x in range(0, MW + 1, 6)])
m_far = m_ridge + f" L{MW} {MH} L0 {MH} Z"
m_back = smooth([(x, m_back_y(x)) for x in range(0, MW + 1, 6)]) + f" L{MW} {MH} L0 {MH} Z"
m_contours = "".join(f'<path class="contour c{k}" d="{smooth([(x, m_far_y(x) + 7 * k) for x in range(0, MW + 1, 6)])}"/>' for k in (1, 2))
m_near = smooth([(0, 470), (90, 476), (180, 466), (260, 450), (MW, 440)]) + f" L{MW} {MH} L0 {MH} Z"
m_sun = sun_at(50, 40, 14)
m_scene = "".join([
    *(pine(x, y, h) for x, y, h in [(26, 548, 13), (38, 552, 16), (50, 547, 11), (300, 548, 12), (312, 552, 15),
                                     (316, 372, 10), (327, 375, 12), (300, 236, 9), (310, 239, 11)]),
    bird(92, 42, 3.8), bird(104, 36, 3.3), bird(82, 49, 3.1), bird(116, 31, 2.8),
])
# Beside the trail on the open right-hand side, level with the gap between eras.
m_huts = "".join(hut(m_trail_x((m_ys[a] + m_ys[a + 1]) / 2) + 20, (m_ys[a] + m_ys[a + 1]) / 2 + 6) for a in (1, 4, 6))
m_eras = []
for i, (lab, ja, a, b, yr) in enumerate(eras):
    ks = [k for k, m in enumerate(milestones) if m[3] == i]
    m_eras.append((lab, ja, yr, (m_ys[ks[0]] + 9, m_ys[ks[-1]] - 9)))

out = ["# Career journey scene on the home page, between the intro and Selected Work (608 wide).",
       "# Generated by tools/journey_layout.py: edit labels, milestones and scenery there, then re-run it.",
       f'back: "{back}"', f'far: "{far}"', f'ridge: "{ridge}"', f"contours: '{contours}'", f"sun: '{sun}'", f'mid: "{mid}"', f'near: "{near}"', f'trail: "{trail}"', f'ahead: "{ahead}"',
       f"scene: '{scene}'", f"huts: '{huts}'", "milestones:"]
for lab, ja, x, era, side in milestones:
    out.append(f'  - {{ label: "{lab}", label_ja: "{ja}", x: {x}, y: {trail_y(x):.1f}, era: {era}, side: "{side}" }}')
out.append("eras:")
for (lab, ja, a, b, yr), (_, _, _, (m0, m1)) in zip(eras, m_eras):
    out.append(f'  - {{ label: "{lab}", label_ja: "{ja}", from: {a}, to: {b}, m_from: {m0:.1f}, m_to: {m1:.1f}' + (f', year: "{yr}"' if yr else "") + " }")
out += ["mobile:", f'  back: "{m_back}"', f'  far: "{m_far}"', f'  ridge: "{m_ridge}"', f"  contours: '{m_contours}'",
        f"  sun: '{m_sun}'", f'  near: "{m_near}"', f'  trail: "{m_trail}"', f'  ahead: "{m_ahead}"', f"  scene: '{m_scene}'", f"  huts: '{m_huts}'",
        "  milestones:"] + [f"    - {{ x: {m_trail_x(y):.1f}, y: {y:.1f} }}" for y in m_ys]
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(out) + "\n")
