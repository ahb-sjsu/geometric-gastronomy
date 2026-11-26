"""Figures for Geometric Gastronomy (Volume 12): Chapters 1 to 14 and Appendices A to C.

Every figure is drawn from a formula, a definition or a worked example in the chapter it
illustrates. Where a chapter gives no numbers, the values are illustrative and the caption
says so. No figure draws as a result an analysis the volume tags "no run is recorded"
(Sections 4.7, 9.2, 10.4, Appendix D), and none draws a number on the "Unresolved" list of
CORRECTIONS-2026-11-26.md.
"""

import math

from figkit import BORDER, CRITICAL, GRID, INK, INK2, INK3, SERIES, SURFACE, Axes, Canvas, legend, reg

CH = {
    1: "chapters/ch01_taste_as_geometry.md",
    2: "chapters/ch02_the_receptor_basis.md",
    3: "chapters/ch03_the_metric_of_flavor.md",
    4: "chapters/ch04_similarity_and_complementarity.md",
    5: "chapters/ch05_the_pairing_manifold.md",
    6: "chapters/ch06_the_algebra_of_seasoning.md",
    7: "chapters/ch07_transformations_under_heat.md",
    8: "chapters/ch08_recipe_as_geometric_construction.md",
    9: "chapters/ch09_the_eigenvalues_of_a_kitchen.md",
    10: "chapters/ch10_flavor_embeddings.md",
    11: "chapters/ch11_the_geometry_of_nutrition.md",
    12: "chapters/ch12_sensory_integration.md",
    13: "chapters/ch13_designing_flavors.md",
    14: "chapters/ch14_open_problems.md",
    "A": "chapters/ch15_appendix_a_mathematical_preliminaries.md",
    "B": "chapters/ch16_appendix_b_flavor_compound_databases.md",
    "C": "chapters/ch17_appendix_c_experimental_methods.md",
}


# ------------------------------------------------------------------ helpers
def _canvas(w, h, title):
    assert len(title) <= 68, title
    return Canvas(w, h, title)


class _Map:
    """Data-to-pixel map for a plotting region, with no ticks drawn."""

    def __init__(self, x0, y0, w, h, xlim, ylim):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.xlim, self.ylim = xlim, ylim
        self.sx = w / (xlim[1] - xlim[0])
        self.sy = h / (ylim[1] - ylim[0])

    def X(self, v):
        return self.x0 + (v - self.xlim[0]) * self.sx

    def Y(self, v):
        return self.y0 + self.h - (v - self.ylim[0]) * self.sy

    def P(self, p):
        return self.X(p[0]), self.Y(p[1])


def _da(dash):
    return f' stroke-dasharray="{dash}"' if dash else ""


def _poly(c, pts, fill, opacity=0.15, stroke="none", width=1.0, dash=None):
    d = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    c.add(f'<polygon points="{d}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" '
          f'stroke-width="{width}"{_da(dash)} stroke-linejoin="round"/>')


def _path(c, pts, stroke, width=2.0, dash=None, opacity=1.0):
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    c.add(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" '
          f'stroke-linecap="round"{_da(dash)} stroke-opacity="{opacity}"/>')


def _hollow(c, x, y, col, r=4.5):
    c.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{SURFACE}" stroke="{col}" stroke-width="2"/>')


def _ring(c, x, y, r, col, width=1.5, dash=None, fill="none", opacity=1.0):
    c.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}" fill-opacity="{opacity}" '
          f'stroke="{col}" stroke-width="{width}"{_da(dash)}/>')


def _rectline(c, x, y, w, h, col, width=1.0, dash=None, fill="none", opacity=1.0):
    c.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" fill-opacity="{opacity}" '
          f'stroke="{col}" stroke-width="{width}"{_da(dash)}/>')


def _htext(c, x, y, s, size=11.5, anchor="start", color=INK, weight="normal", italic=False):
    """Text with a surface-coloured halo, for labels that sit over lines (contours, curves)."""
    from xml.sax.saxutils import escape
    from svgfig import FONT
    it = ' font-style="italic"' if italic else ""
    c.add(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" fill="{color}" '
          f'text-anchor="{anchor}" font-weight="{weight}"{it} stroke="{SURFACE}" stroke-width="4" '
          f'stroke-linejoin="round" paint-order="stroke">{escape(str(s))}</text>')


def _lines(c, x, y, rows, size=11.5, anchor="start", color=INK2, lh=17):
    for i, s in enumerate(rows):
        if s:
            c.text(x, y + i * lh, s, size, anchor, color)


def _mbox(c, x, y, w, h, title, subs=(), stroke=BORDER, fill="#1a3248", tsize=12):
    """Box with a bold title and up to three plain lines under it."""
    c.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="6" fill="{fill}" '
          f'stroke="{stroke}" stroke-width="1"/>')
    n = 1 + len(subs)
    top = y + h / 2 - (n - 1) * 7.5 + 4
    c.text(x + w / 2, top, title, tsize, "middle", INK, "600")
    for i, s in enumerate(subs):
        c.text(x + w / 2, top + 15 * (i + 1), s, 10.5, "middle", INK2)


def _sym2(a, b, d):
    """Eigenvalues of [[a, b], [b, d]] and the angle (degrees) of the leading eigenvector."""
    tr, disc = (a + d) / 2, math.sqrt(((a - d) / 2) ** 2 + b * b)
    return tr + disc, tr - disc, 0.5 * math.degrees(math.atan2(2 * b, a - d))


def _ell(c, cx, cy, S, m, k=1.0, **kw):
    """Draw the k-standard-deviation ellipse of covariance S (data units) at pixel (cx, cy)."""
    a, b, d = S[0][0] * m.sx ** 2, -S[0][1] * m.sx * m.sy, S[1][1] * m.sy ** 2
    l1, l2, ang = _sym2(a, b, d)
    c.ellipse(cx, cy, k * math.sqrt(l1), k * math.sqrt(max(l2, 0.0)), ang, **kw)


def _inv2(M):
    (a, b), (cc, d) = M
    det = a * d - b * cc
    return [[d / det, -b / det], [-cc / det, a / det]]


def _mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def _tr(A):
    return [[A[0][0], A[1][0]], [A[0][1], A[1][1]]]


def _mv(M, v):
    return (M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1])


def _sqrtm(M):
    """Square root of a 2 x 2 symmetric positive-definite matrix."""
    s = math.sqrt(M[0][0] * M[1][1] - M[0][1] * M[1][0])
    t = math.sqrt(M[0][0] + M[1][1] + 2 * s)
    return [[(M[0][0] + s) / t, M[0][1] / t], [M[1][0] / t, (M[1][1] + s) / t]]


def _rot(deg, v):
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def _norm(v):
    return math.hypot(v[0], v[1])


def _contour_d(fn, m, nx, ny, level):
    """Marching squares: an SVG path string for the level set fn = level over the map's box."""
    xs = [m.xlim[0] + (m.xlim[1] - m.xlim[0]) * i / nx for i in range(nx + 1)]
    ys = [m.ylim[0] + (m.ylim[1] - m.ylim[0]) * j / ny for j in range(ny + 1)]
    V = [[fn(x, y) for x in xs] for y in ys]
    parts = []
    for j in range(ny):
        for i in range(nx):
            cs = [(xs[i], ys[j], V[j][i]), (xs[i + 1], ys[j], V[j][i + 1]),
                  (xs[i + 1], ys[j + 1], V[j + 1][i + 1]), (xs[i], ys[j + 1], V[j + 1][i])]
            pts = []
            for k in range(4):
                (xa, ya, va), (xb, yb, vb) = cs[k], cs[(k + 1) % 4]
                if (va - level) * (vb - level) < 0:
                    t = (level - va) / (vb - va)
                    pts.append(m.P((xa + t * (xb - xa), ya + t * (yb - ya))))
            for q in range(0, len(pts) - 1, 2):
                (x1, y1), (x2, y2) = pts[q], pts[q + 1]
                parts.append(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}")
    return " ".join(parts)


# ------------------------------------------------------------------ chapter 1
def fig_1_1():
    names = ["sweet", "umami", "salty", "bitter", "sour"]
    w = {"umami": 0.40, "sweet": 0.35, "sour": 0.20, "salty": 0.03, "bitter": 0.02}
    assert abs(sum(w.values()) - 1.0) < 1e-12
    p = reg(CH[1], "1.1",
            "The five taste qualities of Section 1.1 as the vertices of a simplex, drawn as a pentagon. The "
            "drawing is a flat projection of a four-dimensional simplex, so distances in it are not to scale. "
            "A vertex is one pure quality, an edge a mixture of two, and the interior a blend of all five, "
            "where the chapter places real tastes. The ripe tomato is an interior point weighted toward umami "
            "and sweet with a sour edge; its weights are illustrative. The dashed curve marks the bulge the "
            "chapter posits for the segment from salt to umami, drawn schematically.",
            "## 1.2 The Olfactory Manifold")
    c = _canvas(720, 400, "Five tastes as the corners of a simplex, not the axes of a cube")
    cx, cy, R = 215, 222, 140
    V = {}
    for k, nm in enumerate(names):
        a = math.radians(-90 + 72 * k)
        V[nm] = (cx + R * math.cos(a), cy + R * math.sin(a))
    for i in range(5):
        for j in range(i + 1, 5):
            side = (j - i) in (1, 4)
            c.line(*V[names[i]], *V[names[j]], INK3 if side else BORDER, 1.5 if side else 1)
    for nm in names:
        x, y = V[nm]
        dx, dy = x - cx, y - cy
        n = math.hypot(dx, dy)
        lx, ly = x + 20 * dx / n, y + 20 * dy / n + 4
        anchor = "middle" if abs(dx) < 30 else ("start" if dx > 0 else "end")
        if abs(dx) < 30:
            ly = y - 12
        c.text(lx, ly, nm, 12.5, anchor, INK, "600")
        c.dot(x, y, SERIES[0], 4.5, title=f"pure {nm}")
    # the posited bulge of the salt to umami segment (schematic)
    (x1, y1), (x2, y2) = V["umami"], V["salty"]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    nx, ny = mx - cx, my - cy
    nn = math.hypot(nx, ny)
    qx, qy = mx + 44 * nx / nn, my + 44 * ny / nn
    c.add(f'<path d="M{x1:.2f},{y1:.2f} Q{qx:.2f},{qy:.2f} {x2:.2f},{y2:.2f}" fill="none" stroke="{SERIES[1]}" '
          f'stroke-width="2" stroke-dasharray="5 4"/>')
    tx = sum(w[nm] * V[nm][0] for nm in names)
    ty = sum(w[nm] * V[nm][1] for nm in names)
    c.line(tx, ty, 296, 108, INK3, 1)
    c.dot(tx, ty, SERIES[4], 5, title="ripe tomato, illustrative weights")
    c.text(300, 104, "ripe tomato", 11.5, "start", INK)
    x0 = 440
    _lines(c, x0, 84, ["A vertex is one pure quality,", "an edge a mixture of two,",
                       "the interior a blend of all five."], 11.5, color=INK2)
    _lines(c, x0, 158, ["Ripe tomato, illustrative weights:", "umami 0.40, sweet 0.35, sour 0.20,",
                        "salty 0.03, bitter 0.02"], 11.5, color=INK2)
    c.line(x0, 236, x0 + 26, 236, SERIES[1], 2, dash="5 4")
    _lines(c, x0 + 34, 240, ["salt to umami mixtures bulge", "(Chapter 3; schematic)"], 11.5, color=INK2)
    _lines(c, x0, 300, ["Henning's tetrahedron (1916):", "four vertices, tastes on its",
                        "surface only"], 11.5, color=INK3)
    c.save(p)


def fig_1_2():
    f0, fs = (0.08, 0.08), (0.60, 0.45)
    v_lime, v_miso = (1.0, 0.0), (0.0, 1.0)
    det = v_lime[0] * v_miso[1] - v_miso[0] * v_lime[1]
    d = (fs[0] - f0[0], fs[1] - f0[1])
    alpha = (d[0] * v_miso[1] - v_miso[0] * d[1]) / det
    beta = (v_lime[0] * d[1] - d[0] * v_lime[1]) / det
    assert abs(alpha - 0.52) < 1e-12 and abs(beta - 0.37) < 1e-12
    p = reg(CH[1], "1.2",
            "The line cook's fix of the closing box of Chapter 1 as vector addition, drawn in the plane of the "
            "sour and umami taste components only. The flat purée f0 sits near zero on both, and the balanced "
            f"target f* lies a short distance away. Lime pushes along +sour and miso along +umami. The fix is "
            f"two numbers, here α = {alpha:.2f} and β = {beta:.2f}, and either order of the two additions reaches "
            "the same point. The coordinates are illustrative; the chapter gives none.",
            "## What This Book Will Show")
    c = _canvas(720, 400, "The line cook's fix: two numbers, not a search over forty jars")
    ax = Axes(c, 80, 50, 380, 290, (0, 0.8), (0, 0.6), [0, 0.2, 0.4, 0.6, 0.8], [0, 0.2, 0.4, 0.6],
              "sour component of f", "umami component of f")
    a1 = (f0[0] + alpha, f0[1])
    b1 = (f0[0], f0[1] + beta)
    P = lambda q: (ax.X(q[0]), ax.Y(q[1]))  # noqa: E731
    # the other order, dashed
    c.line(*P(f0), *P(b1), SERIES[1], 1.5, dash="5 4", opacity=0.6)
    c.line(*P(b1), *P(fs), SERIES[0], 1.5, dash="5 4", opacity=0.6)
    c.arrow(*P(f0), *P(a1), SERIES[0], 2.5)
    c.arrow(*P(a1), *P(fs), SERIES[1], 2.5)
    c.dot(*P(f0), INK, 5, title="flat purée f0")
    c.dot(*P(fs), CRITICAL, 5.5, title="balanced target f*")
    x, y = P(f0)
    c.text(x - 10, y + 20, "flat purée f0", 11.5, "end", INK)
    xm = (ax.X(f0[0]) + ax.X(a1[0])) / 2
    c.text(xm, ax.Y(f0[1]) + 18, "+ α v_lime", 11.5, "middle", INK)
    c.text(ax.X(fs[0]) + 10, (ax.Y(a1[1]) + ax.Y(fs[1])) / 2 + 4, "+ β v_miso", 11.5, "start", INK)
    c.text(ax.X(fs[0]) + 10, ax.Y(fs[1]) - 8, "balanced target f*", 11.5, "start", INK)
    _lines(c, 500, 92, ["f0 + α v_lime + β v_miso = f*", f"α = {alpha:.2f},  β = {beta:.2f}"], 12, color=INK)
    _lines(c, 500, 150, ["solid: lime, then miso", "dashed: miso, then lime", "both orders reach f*"], 11.5)
    _lines(c, 500, 228, ["only the sour and umami", "components are drawn; lime and",
                         "miso also carry aroma, and miso", "a little salt"], 11, color=INK3)
    c.save(p)


