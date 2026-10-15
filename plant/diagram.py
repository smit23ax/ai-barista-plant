"""Process flow diagram (P&ID style) of the coffee plant as an SVG string.

Styling follows the idea of a high-performance operator display (ISA-101): equipment is drawn in muted
grey, and bright colour is used only for live values and alarms.
"""

GREY, LINE, TEXT, VALUE = "#8b95a1", "#5d6773", "#c9d1d9", "#7ee787"
ALARM, WARN, WATER, COFFEE = "#ff5f56", "#f2b84b", "#58a6ff", "#c08a5b"


def _tag(x, y, tag, value, color=VALUE):
    """Instrument bubble (circle with tag) and a live value box next to it."""
    kind, num = tag.split("-")
    return (f'<circle cx="{x}" cy="{y}" r="17" fill="#161b22" stroke="{GREY}" stroke-width="1.5"/>'
            f'<line x1="{x - 17}" y1="{y}" x2="{x + 17}" y2="{y}" stroke="{GREY}" stroke-width="1"/>'
            f'<text x="{x}" y="{y - 4}" class="tg">{kind}</text><text x="{x}" y="{y + 11}" class="tg">{num}</text>'
            f'<rect x="{x + 21}" y="{y - 10}" width="86" height="20" rx="3" fill="#0d1117" stroke="{LINE}"/>'
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


def plant_svg(v, running=False):
    """v: dict of live values (already formatted strings) and alarm flags. Keys used:
    T_kettle, Q_pump, H_pump, npsh, cav_alarm, grind, T_brew, TDS, EY, stir_Re, plunge_F, plug_alarm,
    settle_t, drain_t, in_box."""
    tds_color = VALUE if v.get("in_box") else WARN
    pump_color = ALARM if v.get("cav_alarm") else GREY
    filt_color = ALARM if v.get("plug_alarm") else GREY
    s = [f'<svg viewBox="0 0 1040 540" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Process flow diagram of the coffee plant" style="width:100%;height:auto;background:#0d1117;border-radius:8px">',
         f'<style>.eq{{font:600 13px ui-monospace,Menlo,monospace;fill:{TEXT};text-anchor:middle}}'
         f'.sub{{font:11px ui-monospace,Menlo,monospace;fill:{GREY};text-anchor:middle}}'
         f'.tg{{font:600 9px ui-monospace,Menlo,monospace;fill:{TEXT};text-anchor:middle}}'
         f'.val{{font:600 11px ui-monospace,Menlo,monospace;text-anchor:middle}}'
         f'.hdr{{font:600 12px ui-monospace,Menlo,monospace;fill:{GREY};letter-spacing:2px}}</style>',
         f'<text x="20" y="28" class="hdr">AREA 100 · COFFEE PLANT · PROCESS FLOW DIAGRAM</text>',
         f'<text x="1020" y="28" class="hdr" text-anchor="end" fill="{VALUE if running else GREY}">'
         f'{"● BATCH RUNNING" if running else "○ IDLE"}</text>']

    # Process lines
    s.append(_pipe([(150, 330), (150, 420), (255, 420)], WATER, running))              # kettle -> pump
    s.append(_pipe([(305, 420), (390, 420), (390, 150), (500, 150)], WATER, running))   # pump -> press top
    s.append(_pipe([(310, 110), (470, 110), (470, 135), (520, 135)], COFFEE, running, 3))  # grinder -> press
    s.append(_pipe([(560, 420), (560, 470), (700, 470)], COFFEE, running))              # press -> filter
    s.append(_pipe([(760, 470), (820, 470), (820, 330)], COFFEE, running))              # filter -> carafe
    s.append(_pipe([(870, 360), (930, 360), (930, 420)], COFFEE, running))              # carafe -> cup
    s.append(_pipe([(730, 500), (730, 520), (640, 520)], GREY, running, 3))             # spent grounds

    # E-101 kettle with heating coil
    s.append(f'<rect x="100" y="190" width="100" height="140" rx="14" fill="#161b22" stroke="{GREY}" stroke-width="2"/>'
             f'<path d="M115 300 q10 -14 20 0 t20 0 t20 0 t20 0" fill="none" stroke="{ALARM if running else GREY}" stroke-width="2"/>'
             f'<rect x="102" y="230" width="96" height="98" fill="{WATER}" opacity="0.18"/>')
    s.append(_label(150, 172, "E-101", "KETTLE / HEATER"))
    s.append(_tag(70, 250, "TI-101", v["T_kettle"]))

    # P-101 centrifugal pump
    s.append(f'<circle cx="280" cy="420" r="26" fill="#161b22" stroke="{pump_color}" stroke-width="2.5"/>'
             f'<path d="M268 405 L298 420 L268 435 Z" fill="none" stroke="{pump_color}" stroke-width="2"/>')
    s.append(_label(280, 468, "P-101", "PUMP + LINE"))
    s.append(_tag(250, 370, "FI-101", v["Q_pump"]))
    s.append(_tag(120, 500, "PI-101", v["H_pump"]))
    s.append(_tag(400, 500, "XI-101", v["npsh"], ALARM if v.get("cav_alarm") else VALUE))

    # SR-101 grinder (hopper + crushing rolls)
    s.append(f'<path d="M240 60 L320 60 L300 95 L260 95 Z" fill="#161b22" stroke="{GREY}" stroke-width="2"/>'
             f'<circle cx="270" cy="108" r="9" fill="none" stroke="{GREY}" stroke-width="2"/>'
             f'<circle cx="290" cy="108" r="9" fill="none" stroke="{GREY}" stroke-width="2"/>')
    s.append(_label(195, 70, "SR-101", "GRINDER"))
    s.append(_tag(200, 120, "XI-102", v["grind"]))

    # R-101 French press with agitator A-101 and plunger
    s.append(f'<rect x="500" y="130" width="120" height="290" rx="6" fill="#161b22" stroke="{GREY}" stroke-width="2"/>'
             f'<rect x="502" y="190" width="116" height="228" fill="{COFFEE}" opacity="0.30"/>'
             f'<line x1="560" y1="80" x2="560" y2="330" stroke="{GREY}" stroke-width="3"/>'
             f'<line x1="530" y1="330" x2="590" y2="330" stroke="{GREY}" stroke-width="4"/>'
             f'<path d="M545 330 l15 -10 l15 10" fill="none" stroke="{GREY}" stroke-width="2">'
             + ('<animateTransform attributeName="transform" type="rotate" from="0 560 330" to="360 560 330" dur="1.2s" repeatCount="indefinite"/>' if running else "")
             + '</path>')
    s.append(_label(560, 62, "R-101 / A-101", "BATCH EXTRACTOR + STIRRER"))
    s.append(_tag(655, 170, "TI-102", v["T_brew"]))
    s.append(_tag(655, 220, "AT-101", v["TDS"], tds_color))
    s.append(_tag(655, 270, "AT-102", v["EY"], tds_color))
    s.append(_tag(655, 320, "XI-103", v["stir_Re"]))

    # F-101 plunger filter (filter symbol: box with diagonal mesh)
    s.append(f'<rect x="700" y="445" width="60" height="50" fill="#161b22" stroke="{filt_color}" stroke-width="2.5"/>'
             f'<line x1="700" y1="495" x2="760" y2="445" stroke="{filt_color}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    s.append(_label(730, 412, "F-101", "PLUNGE FILTER"))
    s.append(_tag(650, 380, "WI-101", v["plunge_F"], ALARM if v.get("plug_alarm") else VALUE))
    s.append(f'<text x="600" y="535" class="sub">spent grounds</text>')

    # D-101 carafe and T-101 cup
    s.append(f'<path d="M800 230 L880 230 L870 360 L810 360 Z" fill="#161b22" stroke="{GREY}" stroke-width="2"/>'
             f'<path d="M806 290 L874 290 L870 358 L810 358 Z" fill="{COFFEE}" opacity="0.35"/>')
    s.append(_label(840, 212, "D-101", "CARAFE"))
    s.append(_tag(905, 300, "KI-101", v["drain_t"]))
    s.append(f'<path d="M905 420 L955 420 L950 480 L910 480 Z" fill="#161b22" stroke="{GREY}" stroke-width="2"/>'
             f'<path d="M955 435 q20 0 20 15 q0 15 -22 15" fill="none" stroke="{GREY}" stroke-width="2"/>')
    s.append(_label(930, 500, "T-101", "CUP"))
    s.append(_tag(895, 395, "KI-102", v["settle_t"]))
    s.append("</svg>")
    return "".join(s)
