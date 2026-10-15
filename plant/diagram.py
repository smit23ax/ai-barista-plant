"""Process flow diagram (P&ID style) of the coffee plant as an SVG string.

Styling follows the idea of a high-performance operator display (ISA-101): equipment is drawn in muted
grey, and bright colour is used only for live values and alarms. Text sizes are chosen to stay readable
when the 1100-unit-wide drawing is shown at laptop width (about 0.9x) or in a 700 px scroll box on a phone.
"""

GREY, LINE, TEXT, SUB, VALUE = "#4b5768", "#b7c3d2", "#18202b", "#3d4756", "#137a3c"
ALARM, WARN, WATER, COFFEE = "#c93434", "#a65c00", "#2f6fd6", "#9a5b2e"
FILL, BOX, HILITE = "#f4f7fb", "#ffffff", "#2f6fd6"
R = 22  # instrument bubble radius


def _tag(x, y, tag, value, color=VALUE):
    """Instrument bubble (circle with tag) and a live value box to its right."""
    kind, num = tag.split("-")
    return (f'<circle cx="{x}" cy="{y}" r="{R}" fill="{BOX}" stroke="{GREY}" stroke-width="1.8"/>'
            f'<line x1="{x - R}" y1="{y}" x2="{x + R}" y2="{y}" stroke="{GREY}" stroke-width="1.2"/>'
            f'<text x="{x}" y="{y - 5}" class="tg">{kind}</text><text x="{x}" y="{y + 15}" class="tg">{num}</text>'
            f'<rect x="{x + R + 4}" y="{y - 16}" width="118" height="32" rx="6" fill="{BOX}" stroke="{GREY}" stroke-width="1.2"/>'
            f'<text x="{x + R + 63}" y="{y + 6}" class="val" fill="{color}">{value}</text>')


def _pipe(points, color, running, width=6):
    """Process line through the given points; dashes move along it while the batch is running."""
    d = "M " + " L ".join(f"{x} {y}" for x, y in points)
    anim = '<animate attributeName="stroke-dashoffset" from="28" to="0" dur="0.8s" repeatCount="indefinite"/>' if running else ""
    return (f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="{width + 4}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="{"16 12" if running else "none"}" '
            f'stroke-linejoin="round" opacity="{1 if running else 0.8}">{anim}</path>')


def _label(x, y, name, sub, anchor="middle"):
    return (f'<text x="{x}" y="{y}" class="eq" text-anchor="{anchor}">{name}</text>'
            f'<text x="{x}" y="{y + 19}" class="sub" text-anchor="{anchor}">{sub}</text>')


# Bounding boxes (x, y, width, height) used to highlight one unit in presenter mode.
UNIT_BOXES = {"E-101": (70, 170, 160, 245), "SR-101": (150, 50, 210, 108),
              "R-101": (540, 40, 180, 435), "F-101": (750, 445, 130, 128), "T-101": (965, 465, 120, 145)}


