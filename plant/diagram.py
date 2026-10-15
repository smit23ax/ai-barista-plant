"""Process flow diagram (P&ID style) of the coffee plant as an SVG string.

Styling follows the idea of a high-performance operator display (ISA-101): equipment is drawn in muted
grey, and bright colour is used only for live values and alarms.
"""

GREY, LINE, TEXT, VALUE = "#64748b", "#c3cedb", "#18202b", "#1f8a4c"
ALARM, WARN, WATER, COFFEE = "#d64545", "#c27a00", "#2f6fd6", "#9a5b2e"
FILL, BOX, HILITE = "#f4f7fb", "#ffffff", "#2f6fd6"


def _tag(x, y, tag, value, color=VALUE):
    """Instrument bubble (circle with tag) and a live value box next to it."""
    kind, num = tag.split("-")
    return (f'<circle cx="{x}" cy="{y}" r="17" fill="{FILL}" stroke="{GREY}" stroke-width="1.5"/>'
            f'<line x1="{x - 17}" y1="{y}" x2="{x + 17}" y2="{y}" stroke="{GREY}" stroke-width="1"/>'
            f'<text x="{x}" y="{y - 4}" class="tg">{kind}</text><text x="{x}" y="{y + 11}" class="tg">{num}</text>'
            f'<rect x="{x + 21}" y="{y - 10}" width="86" height="20" rx="3" fill="{BOX}" stroke="{LINE}"/>'
            f'<text x="{x + 64}" y="{y + 4}" class="val" fill="{color}">{value}</text>')


def _pipe(points, color, running, width=4):
    """Process line through the given points; dashes move along it while the batch is running."""
    d = "M " + " L ".join(f"{x} {y}" for x, y in points)
    anim = '<animate attributeName="stroke-dashoffset" from="24" to="0" dur="0.8s" repeatCount="indefinite"/>' if running else ""
    return (f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="{width + 3}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="12 12" '
            f'stroke-linejoin="round" opacity="{0.95 if running else 0.35}">{anim}</path>')


def _label(x, y, name, sub):
    return f'<text x="{x}" y="{y}" class="eq">{name}</text><text x="{x}" y="{y + 15}" class="sub">{sub}</text>'


# Bounding boxes (x, y, width, height) used to highlight one unit in presenter mode.
UNIT_BOXES = {"E-101": (60, 150, 160, 200), "SR-101": (180, 45, 150, 90),
              "R-101": (485, 45, 160, 390), "F-101": (690, 395, 80, 110), "T-101": (880, 380, 105, 135)}