# ------------------------------------------------------------------ chapter 2
def fig_2_1():
    N, M, Dlo, Dhi = 1e4, 400, 10, 30
    assert N / M == 25 and int(M / Dhi) == 13 and M / Dlo == 40
    p = reg(CH[2], "2.1",
            "The chain of three dimensionalities of Section 2.4 on a logarithmic scale: about 10,000 chemical "
            "species, about 400 receptor channels, and 10 to 30 perceptual dimensions. The binding affinity "
            "matrix A performs a 25-fold compression, and the neural reduction a further 13-to-40-fold one "
            "(400/30 and 400/10). The lighter part of the last bar is the range from 10 to 30.",
            "## 2.5 Individual Variation as Rotations of Flavor Space")
    c = _canvas(720, 400, "From ten thousand compounds to a few tens of perceptual axes")
    m = _Map(230, 60, 450, 270, (1, 1e5), (0, 1))
    X = lambda v: m.x0 + m.w * math.log10(v) / 5  # noqa: E731
    for v, lab in ((1, "1"), (10, "10"), (100, "100"), (1e3, "1,000"), (1e4, "10,000"), (1e5, "100,000")):
        c.line(X(v), 60, X(v), 316, GRID, 1)
        c.text(X(v), 334, lab, 11, "middle", INK2)
    c.text(m.x0 + m.w / 2, 356, "count, logarithmic scale", 11.5, "middle", INK2)
    rows = [("chemical species, N", 105, N, "about 10,000"), ("receptor channels, M", 195, M, "about 400"),
            ("perceptual dimensions, D", 285, Dlo, "10 to 30")]
    for name, y, v, lab in rows:
        c.text(m.x0 - 14, y + 4, name, 12, "end", INK, "600")
        c.hrect(X(1), y - 11, X(v) - X(1), 22, SERIES[0], title=f"{name}: {lab}")
        if v == Dlo:
            c.hrect(X(Dlo), y - 11, X(Dhi) - X(Dlo), 22, SERIES[0], opacity=0.4, title="range 10 to 30")
            c.text(X(Dhi) + 8, y + 4, lab, 11.5, "start", INK)
        else:
            c.text(X(v) + 8, y + 4, lab, 11.5, "start", INK)
    c.text(X(1) + 12, 152, "binding affinity matrix A: 25-fold", 11.5, "start", INK2, italic=True)
    c.text(X(1) + 12, 242, "neural reduction: 13- to 40-fold", 11.5, "start", INK2, italic=True)
    c.save(p)


def fig_2_2():
    K = list(range(1, 17))
    gains = [0.5, 1.0, 2.0]
    floor = 0.1
    counts = [sum(1 for k in K if g * math.exp(-(k - 1) / 4) > floor) for g in gains]
    assert counts == [7, 10, 12]
    p = reg(CH[2], "2.2",
            "Effective flavor dimensionality as Section 2.6 defines it: the count of eigenvalues of a person's "
            "receptor covariance that clear the noise floor. One illustrative spectrum, λk = g·exp(−(k − 1)/4), "
            "is drawn at three gains g. Raising the gain lifts marginal eigenvalues above the floor of 0.1, "
            "from 7 axes at g = 0.5 to 10 at g = 1 and 12 at g = 2, as the chapter describes for supertasters. "
            "Hollow markers lie below the floor. The vertical axis is logarithmic; spectrum, gains and floor "
            "are illustrative, not measured.",
            "## What the Basis Buys Us")
    c = _canvas(720, 400, "Higher gain lifts more eigenvalues above the noise floor")
    ax = Axes(c, 80, 66, 470, 256, (0.5, 16.5), (0.008, 3.0), [1, 4, 8, 12, 16], [0.01, 0.1, 1],
              "eigenvalue rank k", "eigenvalue, log scale", ylog=True)
    yf = ax.Y(floor)
    c.line(ax.x0, yf, ax.x0 + ax.w, yf, INK3, 1.5, dash="5 4")
    c.text(ax.x0 + ax.w, yf - 6, "noise floor 0.1", 10.5, "end", INK2, italic=True)
    for j, (g, n) in enumerate(zip(gains, counts)):
        pts = [(ax.X(k), ax.Y(g * math.exp(-(k - 1) / 4))) for k in K]
        c.polyline(pts, SERIES[j], 2, title=f"gain {g}")
        for k, (x, y) in zip(K, pts):
            val = g * math.exp(-(k - 1) / 4)
            if val > floor:
                c.dot(x, y, SERIES[j], 4, title=f"g = {g}, k = {k}: {val:.3f}")
            else:
                _hollow(c, x, y, SERIES[j], 3.5)
        c.text(pts[-1][0] + 12, pts[-1][1] + 4, f"g = {g:g}: {n} axes", 11, "start", INK2)
    legend(c, 80, 48, [("g = 0.5, non-taster", SERIES[0]), ("g = 1", SERIES[1]),
                       ("g = 2, supertaster", SERIES[2])])
    c.save(p)


# ------------------------------------------------------------------ chapter 3
def fig_3_1():
    base, n = 2.0, list(range(1, 9))
    a = 1.4

    def step_pow(k):
        return (base + k) ** a - (base + k - 1) ** a

    def step_log(k):
        return math.log((base + k) / (base + k - 1))

    pw = [step_pow(k) / step_pow(1) for k in n]
    lg = [step_log(k) / step_log(1) for k in n]
    assert abs(pw[5] - 1.554) < 1e-3 and abs(lg[5] - 0.329) < 1e-3
    p = reg(CH[3], "3.1",
            "The pinch test of Chapter 3 under the chapter's two laws. Each pinch adds the same amount of salt "
            "to a soup that already holds two pinches' worth, an illustrative baseline. The vertical axis is "
            "the change in perceived intensity that each pinch produces, relative to the first pinch. Under "
            "Fechner's logarithm (Section 3.1) each pinch is a smaller ratio of what is already present and "
            f"moves perception less: the sixth moves it {lg[5]:.2f} times as far as the first. Under Stevens' "
            "power law with the chapter's salt exponent of 1.4 (Section 3.3) each pinch moves it more: the "
            f"sixth moves it {pw[5]:.2f} times as far.",
            "## 3.4 Cross-Adaptation as Metric Distortion")
    c = _canvas(720, 400, "Equal pinches, unequal steps: the logarithm against the power law")
    ax = Axes(c, 80, 66, 470, 256, (0.6, 8.4), (0, 2.0), n, [0, 0.5, 1, 1.5, 2],
              "pinch number", "step relative to the first pinch")
    y1 = ax.Y(1)
    c.line(ax.x0, y1, ax.x0 + ax.w, y1, INK3, 1.5, dash="4 4")
    c.text(ax.x0 + ax.w, y1 + 16, "a linear ruler: equal steps", 10.5, "end", INK2, italic=True)
    for j, (name, ys) in enumerate([("power law, a = 1.4", pw), ("logarithm", lg)]):
        pts = [(ax.X(k), ax.Y(v)) for k, v in zip(n, ys)]
        c.polyline(pts, SERIES[j], 2, title=name)
        for k, (x, y), v in zip(n, pts, ys):
            c.dot(x, y, SERIES[j], 4.5, title=f"{name}, pinch {k}: {v:.3f}")
        c.text(pts[-1][0] + 12, pts[-1][1] + 4, name, 11, "start", INK2)
        x6, y6 = pts[5]
        c.text(x6, y6 - 11, f"{ys[5]:.2f}", 11, "middle", INK)
    legend(c, 80, 48, [("Stevens, salt exponent 1.4", SERIES[0]), ("Fechner, logarithm", SERIES[1])])
    c.save(p)