def plant_svg(v, running=False, highlight=None):
    """v: dict of live values (already formatted strings) and alarm flags. Keys used:
    T_kettle, grind, T_brew, TDS, EY, plunge_F, plug_alarm, settle_t, in_box. highlight: a unit tag from UNIT_BOXES to outline, or None."""
    tds_color = VALUE if v.get("in_box") else WARN
    filt_color = ALARM if v.get("plug_alarm") else GREY
    s = [f'<svg viewBox="0 0 1100 620" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Process flow diagram of the coffee plant" style="width:100%;height:auto;background:#ffffff;border-radius:8px">',
         f'<style>.eq{{font:700 18px ui-monospace,Menlo,Consolas,monospace;fill:{TEXT}}}'
         f'.sub{{font:500 14px ui-monospace,Menlo,Consolas,monospace;fill:{SUB}}}'
         f'.tg{{font:700 12px ui-monospace,Menlo,Consolas,monospace;fill:{TEXT};text-anchor:middle}}'
         f'.val{{font:700 17px ui-monospace,Menlo,Consolas,monospace;text-anchor:middle}}'
         f'.hdr{{font:700 15px ui-monospace,Menlo,Consolas,monospace;fill:{SUB};letter-spacing:2px}}</style>',
         f'<text x="24" y="34" class="hdr">AREA 100 · COFFEE PLANT · PROCESS FLOW DIAGRAM</text>',
         f'<text x="1076" y="34" class="hdr" text-anchor="end" style="fill:{VALUE if running else SUB}">'
         f'{"● BATCH RUNNING" if running else "○ IDLE"}</text>']

    # Process lines
    s.append(_pipe([(150, 400), (150, 500), (450, 500), (450, 180), (560, 180)], WATER, running))      # kettle -> press
    s.append(_pipe([(316, 128), (520, 128), (520, 160), (560, 160)], COFFEE, running, 4))                # grinder -> press
    s.append(_pipe([(630, 460), (630, 530), (780, 530)], COFFEE, running))                              # press -> filter
    s.append(_pipe([(850, 530), (915, 530), (915, 445), (1015, 445), (1015, 478)], COFFEE, running))    # filter -> cup
    s.append(_pipe([(815, 560), (815, 592), (720, 592)], GREY, running, 4))                             # spent grounds
    s.append(f'<text x="708" y="597" class="sub" text-anchor="end">spent grounds</text>')

    # E-101 kettle with heating coil
    s.append(f'<rect x="90" y="240" width="120" height="160" rx="16" fill="{FILL}" stroke="{GREY}" stroke-width="2.2"/>'
             f'<rect x="92" y="285" width="116" height="113" fill="{WATER}" opacity="0.2"/>'
             f'<path d="M108 368 q11 -16 22 0 t22 0 t22 0 t22 0" fill="none" stroke="{ALARM if running else GREY}" stroke-width="2.4"/>')
    s.append(_label(150, 200, "E-101", "KETTLE / HEATER"))
    s.append(_tag(262, 300, "TI-101", v["T_kettle"]))

    # SR-101 grinder (hopper + crushing rolls)
    s.append(f'<path d="M250 68 L340 68 L318 106 L272 106 Z" fill="{FILL}" stroke="{GREY}" stroke-width="2.2"/>'
             f'<circle cx="284" cy="120" r="10" fill="{BOX}" stroke="{GREY}" stroke-width="2.2"/>'
             f'<circle cx="306" cy="120" r="10" fill="{BOX}" stroke="{GREY}" stroke-width="2.2"/>')
    s.append(_label(236, 90, "SR-101", "GRINDER", anchor="end"))
    s.append(_tag(290, 186, "XI-102", v["grind"]))

    # R-101 French press with plunger
    s.append(f'<rect x="560" y="140" width="140" height="320" rx="8" fill="{FILL}" stroke="{GREY}" stroke-width="2.2"/>'
             f'<rect x="562" y="205" width="136" height="253" fill="{COFFEE}" opacity="0.3"/>'
             f'<line x1="630" y1="104" x2="630" y2="370" stroke="{GREY}" stroke-width="3.5"/>'
             f'<line x1="595" y1="370" x2="665" y2="370" stroke="{GREY}" stroke-width="5"/>')
    s.append(_label(630, 66, "R-101", "BATCH EXTRACTOR"))
    s.append(_tag(752, 190, "TI-102", v["T_brew"]))
    s.append(_tag(752, 250, "AT-101", v["TDS"], tds_color))
    s.append(_tag(752, 310, "AT-102", v["EY"], tds_color))

    # F-101 plunger filter (filter symbol: box with diagonal mesh)
    s.append(f'<rect x="780" y="500" width="70" height="60" fill="{FILL}" stroke="{filt_color}" stroke-width="2.8"/>'
             f'<line x1="780" y1="560" x2="850" y2="500" stroke="{filt_color}" stroke-width="1.8" stroke-dasharray="5 4"/>')
    s.append(_label(815, 470, "F-101", "PLUNGE FILTER"))
    s.append(_tag(752, 400, "WI-101", v["plunge_F"], ALARM if v.get("plug_alarm") else VALUE))

    # T-101 cup
    s.append(f'<path d="M987 480 L1043 480 L1037 545 L993 545 Z" fill="{FILL}" stroke="{GREY}" stroke-width="2.2"/>'
             f'<path d="M1043 496 q22 0 22 16 q0 16 -24 16" fill="none" stroke="{GREY}" stroke-width="2.2"/>')
    s.append(_label(1015, 572, "T-101", "CUP"))
    s.append(_tag(940, 392, "KI-102", v["settle_t"]))
    if highlight in UNIT_BOXES:
        x, y, w, h = UNIT_BOXES[highlight]
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="none" stroke="{HILITE}" '
                 f'stroke-width="3" stroke-dasharray="9 6"><animate attributeName="opacity" values="1;0.35;1" '
                 f'dur="1.6s" repeatCount="indefinite"/></rect>')
    s.append("</svg>")
    return "".join(s)
