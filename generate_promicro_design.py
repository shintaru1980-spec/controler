from __future__ import annotations

from pathlib import Path
import csv
import uuid


ROOT = Path(__file__).resolve().parent


# Compact host-board envelope.  The right-facing Pro Micro is flush with the
# right edge; the switch/diode field still has several millimetres of margin.
BOARD_W = 150.0
BOARD_H = 120.0


def uid() -> str:
    return str(uuid.uuid4())


def f(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def txt(text: str, x: float, y: float, layer: str = "F.SilkS", size: float = 1.0, thick: float = 0.15, justify: str = "") -> str:
    just = f" (justify {justify})" if justify else ""
    return f'\t(gr_text "{text}" (at {f(x)} {f(y)}) (layer "{layer}") (uuid {uid()}) (effects (font (size {f(size)} {f(size)}) (thickness {f(thick)})){just}))'


def segment(x1: float, y1: float, x2: float, y2: float, net: int, layer: str, width: float = 0.25) -> str:
    return f'\t(segment (start {f(x1)} {f(y1)}) (end {f(x2)} {f(y2)}) (width {f(width)}) (layer "{layer}") (net {net}) (uuid {uid()}))'


def via(x: float, y: float, net: int) -> str:
    return f'\t(via (at {f(x)} {f(y)}) (size 0.70) (drill 0.35) (layers "F.Cu" "B.Cu") (net {net}) (uuid {uid()}))'


def th_pad(num: str, x: float, y: float, net: int = 0, net_name: str = "", drill: float = 1.2, size: float = 2.2, npth: bool = False) -> str:
    kind = "np_thru_hole circle" if npth else "thru_hole circle"
    netpart = "" if npth or net == 0 else f' (net {net} "{net_name}")'
    return f'\t\t(pad "{num}" {kind} (at {f(x)} {f(y)}) (size {f(size)} {f(size)}) (drill {f(drill)}) (layers "*.Cu" "*.Mask"){netpart} (uuid {uid()}))'


def smd_pad(num: str, x: float, y: float, net: int, net_name: str) -> str:
    return f'\t\t(pad "{num}" smd roundrect (at {f(x)} {f(y)}) (size 0.63 0.83) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net {net} "{net_name}") (uuid {uid()}))'


def footprint_header(name: str, x: float, y: float, rot: float = 0) -> list[str]:
    at = f" (at {f(x)} {f(y)}" + (f" {f(rot)})" if rot else ")")
    return [f'\t(footprint "{name}" (layer "F.Cu"){at} (uuid {uid()})']


# Board design coordinates.  The six-column field is 19 mm pitch, with the
# first row containing the left-aligned three-button subset.
BUTTON_XS = [15.0, 34.0, 53.0, 72.0, 91.0, 110.0]
BUTTON_YS = [22.0, 41.0, 60.0, 79.0, 98.0]
BUTTONS: list[tuple[int, int, int, float, float]] = []
_button_number = 1
for _r, _y in enumerate(BUTTON_YS):
    if _r == 0:
        _xs = [15.0, 34.0, 53.0]
        _cols = [0, 1, 2]  # left-aligned with the six-button rows
    else:
        _xs = BUTTON_XS
        _cols = list(range(6))
    for _x, _c in zip(_xs, _cols):
        BUTTONS.append((_button_number, _r, _c, _x, _y))
        _button_number += 1


ROW_NETS = {r: r + 1 for r in range(5)}
COL_NETS = {c: 6 + c for c in range(6)}
DIODE_NETS = {n: 11 + n for n in range(1, 28)}
DIODE_DX = 10.0
DIODE_DY = 4.5


def add_dts(lines: list[str], ref: str, x: float, y: float, row_net: int, diode_net: int, button_number: int) -> None:
    lines.extend(footprint_header("DTS-24N", x, y))
    lines.append(f'\t\t(fp_text reference "{ref}" (at 0 -7.2) (layer "F.SilkS") (uuid {uid()}) (effects (font (size 0.85 0.85) (thickness 0.14))))')
    lines.append('\t\t(fp_text value "DTS-24N" (at 0 0) (layer "F.Fab") hide (uuid ' + uid() + ') (effects (font (size 1 1) (thickness 0.15))))')
    lines.append(f'\t\t(fp_rect (start -6 -6) (end 6 6) (stroke (width 0.20) (type default)) (fill none) (layer "F.Fab") (uuid {uid()}))')
    lines.append(f'\t\t(fp_circle (center 0 0) (end 3.55 0) (stroke (width 0.20) (type default)) (fill none) (layer "F.SilkS") (uuid {uid()}))')
    # DTS-24N datasheet: 1-2 are one internal contact, 3-4 are the other.
    lines.append(th_pad("1", -6.25, -2.5, row_net, f"ROW{row_net}"))
    lines.append(th_pad("2", 6.25, -2.5, row_net, f"ROW{row_net}"))
    lines.append(th_pad("3", -6.25, 2.5, diode_net, f"D{button_number:02d}_A"))
    lines.append(th_pad("4", 6.25, 2.5, diode_net, f"D{button_number:02d}_A"))
    lines.append("\t)")


def add_diode(lines: list[str], ref: str, x: float, y: float, column_net: int, diode_net: int, button_number: int) -> None:
    # SOD-323, pad 1 = cathode (K), pad 2 = anode (A).  The switch side is
    # pad 2; the column side is pad 1.  This is the normal KiCad diode pin
    # convention and is also called out in the README.
    lines.extend(footprint_header("D_SOD-323_1N4148WS", x + DIODE_DX, y + DIODE_DY))
    lines.append('\t\t(attr smd)')
    lines.append(f'\t\t(fp_text reference "{ref}" (at 0 1.65) (layer "F.SilkS") (uuid {uid()}) (effects (font (size 0.65 0.65) (thickness 0.11))))')
    lines.append('\t\t(fp_text value "1N4148WS" (at 0 0) (layer "F.Fab") hide (uuid ' + uid() + ') (effects (font (size 0.7 0.7) (thickness 0.1))))')
    lines.append(f'\t\t(fp_rect (start -1.35 -0.75) (end 1.35 0.75) (stroke (width 0.15) (type default)) (fill none) (layer "F.SilkS") (uuid {uid()}))')
    lines.append(f'\t\t(fp_line (start -0.50 -0.75) (end -0.50 0.75) (stroke (width 0.22) (type default)) (layer "F.SilkS") (uuid {uid()}))')
    lines.append(smd_pad("1", -1.15, 0, column_net, f"COL{column_net - 5}"))
    lines.append(smd_pad("2", 1.15, 0, diode_net, f"D{button_number:02d}_A"))
    lines.append("\t)")


PROMICRO_Y0 = 10.0
PROMICRO_W = 17.78
PROMICRO_H = 33.02
PROMICRO_X0 = BOARD_W - PROMICRO_H


def promicro_transform(local_x: float, local_y: float) -> tuple[float, float]:
    # The Amazon Type-C module is turned +90 degrees so the connector opening
    # faces the right edge of the host board. The connector is on the module;
    # the host PCB does not implement USB.
    return PROMICRO_X0 + local_y, PROMICRO_Y0 + PROMICRO_W - local_x


PROMICRO_PADS = [
    # The official JP7/JP6 headers are 1.27 mm from the board edges and use
    # a 2.54 mm pitch.  The nearby silk labels in the Eagle file are offset
    # from the actual pad centers, so the package/element coordinates below
    # are used for the mechanical footprint.
    ("D9", 1.27, 1.27), ("D8", 1.27, 3.81), ("D7", 1.27, 6.35),
    ("D6", 1.27, 8.89), ("D5", 1.27, 11.43), ("D4", 1.27, 13.97),
    ("D3", 1.27, 16.51), ("D2", 1.27, 19.05), ("GND_L1", 1.27, 21.59),
    ("GND_L2", 1.27, 24.13), ("RXI", 1.27, 26.67), ("TXO", 1.27, 29.21),
    ("D10", 16.51, 1.27), ("D16", 16.51, 3.81), ("D14", 16.51, 6.35),
    ("D15", 16.51, 8.89), ("A0", 16.51, 11.43), ("A1", 16.51, 13.97),
    ("A2", 16.51, 16.51), ("A3", 16.51, 19.05), ("VCC", 16.51, 21.59),
    ("RST", 16.51, 24.13), ("GND_R", 16.51, 26.67), ("RAW", 16.51, 29.21),
]


def promicro_global_pad(label: str) -> tuple[float, float]:
    for name, lx, ly in PROMICRO_PADS:
        if name == label:
            return promicro_transform(lx, ly)
    raise KeyError(label)


def add_promicro(lines: list[str]) -> None:
    # A +90-degree footprint rotates about its local origin. Use the lower
    # left anchor so the transformed 17.78 x 33.02 mm outline occupies
    # x=(BOARD_W-33.02)..BOARD_W and y=5.00..22.78 mm.
    lines.extend(footprint_header("Pro_Micro_USB-C_5V16MHz_THT", PROMICRO_X0, PROMICRO_Y0 + PROMICRO_W, 90))
    lines.append('\t\t(fp_text reference "U1" (at 8.89 16.5 180) (layer "F.SilkS") (uuid ' + uid() + ') (effects (font (size 1.0 1.0) (thickness 0.16))))')
    lines.append('\t\t(fp_text value "Pro Micro 5V/16MHz USB-C THT" (at 8.89 36.0 180) (layer "F.Fab") hide (uuid ' + uid() + ') (effects (font (size 0.9 0.9) (thickness 0.13))))')
    lines.append(f'\t\t(fp_rect (start 0 0) (end {f(PROMICRO_W)} {f(PROMICRO_H)}) (stroke (width 0.25) (type default)) (fill none) (layer "F.SilkS") (uuid {uid()}))')
    lines.append('\t\t(fp_line (start 5.8 32.9) (end 11.9 32.9) (stroke (width 0.25) (type default)) (layer "F.SilkS") (uuid ' + uid() + '))')
    lines.append('\t\t(fp_text user "USB-C" (at 8.89 32.2 180) (layer "F.SilkS") (uuid ' + uid() + ') (effects (font (size 0.8 0.8) (thickness 0.12))))')
    matrix_pad_nets = {
        "D2": (ROW_NETS[0], "ROW1"),
        "D3": (ROW_NETS[1], "ROW2"),
        "D4": (ROW_NETS[2], "ROW3"),
        "D5": (ROW_NETS[3], "ROW4"),
        "D6": (ROW_NETS[4], "ROW5"),
        "A2": (COL_NETS[0], "COL1"),
        "A1": (COL_NETS[1], "COL2"),
        "A0": (COL_NETS[2], "COL3"),
        "D15": (COL_NETS[3], "COL4"),
        "D14": (COL_NETS[4], "COL5"),
        "D16": (COL_NETS[5], "COL6"),
    }
    for name, lx, ly in PROMICRO_PADS:
        # Local pad coordinates follow the official Eagle board file.  The
        # host hole is 1.1 mm to accommodate common 0.64 mm square headers.
        net, net_name = matrix_pad_nets.get(name, (0, ""))
        lines.append(th_pad(name, lx, ly, net, net_name, drill=1.1, size=1.9))
    lines.append("\t)")


def build_pcb() -> str:
    lines: list[str] = []
    lines += [
        '(kicad_pcb (version 20240108) (generator pcbnew)',
        '\t(general (thickness 1.6))',
        '\t(paper "A4")',
        '\t(layers',
        '\t\t(0 "F.Cu" signal)',
        '\t\t(31 "B.Cu" signal)',
        '\t\t(36 "B.SilkS" user "b.silkscreen")',
        '\t\t(37 "F.SilkS" user "f.silkscreen")',
        '\t\t(38 "B.Mask" user "b.soldermask")',
        '\t\t(39 "F.Mask" user "f.soldermask")',
        '\t\t(44 "Edge.Cuts" user)',
        '\t\t(46 "B.CrtYd" user "b.courtyard")',
        '\t\t(47 "F.CrtYd" user "f.courtyard")',
        '\t\t(48 "B.Fab" user)',
        '\t\t(49 "F.Fab" user)',
        '\t)',
        '\t(setup (pad_to_mask_clearance 0))',
        '\t(net 0 "")',
    ]
    for r in range(1, 6):
        lines.append(f'\t(net {ROW_NETS[r-1]} "ROW{r}")')
    for c in range(1, 7):
        lines.append(f'\t(net {COL_NETS[c-1]} "COL{c}")')
    for n in range(1, 28):
        lines.append(f'\t(net {DIODE_NETS[n]} "D{n:02d}_A")')

    add_promicro(lines)

    # Add the switches and the one SMD diode per button.
    for number, row, col, x, y in BUTTONS:
        add_dts(lines, f"SW{number:02d}", x, y, ROW_NETS[row], DIODE_NETS[number], number)
        add_diode(lines, f"D{number:02d}", x, y, COL_NETS[col], DIODE_NETS[number], number)
        # Copper is required across both internally-common DTS contact pairs,
        # and from the external switch contact to the diode anode. The
        # datasheet confirms that pads 1-2 and 3-4 are the two common pairs.
        lines.append(segment(x - 6.25, y - 2.5, x + 6.25, y - 2.5, ROW_NETS[row], "F.Cu"))
        lines.append(segment(x, y - 2.5, x, y, ROW_NETS[row], "F.Cu"))
        lines.append(segment(x - 6.25, y + 2.5, x + 6.25, y + 2.5, DIODE_NETS[number], "F.Cu"))
        # Route around the neighbouring switch pad. Enter diode pad 2 from
        # below so the anode trace never crosses the next switch's pad 3.
        lines.append(segment(x + 6.25, y + 2.5, x + 7.0, y + 2.5, DIODE_NETS[number], "F.Cu"))
        lines.append(segment(x + 6.5, y + 2.5, x + 6.5, y + 6.0, DIODE_NETS[number], "F.Cu"))
        lines.append(segment(x + 6.5, y + 6.0, x + DIODE_DX + 1.15, y + 6.0, DIODE_NETS[number], "F.Cu"))
        lines.append(segment(x + DIODE_DX + 1.15, y + 6.0, x + DIODE_DX + 1.15, y + DIODE_DY, DIODE_NETS[number], "F.Cu"))

    # Row buses are on F.Cu.  The five dedicated vertical lanes run along the
    # right edge, then use descending escape levels above the Pro Micro's
    # left-side header row.  The final pad drops are above the button/diode
    # field and do not cross any switch copper.
    row_pad_labels = ["D2", "D3", "D4", "D5", "D6"]
    row_lanes = [BOARD_W - 2.5, BOARD_W - 2.05, BOARD_W - 1.6, BOARD_W - 1.15, BOARD_W - 0.7]
    row_escape_ys = [24.0, 22.0, 20.0, 18.0, 16.0]
    for row, y in enumerate(BUTTON_YS):
        net = ROW_NETS[row]
        lane = row_lanes[row]
        escape_y = row_escape_ys[row]
        row_start = min(bx for _, r, _, bx, _ in BUTTONS if r == row)
        lines.append(segment(row_start, y, lane, y, net, "F.Cu"))
        px, py = promicro_global_pad(row_pad_labels[row])
        lines.append(segment(lane, y, lane, escape_y, net, "F.Cu"))
        lines.append(segment(lane, escape_y, px, escape_y, net, "F.Cu"))
        lines.append(segment(px, escape_y, px, py, net, "F.Cu"))

    # Column buses are on B.Cu.  Diode cathodes reach the column bus through a
    # short front-copper segment and a via, then run up the six center lanes.
    # The six target pads share one header row after the +90-degree rotation.
    # Use six staggered escape levels above that row.  The levels are ordered
    # with the bus columns, so each horizontal escape passes above the later
    # vertical lanes without crossing them.
    column_targets = ["A2", "A1", "A0", "D15", "D14", "D16"]
    column_stage_ys = [0.8, 1.6, 2.4, 3.2, 4.0, 4.8]
    # COL5 stays left of the module.  COL6 uses a separate top fanout because
    # the compact board shifts the Pro Micro column pads over the old bus lane.
    column_bus_xs = [15.0, 34.0, 53.0, 72.0, 91.0, 110.0]
    for col, pad_label in enumerate(column_targets):
        net = COL_NETS[col]
        x = column_bus_xs[col]
        px, py = promicro_global_pad(pad_label)
        stage_y = column_stage_ys[col]
        via_ys: list[float] = []
        for number, row, button_col, bx, by in BUTTONS:
            if button_col != col:
                continue
            # Cathode pad 1 is 1.15 mm left of the diode center.  Move the
            # via slightly below the pad to avoid a via-in-pad construction.
            cathode_x = bx + DIODE_DX - 1.15
            cathode_y = by + DIODE_DY
            via_y = cathode_y + 0.75
            via_ys.append(via_y)
            lines.append(segment(cathode_x, cathode_y, cathode_x, via_y, net, "F.Cu"))
            lines.append(via(cathode_x, via_y, net))
            lines.append(segment(cathode_x, via_y, x, via_y, net, "B.Cu"))
        max_y = max(via_ys)
        if col < 5:
            lines.append(segment(x, stage_y, x, max_y, net, "B.Cu"))
            lines.append(segment(x, stage_y, px, stage_y, net, "B.Cu"))
            lines.append(segment(px, stage_y, px, py, net, "B.Cu"))
        else:
            # Escape COL6 around the lower edge of the Pro Micro header row,
            # then cross to F.Cu above the other column-pad fanouts.  The
            # final F.Cu drop enters D16 from above without crossing ROW.
            bypass_x = BOARD_W - 2.0
            bypass_y = 28.0
            lines.append(segment(x, bypass_y, x, max_y, net, "B.Cu"))
            lines.append(segment(x, bypass_y, bypass_x, bypass_y, net, "B.Cu"))
            lines.append(segment(bypass_x, bypass_y, bypass_x, stage_y, net, "B.Cu"))
            # Change layer at the right-side escape so this horizontal fanout
            # can pass over the B.Cu target drops for COL1..COL5.
            lines.append(via(bypass_x, stage_y, net))
            lines.append(segment(bypass_x, stage_y, px, stage_y, net, "F.Cu"))
            lines.append(segment(px, stage_y, px, py, net, "F.Cu"))

    # Host board outline and assembly notes.
    lines.append(f'\t(gr_rect (start 0 0) (end {f(BOARD_W)} {f(BOARD_H)}) (stroke (width 0.05) (type default)) (fill none) (layer "Edge.Cuts") (uuid ' + uid() + '))')
    lines.append(txt("PROMICRO 27-BUTTON MATRIX", BOARD_W / 2, 1.5, "F.SilkS", 1.25, 0.20))
    lines.append(txt("USB-C EXIT  ->  RIGHT", BOARD_W / 2, 3.2, "F.SilkS", 0.85, 0.13))
    lines.append(txt("Pro Micro: 5V / 16MHz / USB-C THT module", BOARD_W / 2, 4.5, "F.SilkS", 0.75, 0.11))
    lines.append(txt("27 x 1N4148WS SOD-323: JLCPCB SMT; DTS-24N + U1 hand solder", BOARD_W / 2, BOARD_H - 2.2, "F.SilkS", 0.76, 0.11))
    lines.append(txt("ROW: D2..D6   COL: A2,A1,A0,D15,D14,D16", BOARD_W / 2, BOARD_H - 1.0, "F.SilkS", 0.70, 0.10))
    for row, y in enumerate(BUTTON_YS, 1):
        lines.append(txt(f"ROW{row}", 3.0, y, "F.SilkS", 0.75, 0.11))
    for col, x in enumerate(BUTTON_XS, 1):
        lines.append(txt(f"C{col}", x, 26.0, "F.SilkS", 0.75, 0.11))
    for number, row, col, x, y in BUTTONS:
        lines.append(txt(f"D{number:02d}", x + DIODE_DX, y + DIODE_DY + 2.0, "F.SilkS", 0.55, 0.09))
    lines.append(')')
    return "\n".join(lines) + "\n"


def build_schematic() -> str:
    # Legacy Eeschema is deliberately used here because it is portable across
    # KiCad releases.  The PCB netlist and wiring_map.csv are the authoritative
    # connection source; this sheet is a readable matrix overview.
    lines = [
        'EESchema Schematic File Version 4',
        'LIBS:ProMicro_27Button-cache',
        'EELAYER 29 0',
        'EELAYER END',
        '$Descr A3 16535 11693',
        'Sheet 1 1',
        'Title "Pro Micro 27-button matrix controller"',
        'Date "2026-11-05"',
        'Rev "1.0-DRAFT"',
        'Comp "Source-verified Pro Micro 5V/16MHz reference design"',
        'Comment1 "Rows: D2,D3,D4,D5,D6; columns: A2,A1,A0,D15,D14,D16"',
        'Comment2 "DTS-24N pins 1-2 = row; pins 3-4 = diode anode"',
        'Comment3 "D_SOD-323 pad 2 = anode, pad 1 = cathode; cathode -> column"',
        'Comment4 "Amazon listing has no mechanical drawing; confirm actual clone before ordering"',
        '$EndDescr',
        'Text Notes 700 600 0    120  ~ 24',
        'PROMICRO 27-BUTTON MATRIX',
        'Text Notes 700 820 0    60   ~ 12',
        'Each button is ROW -> DTS-24N -> diode anode -> diode cathode -> COL.',
        'Text Notes 700 980 0    60   ~ 12',
        'All 27 diodes are SMD 1N4148WS / SOD-323 and are intended for JLCPCB SMT assembly.',
        'Text Notes 700 1140 0    60   ~ 12',
        'The first row is left-aligned and has three buttons; rows 2-5 have six buttons.',
        'Text Notes 10800 650 0    65   ~ 13',
        'PRO MICRO PIN MAP',
        'Text Notes 10800 820 0    55   ~ 11',
        'ROW1 = D2',
        'Text Notes 10800 940 0    55   ~ 11',
        'ROW2 = D3',
        'Text Notes 10800 1060 0    55   ~ 11',
        'ROW3 = D4',
        'Text Notes 10800 1180 0    55   ~ 11',
        'ROW4 = D5',
        'Text Notes 10800 1300 0    55   ~ 11',
        'ROW5 = D6',
        'Text Notes 10800 1460 0    55   ~ 11',
        'COL1 = A2',
        'Text Notes 10800 1580 0    55   ~ 11',
        'COL2 = A1',
        'Text Notes 10800 1700 0    55   ~ 11',
        'COL3 = A0',
        'Text Notes 10800 1820 0    55   ~ 11',
        'COL4 = D15',
        'Text Notes 10800 1940 0    55   ~ 11',
        'COL5 = D14',
        'Text Notes 10800 2060 0    55   ~ 11',
        'COL6 = D16',
    ]

    # Repeated labels make each row/column a named net without creating a
    # visually unreadable 27-way bus on an A3 sheet.
    sch_x = [1800, 3000, 4200, 5400, 6600, 7800]
    sch_y = [1800, 2800, 3800, 4800, 5800]
    n = 1
    for row, y in enumerate(sch_y):
        cols = [1, 2, 3] if row == 0 else [1, 2, 3, 4, 5, 6]
        use_xs = [3000, 4200, 5400] if row == 0 else sch_x
        for col, x in zip(cols, use_xs):
            lines += [
                '$Comp',
                f'L Switch:SW_Push SW{n:02d}',
                f'U 1 1 {0x10000000+n:08X}',
                f'P {x} {y}',
                f'F 0 "SW{n:02d}" H {x} {y+250} 50  0000 C CNN',
                f'F 1 "DTS-24N" H {x} {y-250} 50  0000 C CNN',
                'F 2 "DTS-24N" H 0 0 50  0001 C CNN',
                'F 3 "" H 0 0 50  0001 C CNN',
                f'\t1    {x} {y}',
                '\t1    0    0    -1',
                '$EndComp',
                '$Comp',
                f'L Device:D D{n:02d}',
                f'U 1 1 {0x20000000+n:08X}',
                f'P {x+350} {y}',
                f'F 0 "D{n:02d}" H {x+350} {y+200} 50  0000 C CNN',
                f'F 1 "1N4148WS" H {x+350} {y-200} 50  0000 C CNN',
                'F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN',
                'F 3 "" H 0 0 50  0001 C CNN',
                f'\t1    {x+350} {y}',
                '\t-1    0    0    1',
                '$EndComp',
                f'Wire Wire Line\n\t{x-300} {y} {x-100} {y}',
                f'Wire Wire Line\n\t{x+100} {y} {x+250} {y}',
                f'Wire Wire Line\n\t{x+450} {y} {x+700} {y}',
                f'Text Label {x-280} {y} 2    50   ~ 0\nROW{row+1}',
                f'Text Label {x+680} {y} 0    50   ~ 0\nCOL{col}',
            ]
            n += 1
    lines += [
        'Text Notes 700 7200 0    60   ~ 12',
        'PCB mechanical reference: provisional 17.78 x 33.02 mm; host holes use 1.1 mm drill.',
        'Text Notes 700 7400 0    60   ~ 12',
        'DTS-24N hole pattern: four holes, 1.2 mm drill, 12.5 mm horizontal x 5.0 mm vertical.',
        'Text Notes 700 7600 0    60   ~ 12',
        'USB-C module is Amazon B0DMNBJHT7; confirm its 24-hole pattern and body before ordering.',
        '$EndSCHEMATC',
    ]
    return "\n".join(lines) + "\n"


def build_csvs() -> None:
    with (ROOT / "wiring_map.csv").open("w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.writer(fp)
        writer.writerow(["button", "row", "column", "DTS pads 1-2", "DTS pads 3-4", "diode", "diode pad 2 A", "diode pad 1 K", "Pro Micro row pin", "Pro Micro column pin"])
        row_pins = ["D2", "D3", "D4", "D5", "D6"]
        col_pins = ["A2", "A1", "A0", "D15", "D14", "D16"]
        for number, row, col, x, y in BUTTONS:
            writer.writerow([
                f"SW{number:02d}", f"ROW{row+1}", f"COL{col+1}",
                f"ROW{row+1}", f"D{number:02d}_A", f"D{number:02d}",
                f"D{number:02d}_A", f"COL{col+1}", row_pins[row], col_pins[col],
            ])

    with (ROOT / "BOM.csv").open("w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.writer(fp)
        writer.writerow(["References", "Quantity", "Value", "Package", "Assembly", "JLCPCB/LCSC part", "Notes"])
        writer.writerow(["D01-D27", 27, "1N4148WS", "SOD-323", "JLCPCB SMT", "C493187", "JLCPCB listing; verify stock at order time"])
        writer.writerow(["SW01-SW27", 27, "DTS-24N", "THT 4-hole", "Hand solder", "", "DTS-2 datasheet footprint; 1.2 mm holes"])
        writer.writerow(["U1", 1, "Pro Micro USB-C 5V/16MHz", "24-pin THT module", "Hand solder / socket", "Amazon B0DMNBJHT7", "Assumed classic Pro Micro 2.54 mm hole pattern; verify actual clone"])

    with (ROOT / "CPL.csv").open("w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.writer(fp)
        writer.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation", "Package", "Comment"])
        for number, row, col, x, y in BUTTONS:
            writer.writerow([f"D{number:02d}", f"{x+DIODE_DX:.3f}", f"{y+DIODE_DY:.3f}", "Top", 0, "SOD-323", "1N4148WS; pad1 K toward column, pad2 A toward switch"])

    with (ROOT / "JLCPCB_CPL.csv").open("w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.writer(fp)
        writer.writerow(["Designator", "Val", "Package", "Mid X", "Mid Y", "Rotation", "Layer"])
        for number, row, col, x, y in BUTTONS:
            writer.writerow([f"D{number:02d}", "1N4148WS", "SOD-323", f"{x+DIODE_DX:.3f}", f"{y+DIODE_DY:.3f}", 0, "Top"])

    # JLCPCB assembly-only BOM. Keep hand-soldered THT parts out of this file
    # so the assembly service receives exactly the 27 diode placements.
    with (ROOT / "JLCPCB_BOM.csv").open("w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.writer(fp)
        writer.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
        for number, row, col, x, y in BUTTONS:
            writer.writerow(["1N4148WS", f"D{number:02d}", "SOD-323", "C493187"])


def build_svg() -> None:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="540" height="600" viewBox="0 0 {f(BOARD_W)} {f(BOARD_H)}">',
        f'<rect x="0" y="0" width="{f(BOARD_W)}" height="{f(BOARD_H)}" fill="#f8fafc" stroke="#111827" stroke-width="0.4"/>',
        f'<text x="{f(BOARD_W / 2)}" y="3" text-anchor="middle" font-family="sans-serif" font-size="2.6">PROMICRO 27-BUTTON / 19 mm pitch / {f(BOARD_W)} x {f(BOARD_H)} mm</text>',
        f'<rect x="{f(PROMICRO_X0)}" y="5" width="{f(PROMICRO_H)}" height="{f(PROMICRO_W)}" fill="#cbd5e1" stroke="#334155" stroke-width="0.3"/>',
        f'<text x="{f(PROMICRO_X0 + PROMICRO_H / 2)}" y="14" text-anchor="middle" font-family="sans-serif" font-size="2.1">PRO MICRO / USB-C RIGHT</text>',
    ]
    for number, row, col, x, y in BUTTONS:
        parts.append(f'<rect x="{x-6}" y="{y-6}" width="12" height="12" rx="1" fill="#dbeafe" stroke="#1d4ed8" stroke-width="0.25"/>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="2.1" fill="none" stroke="#1e3a8a" stroke-width="0.25"/>')
        parts.append(f'<rect x="{x+DIODE_DX-1.15}" y="{y+DIODE_DY-0.65}" width="2.3" height="1.3" fill="#fbbf24" stroke="#92400e" stroke-width="0.18"/>')
        parts.append(f'<text x="{x}" y="{y+0.8}" text-anchor="middle" font-family="sans-serif" font-size="1.65">SW{number:02d}</text>')
        parts.append(f'<text x="{x+DIODE_DX}" y="{y+DIODE_DY+2.0}" text-anchor="middle" font-family="sans-serif" font-size="1.2">D{number:02d}</text>')
    parts.append(f'<text x="{f(BOARD_W / 2)}" y="{f(BOARD_H - 1.5)}" text-anchor="middle" font-family="sans-serif" font-size="1.8">27 x SOD-323 diodes for JLCPCB SMT; switches and Pro Micro hand solder</text>')
    parts.append('</svg>')
    (ROOT / "placement_preview.svg").write_text("\n".join(parts), encoding="utf-8")


def build_readme() -> None:
    text = """# ProMicro_27Button

27-button matrix controller board for DTS-24N switches, using a separate Pro Micro module.

## Current reference configuration

- Pro Micro: Amazon B0DMNBJHT7, USB-C, ATmega32U4, 5 V / 16 MHz.
- Module provisional outline: 17.78 x 33.02 mm, using the common Pro Micro 24-pin THT geometry.
- Host board: 150 x 120 mm, 1.6 mm, two copper layers (preliminary layout).
- Button pitch: 19 mm horizontal and vertical.
- Button arrangement: 3 / 6 / 6 / 6 / 6, with the first row left-aligned.
- USB exit: USB-C connector faces right in the top view; the Pro Micro is rotated +90 degrees.
- Switch holes: 4 x 1.2 mm per DTS-24N, centers 12.5 mm horizontally and 5.0 mm vertically.
- Pro Micro header holes: 1.1 mm host drill, based on the official 1.016 mm module pad drill and intended for common square headers.

## Electrical mapping

Each switch is `ROW -> DTS-24N -> diode anode (A) -> diode cathode (K) -> COL`.

- ROW1..ROW5 = Pro Micro D2, D3, D4, D5, D6.
- COL1..COL6 = Pro Micro A2, A1, A0, D15, D14, D16.
- DTS-24N pads 1-2 are the row side; pads 3-4 are internally common and are the diode-anode side.
- D01..D27 are 1N4148WS SOD-323. Pad 2 is A and faces the switch; pad 1 is K and faces the column bus.

`wiring_map.csv` is the assembly/wiring reference for every button.

## JLCPCB assembly plan

The 27 diodes are SMD and are included in `BOM.csv` and `CPL.csv` for JLCPCB SMT assembly. The chosen provisional JLCPCB part is 1N4148WS SOD-323, C493187. Confirm current stock and the exact selected part at order time. DTS-24N and the Pro Micro module remain hand-soldered unless a separate THT assembly request is made.

## Important release gate

The linked Amazon product image shows USB-C and the listing specifies ATmega32U4, 5 V / 16 MHz, but the listing does not provide a mechanical drawing. This draft therefore assumes the common 24-pin Pro Micro THT pattern, 2.54 mm pitch, 17.78 x 33.02 mm body, and 1.1 mm host drills. Before ordering, measure one actual module: body width/length, both header-row centers, first-hole edge offsets, and USB-C connector position/overhang. Do not release Gerbers if those measurements differ. Some units may also omit USB-C CC pull-down resistors; verify USB-C-to-USB-C operation separately.

## Files

- `ProMicro_27Button.kicad_pcb`: routed two-layer PCB.
- `ProMicro_27Button.sch`: portable legacy KiCad schematic overview.
- `wiring_map.csv`: button-by-button net map.
- `BOM.csv`: parts and assembly responsibility.
- `CPL.csv`: diode placement file for SMT assembly.
- `JLCPCB_BOM.csv`: JLCPCB upload BOM containing only D01-D27.
- `JLCPCB_CPL.csv`: JLCPCB upload centroid file containing only D01-D27.
- `placement_preview.svg`: top-view placement preview.
- `generate_promicro_design.py`: reproducible generator.
"""
    (ROOT / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    (ROOT / "ProMicro_27Button.kicad_pcb").write_text(build_pcb(), encoding="utf-8")
    (ROOT / "ProMicro_27Button.sch").write_text(build_schematic(), encoding="utf-8")
    (ROOT / "ProMicro_27Button.kicad_pro").write_text("{}\n", encoding="utf-8")
    (ROOT / "sym-lib-table").write_text('(sym_lib_table\n  (version 7)\n)\n', encoding="utf-8")
    build_csvs()
    build_svg()
    build_readme()


if __name__ == "__main__":
    main()