def fig_3_2():
    s, phi = 0.6, 35.0
    G1 = [[1.0, 0.0], [0.0, 1.0]]
    A1 = [[s, 0.0], [0.0, 1.0]]
    G1a = _mm(_tr(A1), _mm(G1, A1))
    G2 = [[1.0, 0.0], [0.0, 0.4]]
    r = math.radians(phi)
    A2 = [[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]]
    G2a = _mm(_tr(A2), _mm(G2, A2))
    # salt: a unit perceived change now needs 1/s of salt
    assert abs(1 / math.sqrt(G1a[0][0]) - 1 / s) < 1e-12
    # rotation: the pure sour step gains a sweet component in perceived coordinates
    v = _mv(A2, (1.0, 0.0))
    assert v[1] > 0.5
    p = reg(CH[3], "3.2",
            "Cross-adaptation as the metric distortion g ↦ Aᵀ g A of Section 3.4, drawn as the set of "
            "displacements of unit perceived length before and after exposure. Left, axis rescaling: "
            "adaptation to salt, with A = diag(0.6, 1), stretches the set along the salt axis, so a step of "
            "1/0.6 ≈ 1.67 times as much salt now reads as the same perceived change. Right, axis rotation: a "
            "rotation of 35°, of the kind the chapter ascribes to miraculin turning sour toward sweet, turns the "
            "principal directions of an anisotropic metric, so a pure sour displacement acquires a sweet "
            "component. The values are illustrative.",
            "## 3.5 Temporal Dynamics: Flavor as a Curve")
    c = _canvas(720, 400, "Adaptation rescales or rotates the metric it measures")
    sc = 80
    panels = [(185, 222, G1, G1a, "axis rescaling (salt adaptation)", "salt", "other"),
              (540, 222, G2, G2a, "axis rotation (miraculin)", "sour", "sweet")]
    for cx, cy, G, Ga, title, xl, yl in panels:
        m = _Map(cx - sc * 2, cy - sc * 2, 4 * sc, 4 * sc, (-2, 2), (-2, 2))
        c.line(cx - 165, cy, cx + 165, cy, BORDER, 1)
        c.line(cx, cy - 130, cx, cy + 128, BORDER, 1)
        c.text(cx + 165, cy + 16, xl, 11.5, "end", INK2)
        c.text(cx, cy - 136, yl, 11.5, "middle", INK2)
        c.text(cx, 60, title, 12.5, "middle", INK, "600")
        _ell(c, cx, cy, _inv2(G), m, 1.0, stroke=SERIES[0], fill=SERIES[0], width=2, opacity=0.08,
             title="before exposure")
        _ell(c, cx, cy, _inv2(Ga), m, 1.0, stroke=SERIES[1], fill="none", width=2, title="after exposure")
    # principal directions after rotation, right panel
    cx, cy = 540, 222
    for ang in (-phi, 90 - phi):
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        c.line(cx - 128 * dx, cy + 128 * dy, cx + 128 * dx, cy - 128 * dy, SERIES[1], 1, dash="3 4")
    c.text(704, cy + 134, "dotted: principal directions", 10.5, "end", INK2)
    c.text(704, cy + 148, "after exposure, turned by 35°", 10.5, "end", INK2)
    legend(c, 18, 388, [("before exposure", SERIES[0]), ("after exposure", SERIES[1])])
    c.text(704, 388, "curves: displacements of unit perceived length", 10.5, "end", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 4
def fig_4_1():
    L1, L2 = 3.0, 2.0
    res = {}
    for th in (10.0, 90.0):
        t = math.radians(th)
        res[th] = (math.sqrt(L1 ** 2 + L2 ** 2 + 2 * L1 * L2 * math.cos(t)), L1 * L2 * math.sin(t))
    assert abs(res[90.0][0] - math.sqrt(13)) < 1e-12 and abs(res[90.0][1] - 6) < 1e-12
    assert abs(res[10.0][0] - 4.98) < 0.005 and abs(res[10.0][1] - 1.04) < 0.005
    p = reg(CH[4], "4.1",
            "Two ways for summands to combine (Sections 4.4 and 4.5), drawn for vectors of length 3 and 2. "
            f"Similar summands at an angle of 10° add nearly colinearly: the resultant has length "
            f"{res[10.0][0]:.2f}, close to the sum of lengths 5, and the pair spans an area of only "
            f"{res[10.0][1]:.2f}. Complementary summands at 90° add by the Pythagorean rule: the resultant has "
            f"length {res[90.0][0]:.2f}, points in a direction neither summand occupies, and the pair spans an "
            "area of 6. The shaded parallelogram is the spanned area the chapter uses as its measure of "
            "complementarity.",
            "## 4.6 Synergy and Antagonism")
    c = _canvas(720, 400, "Similar summands lengthen the sum; complementary ones steer it")
    sc = 62
    for (ox, oy), a1, a2, th, head in (((50, 334), 15, 25, 10.0, "(a) similar: angle 10°"),
                                      ((420, 334), 0, 90, 90.0, "(b) complementary: angle 90°")):
        v1 = (L1 * math.cos(math.radians(a1)), L1 * math.sin(math.radians(a1)))
        v2 = (L2 * math.cos(math.radians(a2)), L2 * math.sin(math.radians(a2)))
        P = lambda q: (ox + sc * q[0], oy - sc * q[1])  # noqa: E731,B023
        sm = (v1[0] + v2[0], v1[1] + v2[1])
        _poly(c, [P((0, 0)), P(v1), P(sm), P(v2)], SERIES[2], 0.18, SERIES[2], 1, dash="4 3")
        c.arrow(*P((0, 0)), *P(v1), SERIES[0], 2.5)
        c.arrow(*P((0, 0)), *P(v2), SERIES[1], 2.5)
        c.arrow(*P((0, 0)), *P(sm), INK, 2.5)
        L, area = res[th]
        c.text(ox, 70, head, 12.5, "start", INK, "600")
        if th == 10.0:
            c.text(P(v1)[0] + 8, P(v1)[1] + 18, "f1, length 3", 11, "start", INK2)
            c.text(P(v2)[0] - 14, P(v2)[1] - 12, "f2, length 2", 11, "end", INK2)
            c.text(P(sm)[0] + 8, P(sm)[1] - 6, "f1 + f2", 11.5, "start", INK)
            _lines(c, ox, 92, [f"|f1 + f2| = {L:.2f}, against 3 + 2 = 5", f"spanned area {area:.2f}"], 11.5)
        else:
            c.text(P(v1)[0] + 8, P(v1)[1] + 4, "f1", 11.5, "start", INK2)
            c.text(P(v2)[0] - 8, P(v2)[1] + 4, "f2", 11.5, "end", INK2)
            c.text(P(sm)[0] + 8, P(sm)[1] - 6, "f1 + f2", 11.5, "start", INK)
            c.text((P((0, 0))[0] + P(sm)[0]) / 2 + 10, (P((0, 0))[1] + P(sm)[1]) / 2 + 30,
                   f"area {area:.0f}", 11, "start", INK2)
            _lines(c, ox, 92, [f"|f1 + f2| = {L:.2f} = √(3² + 2²)", f"spanned area {area:.0f}"], 11.5)
    c.save(p)


def fig_4_2():
    p = reg(CH[4], "4.2",
            "The second-order sum of Section 4.6, f1 + f2 + B(f1, f2), with illustrative values. Left, synergy: "
            "for salt and glutamate the interaction term B pushes along +umami, so the mixture lands above the "
            "linear sum. Right, antagonism: for sugar and quinine B pulls along −bitter, so the mixture lands "
            "below it. The hollow marker is the linear sum that a flat model would predict.",
            "## 4.7 Experimental Validation: A Proposed Reanalysis")
    c = _canvas(720, 400, "Synergy and antagonism bend the sum off the linear prediction")
    sc = 150
    for (ox, oy), xl, yl, n1, n2, B, head, blab in (
            ((90, 340), "saltiness", "umami", "f1: salt", "f2: glutamate", 0.45, "(a) synergy: salt and glutamate",
             "B pushes +umami"),
            ((450, 340), "sweetness", "bitterness", "f1: sugar", "f2: quinine", -0.45, "(b) antagonism: sugar and quinine",
             "B pulls −bitter")):
        P = lambda q: (ox + sc * q[0], oy - sc * q[1])  # noqa: E731,B023
        f1, f2 = (0.9, 0.0), (0.0, 0.8)
        lin = (0.9, 0.8)
        dish = (0.9, 0.8 + B)
        c.line(ox, oy, ox + 236, oy, BORDER, 1)
        c.line(ox, oy, ox, oy - 215, BORDER, 1)
        c.text(ox + 236, oy + 16, xl, 11.5, "end", INK2)
        c.text(ox + 6, oy - 207, yl, 11.5, "start", INK2)
        c.text(ox - 40, 62, head, 12.5, "start", INK, "600")
        c.line(*P(f1), *P(lin), INK3, 1, dash="3 3")
        c.line(*P(f2), *P(lin), INK3, 1, dash="3 3")
        c.arrow(*P((0, 0)), *P(f1), SERIES[0], 2.5)
        c.arrow(*P((0, 0)), *P(f2), SERIES[1], 2.5)
        c.text(P(f1)[0], P(f1)[1] + 16, n1, 11, "middle", INK2)
        c.text(P(f2)[0] - 8, P(f2)[1] + 4, n2, 11, "end", INK2)
        c.arrow(*P(lin), *P(dish), SERIES[2], 2.5)
        _hollow(c, *P(lin), INK2, 4.5)
        c.dot(*P(dish), INK, 5, title="perceived mixture")
        c.text(P(lin)[0] + 12, P(lin)[1] + 4, "linear sum f1 + f2", 11, "start", INK2)
        c.text(P(dish)[0] + 12, P(dish)[1] + 4, "with B: the mixture", 11, "start", INK)
        mid = ((P(lin)[1] + P(dish)[1]) / 2)
        c.text(P(lin)[0] - 10, mid + 4, blab, 11, "end", INK2, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 5
def _kshell(d, sigma=1.0):
    u = (d / sigma) ** 2
    return u * math.exp(-u)


def fig_5_1():
    mu, A = (6.2, 3.6), (0.035, 0.08)
    anc, sigma, beta = (3.2, 4.2), 1.0, 1.0

    def H(x, y):
        t1 = -(A[0] * (x - mu[0]) ** 2 + A[1] * (y - mu[1]) ** 2)
        return t1 - beta * _kshell(math.hypot(x - anc[0], y - anc[1]), sigma)

    tom = (anc[0] + sigma * math.cos(math.radians(-35)), anc[1] + sigma * math.sin(math.radians(-35)))
    blue = (6.6, 3.1)
    h_tom, h_blue, h_anc = H(*tom), H(*blue), H(*anc)
    assert h_tom < h_anc and h_tom < h_blue
    p = reg(CH[5], "5.1",
            "A two-dimensional slice of the hedonic function H that Section 5.6 posits, keeping its "
            "inverted-paraboloid term (i) and one uncanny-valley term (iii). The contours are levels of H, "
            "brighter for higher values. Around the strawberry anchor the penalty digs a ring-shaped moat at "
            "the radius σ (dashed), lower than both the anchor and the ground outside it. A pairing whose sum "
            f"lands in the moat, where the chapter places strawberry and tomato, scores H = {h_tom:.2f}; one that "
            f"lands in open country near the interior, where it places blue cheese and honey, scores "
            f"{h_blue:.2f}. All positions and parameters are illustrative: μ = (6.2, 3.6), A = diag(0.035, "
            "0.08), σ = 1, β = 1.",
            "## 5.4 Novelty as Distance from the Training Manifold")
    c = _canvas(720, 400, "A moat around the anchor: the posited hedonic map in two dimensions")
    m = _Map(40, 50, 440, 308, (0, 10), (0, 7))
    _rectline(c, m.x0, m.y0, m.w, m.h, GRID, 1)
    levels = [-2.0, -1.6, -1.2, -0.9, -0.65, -0.45, -0.3, -0.18, -0.08]
    for i, lv in enumerate(levels):
        op = 0.25 + 0.75 * i / (len(levels) - 1)
        d = _contour_d(H, m, 120, 84, lv)
        c.add(f'<path d="{d}" fill="none" stroke="{SERIES[0]}" stroke-width="1.4" stroke-opacity="{op:.2f}">'
              f'<title>H = {lv}</title></path>')
    ax, ay = m.P(anc)
    _ring(c, ax, ay, sigma * m.sx, INK2, 1.5, dash="5 4")
    c.dot(ax, ay, INK, 4.5, title="strawberry anchor")
    _htext(c, ax, ay - m.sx * sigma - 10, "strawberry anchor", 11.5, "middle", INK)
    tx, ty = m.P(tom)
    c.dot(tx, ty, SERIES[1], 5.5, title=f"strawberry + tomato, H = {h_tom:.2f}")
    _htext(c, tx + 2, ty + 22, "strawberry + tomato", 11.5, "middle", INK)
    bx, by = m.P(blue)
    c.dot(bx, by, SERIES[2], 5.5, title=f"blue cheese + honey, H = {h_blue:.2f}")
    _htext(c, bx, by + 22, "blue cheese + honey", 11.5, "middle", INK)
    c.text(m.x0 + m.w / 2, m.y0 + m.h + 20, "a two-dimensional slice of flavor space", 11, "middle", INK3,
           italic=True)
    _lines(c, 500, 74, ["contours of H, brighter is higher:", "terms (i) and (iii) of Section 5.6"], 11.5)
    c.line(500, 122, 526, 122, INK2, 1.5, dash="5 4")
    c.text(534, 126, "moat radius σ", 11.5, "start", INK2)
    _lines(c, 500, 166, [f"H at strawberry + tomato: {h_tom:.2f}", f"H at the anchor: {h_anc:.2f}",
                         f"H at blue cheese + honey: {h_blue:.2f}"], 11.5, color=INK)
    _lines(c, 500, 248, ["illustrative values:", "μ = (6.2, 3.6)", "A = diag(0.035, 0.08)",
                         "σ = 1, β = 1"], 11, color=INK3)
    c.save(p)


def fig_5_2():
    ds = [4 * i / 400 for i in range(401)]
    ks = [_kshell(d) for d in ds]
    i = max(range(len(ks)), key=lambda j: ks[j])
    assert abs(ds[i] - 1.0) < 1e-9 and abs(ks[i] - math.exp(-1)) < 1e-12
    p = reg(CH[5], "5.2",
            "The shell penalty of Section 5.6, K(d) = (d²/σ²)·exp(−d²/σ²), drawn with the sign it carries in H. "
            "It is zero at the anchor, where the prediction is confirmed, deepest at d = σ, where it reaches "
            "−1/e ≈ −0.368, and returns toward zero far away, where no prediction fires. The horizontal axis "
            "is the distance from the anchor in units of the moat radius σ.",
            "## Where the Manifold Leads")
    c = _canvas(720, 400, "The shell penalty is zero at the anchor and deepest at d = σ")
    ax = Axes(c, 90, 56, 560, 266, (0, 4), (-0.42, 0.12), [0, 1, 2, 3, 4], [-0.4, -0.3, -0.2, -0.1, 0],
              "distance from the anchor, d / σ", "penalty term, −K(d)")
    c.polyline([(ax.X(d), ax.Y(-k)) for d, k in zip(ds, ks)], SERIES[0], 2.5, title="−K(d)")
    c.dot(ax.X(1), ax.Y(-math.exp(-1)), CRITICAL, 5.5, title="−1/e at d = σ")
    c.text(ax.X(1) + 14, ax.Y(-math.exp(-1)) + 4, "−1/e ≈ −0.368 at d = σ", 11.5, "start", INK)
    yz = ax.Y(0.07)
    c.text(ax.X(0.02), yz, "anchor: prediction confirmed", 11, "start", INK2, italic=True)
    c.text(ax.X(1.6), yz, "near shell: the moat", 11, "middle", INK2, italic=True)
    c.text(ax.X(3.3), yz, "open country: no prediction", 11, "middle", INK2, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 6
LAM, EPS, THETA = 1.3, 0.3, 20.0


def _t_salt(f):
    return (LAM * f[0], f[1])


def _t_acid(f):
    return _rot(THETA, (f[0], f[1] + EPS))


def fig_6_1():
    p = reg(CH[6], "6.1",
            "The four seasoning operators of Sections 6.1 to 6.4 as the chapter posits them, with illustrative "
            "values. Salt stretches the savory component by λ = 1.3 and leaves the rest fixed. Acid adds a small "
            "step ε = 0.3 along the bright axis b̂ and rotates by θ = 20°. Fat is the low-pass kernel "
            "K(ω) = 1/(1 + (ω/ωc)²), drawn for two cutoffs; more fat lowers the cutoff. Heat is the flow "
            "df/dτ = −Γf with unequal release rates (1.0 and 0.3), which shrinks the components at different "
            "speeds and so turns the vector.",
            "## 6.5 Salt Fat Acid Heat as a Basis for the Group of Transformations")
    c = _canvas(720, 400, "Four verbs: salt stretches, acid rotates, fat filters, heat flows")
    sc = 58
    heads = [("Salt: stretch", "λ = 1.3 on the savory axis"), ("Acid: rotate", "ε = 0.3 along b̂, then 20°"),
             ("Fat: low-pass", "K(ω) = 1/(1 + (ω/ωc)²)"), ("Heat: flow", "df/dτ = −Γ f")]
    foots = ["direction kept, length grows", "components pulled apart", "fast volatiles damped",
             "unequal rates turn it"]
    for k in range(4):
        px = 12 + 177 * k
        c.text(px + 82, 64, heads[k][0], 12.5, "middle", INK, "600")
        c.text(px + 82, 81, heads[k][1], 10.5, "middle", INK2)
        c.text(px + 82, 352, foots[k], 10.5, "middle", INK2, italic=True)
        ox, oy = px + 18, 305
        P = lambda q: (ox + sc * q[0], oy - sc * q[1])  # noqa: E731,B023
        if k != 2:
            c.line(ox, oy, px + 160, oy, BORDER, 1)
            c.line(ox, oy, ox, 112, BORDER, 1)
        if k == 0:
            f = (1.6, 1.4)
            g = _t_salt(f)
            c.line(*P(f), *P(g), INK3, 1.2, dash="3 3")
            c.arrow(*P((0, 0)), *P(f), SERIES[0], 2.2)
            c.arrow(*P((0, 0)), *P(g), SERIES[1], 2.2)
            c.text(px + 160, oy + 15, "savory", 10.5, "end", INK2)
            c.text(ox + 6, 116, "other", 10.5, "start", INK2)
            c.text(P(f)[0] - 8, P(f)[1] - 6, "f", 11.5, "end", INK)
            c.text(P(g)[0] + 6, P(g)[1] - 6, "T f", 11.5, "start", INK)
        elif k == 1:
            f = (2.0, 0.4)
            mid = (2.0, 0.4 + EPS)
            g = _t_acid(f)
            c.line(*P(f), *P(mid), INK3, 1.2, dash="3 3")
            rr = _norm(mid)
            a0 = math.degrees(math.atan2(mid[1], mid[0]))
            _path(c, [P((rr * math.cos(math.radians(a0 + t)), rr * math.sin(math.radians(a0 + t))))
                      for t in [THETA * i / 20 for i in range(21)]], INK3, 1.2, dash="3 3")
            c.arrow(*P((0, 0)), *P(f), SERIES[0], 2.2)
            c.arrow(*P((0, 0)), *P(g), SERIES[1], 2.2)
            c.text(px + 160, oy + 15, "dominant", 10.5, "end", INK2)
            c.text(ox + 6, 116, "bright b̂", 10.5, "start", INK2)
            c.text(P(f)[0] + 4, P(f)[1] + 16, "f", 11.5, "middle", INK)
            c.text(P(g)[0] - 6, P(g)[1] - 6, "T f", 11.5, "end", INK)
        elif k == 2:
            m = _Map(ox, 150, 140, 155, (0, 4), (0, 1))
            c.line(ox, oy, px + 160, oy, BORDER, 1)
            c.line(ox, oy, ox, 140, BORDER, 1)
            for j, wc in enumerate((1.5, 0.6)):
                pts = [m.P((w, 1 / (1 + (w / wc) ** 2))) for w in [4 * i / 80 for i in range(81)]]
                c.polyline(pts, SERIES[j], 2, title=f"cutoff {wc}")
            c.line(px + 30, 106, px + 48, 106, SERIES[0], 2)
            c.text(px + 54, 110, "less fat, ωc = 1.5", 10.5, "start", INK2)
            c.line(px + 30, 122, px + 48, 122, SERIES[1], 2)
            c.text(px + 54, 126, "more fat, ωc = 0.6", 10.5, "start", INK2)
            c.text(ox - 5, 154, "K", 10.5, "end", INK2)
            c.text(ox, oy + 15, "slow: taste", 10.5, "start", INK2)
            c.text(px + 160, oy + 15, "fast: volatiles", 10.5, "end", INK2)
        else:
            f0 = (2.2, 1.6)
            traj = [(f0[0] * math.exp(-1.0 * t), f0[1] * math.exp(-0.3 * t)) for t in [4 * i / 60 for i in range(61)]]
            _path(c, [P(q) for q in traj], INK3, 1.2, dash="3 3")
            ft = (f0[0] * math.exp(-1.0), f0[1] * math.exp(-0.3))
            c.arrow(*P((0, 0)), *P(f0), SERIES[0], 2.2)
            c.arrow(*P((0, 0)), *P(ft), SERIES[1], 2.2)
            c.text(px + 160, oy + 15, "fast-releasing", 10.5, "end", INK2)
            c.text(ox + 6, 116, "slow-releasing", 10.5, "start", INK2)
            c.text(P(f0)[0] - 4, P(f0)[1] - 8, "τ = 0", 11, "middle", INK)
            c.text(P(ft)[0] - 9, P(ft)[1] + 3, "τ = 1", 11, "end", INK)
    legend(c, 18, 388, [("before", SERIES[0]), ("after the operator", SERIES[1])])
    c.save(p)


def fig_6_2():
    f0 = (2.0, 0.4)
    sa = _t_acid(_t_salt(f0))
    as_ = _t_salt(_t_acid(f0))
    gap = math.dist(sa, as_)
    assert abs(sa[0] - 2.204) < 1e-3 and abs(sa[1] - 1.547) < 1e-3
    assert abs(as_[0] - 2.132) < 1e-3 and abs(as_[1] - 1.342) < 1e-3 and gap > 0.2
    p = reg(CH[6], "6.2",
            "Salt and acid do not commute (Section 6.5). The same starting dish f0 = (2.0, 0.4) is seasoned in "
            f"both orders with the operators of Figure 6.1 (λ = {LAM}, ε = {EPS}, θ = {THETA:.0f}°). Salt then "
            f"acid lands at ({sa[0]:.2f}, {sa[1]:.2f}); acid then salt lands at ({as_[0]:.2f}, {as_[1]:.2f}). "
            f"The gap of {gap:.2f} between the two endpoints is the commutator acting on f0. The values are "
            "illustrative.",
            "## 6.6 The Seasoning Fixed Point")
    c = _canvas(720, 400, "Salt then acid is not acid then salt")
    ax = Axes(c, 70, 64, 360, 288, (0, 3), (0, 2.4), [0, 1, 2, 3], [0, 0.6, 1.2, 1.8, 2.4],
              "dominant (savory) component", "bright component")
    P = lambda q: (ax.X(q[0]), ax.Y(q[1]))  # noqa: E731

    def arc(q, deg):
        r = _norm(q)
        a0 = math.degrees(math.atan2(q[1], q[0]))
        return [P((r * math.cos(math.radians(a0 + deg * i / 24)), r * math.sin(math.radians(a0 + deg * i / 24))))
                for i in range(25)]

    s1 = _t_salt(f0)
    e1 = (s1[0], s1[1] + EPS)
    _path(c, [P(f0), P(s1), P(e1)] + arc(e1, THETA), SERIES[0], 2.2)
    e2 = (f0[0], f0[1] + EPS)
    r2 = _rot(THETA, e2)
    _path(c, [P(f0), P(e2)] + arc(e2, THETA), SERIES[1], 2.2)
    c.arrow(*P(r2), *P(as_), SERIES[1], 2.2)
    c.dot(*P(f0), INK, 5, title="f0")
    c.text(P(f0)[0] - 10, P(f0)[1] + 18, "f0", 12, "end", INK)
    c.dot(*P(sa), SERIES[0], 5.5, title="salt then acid")
    c.dot(*P(as_), SERIES[1], 5.5, title="acid then salt")
    c.line(*P(sa), *P(as_), CRITICAL, 2, dash="3 3")
    c.text(P(sa)[0] + 12, P(sa)[1] - 6, "salt, then acid", 11.5, "start", INK)
    c.text(P(as_)[0] - 12, P(as_)[1] - 10, "acid, then salt", 11.5, "end", INK)
    gx, gy = (P(sa)[0] + P(as_)[0]) / 2, (P(sa)[1] + P(as_)[1]) / 2
    lx = ax.X(2.68)
    c.line(gx + 3, gy, lx - 4, gy, INK3, 1)
    c.text(lx, gy + 4, f"gap {gap:.2f}", 11.5, "start", INK)
    c.text((P(f0)[0] + P(s1)[0]) / 2, P(f0)[1] + 16, "salt", 10.5, "middle", INK2, italic=True)
    c.text(P(e2)[0] - 8, (P(f0)[1] + P(e2)[1]) / 2 + 4, "acid", 10.5, "end", INK2, italic=True)
    _lines(c, 462, 84, ["salt then acid:", f"T_acid(T_salt(f0)) = ({sa[0]:.2f}, {sa[1]:.2f})", "",
                        "acid then salt:", f"T_salt(T_acid(f0)) = ({as_[0]:.2f}, {as_[1]:.2f})"], 11.5, color=INK)
    _lines(c, 462, 194, [f"λ = {LAM}: salt stretches the savory axis", f"ε = {EPS} along b̂, then a {THETA:.0f}° turn",
                         "values illustrative"], 11, color=INK3)
    legend(c, 70, 48, [("salt, then acid", SERIES[0]), ("acid, then salt", SERIES[1])])
    c.save(p)


# ------------------------------------------------------------------ chapter 7
def fig_7_1():
    p = reg(CH[7], "7.1",
            "Caramelization as the one-dimensional trajectory of Section 7.2, schematic. A single progress "
            "coordinate s, which rises with accumulated heat and cannot run backward, carries sweetness down, "
            "caramel aroma up to a peak, and then bitterness up toward the burnt corner. The pleasant region is "
            "bounded on both sides, so the only control is where on the arc to stop. The chapter gives the order "
            "of the stages, not the shapes of the curves; the shapes are illustrative.",
            "## 7.3 Protein Denaturation as Dimensional Collapse")
    c = _canvas(720, 400, "Caramel moves along one arc, in one direction only")
    ax = Axes(c, 70, 60, 500, 250, (0, 1), (0, 1.1), [], [], "", "relative level")
    ss = [i / 200 for i in range(201)]
    sweet = [(1 - s) ** 1.3 for s in ss]
    car = [0.85 * (s / 0.45) ** 2 * math.exp(2 * (1 - s / 0.45)) for s in ss]
    bit = [1 / (1 + math.exp(-(s - 0.72) / 0.06)) for s in ss]
    x1, x2 = ax.X(0.36), ax.X(0.6)
    c.add(f'<rect x="{x1:.2f}" y="{ax.y0:.2f}" width="{x2 - x1:.2f}" height="{ax.h:.2f}" fill="{INK3}" '
          f'fill-opacity="0.10"/>')
    c.text((x1 + x2) / 2, ax.y0 + 16, "pleasant: stop here", 11, "middle", INK, italic=True)
    for j, (name, ys) in enumerate([("sweetness", sweet), ("caramel aroma", car), ("bitterness, burnt", bit)]):
        c.polyline([(ax.X(s), ax.Y(v)) for s, v in zip(ss, ys)], SERIES[j], 2.2, title=name)
        c.text(ax.X(1) + 10, ax.Y(ys[-1]) + 4, name, 11, "start", INK2)
    c.text(ax.X(0), ax.y0 + ax.h + 18, "s = 0: pure sugar", 11, "start", INK2)
    c.text(ax.X(1), ax.y0 + ax.h + 18, "s large: burnt", 11, "end", INK2)
    c.arrow(ax.X(0), 350, ax.X(1), 350, INK2, 1.5)
    c.text(ax.X(0.5), 372, "extent of reaction s: rises with accumulated heat, cannot be reversed", 11.5,
           "middle", INK2)
    c.text(704, 392, "schematic: curve shapes illustrative", 10.5, "end", INK3, italic=True)
    c.save(p)


def fig_7_2():
    p = reg(CH[7], "7.2",
            "The five geometric types of cooking map that Chapter 7 posits, sketched schematically. Maillard "
            "browning expands a few precursor dimensions into many aroma dimensions; caramelization moves along "
            "one coordinate; denaturation maps directions toward zero; fermentation follows a trajectory toward "
            "an attractor, and a small change in a control parameter can send it to a different end state; "
            "smoking, curing and aging translate the vector by a characteristic step.",
            "## From Transformation to Construction")
    c = _canvas(720, 400, "Five cooking maps: expand, traverse, collapse, flow, translate")
    heads = [("Expand", "Maillard browning", ["m precursors to n", "aroma dims, m ≪ n"]),
             ("Traverse", "caramelization", ["one coordinate s,", "one direction"]),
             ("Collapse", "denaturation", ["directions mapped", "toward zero"]),
             ("Flow", "fermentation", ["toward an attractor;", "or a bifurcation"]),
             ("Translate", "smoke, cure, age", ["f ↦ f + v_smoke,", "base vector kept"])]
    for k, (h, sub, foot) in enumerate(heads):
        x0 = 10 + 142 * k
        cx = x0 + 68
        c.add(f'<rect x="{x0:.2f}" y="46" width="136" height="330" rx="6" fill="none" stroke="{GRID}" '
              f'stroke-width="1"/>')
        c.text(cx, 70, h, 13, "middle", INK, "600")
        c.text(cx, 87, sub, 10.5, "middle", INK2)
        _lines(c, cx, 334, foot, 10.5, "middle", INK2, 15)
        if k == 0:
            left = [(cx - 46, 175 + 25 * i) for i in range(3)]
            right = [(cx + 46, 115 + 19.5 * i) for i in range(10)]
            for i, (lx, ly) in enumerate(left):
                for j in range(i * 3, i * 3 + 5):
                    rx, ry = right[j % 10]
                    c.line(lx, ly, rx, ry, INK3, 0.8, opacity=0.6)
            for lx, ly in left:
                c.dot(lx, ly, SERIES[1], 4.5)
            for rx, ry in right:
                c.dot(rx, ry, SERIES[0], 3.5)
        elif k == 1:
            pts = []
            for i in range(41):
                t = i / 40
                pts.append(((1 - t) ** 2 * (cx - 50) + 2 * t * (1 - t) * (cx - 44) + t * t * (cx + 50),
                            (1 - t) ** 2 * 288 + 2 * t * (1 - t) * 124 + t * t * 136))
            _path(c, pts, SERIES[0], 2.2)
            c.arrow(pts[-3][0], pts[-3][1], pts[-1][0], pts[-1][1], SERIES[0], 2.2)
            sx, sy = pts[22]
            c.dot(sx, sy, CRITICAL, 5)
            c.text(sx + 10, sy + 18, "stop here", 10.5, "start", INK2)
        elif k == 2:
            _ring(c, cx, 152, 38, SERIES[0], 2, fill=SERIES[0], opacity=0.1)
            c.arrow(cx, 200, cx, 244, INK2, 1.5)
            c.ellipse(cx, 268, 46, 7, 0, SERIES[1], SERIES[1], 2, 0.15)
        elif k == 3:
            axx, ayy = cx - 4, 205
            sp = []
            for i in range(241):
                th = 4 * math.pi * i / 240
                r = 56 * math.exp(-0.28 * th)
                sp.append((axx + r * math.cos(th), ayy - 0.85 * r * math.sin(th)))
            _path(c, sp, SERIES[0], 2)
            c.dot(axx, ayy, INK, 4)
            c.text(axx, ayy + 34, "attractor", 10.5, "middle", INK2)
            br = []
            for i in range(31):
                t = i / 30
                br.append(((1 - t) ** 2 * (axx + 56) + 2 * t * (1 - t) * (axx + 64) + t * t * (axx + 52),
                           (1 - t) ** 2 * ayy + 2 * t * (1 - t) * (ayy - 40) + t * t * (ayy - 92)))
            _path(c, br, SERIES[1], 1.8, dash="4 3")
            c.dot(br[-1][0], br[-1][1], SERIES[1], 4)
        else:
            o = (cx - 56, 292)
            f = (cx - 8, 216)
            fv = (cx + 26, 134)
            c.arrow(*o, *f, SERIES[0], 2.2)
            c.arrow(*f, *fv, SERIES[1], 2.2)
            c.line(*o, *fv, INK3, 1, dash="3 3")
            c.text(f[0] + 8, f[1] + 12, "f", 11.5, "start", INK)
            c.text((f[0] + fv[0]) / 2 + 10, (f[1] + fv[1]) / 2 + 4, "v_smoke", 10.5, "start", INK2)
            c.dot(*fv, INK, 4)
            c.text(fv[0] - 8, fv[1] - 8, "f + v", 11, "end", INK)
    c.save(p)


# ------------------------------------------------------------------ chapter 8
def fig_8_1():
    p = reg(CH[8], "8.1",
            "A recipe as the directed acyclic graph of Section 8.5, drawn for a braise of the kind the section "
            "describes; the graph is an illustration, not a recipe from the book. Raw ingredients are the "
            "sources, operations are internal nodes, and the dish is the single sink. Searing S and braising B "
            "lie on one path, so they cannot be swapped. The sweated vegetables and the reduced wine are separate "
            "branches with no edge between them, so they can be prepared in parallel and their order does not "
            "matter.",
            "## 8.6 Recipe Similarity as Distance")
    c = _canvas(720, 420, "A braise as a directed acyclic graph")
    H = 42
    nodes = {
        "rib": (14, 62, 126, "short rib", []), "salt": (14, 118, 126, "salt", []),
        "veg": (14, 194, 126, "mirepoix", ["onion, carrot, celery"]),
        "wine": (14, 280, 126, "red wine", []), "stock": (14, 336, 126, "stock", []),
        "season": (176, 90, 92, "season", []), "sweat": (176, 194, 92, "sweat", []),
        "reduce": (176, 308, 92, "reduce", []), "sear": (304, 90, 92, "sear", ["operator S"]),
        "combine": (432, 194, 96, "combine", ["weighted sum"]),
        "braise": (560, 194, 74, "braise", ["operator B"]), "dish": (648, 194, 64, "dish", ["sink"]),
    }
    hot = {("rib", "season"), ("season", "sear"), ("sear", "combine"), ("combine", "braise"), ("braise", "dish")}
    edges = [("rib", "season"), ("salt", "season"), ("season", "sear"), ("sear", "combine"), ("veg", "sweat"),
             ("sweat", "combine"), ("wine", "reduce"), ("stock", "reduce"), ("reduce", "combine"),
             ("combine", "braise"), ("braise", "dish")]
    for a, b in edges:
        xa, ya, wa, _, _ = nodes[a]
        xb, yb, wb, _, _ = nodes[b]
        y1, y2 = ya + H / 2, yb + H / 2
        if b in ("season", "reduce", "combine"):
            ins = [e for e in edges if e[1] == b]
            k = ins.index((a, b))
            y2 = yb + H / 2 + (k - (len(ins) - 1) / 2) * 10
        col = CRITICAL if (a, b) in hot else INK3
        c.arrow(xa + wa + 2, y1, xb - 3, y2, col, 2 if (a, b) in hot else 1.4)
    for key, (x, y, w, lab, subs) in nodes.items():
        stroke = CRITICAL if key in ("sear", "braise") else BORDER
        _mbox(c, x, y, w, H, lab, subs, stroke=stroke, tsize=12)
    c.text(77, 50, "sources", 11, "middle", INK3, italic=True)
    c.text(400, 50, "operations", 11, "middle", INK3, italic=True)
    c.text(680, 182, "sink", 11, "middle", INK3, italic=True)
    c.line(176, 398, 200, 398, CRITICAL, 2)
    c.text(206, 402, "the path on which S and B both lie: they cannot be reordered", 11, "start", INK2)
    c.save(p)


def fig_8_2():
    f0 = (0.15, 0.20)
    v = {"lime": (1.00, 0.80), "lemon": (0.95, 0.72), "vinegar": (1.15, 0.00)}
    a = 1.0
    end = {k: (f0[0] + a * q[0], f0[1] + a * q[1]) for k, q in v.items()}
    d_lemon = a * math.dist(v["lemon"], v["lime"])
    d_vin = a * math.dist(v["vinegar"], v["lime"])
    R = 0.13
    assert d_lemon < R < d_vin
    p = reg(CH[8], "8.2",
            "Substitution as a short or a long step (Sections 8.4 and 8.6), with illustrative vectors in the "
            "plane of the sour component and the citrus aroma. The vinaigrette without acid sits at f0, and lime "
            "would carry it to the target inside the tolerance region R (dashed). Lemon is nearly parallel to "
            f"lime: the difference vector has length {d_lemon:.2f} and the dressing stays inside R. Vinegar "
            "matches lime on the sour axis but carries almost no citrus aroma: the difference has length "
            f"{d_vin:.2f} in this plane alone, before its acetic note on an axis not drawn. The step is drawn "
            "with the coefficient a = 1; Section 8.6 scales it by the amount of the ingredient.",
            "## From Construction to Cuisine")
    c = _canvas(720, 400, "Lemon is a short step from lime; vinegar is a long one")
    ax = Axes(c, 80, 50, 400, 300, (0, 1.6), (0, 1.2), [0, 0.4, 0.8, 1.2, 1.6], [0, 0.4, 0.8, 1.2],
              "sour component", "citrus aroma")
    P = lambda q: (ax.X(q[0]), ax.Y(q[1]))  # noqa: E731
    _ring(c, *P(end["lime"]), R * ax.w / 1.6, INK2, 1.5, dash="5 4")
    for j, k in enumerate(["lime", "lemon", "vinegar"]):
        c.arrow(*P(f0), *P(end[k]), SERIES[j], 2.2)
    c.line(*P(end["lime"]), *P(end["vinegar"]), CRITICAL, 2, dash="4 3")
    c.dot(*P(f0), INK, 5, title="f0: oil, mustard, honey")
    c.text(P(f0)[0] + 10, P(f0)[1] + 18, "f0: oil, mustard, honey", 11, "start", INK)
    c.text(P(end["lime"])[0] - 10, P(end["lime"])[1] - 34, "lime", 11.5, "end", INK)
    c.text(P(end["lemon"])[0] + 26, P(end["lemon"])[1] + 22, "lemon, inside R", 11.5, "start", INK)
    c.text(P(end["vinegar"])[0] + 8, P(end["vinegar"])[1] + 18, "vinegar", 11.5, "start", INK)
    xm, ym = (P(end["lime"])[0] + P(end["vinegar"])[0]) / 2, (P(end["lime"])[1] + P(end["vinegar"])[1]) / 2
    c.text(xm + 10, ym, f"difference {d_vin:.2f}", 11.5, "start", INK)
    c.text(P(end["lime"])[0] + 36, P(end["lime"])[1] - 26, "R", 11.5, "start", INK2, italic=True)
    _lines(c, 498, 84, ["Δf_dish ≈ a (f′ − f)", ""], 12, color=INK)
    _lines(c, 498, 118, [f"lemon − lime: {d_lemon:.2f}, inside R", f"vinegar − lime: {d_vin:.2f} in this plane",
                         "plus an acetic note on an", "axis the dressing never wanted", "(not drawn)"], 11.5)
    _lines(c, 498, 228, ["drawn with a = 1; acid is the", "dominant term, so a is large"], 11, color=INK3)
    c.save(p)


# ------------------------------------------------------------------ chapter 9
def fig_9_1():
    muA, SA = (1.4, 2.6), [[0.30, 0.10], [0.10, 0.45]]
    muB, SB = (5.0, 0.7), [[0.25, 0.0], [0.0, 0.012]]
    rA = _sqrtm(SA)
    rAi = _inv2(rA)
    T = _mm(rAi, _mm(_sqrtm(_mm(rA, _mm(SB, rA))), rAi))
    T = [[T[0][0], 0.5 * (T[0][1] + T[1][0])], [0.5 * (T[0][1] + T[1][0]), T[1][1]]]

    def at(t):
        Mt = [[(1 - t) + t * T[0][0], t * T[0][1]], [t * T[1][0], (1 - t) + t * T[1][1]]]
        return ((1 - t) * muA[0] + t * muB[0], (1 - t) * muA[1] + t * muB[1]), _mm(Mt, _mm(SA, Mt))

    S1 = at(1.0)[1]
    assert all(abs(S1[i][j] - SB[i][j]) < 1e-9 for i in range(2) for j in range(2))
    for t in (0.25, 0.5, 0.75):
        S = at(t)[1]
        l1, l2, _ = _sym2(S[0][0], S[0][1], S[1][1])
        assert l2 > 0
    sd = {t: math.sqrt(at(t)[1][1][1]) for t in (0.0, 0.5, 1.0)}
    p = reg(CH[9], "9.1",
            "Fusion as interpolation between two cuisine distributions (Section 9.4), drawn for two illustrative "
            "Gaussians: a mole-like cuisine A with a wide spread in fat and char, and a dashi-like cuisine B with "
            "almost none. The filled ellipses are the Wasserstein geodesic at t = 0.25, 0.5 and 0.75: a single "
            "coherent cloud whose mean moves on a straight line while its covariance changes shape, here losing "
            f"its fat-and-char spread (standard deviation {sd[0.0]:.2f} at A, {sd[0.5]:.2f} halfway, {sd[1.0]:.2f} "
            "at B). The mixture ½pA + ½pB is instead the two end clouds side by side, with almost no mass at the "
            "midpoint where the geodesic places its whole cloud. One-standard-deviation contours.",
            "## 9.5 Cultural Evolution as Gradient Descent")
    c = _canvas(720, 400, "The geodesic morphs one cloud; the mixture keeps two")
    ax = Axes(c, 70, 66, 448, 273, (0, 6.4), (0, 3.9), [], [], "shared axis (umami, acid)", "fat and char")
    m = _Map(ax.x0, ax.y0, ax.w, ax.h, (0, 6.4), (0, 3.9))
    _path(c, [m.P(muA), m.P(muB)], INK3, 1.2, dash="2 4")
    for t in (0.25, 0.5, 0.75):
        mu, S = at(t)
        _ell(c, *m.P(mu), S, m, 1.0, stroke=SERIES[0], fill=SERIES[0], width=1.8, opacity=0.18,
             title=f"geodesic, t = {t}")
        c.dot(*m.P(mu), SERIES[0], 3.5)
    _ell(c, *m.P(muA), SA, m, 1.0, stroke=SERIES[1], fill=SERIES[1], width=2, opacity=0.06, title="cuisine A")
    _ell(c, *m.P(muB), SB, m, 1.0, stroke=SERIES[2], fill=SERIES[2], width=2, opacity=0.06, title="cuisine B")
    c.dot(*m.P(muA), SERIES[1], 4.5)
    c.dot(*m.P(muB), SERIES[2], 4.5)
    c.text(m.X(muA[0]), m.Y(muA[1]) - 58, "A: mole-like", 11.5, "middle", INK)
    c.text(m.X(muB[0]), m.Y(muB[1]) + 26, "B: dashi-like", 11.5, "middle", INK)
    mid = at(0.5)[0]
    c.text(m.X(mid[0]) + 4, m.Y(mid[1]) - 40, "t = 0.5", 11, "middle", INK2)
    c.text(m.X(at(0.25)[0][0]) - 2, m.Y(at(0.25)[0][1]) - 46, "t = 0.25", 11, "middle", INK2)
    c.text(m.X(at(0.75)[0][0]) + 10, m.Y(at(0.75)[0][1]) - 30, "t = 0.75", 11, "middle", INK2)
    _lines(c, 540, 84, ["geodesic: one cloud", "at every t", "", "mixture ½ pA + ½ pB:",
                        "the two end clouds side", "by side, little mass at", "the midpoint"], 11.5)
    _lines(c, 540, 218, ["fat-and-char spread", f"t = 0: {sd[0.0]:.2f}", f"t = 0.5: {sd[0.5]:.2f}",
                         f"t = 1: {sd[1.0]:.2f}"], 11.5, color=INK)
    legend(c, 70, 48, [("geodesic", SERIES[0]), ("cuisine A", SERIES[1]), ("cuisine B", SERIES[2])])
    c.text(704, 392, "illustrative Gaussians; one-standard-deviation contours", 10.5, "end", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 10
def fig_10_1():
    sweet = {"honey": (1.5, 1.2), "fig": (2.4, 2.2), "pear": (1.2, 3.0)}
    blue = {"Stilton": (5.4, 2.2), "Gorgonzola": (6.1, 3.3), "Roquefort": (5.0, 4.0)}
    pairs = [("honey", "Stilton"), ("fig", "Gorgonzola"), ("pear", "Roquefort")]
    disp = [(blue[b][0] - sweet[s][0], blue[b][1] - sweet[s][1]) for s, b in pairs]
    r = (sum(d[0] for d in disp) / 3, sum(d[1] for d in disp) / 3)
    assert abs(r[0] - 3.8) < 1e-9 and abs(r[1] - 3.1 / 3) < 1e-9
    peach = (1.9, 3.9)
    land = (peach[0] + r[0], peach[1] + r[1])
    others = dict(sweet, **blue)
    near = min(others, key=lambda k: math.dist(others[k], land))
    assert near == "Roquefort"
    p = reg(CH[10], "10.1",
            "The analogy arithmetic of Section 10.3 as the chapter's closing box writes it, in a schematic "
            "two-dimensional picture of an embedding. The displacement from each sweet partner to its blue "
            "cheese (honey to Stilton, fig to Gorgonzola, pear to Roquefort) is nearly the same vector, and "
            "their average is the role vector r. Added to peach, which sits near fig and pear, r lands among "
            "the blue cheeses; its nearest neighbor here is Roquefort. The positions are illustrative, not taken from a trained embedding; the "
            "embeddings of the chapter have about 100 to 300 dimensions.",
            "## 10.4 Flavor Compression: PCA-Matryoshka on Flavor Profiles")
    c = _canvas(720, 400, "One role vector, transported from fig and pear to peach")
    m = _Map(40, 50, 440, 308, (0, 10), (0, 7))
    _rectline(c, m.x0, m.y0, m.w, m.h, GRID, 1)
    c.text(m.X(5.75), m.Y(1.55), "blue cheeses", 11.5, "middle", INK2, italic=True)
    for (s, b), d in zip(pairs, disp):
        c.arrow(*m.P(sweet[s]), *m.P(blue[b]), SERIES[0], 1.6)
    c.arrow(*m.P(peach), *m.P(land), SERIES[1], 2.8)
    for nm, q in sweet.items():
        c.dot(*m.P(q), SERIES[4], 4.5, title=nm)
    for nm, q in blue.items():
        c.dot(*m.P(q), SERIES[2], 4.5, title=nm)
    off = {"honey": (-8, 4, "end"), "fig": (0, 20, "middle"), "pear": (-8, 4, "end"),
           "Stilton": (10, 4, "start"), "Gorgonzola": (10, 4, "start"), "Roquefort": (0, 20, "middle")}
    for nm, q in list(sweet.items()) + list(blue.items()):
        dx, dy, an = off[nm]
        c.text(m.X(q[0]) + dx, m.Y(q[1]) + dy, nm, 11, an, INK2)
    c.dot(*m.P(peach), SERIES[1], 5.5, title="peach")
    c.text(m.X(peach[0]) - 8, m.Y(peach[1]) + 4, "peach", 11.5, "end", INK)
    c.dot(*m.P(land), INK, 5, title="peach + r")
    c.text(m.X(land[0]) + 10, m.Y(land[1]) - 6, "peach + r", 11.5, "start", INK)
    _lines(c, 500, 80, ["r = (1/N) Σ (v_blue − v_sweet)", "over N = 3 sweet-and-blue pairings",
                        f"r = ({r[0]:.2f}, {r[1]:.2f}) in this picture"], 11.5, color=INK)
    _lines(c, 500, 150, ["peach + r lands among the", "blue cheeses: a relation", "transported, not a recipe recalled"],
           11.5)
    _lines(c, 500, 226, ["schematic, positions illustrative;", "real embeddings: d ≈ 100 to 300"], 11, color=INK3)
    legend(c, 40, 384, [("displacements", SERIES[0]), ("role vector r, from peach", SERIES[1])])
    c.save(p)


# ------------------------------------------------------------------ chapter 11
def fig_11_1():
    cons = [((8, 2), 16, ">="), ((1, 6), 12, ">="), ((3, 2), 24, "<=")]
    cost = (1.0, 1.6)

    def feasible(x, y):
        if x < -1e-9 or y < -1e-9:
            return False
        for (a, b), rhs, s in cons:
            v = a * x + b * y
            if (s == ">=" and v < rhs - 1e-9) or (s == "<=" and v > rhs + 1e-9):
                return False
        return True

    lines = [((a, b), rhs) for (a, b), rhs, _ in cons] + [((1, 0), 0), ((0, 1), 0)]
    verts = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            (a1, b1), r1 = lines[i]
            (a2, b2), r2 = lines[j]
            det = a1 * b2 - a2 * b1
            if abs(det) < 1e-12:
                continue
            x, y = (r1 * b2 - r2 * b1) / det, (a1 * r2 - a2 * r1) / det
            if feasible(x, y):
                verts.append((x, y))
    vc = sorted({(round(x, 6), round(y, 6)) for x, y in verts}, key=lambda q: cost[0] * q[0] + cost[1] * q[1])
    costs = [cost[0] * x + cost[1] * y for x, y in vc]
    best = vc[0]
    grid = min(cost[0] * (9 * i / 300) + cost[1] * (13 * j / 300)
               for i in range(301) for j in range(301) if feasible(9 * i / 300, 13 * j / 300))
    assert grid >= costs[0] - 1e-9 and len(vc) == 4
    assert abs(costs[0] - 4.348) < 1e-3
    p = reg(CH[11], "11.1",
            "Why a single scalar objective picks a corner (Section 11.1), in an illustrative two-food version "
            "of Stigler's diet problem. The shaded polygon is the set of diets that meet two nutrient floors and "
            "stay under an energy ceiling; it is convex, as the chapter's feasible set is. Cost is linear, so "
            f"its minimum lies at a vertex, here the one where both floors bind exactly, at a cost of "
            f"{costs[0]:.2f}; the other vertices cost " + ", ".join(f"{v:.2f}" for v in costs[1:]) +
            ". No linear cost, other than a constant one, has its minimum in the interior, where the balanced "
            "diets lie.",
            "## 11.2 The Palatability–Nutrition Tradeoff")
    c = _canvas(720, 400, "A single linear objective picks a corner of the polytope")
    ax = Axes(c, 70, 64, 400, 282, (0, 9), (0, 13), [0, 3, 6, 9], [0, 4, 8, 12],
              "amount of food 1", "amount of food 2")
    P = lambda q: (ax.X(q[0]), ax.Y(q[1]))  # noqa: E731
    order = sorted(vc, key=lambda q: math.atan2(q[1] - 5.5, q[0] - 2.3))
    _poly(c, [P(q) for q in order], SERIES[0], 0.18, SERIES[0], 1.5)
    seg = {"protein floor": ((0, 8), (2, 0)), "vitamin floor": ((0, 2), (9, 0.5)),
           "energy ceiling": ((0, 12), (8, 0))}
    for j, (nm, (a, b)) in enumerate(seg.items()):
        c.line(*P(a), *P(b), SERIES[2 + j], 1.4, dash="4 3")
    k0 = costs[0]
    c.line(*P((0, k0 / cost[1])), *P((k0 / cost[0], 0)), SERIES[1], 1.8, dash="6 4")
    for q in vc[1:]:
        _hollow(c, *P(q), INK2, 4.5)
    c.dot(*P(best), CRITICAL, 6, title=f"optimum, cost {costs[0]:.2f}")
    c.text(P(best)[0] + 12, P(best)[1] - 8, f"cheapest diet: cost {costs[0]:.2f}", 11.5, "start", INK)
    c.text(P((2.0, 7.4))[0], P((2.0, 7.4))[1], "interior:", 11.5, "middle", INK, italic=True)
    c.text(P((2.0, 7.4))[0], P((2.0, 7.4))[1] + 16, "balanced diets", 11.5, "middle", INK, italic=True)
    rows = ["protein floor: 8 x1 + 2 x2 ≥ 16", "vitamin floor: x1 + 6 x2 ≥ 12", "energy ceiling: 3 x1 + 2 x2 ≤ 24"]
    for j, row in enumerate(rows):
        c.line(486, 72 + 17 * j, 504, 72 + 17 * j, SERIES[2 + j], 1.6, dash="4 3")
        c.text(510, 76 + 17 * j, row, 11, "start", INK)
    c.line(486, 123, 504, 123, SERIES[1], 1.6, dash="6 4")
    c.text(510, 127, "cost: 1.0 x1 + 1.6 x2", 11, "start", INK)
    _lines(c, 492, 160, ["cost at the four vertices:", ", ".join(f"{v:.2f}" for v in costs),
                         "", "the minimum sits where both", "floors bind: Stigler's corner"], 11.5)
    _lines(c, 492, 262, ["illustrative numbers"], 11, color=INK3)
    legend(c, 70, 48, [("feasible diets", SERIES[0]), ("cost level through the optimum", SERIES[1])])
    c.save(p)


def fig_11_2():
    p = reg(CH[11], "11.2",
            "The palatability and nutrition plane of Section 11.2, schematic. The inner curve stands for the "
            "Pareto frontier of the industrial food supply as the chapter describes it, with junk food at its "
            "high-palatability end and Soylent at its high-nutrition end. Section 11.5 posits that cooking with "
            "the seasoning operators pushes the frontier outward, so that the geometric diet set, nutritious and "
            "near the hedonic manifold, lies beyond the industrial frontier. The shapes are illustrative; no "
            "data are plotted.",
            "## 11.6 Personalized Nutrition as Personal Flavor Space")
    c = _canvas(720, 400, "Craft pushes the palatability and nutrition frontier outward")
    ax = Axes(c, 80, 66, 420, 260, (0, 1), (0, 1.05), [], [], "nutritional quality Q", "palatability P")
    c.line(ax.x0, ax.y0, ax.x0, ax.y0 + ax.h, GRID, 1)

    def bez(p0, p1, p2, n=60):
        return [((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1[0] + t * t * p2[0],
                 (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]

    ind = bez((0.10, 0.90), (0.55, 0.62), (0.92, 0.18))
    cra = bez((0.12, 0.98), (0.88, 0.98), (0.95, 0.30))
    c.polyline([(ax.X(x), ax.Y(y)) for x, y in ind], SERIES[0], 2.2, title="industrial frontier")
    c.polyline([(ax.X(x), ax.Y(y)) for x, y in cra], SERIES[1], 2.2, title="frontier with craft")
    c.dot(ax.X(0.10), ax.Y(0.90), SERIES[0], 5)
    c.text(ax.X(0.10) + 4, ax.Y(0.90) + 26, "junk food", 11, "middle", INK)
    c.text(ax.X(0.10) + 4, ax.Y(0.90) + 41, "high P, low Q", 11, "middle", INK2)
    c.dot(ax.X(0.92), ax.Y(0.18), SERIES[0], 5)
    c.text(ax.X(0.92) - 10, ax.Y(0.18) + 4, "Soylent: high Q, low P", 11, "end", INK)
    gx, gy = 0.72, 0.84
    c.ellipse(ax.X(gx), ax.Y(gy), 30, 16, -20, CRITICAL, CRITICAL, 1.8, 0.15, title="geometric diet set")
    c.text(ax.X(gx) + 36, ax.Y(gy) - 18, "geometric diet set", 11.5, "start", INK)
    a0 = ind[30]
    a1 = cra[30]
    c.arrow(ax.X(a0[0]), ax.Y(a0[1]), ax.X(a1[0]) - 4, ax.Y(a1[1]) + 6, INK2, 1.5)
    c.text((ax.X(a0[0]) + ax.X(a1[0])) / 2 + 8, (ax.Y(a0[1]) + ax.Y(a1[1])) / 2 + 10, "craft", 11, "start", INK2,
           italic=True)
    legend(c, 80, 48, [("industrial frontier", SERIES[0]), ("with craft, Section 11.5", SERIES[1])])
    _lines(c, 524, 120, ["up and right is better", "on both axes", "", "scalar optimization of P",
                         "alone or Q alone lands at", "one end of the frontier"], 11.5)
    c.text(704, 392, "schematic: no data plotted", 10.5, "end", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 12
def fig_12_1():
    p = reg(CH[12], "12.1",
            "The aroma stream through the stages Section 12.2 names, with the counts it gives: about 10,000 "
            "compounds, about 400 receptor types, a few thousand glomeruli in the olfactory bulb, odor objects "
            "in piriform cortex, and the orbitofrontal cortex, where the binding map Φ lands in a flavor space "
            "of 10 to 30 dimensions. Taste, texture, temperature and vision enter at the orbitofrontal cortex "
            "as side channels. The figure restates the structure of the text; it is not a measurement.",
            "## 12.3 Cross-Modal Correspondences")
    c = _canvas(720, 400, "Many streams into one low-dimensional space")
    boxes = [("chemistry", ["about 10,000", "compounds"]), ("epithelium", ["about 400", "receptor types"]),
             ("olfactory bulb", ["a few thousand", "glomeruli"]), ("piriform", ["cortex:", "odor objects"]),
             ("orbitofrontal", ["cortex: the", "binding map Φ"]), ("flavor space", ["F, 10 to 30", "dimensions"])]
    w, h, y = 104, 74, 92
    xs = [12 + (w + 12) * i for i in range(6)]
    for i, (t, subs) in enumerate(boxes):
        _mbox(c, xs[i], y, w, h, t, subs, stroke=CRITICAL if i == 4 else BORDER, tsize=12)
        if i:
            c.arrow(xs[i - 1] + w + 1, y + h / 2, xs[i] - 2, y + h / 2, INK2, 1.5)
    c.text(12, 78, "aroma stream", 11, "start", INK3, italic=True)
    side = [("taste", "via insula"), ("texture", "somatosensory"), ("temperature", "somatosensory"),
            ("vision", "colour, shape")]
    ofc = (xs[4] + w / 2, y + h)
    sx = [190, 318, 446, 574]
    for (t, s), x in zip(side, sx):
        _mbox(c, x - 56, 262, 112, 44, t, [s], tsize=11.5)
        c.arrow(x, 260, ofc[0] + (x - 446) * 0.12, ofc[1] + 3, INK3, 1.3)
    c.text(360, 336, "side channels join at the orbitofrontal cortex", 11.5, "middle", INK2, italic=True)
    c.text(360, 356, "a point in F records no tag of which sense supplied which coordinate", 11.5, "middle",
           INK2, italic=True)
    c.save(p)


def fig_12_2():
    fw, fd = (2.2, 2.9), (4.6, 3.1)
    p = reg(CH[12], "12.2",
            "Attention as projection (Section 12.5) and why it cannot undo the dye (Section 12.4), with "
            "illustrative coordinates. The red dye drags the integrated point of the white wine from f_white "
            "toward the red-wine region. Attending to aroma applies the projection P_S onto the aroma axis, which "
            f"reads the coordinate of the moved point, {fd[0]:.1f}, not that of the honest one, {fw[0]:.1f}. The "
            "projection acts after integration and has no access to the input that moved the point.",
            "## 12.6 Memory and Flavor: The Madeleine as Associative Retrieval")
    c = _canvas(720, 400, "Attention projects the moved point; it cannot unmove it")
    ax = Axes(c, 70, 52, 440, 275, (0, 8), (0, 5), [], [], "aroma coordinate, the attended subspace S",
              "other coordinates")
    c.line(ax.x0, ax.y0, ax.x0, ax.y0 + ax.h, GRID, 1)
    m = _Map(ax.x0, ax.y0, ax.w, ax.h, (0, 8), (0, 5))
    c.ellipse(m.X(1.9), m.Y(2.6), 1.05 * m.sx, 1.55 * m.sy, 0, SERIES[2], SERIES[2], 1.5, 0.06)
    c.ellipse(m.X(6.8), m.Y(2.6), 1.1 * m.sx, 1.55 * m.sy, 0, SERIES[1], SERIES[1], 1.5, 0.06)
    c.text(m.X(1.9), m.Y(4.15) - 8, "white-wine region", 11.5, "middle", INK2)
    c.text(m.X(6.8), m.Y(4.15) - 8, "red-wine region", 11.5, "middle", INK2)
    for q, col in ((fw, SERIES[2]), (fd, CRITICAL)):
        c.line(m.X(q[0]), m.Y(q[1]), m.X(q[0]), m.Y(0), col, 1.5, dash="4 3")
        c.dot(m.X(q[0]), m.Y(0), col, 4.5)
    c.arrow(m.X(fw[0]) + 8, m.Y(fw[1]) - 1, m.X(fd[0]) - 9, m.Y(fd[1]) + 1, INK2, 1.8)
    c.dot(*m.P(fw), SERIES[2], 5.5, title="honest white wine")
    c.dot(*m.P(fd), CRITICAL, 5.5, title="integrated point with the red dye")
    c.text(m.X(fw[0]) - 10, m.Y(fw[1]) + 4, "f_white", 11.5, "end", INK)
    c.text(m.X(fd[0]) + 10, m.Y(fd[1]) + 4, "f_dyed", 11.5, "start", INK)
    c.text(m.X(3.8), m.Y(fd[1]) + 22, "red dye (vision)", 10.5, "middle", INK2, italic=True)
    c.text(m.X(fw[0]) + 8, m.Y(0.35), f"P_S f = {fw[0]:.1f}", 11, "start", INK2)
    c.text(m.X(fd[0]) + 8, m.Y(0.35), f"P_S f = {fd[0]:.1f}", 11, "start", INK2)
    _lines(c, 530, 92, ["attention projects after", "binding: it reads the moved", f"coordinate {fd[0]:.1f}",
                        "", f"the honest {fw[0]:.1f} is not", "recoverable from the point"], 11.5)
    _lines(c, 530, 222, ["coordinates illustrative"], 11, color=INK3)
    c.save(p)


# ------------------------------------------------------------------ chapter 13
def fig_13_1():
    f = (0.4, 1.6)
    removed = (0.4, 0.0)
    antag = (0.4, 0.3 * 1.6)
    over = (0.4 + 2.6, 1.6)
    share = lambda q: q[1] / _norm(q)  # noqa: E731
    assert abs(share(f) - 0.970) < 1e-3 and abs(share(over) - 0.470) < 1e-3 and over[1] == f[1]
    p = reg(CH[13], "13.1",
            "Three ways to mask a bitter drug (Section 13.2), with illustrative values. Removal at the source "
            "projects out the bitter coordinate, from 1.6 to 0. Receptor antagonism rescales it toward zero, "
            f"here to {antag[1]:.2f}. Additive overshadowing adds a large component on another axis: the bitter "
            f"coordinate stays at 1.6, although its share of the vector's length falls from {share(f):.2f} to "
            f"{share(over):.2f}, which is why the chapter says the bitterness leaks back.",
            "## 13.3 Plant-Based Meat as Flavor Mimicry")
    c = _canvas(720, 400, "Projection removes the bitter axis; overshadowing only dilutes it")
    ax = Axes(c, 80, 66, 396, 252, (0, 3.6), (0, 2.0), [0, 1, 2, 3], [0, 0.5, 1, 1.5, 2],
              "other flavor (sweet, fruit)", "bitter coordinate")
    P = lambda q: (ax.X(q[0]), ax.Y(q[1]))  # noqa: E731
    for q in (removed, antag, over):
        c.line(*P(f), *P(q), INK3, 1.2, dash="3 3")
    c.arrow(*P((0, 0)), *P(f), SERIES[0], 2.4)
    c.arrow(*P((0, 0)), *P(antag), SERIES[2], 2.4)
    c.arrow(*P((0, 0)), *P(over), SERIES[3], 2.4)
    c.dot(*P(removed), SERIES[1], 5.5, title="removed at the source")
    c.text(P(f)[0] + 10, P(f)[1] - 6, "drug: bitter 1.6", 11.5, "start", INK)
    c.text(P(removed)[0] + 12, P(removed)[1] - 8, "removed: bitter 0", 11.5, "start", INK)
    c.text(ax.X(0.62), ax.Y(0.22), f"antagonist: bitter {antag[1]:.2f}", 11.5, "start", INK)
    c.text(P(over)[0] - 8, P(over)[1] - 12, "overshadowed: bitter 1.6", 11.5, "end", INK)
    legend(c, 80, 48, [("drug", SERIES[0]), ("removal", SERIES[1]), ("antagonism", SERIES[2]),
                       ("overshadowing", SERIES[3])])
    _lines(c, 500, 92, ["bitter share of the length:", f"drug alone {share(f):.2f}",
                        f"overshadowed {share(over):.2f}", "", "the bitter coordinate itself", "is unchanged at 1.6"],
           11.5, color=INK)
    _lines(c, 500, 210, ["values illustrative"], 11, color=INK3)
    c.save(p)


def fig_13_2():
    b = [(3.0, 0.5), (2.0, 2.0), (0.6, 3.0)]
    Mx, My = 1.0, 4.0
    fstar = (2.9, 2.55)
    poly = [(0.0, 0.0), b[0], b[1], b[2]]

    def nearest(wx, wy):
        best = None
        for a, e in zip(poly, poly[1:] + poly[:1]):
            dx, dy = e[0] - a[0], e[1] - a[1]
            t = ((fstar[0] - a[0]) * dx * wx + (fstar[1] - a[1]) * dy * wy) / (dx * dx * wx + dy * dy * wy)
            t = min(1.0, max(0.0, t))
            q = (a[0] + t * dx, a[1] + t * dy)
            d2 = (q[0] - fstar[0]) ** 2 * wx + (q[1] - fstar[1]) ** 2 * wy
            if best is None or d2 < best[0]:
                best = (d2, q, t, a, e)
        return best

    d2, qM, tM, aM, eM = nearest(Mx, My)
    dM = math.sqrt(d2)
    _, qE, _, _, _ = nearest(1.0, 1.0)
    assert aM == b[1] and eM == b[2] and 0 < tM < 1
    assert abs(dM - 1.368) < 1e-3
    xa = (0.0, 0.75, 0.0)
    cz = (7.5 / 17.4)
    xb = (3 - 6 * cz, 0.0, cz)
    fa = (sum(x * q[0] for x, q in zip(xa, b)), sum(x * q[1] for x, q in zip(xa, b)))
    fb = (sum(x * q[0] for x, q in zip(xb, b)), sum(x * q[1] for x, q in zip(xb, b)))
    assert math.dist(fa, (1.5, 1.5)) < 1e-12 and math.dist(fb, (1.5, 1.5)) < 1e-9 and sum(xb) <= 1
    p = reg(CH[13], "13.2",
            "The inverse flavor problem of Section 13.4 in two dimensions, with illustrative values. Three "
            "palette vectors b1, b2 and b3, a unit cost each and a budget of 1 make the reachable set the shaded "
            "polygon. For a target f* outside it, the solution is the point of the polygon nearest f* in the "
            "metric M = diag(1, 4), where the metric ellipse around f* first touches the polygon. The residual, "
            f"{dM:.2f}, is the artificiality gap, and the active constraints are the budget and the zero dose of "
            "b1. The Euclidean nearest point, marked for contrast, lies elsewhere. For the target inside the "
            "polygon the distance is 0, and two different dose vectors, (0, 0.75, 0) and "
            f"({xb[0]:.2f}, 0, {xb[2]:.2f}), reach the same flavor point: with three palette vectors in two "
            "dimensions the flavor point Bx is unique and the dose vector is not, as the theorem of the section states.",
            "## 13.5 Personalized Flavor")
    c = _canvas(720, 430, "The nearest reachable flavor point in a stretched metric")
    ax = Axes(c, 70, 50, 360, 324, (0, 4), (0, 3.6), [0, 1, 2, 3, 4], [0, 1, 2, 3],
              "flavor coordinate 1", "flavor coordinate 2")
    P = lambda q: (ax.X(q[0]), ax.Y(q[1]))  # noqa: E731
    _poly(c, [P(q) for q in poly], SERIES[0], 0.16, SERIES[0], 1.5)
    for i, q in enumerate(b):
        c.arrow(*P((0, 0)), *P(q), INK3, 1.2)
        c.dot(*P(q), SERIES[0], 4)
    c.text(P(b[0])[0] + 8, P(b[0])[1] + 16, "b1", 11.5, "start", INK2)
    c.text(P((1.0, 1.0))[0] - 8, P((1.0, 1.0))[1] - 6, "b2", 11.5, "end", INK2)
    c.text(P(b[2])[0] - 8, P(b[2])[1] - 6, "b3", 11.5, "end", INK2)
    c.ellipse(*P(fstar), dM * ax.w / 4 / math.sqrt(Mx), dM * ax.h / 3.6 / math.sqrt(My), 0, SERIES[1], "none",
              1.5, title="metric ellipse through the solution")
    c.line(*P(fstar), *P(qM), SERIES[1], 1.5, dash="4 3")
    c.dot(*P(fstar), CRITICAL, 5.5, title="target f*")
    c.text(P(fstar)[0] + 10, P(fstar)[1] - 8, "target f*", 11.5, "start", INK)
    c.dot(*P(qM), SERIES[1], 5.5, title="nearest in the metric M")
    c.text(P(qM)[0] - 12, P(qM)[1] + 4, "nearest in M", 11.5, "end", INK)
    _hollow(c, *P(qE), INK2, 4.5)
    lab = P((2.55, 1.55))
    c.line(P(qE)[0] + 4, P(qE)[1] + 4, lab[0] - 2, lab[1] - 10, INK3, 1)
    c.text(lab[0], lab[1], "Euclidean nearest", 11, "start", INK2)
    fi = (1.5, 1.5)
    c.dot(*P(fi), SERIES[2], 5.5, title="target inside")
    c.text(P(fi)[0] - 10, P(fi)[1] + 4, "target inside", 11.5, "end", INK)
    _lines(c, 470, 74, ["palette b1, b2, b3; cost 1 each;", "budget 1", "",
                        f"outside target: residual {dM:.2f}", "in the metric M = diag(1, 4);",
                        "active: the budget and x1 = 0"], 11.5, color=INK)
    _lines(c, 470, 196, ["inside target (1.5, 1.5): distance 0", "doses (0, 0.75, 0) and",
                         f"({xb[0]:.2f}, 0, {xb[2]:.2f}) give the same", "flavor point Bx"], 11.5)
    _lines(c, 470, 276, ["values illustrative"], 11, color=INK3)
    c.save(p)


# ------------------------------------------------------------------ chapter 14
def fig_14_1():
    us = [10 * i / 400 for i in range(401)]

    def H0(u):
        return 0.35 + 0.65 * math.exp(-(u - 3) ** 2 / (2 * 1.3 ** 2)) + 0.55 * math.exp(-(u - 7.5) ** 2 / 2)

    R, at = 0.55, 3.0

    def Ht(u, w):
        return H0(u) - R * math.exp(-(u - at) ** 2 / (2 * w * w))

    dn = H0(7.5) - Ht(7.5, 0.9)
    db = H0(7.5) - Ht(7.5, 3.5)
    assert dn < 1e-3 and db > 0.2
    p = reg(CH[14], "14.1",
            "Sensory-specific satiety as the deforming hedonic field of Section 14.3, "
            "H_t(f) = H_0(f) − ∫ρ(s) K(f, f(s)) ds, along one flavor coordinate. A savory course is eaten at "
            "the marked point, with a total intake of 0.55. With a narrow kernel the meal digs a well around the "
            "savory region and leaves the dessert region untouched (a drop of less than 0.001 there); with a broad "
            f"kernel everything dims together (a drop of {db:.2f} at the dessert). The field H_0, the intake and "
            "the Gaussian kernels of width 0.9 and 3.5 are illustrative; the chapter posits the formula and "
            "conjectures that K is the heat kernel of the flavor metric.",
            "## 14.4 The Social Geometry of Eating")
    c = _canvas(720, 400, "Satiety digs a well where you ate and spares the dessert")
    ax = Axes(c, 70, 70, 520, 252, (0, 10), (0, 1.3), [], [0, 0.4, 0.8, 1.2], "one direction of flavor space",
              "pleasantness H")
    xs = ax.X(at)
    c.line(xs, ax.y0 + 14, xs, ax.y0 + ax.h, INK3, 1.2, dash="3 4")
    c.text(xs, ax.y0 + 8, "savory course eaten here", 11, "middle", INK2, italic=True)
    c.text(ax.X(7.5), ax.Y(H0(7.5)) - 14, "dessert", 11.5, "middle", INK)
    series = [("before the meal", H0, INK3), ("narrow kernel", lambda u: Ht(u, 0.9), SERIES[0]),
              ("broad kernel", lambda u: Ht(u, 3.5), SERIES[1])]
    for name, fn, col in series:
        pts = [(ax.X(u), ax.Y(fn(u))) for u in us]
        if name == "before the meal":
            _path(c, pts, col, 1.8, dash="5 4")
        else:
            c.polyline(pts, col, 2.2, title=name)
    dz = ax.X(7.5)
    _lines(c, 604, 120, ["at the dessert:", f"before {H0(7.5):.2f}", f"narrow kernel {Ht(7.5, 0.9):.2f}",
                         f"broad kernel {Ht(7.5, 3.5):.2f}"], 11, color=INK2, lh=16)
    assert dz < 604
    legend(c, 70, 48, [("before the meal", INK3), ("after, narrow kernel", SERIES[0]),
                       ("after, broad kernel", SERIES[1])])
    c.text(704, 392, "illustrative field and kernels", 10.5, "end", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ appendix A
def fig_A_1():
    g = [[1.0, 0.6], [0.6, 1.0]]
    q = lambda v: g[0][0] * v[0] ** 2 + 2 * g[0][1] * v[0] * v[1] + g[1][1] * v[1] ** 2  # noqa: E731
    assert abs(q((1, 1)) - 3.2) < 1e-12 and abs(q((1, -1)) - 0.8) < 1e-12
    assert round(math.sqrt(3.2), 2) == 1.79
    p = reg(CH["A"], "A.1",
            "The worked micro-example of Section A.1. The metric g = [[1, 0.6], [0.6, 1]] on a salt and umami "
            "patch makes the set of displacements of unit length an ellipse, drawn against the Euclidean unit "
            "circle. The displacement (1, 1), along the joint salt-and-umami direction, has perceptual length "
            "√3.2 ≈ 1.79 under g, against √2 ≈ 1.41 under the Euclidean metric, and reaches outside the "
            "ellipse; the displacement (1, −1) has length √0.8 ≈ 0.89 and stays inside it.",
            "## A.2 Convex Optimization, Simplex Geometry, and Pareto Frontiers")
    c = _canvas(720, 400, "One displacement, two lengths: the metric of the worked example")
    cx, cy, sc = 240, 216, 80
    m = _Map(cx - 2 * sc, cy - 2 * sc, 4 * sc, 4 * sc, (-2, 2), (-2, 2))
    c.line(cx - 175, cy, cx + 175, cy, BORDER, 1)
    c.line(cx, cy - 165, cx, cy + 165, BORDER, 1)
    c.text(cx + 175, cy + 16, "salt", 11.5, "end", INK2)
    c.text(cx + 6, cy - 156, "umami", 11.5, "start", INK2)
    _ring(c, cx, cy, sc, INK3, 1.5, dash="5 4")
    _ell(c, cx, cy, _inv2(g), m, 1.0, stroke=SERIES[0], fill=SERIES[0], width=2, opacity=0.1,
         title="unit length under g")
    for v, col in (((1, 1), SERIES[1]), ((1, -1), SERIES[2])):
        c.arrow(cx, cy, *m.P(v), col, 2.5)
    c.text(m.X(1) + 8, m.Y(1) - 6, "(1, 1)", 11.5, "start", INK)
    c.text(m.X(1) + 6, m.Y(-1) + 32, "(1, −1)", 11.5, "middle", INK)
    _lines(c, 450, 84, ["g = [[1, 0.6], [0.6, 1]]", "", "(1, 1): ds² = 3.2, ds = 1.79",
                        "(1, −1): ds² = 0.8, ds = 0.89", "Euclidean, both: ds = 1.41"], 12, color=INK)
    c.line(450, 206, 476, 206, SERIES[0], 2)
    c.text(484, 210, "unit length under g", 11.5, "start", INK2)
    c.line(450, 228, 476, 228, INK3, 1.5, dash="5 4")
    c.text(484, 232, "unit length, Euclidean", 11.5, "start", INK2)
    c.save(p)


def fig_A_2():
    pts = {"A": (0.9, 0.9), "B": (0.5, 0.7), "C": (0.3, 0.5), "D": (0.6, 0.4)}  # (sodium N, savoriness S)

    def dominates(a, b):
        return a[0] <= b[0] and a[1] >= b[1] and (a[0] < b[0] or a[1] > b[1])

    front = sorted(k for k in pts if not any(dominates(pts[o], pts[k]) for o in pts if o != k))
    assert front == ["A", "B", "C"] and dominates(pts["C"], pts["D"])
    p = reg(CH["A"], "A.2",
            "The worked micro-example of Section A.2: four low-sodium broth formulas plotted by sodium, where "
            "lower is better, and savoriness, where higher is better. C is both more savory and lower in sodium "
            "than D, so D is off the frontier (B dominates it too). None of A, B and C dominates another, so "
            "they form the Pareto frontier, and choosing among them means choosing a rate of trade between "
            "salt and savor. The shaded box is the region whose formulas would dominate D.",
            "## A.3 PCA and Dimensionality Reduction")
    c = _canvas(720, 400, "Three formulas on the frontier, one dominated")
    ax = Axes(c, 90, 64, 420, 262, (0.2, 1.0), (0.3, 1.0), [0.2, 0.4, 0.6, 0.8, 1.0],
              [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], "sodium N, lower is better", "savoriness S, higher is better")
    P = lambda q: (ax.X(q[0]), ax.Y(q[1]))  # noqa: E731
    x0, y0 = P((0.2, 1.0))
    x1, y1 = P(pts["D"])
    _rectline(c, x0, y0, x1 - x0, y1 - y0, INK3, 1, dash="4 3", fill=INK3, opacity=0.07)
    c.text(x0 + 8, y0 + 18, "formulas here would dominate D", 11, "start", INK2, italic=True)
    c.polyline([P(pts[k]) for k in ("C", "B", "A")], SERIES[0], 2.2, title="Pareto frontier")
    for k in front:
        c.dot(*P(pts[k]), SERIES[0], 5.5, title=k)
    _hollow(c, *P(pts["D"]), INK2, 5.5)
    lab = {"A": (12, 4, "start"), "B": (-10, -8, "end"), "C": (10, 20, "start"), "D": (12, 4, "start")}
    for k, (dx, dy, an) in lab.items():
        s = f"{k} ({pts[k][1]}, {pts[k][0]})" if k != "D" else "D, dominated"
        c.text(P(pts[k])[0] + dx, P(pts[k])[1] + dy, s, 11.5, an, INK)
    _lines(c, 566, 92, ["labels give (S, N)", "", "frontier: A, B, C", "C beats D on both", "objectives"], 11.5)
    legend(c, 90, 48, [("Pareto frontier", SERIES[0])])
    c.save(p)


def fig_A_3():
    X = [(-2.0, -1.8), (0.0, 0.1), (2.0, 1.7)]
    n = len(X)
    mx, my = sum(x for x, _ in X) / n, sum(y for _, y in X) / n
    assert abs(mx) < 1e-12 and abs(my) < 1e-12
    sxx = sum((x - mx) ** 2 for x, _ in X) / n
    sxy = sum((x - mx) * (y - my) for x, y in X) / n
    syy = sum((y - my) ** 2 for _, y in X) / n
    assert abs(sxx - 2.667) < 1e-3 and abs(sxy - 2.333) < 1e-3 and abs(syy - 2.047) < 1e-3
    assert (round(sxx, 2), round(sxy, 2), round(syy, 2)) == (2.67, 2.33, 2.05)
    l1, l2, ang = _sym2(sxx, sxy, syy)
    v1 = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    v2 = (-v1[1], v1[0])
    assert abs(v1[0] - 0.752) < 1e-3 and abs(v1[1] - 0.659) < 1e-3
    assert (round(v1[0], 2), round(v1[1], 2)) == (0.75, 0.66) and (round(v2[0], 2), round(v2[1], 2)) == (-0.66, 0.75)
    share = l1 / (l1 + l2)
    p = reg(CH["A"], "A.3",
            "The worked micro-example of Section A.3, recomputed from its three printed points: three centered "
            "foods described by sweetness and perceived ripeness. Their covariance is [[2.67, 2.33], [2.33, "
            f"2.05]]. The leading eigenvector (0.75, 0.66) carries {100 * share:.1f} % of the variance, and the "
            "orthogonal eigenvector (−0.66, 0.75) almost none. The arrow along the leading eigenvector is drawn "
            f"at one standard deviation, √λ1 = {math.sqrt(l1):.2f}; the standard deviation along the other, "
            f"{math.sqrt(l2):.2f}, is too small to draw, so only its direction is marked.",
            "## How to Read the Rest of the Book with These Tools")
    c = _canvas(720, 400, "Two measured coordinates, one principal direction")
    cx, cy, sc = 230, 216, 60
    m = _Map(cx - 3 * sc, cy - 3 * sc, 6 * sc, 6 * sc, (-3, 3), (-3, 3))
    c.line(cx - 170, cy, cx + 170, cy, BORDER, 1)
    c.line(cx, cy - 165, cx, cy + 165, BORDER, 1)
    c.text(cx + 170, cy + 16, "sweetness", 11.5, "end", INK2)
    c.text(cx + 6, cy - 156, "ripeness", 11.5, "start", INK2)
    c.line(*m.P((-2.9 * v1[0], -2.9 * v1[1])), *m.P((2.9 * v1[0], 2.9 * v1[1])), SERIES[1], 1, dash="4 4")
    s1 = math.sqrt(l1)
    c.arrow(cx, cy, *m.P((s1 * v1[0], s1 * v1[1])), SERIES[1], 2.6)
    c.arrow(cx, cy, *m.P((0.55 * v2[0], 0.55 * v2[1])), SERIES[2], 1.6)
    for i, q in enumerate(X):
        c.dot(*m.P(q), SERIES[0], 5.5, title=f"x{i + 1} = {q}")
    c.text(m.X(X[0][0]) + 10, m.Y(X[0][1]) + 16, "x1", 11.5, "start", INK)
    c.text(m.X(X[1][0]) + 12, m.Y(X[1][1]) + 16, "x2", 11.5, "start", INK)
    c.text(m.X(X[2][0]) + 10, m.Y(X[2][1]) + 16, "x3", 11.5, "start", INK)
    e1 = m.P((s1 * v1[0], s1 * v1[1]))
    c.text(e1[0] - 30, e1[1] - 4, "v1", 12, "end", INK)
    e2 = m.P((0.55 * v2[0], 0.55 * v2[1]))
    c.text(e2[0] - 6, e2[1] - 6, "v2", 12, "end", INK)
    _lines(c, 450, 84, ["Σ = [[2.67, 2.33], [2.33, 2.05]]", f"λ1 = {l1:.3f},  λ2 = {l2:.4f}",
                        "v1 = (0.75, 0.66)", "v2 = (−0.66, 0.75)", f"share of variance on v1: {100 * share:.1f} %"],
           11.5, color=INK)
    _lines(c, 450, 186, ["v1: one standard deviation;", "v2: direction only, its", f"standard deviation is {math.sqrt(l2):.2f}"],
           11, color=INK3)
    c.save(p)


# ------------------------------------------------------------------ appendix B
def fig_B_1():
    p = reg(CH["B"], "B.1",
            "The extraction pipeline of Section B.2, which turns database records into a compound vector. "
            "FlavorDB's table of ingredient-molecule associations is the backbone; FooDB concentrations and VCF "
            "volatility flags and thresholds are joined on InChIKey; the vocabulary of columns is fixed; and "
            "components are weighted by odor activity value, OAV = c / θ. Missing concentrations are kept as "
            "their own stratum and never filled with zero. The result is a chemical vector c_i, not yet the "
            "perceptual flavor vector f_i, which needs the receptor map of Chapter 2 and the metric of Chapter 3.",
            "## B.3 Worked Construction: A Compound Vector for Strawberry")
    c = _canvas(720, 420, "From database records to a compound vector, one join at a time")
    w, h, gap = 124, 56, 13
    xs = [20 + (w + gap) * i for i in range(5)]
    dbs = [("FlavorDB", ["presence only"]), ("FooDB", ["concentrations,", "uneven"]),
           ("VCF", ["volatiles, thresholds;", "licensed"])]
    steps = [("1. backbone", ["FlavorDB", "contains table"]), ("2. quantify", ["left join", "on InChIKey"]),
             ("3. enrich", ["join on InChIKey", "or CAS"]), ("4. vocabulary", ["fix the", "column set"]),
             ("5. weight", ["OAV = c / θ"])]
    for i, (t, s) in enumerate(dbs):
        _mbox(c, xs[i], 52, w, 52, t, s, tsize=12)
        c.arrow(xs[i] + w / 2, 106, xs[i] + w / 2, 140, INK3, 1.4)
    for i, (t, s) in enumerate(steps):
        _mbox(c, xs[i], 144, w, h + 8, t, s, tsize=12)
        if i:
            c.arrow(xs[i - 1] + w + 1, 144 + (h + 8) / 2, xs[i] - 2, 144 + (h + 8) / 2, INK2, 1.5)
    bx, bw = 486, 214
    _mbox(c, bx, 250, bw, 52, "compound vector c_i", ["chemistry, about 10⁴ columns"], stroke=SERIES[0])
    c.arrow(xs[4] + w / 2, 210, xs[4] + w / 2, 247, INK2, 1.5)
    _mbox(c, bx, 350, bw, 52, "flavor vector f_i", ["needs Chapters 2 and 3"], stroke=INK3)
    xm = bx + bw / 2
    c.add(f'<line x1="{xm}" y1="304" x2="{xm}" y2="346" stroke="{INK3}" stroke-width="1.5" '
          f'stroke-dasharray="5 4"/>')
    c.line(xm, 347, xm - 5, 339, INK3, 1.5)
    c.line(xm, 347, xm + 5, 339, INK3, 1.5)
    c.text(xm + 10, 330, "not yet", 10.5, "start", INK2, italic=True)
    c.text(20, 262, "three strata, kept apart:", 11.5, "start", INK)
    for i, (lab, col) in enumerate([("absent", INK3), ("present, unquantified", SERIES[1]),
                                    ("quantified", SERIES[0])]):
        y = 280 + 22 * i
        c.add(f'<rect x="28" y="{y}" width="14" height="14" rx="3" fill="{col}"/>')
        c.text(50, y + 12, lab, 11.5, "start", INK2)
    _lines(c, 20, 368, ["a null in the contains table means not measured,", "so it is never filled with zero"],
           11.5, color=INK2)
    c.save(p)


# ------------------------------------------------------------------ appendix C
def fig_C_1():
    p = reg(CH["C"], "C.1",
            "The three instruments of Appendix C placed along the encoding chain from chemistry to perception, "
            "with the sizes the appendix gives. GC-MS reads the chemical vector c, about 10² to 10³ compounds "
            "for one complex food, and is blind to salience. Electronic noses and tongues read a short response "
            "vector r of 6 to 32 channels and are reliable only inside their calibration region. A trained panel "
            "of 8 to 15 assessors reads the perceptual estimate f̂ on 10 to 40 attributes. The panel calibrates "
            "the sensors, and GC-olfactometry splices a human nose onto the chemical encoder.",
            "## C.4 Reading the Three Together")
    c = _canvas(720, 420, "Three instruments at three points of the encoding chain")
    w = 150
    xs = [16, 196, 376, 556]
    top = [("food sample", []), ("chemistry", ["vector c"]), ("receptor stage", ["vector r"]),
           ("perception", ["flavor vector f"])]
    for i, (t, s) in enumerate(top):
        _mbox(c, xs[i], 56, w, 50, t, s, tsize=12)
        if i:
            c.arrow(xs[i - 1] + w + 1, 81, xs[i] - 2, 81, INK2, 1.5)
    inst = [("GC-MS", ["N ≈ 10² to 10³", "compounds per food"]), ("e-nose, e-tongue", ["m = 6 to 32 channels",
                                                                                        "about 16 typical"]),
            ("sensory panel", ["p = 10 to 40 attributes", "8 to 15 assessors"])]
    notes = [["identity and quantity;", "blind to salience"], ["reliable only inside", "its calibration region"],
             ["ground truth;", "slow, costly, noisy"]]
    for i, ((t, s), nt) in enumerate(zip(inst, notes)):
        x = xs[i + 1]
        _mbox(c, x, 156, w, 64, t, s, stroke=SERIES[i], tsize=12)
        c.arrow(x + w / 2, 154, x + w / 2, 109, SERIES[i], 1.6)
        c.text(x + w / 2 + 6, 136, "reads", 10.5, "start", INK3, italic=True)
        _lines(c, x + w / 2, 244, nt, 11, "middle", INK2, 15)
    # the panel calibrates the sensors
    xa, xb = xs[2] + w - 6, xs[3] + 10
    _path(c, [(xb, 222), (xb, 300), (xa, 300)], SERIES[2], 1.5, dash="5 4")
    c.arrow(xa, 300, xa, 224, SERIES[2], 1.5)
    c.text((xa + xb) / 2, 318, "the panel calibrates the sensors", 11, "middle", INK2, italic=True)
    # GC-olfactometry splices a human nose onto the chemical encoder
    xg, xp = xs[1] + 8, xs[3] + w - 6
    _path(c, [(xg, 222), (xg, 346), (xp, 346)], SERIES[0], 1.5, dash="5 4")
    c.arrow(xp, 346, xp, 224, SERIES[0], 1.5)
    c.text((xg + xp) / 2, 364, "GC-olfactometry: a human nose at the column outlet", 11, "middle", INK2,
           italic=True)
    c.save(p)