def plant_svg(v, running=False, highlight=None):
    """v: dict of live values (already formatted strings) and alarm flags. Keys used:
    T_kettle, grind, T_brew, TDS, EY, plunge_F, plug_alarm, settle_t, in_box. highlight: a unit tag from UNIT_BOXES to outline, or None."""
    tds_color = VALUE if v.get("in_box") else WARN
    filt_color = ALARM if v.get("plug_alarm") else GREY
    s = [f'<svg viewBox="0 0 1040 540" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Process flow diagram of the coffee plant" style="width:100%;height:auto;background:#ffffff;border-radius:8px">',
         f'<style>.eq{{font:600 13px ui-monospace,Menlo,monospace;fill:{TEXT};text-anchor:middle}}'
         f'.sub{{font:11px ui-monospace,Menlo,monospace;fill:{GREY};text-anchor:middle}}'
         f'.tg{{font:600 9px ui-monospace,Menlo,monospace;fill:{TEXT};text-anchor:middle}}'
         f'.val{{font:600 11px ui-monospace,Menlo,monospace;text-anchor:middle}}'
         f'.hdr{{font:600 12px ui-monospace,Menlo,monospace;fill:{GREY};letter-spacing:2px}}</style>',
         f'<text x="20" y="28" class="hdr">AREA 100 · COFFEE PLANT · PROCESS FLOW DIAGRAM</text>',
         f'<text x="1020" y="28" class="hdr" text-anchor="end" fill="{VALUE if running else GREY}">'
         f'{"● BATCH RUNNING" if running else "○ IDLE"}</text>']

    # Process lines
    s.append(_pipe([(150, 330), (150, 420), (390, 420), (390, 150), (500, 150)], WATER, running))  # kettle -> press
    s.append(_pipe([(310, 110), (470, 110), (470, 135), (520, 135)], COFFEE, running, 3))  # grinder -> press
    s.append(_pipe([(560, 420), (560, 470), (700, 470)], COFFEE, running))              # press -> filter
    s.append(_pipe([(760, 470), (830, 470), (830, 360), (930, 360), (930, 420)], COFFEE, running))  # filter -> cup
    s.append(_pipe([(730, 500), (730, 520), (640, 520)], GREY, running, 3))             # spent grounds

    # E-101 kettle with heating coil
    s.append(f'<rect x="100" y="190" width="100" height="140" rx="14" fill="{FILL}" stroke="{GREY}" stroke-width="2"/>'
             f'<path d="M115 300 q10 -14 20 0 t20 0 t20 0 t20 0" fill="none" stroke="{ALARM if running else GREY}" stroke-width="2"/>'
             f'<rect x="102" y="230" width="96" height="98" fill="{WATER}" opacity="0.18"/>')
    s.append(_label(150, 172, "E-101", "KETTLE / HEATER"))
    s.append(_tag(70, 250, "TI-101", v["T_kettle"]))

    # SR-101 grinder (hopper + crushing rolls)
    s.append(f'<path d="M240 60 L320 60 L300 95 L260 95 Z" fill="{FILL}" stroke="{GREY}" stroke-width="2"/>'
             f'<circle cx="270" cy="108" r="9" fill="none" stroke="{GREY}" stroke-width="2"/>'
             f'<circle cx="290" cy="108" r="9" fill="none" stroke="{GREY}" stroke-width="2"/>')
    s.append(_label(195, 70, "SR-101", "GRINDER"))
    s.append(_tag(200, 120, "XI-102", v["grind"]))

    # R-101 French press with plunger
    s.append(f'<rect x="500" y="130" width="120" height="290" rx="6" fill="{FILL}" stroke="{GREY}" stroke-width="2"/>'
             f'<rect x="502" y="190" width="116" height="228" fill="{COFFEE}" opacity="0.30"/>'
             f'<line x1="560" y1="80" x2="560" y2="330" stroke="{GREY}" stroke-width="3"/>'
             f'<line x1="530" y1="330" x2="590" y2="330" stroke="{GREY}" stroke-width="4"/>')
    s.append(_label(560, 62, "R-101", "BATCH EXTRACTOR (PRESS)"))
    s.append(_tag(655, 170, "TI-102", v["T_brew"]))
    s.append(_tag(655, 220, "AT-101", v["TDS"], tds_color))
    s.append(_tag(655, 270, "AT-102", v["EY"], tds_color))

    # F-101 plunger filter (filter symbol: box with diagonal mesh)
    s.append(f'<rect x="700" y="445" width="60" height="50" fill="{FILL}" stroke="{filt_color}" stroke-width="2.5"/>'
             f'<line x1="700" y1="495" x2="760" y2="445" stroke="{filt_color}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    s.append(_label(730, 412, "F-101", "PLUNGE FILTER"))
    s.append(_tag(650, 380, "WI-101", v["plunge_F"], ALARM if v.get("plug_alarm") else VALUE))
    s.append(f'<text x="600" y="535" class="sub">spent grounds</text>')

    # T-101 cup
    s.append(f'<path d="M905 420 L955 420 L950 480 L910 480 Z" fill="{FILL}" stroke="{GREY}" stroke-width="2"/>'
             f'<path d="M955 435 q20 0 20 15 q0 15 -22 15" fill="none" stroke="{GREY}" stroke-width="2"/>')
    s.append(_label(930, 500, "T-101", "CUP"))
    s.append(_tag(895, 395, "KI-102", v["settle_t"]))
    if highlight in UNIT_BOXES:
        x, y, w, h = UNIT_BOXES[highlight]
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" stroke="{HILITE}" '
                 f'stroke-width="2.5" stroke-dasharray="8 5"><animate attributeName="opacity" values="1;0.35;1" '
                 f'dur="1.6s" repeatCount="indefinite"/></rect>')
    s.append("</svg>")
    return "".join(s)
