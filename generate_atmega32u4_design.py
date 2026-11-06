from __future__ import annotations

import csv
import math
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = "ATmega32U4_27Button"
BOARD_W, BOARD_H = 150.0, 120.0
BUTTON_XS = [15.0, 34.0, 53.0, 72.0, 91.0, 110.0]
BUTTON_YS = [22.0, 41.0, 60.0, 79.0, 98.0]
ROW_LAYOUT = [[0, 1, 2], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5],
              [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]]
MCU_X, MCU_Y = 132.0, 10.0
USB_X, USB_Y = 144.0, 8.0


def uid():
    return str(uuid.uuid4())


def n(v):
    return f"{v:.4f}".rstrip("0").rstrip(".")


def xy(x, y):
    return f"(xy {n(x)} {n(y)})"


def netpart(net, name):
    return f' (net {net} "{name}")' if net else ""


class Design:
    def __init__(self):
        self.nets = {}
        self.net_names = []
        self.lines = []
        self.csv_rows = []
        self.smd_placements = []
        self.tht_placements = []

    def add_net(self, name):
        if name not in self.nets:
            self.nets[name] = len(self.net_names) + 1
            self.net_names.append(name)
        return self.nets[name]

    def get_net(self, name):
        if not name:
            return 0, ""
        return self.add_net(name), name

    def line(self, text):
        self.lines.append(text)

    def text(self, text, x, y, size=1.0, layer="F.SilkS", thickness=0.15):
        self.line(
            f'  (gr_text "{text}" (at {n(x)} {n(y)}) (layer "{layer}")'
            f' (effects (font (size {n(size)} {n(size)})'
            f' (thickness {n(thickness)}))))'
        )

    def segment(self, x1, y1, x2, y2, layer, net, width=0.25):
        net_id = self.add_net(net)
        self.line(
            f'  (segment (start {n(x1)} {n(y1)}) (end {n(x2)} {n(y2)})'
            f' (width {n(width)}) (layer "{layer}") (net {net_id}))'
        )

    def via(self, x, y, net, size=0.8, drill=0.4):
        net_id = self.add_net(net)
        self.line(
            f'  (via (at {n(x)} {n(y)}) (size {n(size)}) (drill {n(drill)})'
            f' (layers "F.Cu" "B.Cu") (net {net_id}))'
        )

    def fp_start(self, name, ref, value, x, y, layer="F.Cu", rot=0.0,
                 attr="smd"):
        self.line(
            f'  (footprint "{name}" (layer "{layer}")'
            f' (at {n(x)} {n(y)} {n(rot)})'
        )
        self.line(f"    (uuid {uid()})")
        self.line(f'    (fp_text reference "{ref}" (at 0 -2.2) (layer "F.SilkS")')
        self.line('      (effects (font (size 0.9 0.9) (thickness 0.14))))')
        self.line(f'    (fp_text value "{value}" (at 0 2.2) (layer "F.Fab")')
        self.line('      (effects (font (size 0.8 0.8) (thickness 0.12))))')
        self.line(f"    (attr {attr})")

    def fp_end(self):
        self.line("  )")

    def fp_rect(self, x1, y1, x2, y2, layer="F.SilkS", width=0.15):
        self.line(
            f'    (fp_rect (start {n(x1)} {n(y1)}) (end {n(x2)} {n(y2)})'
            f' (stroke (width {n(width)}) (type default)) (fill none)'
            f' (layer "{layer}"))'
        )

    def fp_line(self, x1, y1, x2, y2, layer="F.SilkS", width=0.15):
        self.line(
            f'    (fp_line (start {n(x1)} {n(y1)}) (end {n(x2)} {n(y2)})'
            f' (stroke (width {n(width)}) (type default)) (layer "{layer}"))'
        )

    def pad_smd(self, number, x, y, size_x, size_y, net=None,
                shape="roundrect", layers='"F.Cu" "F.Paste" "F.Mask"', rr=0.2):
        net_id, net_name = self.get_net(net)
        extra = f" (roundrect_rratio {n(rr)})" if shape == "roundrect" else ""
        self.line(
            f'    (pad "{number}" smd {shape} (at {n(x)} {n(y)})'
            f' (size {n(size_x)} {n(size_y)}) (layers {layers}){extra}'
            f'{netpart(net_id, net_name)})'
        )

    def pad_tht(self, number, x, y, size, drill, net=None, shape="circle"):
        net_id, net_name = self.get_net(net)
        self.line(
            f'    (pad "{number}" thru_hole {shape} (at {n(x)} {n(y)})'
            f' (size {n(size)} {n(size)}) (drill {n(drill)})'
            f' (layers "*.Cu" "*.Mask"){netpart(net_id, net_name)})'
        )

    def pad_npth(self, x, y, diameter):
        self.line(
            f'    (pad "" np_thru_hole circle (at {n(x)} {n(y)})'
            f' (size {n(diameter)} {n(diameter)}) (drill {n(diameter)})'
            f' (layers "*.Cu" "*.Mask"))'
        )

    def add_csv(self, ref, value, footprint, x, y, rot, side, assembly,
                lcsc="", note=""):
        self.csv_rows.append({
            "Designator": ref, "Value": value, "Footprint": footprint,
            "X_mm": n(x), "Y_mm": n(y), "Rotation_deg": n(rot),
            "Side": side, "Assembly": assembly, "LCSC/JLCPCB": lcsc,
            "Note": note,
        })
        item = {
            "Designator": ref, "Mid X": n(x), "Mid Y": n(y),
            "Rotation": n(rot), "Layer": "Top" if side == "Top" else "Bottom",
        }
        (self.smd_placements if assembly == "SMT" else self.tht_placements).append(item)


def add_mount_hole(d, ref, x, y):
    d.fp_start("MountingHole:MountingHole_3.2mm_M3", ref, "M3_NPTH", x, y,
               attr="exclude_from_pos_files exclude_from_bom")
    d.fp_rect(-2.0, -2.0, 2.0, 2.0)
    d.pad_npth(0, 0, 3.2)
    d.fp_end()


def add_dts(d, ref, x, y, row, anode_net):
    d.fp_start("DTS-24N", ref, "DTS-24N", x, y, attr="through_hole")
    d.fp_rect(-7.0, -3.3, 7.0, 3.3)
    d.pad_tht("1", -6.25, -2.5, 2.2, 1.2, row, "rect")
    d.pad_tht("2", 6.25, -2.5, 2.2, 1.2, row)
    d.pad_tht("3", -6.25, 2.5, 2.2, 1.2, anode_net)
    d.pad_tht("4", 6.25, 2.5, 2.2, 1.2, anode_net)
    d.fp_end()


def add_diode(d, ref, x, y, cathode, anode):
    d.fp_start("Diode_SMD:D_SOD-323", ref, "1N4148WS", x, y)
    d.fp_rect(-1.65, -0.85, 1.65, 0.85)
    d.fp_line(-0.35, -0.7, -0.35, 0.7, "F.SilkS", 0.25)
    d.pad_smd("1", -1.15, 0, 1.25, 1.0, cathode)
    d.pad_smd("2", 1.15, 0, 1.25, 1.0, anode)
    d.fp_end()


def add_passive(d, ref, value, x, y, pad1, pad2, footprint="R_0603"):
    d.fp_start(f"Custom:{footprint}", ref, value, x, y)
    d.fp_rect(-1.45, -0.75, 1.45, 0.75)
    d.pad_smd("1", -1.0, 0, 0.9, 0.9, pad1)
    d.pad_smd("2", 1.0, 0, 0.9, 0.9, pad2)
    d.fp_end()


def add_crystal(d, ref, x, y, left_net, right_net):
    d.fp_start("Crystal:Crystal_SMD_5032-2Pin", ref, "16MHz", x, y)
    d.fp_rect(-2.5, -1.6, 2.5, 1.6)
    d.pad_smd("1", -1.6, 0, 1.5, 1.4, left_net)
    d.pad_smd("2", 1.6, 0, 1.5, 1.4, right_net)
    d.fp_end()


def qfp_pin_pos(pin):
    if 1 <= pin <= 11:
        return -6.5, -4.0 + (pin - 1) * 0.8
    if 12 <= pin <= 22:
        return -4.0 + (pin - 12) * 0.8, 6.5
    if 23 <= pin <= 33:
        return 6.5, 4.0 - (pin - 23) * 0.8
    return 4.0 - (pin - 34) * 0.8, -6.5


def add_qfp44(d):
    pin_nets = {
        2: "+5V", 3: "USB_D-", 4: "USB_D+", 5: "GND", 6: "UCAP",
        7: "+5V", 9: "ICSP_SCK", 10: "ICSP_MOSI", 11: "ICSP_MISO",
        12: "COL1", 13: "RESET", 14: "+5V", 15: "GND", 16: "XTAL2",
        17: "XTAL1", 18: "COL2", 19: "COL3", 20: "COL4", 21: "COL5",
        22: "COL6", 23: "GND", 24: "+5V", 33: "HWB", 34: "+5V",
        35: "GND", 36: "ROW1", 37: "ROW2", 38: "ROW3", 39: "ROW4",
        40: "ROW5", 42: "AREF", 43: "GND", 44: "+5V",
    }
    d.fp_start("Package_QFP:LQFP-44_10x10mm_P0.8mm", "U1",
               "ATmega32U4-AU", MCU_X, MCU_Y)
    d.fp_rect(-5.0, -5.0, 5.0, 5.0, "F.Fab", 0.1)
    d.fp_rect(-5.6, -5.6, 5.6, 5.6)
    d.fp_line(-5.0, -5.0, -4.2, -5.0, "F.SilkS", 0.3)
    d.fp_line(-5.0, -5.0, -5.0, -4.2, "F.SilkS", 0.3)
    d.line('    (fp_circle (center -4.3 -4.3) (end -4.0 -4.3)'
            ' (stroke (width 0.2) (type default)) (fill none)'
            ' (layer "F.SilkS"))')
    for pin in range(1, 45):
        px, py = qfp_pin_pos(pin)
        if 1 <= pin <= 11 or 23 <= pin <= 33:
            # Left/right lead: long dimension is in X, pin pitch in Y.
            sx, sy = 1.6, 0.3
        else:
            # Top/bottom lead: long dimension is in Y, pin pitch in X.
            sx, sy = 0.3, 1.6
        d.pad_smd(str(pin), px, py, sx, sy, pin_nets.get(pin))
    d.fp_end()
    d.add_csv("U1", "ATmega32U4-AU", "LQFP-44_10x10_P0.8", MCU_X, MCU_Y,
              0, "Top", "SMT", "C44854", "JLC basic SMT part")
    return {pin: (MCU_X + qfp_pin_pos(pin)[0], MCU_Y + qfp_pin_pos(pin)[1])
            for pin in range(1, 45)}


def rotate_xy(x, y, cx, cy, rot):
    # KiCad's positive footprint rotation is clockwise in board coordinates.
    r = math.radians(rot)
    return cx + x * math.cos(r) + y * math.sin(r), cy - x * math.sin(r) + y * math.cos(r)


def add_usb_c(d):
    d.fp_start("Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12",
               "J1", "TYPE-C-31-M-12", USB_X, USB_Y, rot=90)
    d.fp_rect(-4.7, -5.0, 4.7, 5.0)
    d.fp_rect(-5.32, -4.0, 5.32, 4.0, "F.CrtYd", 0.05)
    raw = {
        "A1": (-3.25, -4.045, "GND"), "A4": (-2.45, -4.045, "+5V"),
        "A5": (-1.25, -4.045, "USB_CC1"), "A6": (-0.25, -4.045, "USB_D+"),
        "A7": (0.25, -4.045, "USB_D-"), "A8": (1.25, -4.045, None),
        "A9": (2.45, -4.045, "+5V"), "A12": (3.25, -4.045, "GND"),
        "B1": (3.25, -4.045, "GND"), "B4": (2.45, -4.045, "+5V"),
        "B5": (1.75, -4.045, "USB_CC2"), "B6": (0.75, -4.045, "USB_D+"),
        "B7": (-0.75, -4.045, "USB_D-"), "B8": (-1.75, -4.045, None),
        "B9": (-2.45, -4.045, "+5V"), "B12": (-3.25, -4.045, "GND"),
    }
    out = {}
    for name, (lx, ly, net) in raw.items():
        gx, gy = rotate_xy(lx, ly, USB_X, USB_Y, 90)
        out.setdefault(net or "NC", []).append((gx, gy))
        wide = name in {"A1", "A4", "A9", "A12", "B1", "B4", "B9", "B12"}
        d.pad_smd(name, lx, ly, 0.6 if wide else 0.3, 1.45, net, rr=0.25)
    for i, (lx, ly) in enumerate([(-4.32, -3.13), (-4.32, 1.05),
                                  (4.32, -3.13), (4.32, 1.05)], 1):
        d.pad_tht(f"SH{i}", lx, ly, 1.8, 1.0, "GND")
    d.fp_end()
    d.add_csv("J1", "TYPE-C-31-M-12", "USB_C_Receptacle_HRO_TYPE-C-31-M-12",
              USB_X, USB_Y, 90, "Top", "SMT", "C165948",
              "USB-C right-facing; confirm JLC footprint revision")
    return out


def add_icsp(d, x, y):
    d.fp_start("Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical",
               "J2", "ICSP_2x03", x, y, attr="through_hole")
    d.fp_rect(-1.9, -3.3, 4.45, 3.3)
    nets = ["ICSP_MISO", "+5V", "ICSP_SCK", "ICSP_MOSI", "RESET", "GND"]
    for i, net in enumerate(nets):
        px = 0 if i % 2 == 0 else 2.54
        py = (i // 2 - 1) * 2.54
        d.pad_tht(str(i + 1), px, py, 1.7, 1.0, net,
                  "rect" if i == 0 else "circle")
    d.fp_end()
    d.add_csv("J2", "ICSP_2x03", "PinHeader_2x03_P2.54mm_Vertical",
              x, y, 0, "Top", "THT", "", "Optional user-installed programming header")


def add_test_pad(d, ref, x, y, net):
    d.fp_start("TestPoint:TestPoint_Pad_D1.5mm", ref, net, x, y)
    d.pad_smd("1", 0, 0, 1.5, 1.5, net, "circle", '"F.Cu" "F.Paste" "F.Mask"', 0)
    d.fp_end()
    d.add_csv(ref, net, "TestPoint_Pad_D1.5mm", x, y, 0, "Top", "SMT", "",
              "Optional test point")


def add_zone(d, net, layer):
    net_id = d.add_net(net)
    d.line(
        f'  (zone (net {net_id}) (net_name "{net}") (layer "{layer}")'
        ' (hatch edge 0.5) (connect_pads (clearance 0.3))'
        ' (min_thickness 0.25)'
        ' (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.3))'
        ' (polygon (pts'
        f' {xy(1.5, 1.5)} {xy(148.5, 1.5)}'
        f' {xy(148.5, 118.5)} {xy(1.5, 118.5)} )))'
    )


def add_zone_rect(d, net, layer, x1, y1, x2, y2, priority=0):
    net_id = d.add_net(net)
    d.line(
        f'  (zone (net {net_id}) (net_name "{net}") (layer "{layer}")'
        f' (priority {priority}) (hatch edge 0.5)'
        ' (connect_pads (clearance 0.3)) (min_thickness 0.25)'
        ' (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.3))'
        ' (polygon (pts'
        f' {xy(x1, y1)} {xy(x2, y1)} {xy(x2, y2)} {xy(x1, y2)} )))'
    )


def build_pcb():
    d = Design()
    for name in ["GND", "+5V", "USB_D+", "USB_D-", "USB_CC1", "USB_CC2",
                 "RESET", "HWB", "UCAP", "XTAL1", "XTAL2", "AREF",
                 "ROW1", "ROW2", "ROW3", "ROW4", "ROW5",
                 "COL1", "COL2", "COL3", "COL4", "COL5", "COL6"]:
        d.add_net(name)
    d.line("(kicad_pcb (version 20240108) (generator pcbnew)")
    d.line("  (general (thickness 1.6))")
    d.line('  (paper "A4")')
    d.line('  (layers (0 "F.Cu" signal) (31 "B.Cu" signal)'
            ' (36 "B.SilkS" user "b.silkscreen")'
            ' (37 "F.SilkS" user "f.silkscreen") (44 "Edge.Cuts" user))')
    d.line('  (setup (pad_to_mask_clearance 0))')
    for name in d.net_names:
        d.line(f'  (net {d.nets[name]} "{name}")')

    for a, b in [((0, 0), (BOARD_W, 0)), ((BOARD_W, 0), (BOARD_W, BOARD_H)),
                 ((BOARD_W, BOARD_H), (0, BOARD_H)), ((0, BOARD_H), (0, 0))]:
        d.line(
            f'  (gr_line (start {n(a[0])} {n(a[1])})'
            f' (end {n(b[0])} {n(b[1])})'
            ' (stroke (width 0.2) (type default)) (layer "Edge.Cuts"))'
        )
    d.text("ATmega32U4 27-BUTTON MATRIX", 75, 3.0, 1.4)
    d.text("USB-C", 143.5, 14.0, 1.0)
    d.text("ICSP", 113.0, 13.0, 0.9)
    d.text("19 mm pitch / 150 x 120 mm", 75, 117.0, 1.0)
    d.text("DTS-24N: pins 1-2=ROW, pins 3-4=diode anode", 75, 114.8, 0.75)
    # No arbitrary mounting holes are added: the confirmed DTS-24N switch
    # holes and USB/header holes are the only mechanical holes in this release.

    button_index = 0
    diode_positions = {}
    for r, y in enumerate(BUTTON_YS):
        for c in ROW_LAYOUT[r]:
            x = BUTTON_XS[c]
            button_index += 1
            sw_ref = f"SW{button_index:02d}"
            d_ref = f"D{button_index:02d}"
            anode = f"D{button_index:02d}_A"
            add_dts(d, sw_ref, x, y, f"ROW{r + 1}", anode)
            dx, dy = x + 10.0, y + 4.5
            diode_positions[(r, c)] = (dx, dy)
            add_diode(d, d_ref, dx, dy, f"COL{c + 1}", anode)
            d.add_csv(sw_ref, "DTS-24N", "DTS-24N_4P_12mm", x, y, 0,
                      "Top", "THT", "C483776",
                      "Verify exact cap-compatible DTS-24N variant before order")
            d.add_csv(d_ref, "1N4148WS", "D_SOD-323", dx, dy, 0,
                      "Top", "SMT", "C493187", "Cathode pad 1 to column")
            d.segment(x - 6.25, y + 2.5, x + 11.15, y + 2.5,
                      "F.Cu", anode, 0.3)
            d.segment(x + 11.15, y + 2.5, x + 11.15, y + 4.5,
                      "F.Cu", anode, 0.3)

    # These lanes are deliberately to the right of every switch trace.  They
    # are on F.Cu only until the row bus, then fan out on B.Cu.
    row_lane_x = [122.0, 123.0, 124.0, 125.0, 126.0]
    row_stage_y = [1.0, 1.4, 1.8, 2.2, 2.6]
    for r, y in enumerate(BUTTON_YS):
        xs = [BUTTON_XS[c] for c in ROW_LAYOUT[r]]
        row_y = y - 2.5
        d.segment(min(xs) - 6.25, row_y, max(xs) + 6.25, row_y,
                  "F.Cu", f"ROW{r + 1}", 0.3)
        d.segment(max(xs) + 6.25, row_y, row_lane_x[r], row_y,
                  "F.Cu", f"ROW{r + 1}", 0.3)
        d.via(row_lane_x[r], row_y, f"ROW{r + 1}")

    mcu_pads = add_qfp44(d)
    usb_pads = add_usb_c(d)
    add_icsp(d, 112.0, 8.0)
    add_crystal(d, "X1", 134.5, 19.0, "XTAL1", "XTAL2")
    d.add_csv("X1", "16MHz", "Crystal_SMD_5032-2Pin", 134.5, 19.0, 0,
              "Top", "SMT", "C122519",
              "16MHz crystal; verify current JLC part package")
    passive_specs = [
        ("R1", "5.1k", 142.0, 9.25, "USB_CC1", "GND", "R_0603", "C20983"),
        ("R2", "5.1k", 142.0, 6.25, "USB_CC2", "GND", "R_0603", "C20983"),
        ("R3", "10k", 124.0, 17.8, "RESET", "+5V", "R_0603", "C25804"),
        ("R4", "10k", 127.0, 17.8, "HWB", "+5V", "R_0603", "C25804"),
        ("C1", "100nF", 120.0, 7.0, "+5V", "GND", "C_0603", "C14663"),
        ("C2", "100nF", 120.0, 12.0, "+5V", "GND", "C_0603", "C14663"),
        ("C3", "1uF", 123.0, 10.0, "UCAP", "GND", "C_0603", "C15849"),
        ("C4", "100nF", 131.5, 5.0, "AREF", "GND", "C_0603", "C14663"),
        ("C5", "33pF", 125.0, 19.0, "XTAL1", "GND", "C_0603", "C1653"),
        ("C6", "33pF", 137.0, 19.0, "XTAL2", "GND", "C_0603", "C1653"),
        ("C7", "1uF", 145.0, 1.5, "+5V", "GND", "C_0603", "C15849"),
    ]
    for ref, value, x, y, p1, p2, fp, lcsc in passive_specs:
        add_passive(d, ref, value, x, y, p1, p2, fp)
        d.add_csv(ref, value, fp, x, y, 0, "Top", "SMT", lcsc,
                  "Provisional JLC basic part; verify package/value")
    add_test_pad(d, "TP1", 120.0, 15.0, "RESET")
    add_test_pad(d, "TP2", 120.0, 17.0, "HWB")

    for r, pin in enumerate([36, 37, 38, 39, 40]):
        px, py = mcu_pads[pin]
        row = f"ROW{r + 1}"
        sx, sy = row_lane_x[r], row_stage_y[r]
        d.segment(sx, BUTTON_YS[r] - 2.5, sx, sy, "B.Cu", row, 0.25)
        d.segment(sx, sy, px, sy, "F.Cu", row, 0.25)

    col_lanes = {c: [] for c in range(6)}
    for r in range(5):
        for c in ROW_LAYOUT[r]:
            dx, dy = diode_positions[(r, c)]
            cath_x, via_y = dx - 1.15, dy + 1.0
            d.segment(cath_x, dy, cath_x, via_y, "F.Cu", f"COL{c + 1}", 0.25)
            d.via(cath_x, via_y, f"COL{c + 1}")
            col_lanes[c].append((cath_x, via_y))
    col_stage_y = [114.0, 112.0, 110.0, 108.0, 106.0, 104.0]
    col_pins = [12, 18, 19, 20, 21, 22]
    for c in range(6):
        net = f"COL{c + 1}"
        points = sorted(col_lanes[c], key=lambda p: p[1])
        first, last = points[0], points[-1]
        d.segment(first[0], first[1], last[0], last[1], "B.Cu", net, 0.25)
        target_x, target_y = mcu_pads[col_pins[c]]
        stage_y = col_stage_y[c]
        d.segment(last[0], last[1], last[0], stage_y, "B.Cu", net, 0.25)
        d.via(last[0], stage_y, net)
        # Horizontal fan-out is on F.Cu.  The target via is intentionally
        # placed on the MCU pad center so the short B.Cu leg reaches the
        # bottom-side SMD pad without crossing another column.
        d.segment(last[0], stage_y, target_x, stage_y, "F.Cu", net, 0.25)
        d.via(target_x, stage_y, net)
        d.segment(target_x, stage_y, target_x, target_y, "B.Cu", net, 0.25)
        d.via(target_x, target_y, net, size=0.5, drill=0.25)

    dplus, dminus = usb_pads["USB_D+"], usb_pads["USB_D-"]
    # USB data pair: D+ crosses the row fan-out on B.Cu and changes to F.Cu
    # at the MCU; D- stays on F.Cu.  They therefore never share a layer in
    # the narrow connector-to-MCU corridor.
    d.segment(dplus[0][0], dplus[0][1], dplus[1][0], dplus[1][1],
              "B.Cu", "USB_D+", 0.25)
    d.segment(dplus[0][0], dplus[0][1], 130.0, dplus[0][1],
              "B.Cu", "USB_D+", 0.25)
    d.segment(130.0, dplus[0][1], 130.0, 8.4, "B.Cu", "USB_D+", 0.25)
    d.segment(130.0, 8.4, 129.0, 8.4, "B.Cu", "USB_D+", 0.25)
    d.via(129.0, 8.4, "USB_D+")
    d.segment(129.0, 8.4, MCU_X - 6.5, MCU_Y - 1.6,
              "F.Cu", "USB_D+", 0.25)
    d.segment(dminus[0][0], dminus[0][1], dminus[1][0], dminus[1][1],
              "F.Cu", "USB_D-", 0.25)
    d.segment(dminus[1][0], dminus[1][1], 137.0, dminus[1][1],
              "F.Cu", "USB_D-", 0.25)
    d.segment(137.0, dminus[1][1], 137.0, MCU_Y - 2.4,
              "F.Cu", "USB_D-", 0.25)
    d.segment(137.0, MCU_Y - 2.4, MCU_X - 6.5, MCU_Y - 2.4,
              "F.Cu", "USB_D-", 0.25)

    # A local B.Cu +5V plane covers the electronics area.  Every SMD +5V pad
    # gets a via, so power does not need to cross the USB/data traces.
    for px, py in usb_pads["+5V"]:
        d.via(px, py, "+5V", size=0.5, drill=0.25)
    # MCU power pins fan out to the local +5V plane through clear areas rather
    # than placing large vias between the 0.8 mm-pitch QFP leads.
    for pin, vx, vy in [
        (2, 127.5, 6.8), (7, 127.5, 10.8), (24, 137.0, 13.2),
        (34, 136.0, 2.8), (44, 127.0, 3.5),
    ]:
        px, py = mcu_pads[pin]
        d.segment(px, py, vx, vy, "F.Cu", "+5V", 0.2)
        d.via(vx, vy, "+5V", size=0.5, drill=0.25)
    d.segment(mcu_pads[14][0], mcu_pads[14][1], 129.6, 18.0,
              "F.Cu", "+5V", 0.2)
    d.segment(129.6, 18.0, 137.0, 18.0, "F.Cu", "+5V", 0.2)
    d.via(137.0, 18.0, "+5V", size=0.5, drill=0.25)
    d.segment(137.0, 18.0, 137.0, 15.0, "B.Cu", "+5V", 0.2)
    for px, py in [(119.0, 7.0), (119.0, 12.0), (125.0, 17.8),
                   (144.0, 1.5)]:
        d.via(px, py, "+5V", size=0.5, drill=0.25)
    d.segment(128.0, 17.8, 128.0, 18.5, "F.Cu", "+5V", 0.2)
    d.segment(128.0, 18.5, 140.0, 18.5, "F.Cu", "+5V", 0.2)
    d.via(140.0, 18.5, "+5V", size=0.5, drill=0.25)
    d.segment(140.0, 18.5, 140.0, 15.0, "B.Cu", "+5V", 0.2)
    d.segment(114.54, 5.46, 114.54, 4.0, "B.Cu", "+5V", 0.25)
    d.segment(114.54, 4.0, 117.0, 4.0, "B.Cu", "+5V", 0.25)
    d.segment(117.0, 4.0, 117.0, 0.4, "B.Cu", "+5V", 0.25)
    d.segment(117.0, 0.4, 127.0, 0.4, "B.Cu", "+5V", 0.25)
    d.via(127.0, 1.0, "+5V")

    # USB-C CC pull-downs. Their resistor pads are aligned with the connector
    # contacts, so no CC trace has to cross the USB data pair.
    for net, (cx, cy), rx, ry in [
        ("USB_CC1", usb_pads["USB_CC1"][0], 141.0, 9.25),
        ("USB_CC2", usb_pads["USB_CC2"][0], 141.0, 6.25),
    ]:
        d.segment(cx, cy, rx, ry, "F.Cu", net, 0.18)

    d.segment(mcu_pads[13][0], mcu_pads[13][1], 123.0, 17.8,
              "F.Cu", "RESET", 0.25)
    d.segment(123.0, 17.8, 123.0, 15.0, "F.Cu", "RESET", 0.25)
    d.segment(123.0, 15.0, 120.0, 15.0, "F.Cu", "RESET", 0.25)
    d.via(mcu_pads[33][0], mcu_pads[33][1], "HWB")
    d.segment(mcu_pads[33][0], mcu_pads[33][1], 138.5, 4.0,
              "B.Cu", "HWB", 0.25)
    d.segment(138.5, 4.0, 147.5, 4.0, "B.Cu", "HWB", 0.25)
    d.segment(147.5, 4.0, 147.5, 17.8, "B.Cu", "HWB", 0.25)
    d.segment(147.5, 17.8, 126.0, 17.8, "F.Cu", "HWB", 0.25)
    d.via(126.0, 17.8, "HWB")
    d.segment(126.0, 17.8, 120.0, 17.0, "F.Cu", "HWB", 0.25)
    # XTAL1 stays on F.Cu; XTAL2 takes a short B.Cu detour so the two
    # adjacent bottom-side MCU pads never cross.
    d.segment(mcu_pads[17][0], mcu_pads[17][1], 132.0, 18.0,
              "F.Cu", "XTAL1", 0.25)
    d.segment(132.0, 18.0, 132.9, 19.0, "F.Cu", "XTAL1", 0.25)
    d.segment(132.9, 19.0, 132.9, 21.0, "F.Cu", "XTAL1", 0.25)
    d.segment(132.9, 21.0, 124.0, 21.0, "F.Cu", "XTAL1", 0.25)
    d.segment(124.0, 21.0, 124.0, 19.0, "F.Cu", "XTAL1", 0.25)
    d.via(mcu_pads[16][0], mcu_pads[16][1], "XTAL2")
    d.segment(mcu_pads[16][0], mcu_pads[16][1], 131.2, 15.5,
              "B.Cu", "XTAL2", 0.25)
    d.segment(131.2, 15.5, 137.0, 15.5, "B.Cu", "XTAL2", 0.25)
    d.segment(137.0, 15.5, 137.0, 19.0, "B.Cu", "XTAL2", 0.25)
    d.via(137.0, 19.0, "XTAL2")
    d.segment(137.0, 19.0, 136.1, 19.0, "F.Cu", "XTAL2", 0.25)
    d.segment(136.1, 19.0, 136.0, 19.0, "F.Cu", "XTAL2", 0.25)
    d.segment(mcu_pads[6][0], mcu_pads[6][1], 122.0, 10.0,
              "F.Cu", "UCAP", 0.25)
    d.segment(mcu_pads[42][0], mcu_pads[42][1], 129.6, 4.0,
              "F.Cu", "AREF", 0.25)
    d.segment(129.6, 4.0, 130.5, 4.0, "F.Cu", "AREF", 0.25)
    d.segment(130.5, 4.0, 130.5, 5.0, "F.Cu", "AREF", 0.25)

    # ICSP routes use separate corridors.  The two adjacent pins on the
    # 2x3 header are deliberately dog-legged before entering the MCU.
    d.segment(112.0, 5.46, 108.0, 5.46, "F.Cu", "ICSP_MISO", 0.25)
    d.segment(108.0, 5.46, 108.0, 14.0, "F.Cu", "ICSP_MISO", 0.25)
    d.segment(108.0, 14.0, mcu_pads[11][0], mcu_pads[11][1],
              "F.Cu", "ICSP_MISO", 0.25)

    d.segment(112.0, 8.0, 110.0, 8.0, "F.Cu", "ICSP_SCK", 0.25)
    d.segment(110.0, 8.0, 110.0, 12.4, "F.Cu", "ICSP_SCK", 0.25)
    d.segment(110.0, 12.4, mcu_pads[9][0], mcu_pads[9][1],
              "F.Cu", "ICSP_SCK", 0.25)

    d.segment(114.54, 8.0, 114.54, 9.0, "F.Cu", "ICSP_MOSI", 0.25)
    d.segment(114.54, 9.0, 116.0, 9.0, "F.Cu", "ICSP_MOSI", 0.25)
    d.segment(116.0, 9.0, 116.0, 13.2, "F.Cu", "ICSP_MOSI", 0.25)
    d.segment(116.0, 13.2, mcu_pads[10][0], mcu_pads[10][1],
              "F.Cu", "ICSP_MOSI", 0.25)

    # J2 pin 2 (+5V) is routed above the neighboring MISO pin.
    d.segment(114.54, 5.46, 114.54, 4.0, "B.Cu", "+5V", 0.25)
    d.segment(114.54, 4.0, 117.0, 4.0, "B.Cu", "+5V", 0.25)
    d.segment(117.0, 4.0, 117.0, 0.4, "B.Cu", "+5V", 0.25)
    d.segment(117.0, 0.4, 127.0, 0.4, "B.Cu", "+5V", 0.25)

    # J2 pin 5 (RESET) uses the left-side corridor and joins TP1.
    d.segment(112.0, 10.54, 112.0, 16.0, "F.Cu", "RESET", 0.25)
    d.segment(112.0, 16.0, 120.0, 16.0, "F.Cu", "RESET", 0.25)
    d.segment(120.0, 16.0, 120.0, 15.0, "F.Cu", "RESET", 0.25)

    # Stitch the two ground pours in an unused area near the top-right
    # electronics section.
    d.via(118.0, 21.0, "GND")
    d.via(146.0, 21.0, "GND")
    add_zone(d, "GND", "F.Cu")
    add_zone(d, "GND", "B.Cu")
    add_zone_rect(d, "+5V", "B.Cu", 127.0, 0.5, 149.0, 15.5, 1)
    for i, name in enumerate(["PF0/ROW1", "PF1/ROW2", "PF4/ROW3",
                              "PF5/ROW4", "PF6/ROW5"]):
        d.text(name, 104, 5.0 + i * 1.6, 0.65)
    for i, name in enumerate(["PB7/COL1", "PD0/COL2", "PD1/COL3",
                              "PD2/COL4", "PD3/COL5", "PD5/COL6"]):
        d.text(name, 144.0, 104.0 + i * 1.5, 0.6)
    for r, y in enumerate(BUTTON_YS):
        d.text(f"ROW{r + 1}", 4.0, y - 2.5, 0.65)
    for c, x in enumerate(BUTTON_XS):
        d.text(f"COL{c + 1}", x + 10.0, 109.0, 0.65)
    d.line(")")
    return d


def build_legacy_schematic():
    lines = [
        "EESchema Schematic File Version 4", "LIBS:power", "LIBS:device",
        "LIBS:Connector_Generic", "EELAYER 29 0", "EELAYER END",
        "$Descr A4 11693 8268", "Sheet 1 1",
        'Title "ATmega32U4 USB-C 27-button matrix controller"',
        'Comment1 "Integrated MCU design for JLCPCB SMT assembly"',
        'Comment2 "150 x 120 mm / 19 mm pitch / 2-layer"',
        'Comment3 "PCB netlist and routing are authoritative"',
        'Comment4 "2026-11-06"', "$EndDescr",
        "Text Notes 800 700 0    120  ~ 24",
        "ATmega32U4-AU (JLC C44854) + USB-C TYPE-C-31-M-12 (JLC C165948)",
        "Text Notes 800 950 0    80   ~ 16",
        "Power: USB VBUS -> +5V; CC1/CC2 each have 5.1k pull-down to GND",
        "Text Notes 800 1150 0    80   ~ 16",
        "Clock: 16MHz crystal X1, 33pF each side; UCAP=1uF; RESET/HWB=10k pull-up",
        "Text Notes 800 1350 0    80   ~ 16",
        "ICSP J2: 1=MISO 2=+5V 3=SCK 4=MOSI 5=RESET 6=GND",
        "Text Notes 800 1550 0    80   ~ 16",
        "Matrix rows: PF0/PF1/PF4/PF5/PF6 = ROW1..ROW5",
        "Text Notes 800 1750 0    80   ~ 16",
        "Matrix columns: PB7/PD0/PD1/PD2/PD3/PD5 = COL1..COL6",
        "Text Notes 800 2050 0    90   ~ 18",
        "DTS-24N internal contact: pins 1-2 are one side; pins 3-4 are the other.",
        "Text Notes 800 2250 0    90   ~ 18",
        "Each key uses one 1N4148WS SOD-323: switch side -> diode anode, cathode -> column.",
        "Text Notes 800 2550 0    80   ~ 16",
        "27 keys: row1 has 3 keys; rows2-5 have 6 keys each.",
        "Text Notes 800 2850 0    75   ~ 15",
        "Do not order until DTS-24N cap and the JLC USB-C footprint are checked against physical parts.",
        "$EndSCHEMATC",
    ]
    return "\n".join(lines) + "\n"


def write_csvs(d):
    fields = ["Designator", "Value", "Footprint", "X_mm", "Y_mm",
              "Rotation_deg", "Side", "Assembly", "LCSC/JLCPCB", "Note"]
    with (ROOT / f"{OUT}_placement.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(d.csv_rows)
    bom = [
        ("U1", "ATmega32U4-AU", "LQFP-44_10x10_P0.8", "C44854", "SMT"),
        ("J1", "TYPE-C-31-M-12", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "C165948", "SMT"),
        ("X1", "16MHz", "Crystal_SMD_5032-2Pin", "C122519", "SMT"),
        ("D01-D27", "1N4148WS", "D_SOD-323", "C493187", "SMT"),
        ("SW01-SW27", "DTS-24N", "DTS-24N_4P_12mm", "C483776", "THT / verify variant"),
        ("R1-R2", "5.1k", "R_0603", "C20983", "SMT / verify current basic part"),
        ("R3-R4", "10k", "R_0603", "C25804", "SMT / verify current basic part"),
        ("C1-C2,C4", "100nF", "C_0603", "C14663", "SMT / verify current basic part"),
        ("C3,C7", "1uF", "C_0603", "C15849", "SMT / verify current basic part"),
        ("C5-C6", "33pF", "C_0603", "C1653", "SMT / verify current basic part"),
        ("J2", "ICSP_2x03", "PinHeader_2x03_P2.54mm_Vertical", "", "Optional THT / user install"),
        ("TP1-TP2", "Test pad", "TestPoint_Pad_D1.5mm", "", "Optional SMT"),
    ]
    with (ROOT / f"{OUT}_BOM.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Designator", "Value", "Footprint", "LCSC/JLCPCB", "Assembly"])
        w.writerows(bom)
    with (ROOT / f"{OUT}_JLCPCB_CPL.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["Designator", "Mid X", "Mid Y", "Rotation", "Layer"])
        w.writeheader()
        w.writerows(d.smd_placements)
    with (ROOT / f"{OUT}_JLCPCB_BOM.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Comment", "Designator", "Footprint", "JLCPCB Part #", "Assembly"])
        for row in bom:
            w.writerow([row[1], row[0], row[2], row[3], row[4]])
    with (ROOT / f"{OUT}_wiring_map.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Button", "Row", "Column", "DTS pins 1-2",
                    "DTS pins 3-4", "Diode", "Diode pad 1 cathode",
                    "Diode pad 2 anode", "MCU raw port"])
        idx = 0
        col_ports = ["PB7 (pin12)", "PD0 (pin18)", "PD1 (pin19)",
                     "PD2 (pin20)", "PD3 (pin21)", "PD5 (pin22)"]
        row_ports = ["PF0 (pin36)", "PF1 (pin37)", "PF4 (pin38)",
                     "PF5 (pin39)", "PF6 (pin40)"]
        for r in range(5):
            for c in ROW_LAYOUT[r]:
                idx += 1
                w.writerow([f"SW{idx:02d}", f"ROW{r + 1}", f"COL{c + 1}",
                            f"ROW{r + 1}", f"D{idx:02d}_A", f"D{idx:02d}",
                            f"COL{c + 1}", f"D{idx:02d}_A",
                            f"{row_ports[r]} / {col_ports[c]}"])


def write_preview():
    sx, sy, scale = 4.0, 4.0, 4.0
    w, h = BOARD_W * scale + 2 * sx, BOARD_H * scale + 2 * sy
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
        f'viewBox="0 0 {w:.0f} {h:.0f}">',
        '<rect width="100%" height="100%" fill="#f5f5f5"/>',
        f'<rect x="{sx}" y="{sy}" width="{BOARD_W*scale}" height="{BOARD_H*scale}" '
        'fill="#174d2a" stroke="#111" stroke-width="2"/>',
    ]
    for r, y in enumerate(BUTTON_YS):
        for c in ROW_LAYOUT[r]:
            x = BUTTON_XS[c]
            cx, cy = sx + x * scale, sy + y * scale
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="24" '
                       'fill="#2b7d45" stroke="#d6e8d6" stroke-width="2"/>')
            out.append(f'<text x="{cx:.1f}" y="{cy+4:.1f}" text-anchor="middle" '
                       'font-size="11" fill="white">SW</text>')
    out.append(f'<rect x="{sx+(MCU_X-6)*scale:.1f}" y="{sy+(MCU_Y-6)*scale:.1f}" '
               'width="48" height="48" fill="#222" stroke="#f2c14e" stroke-width="2"/>')
    out.append(f'<text x="{sx+MCU_X*scale:.1f}" y="{sy+(MCU_Y+1)*scale:.1f}" '
               'text-anchor="middle" font-size="10" fill="white">ATmega32U4</text>')
    out.append(f'<rect x="{sx+(USB_X-5.3)*scale:.1f}" y="{sy+(USB_Y-5.3)*scale:.1f}" '
               'width="42" height="42" fill="#888" stroke="#fff" stroke-width="2"/>')
    out.append(f'<text x="{sx+USB_X*scale:.1f}" y="{sy+(USB_Y+1)*scale:.1f}" '
               'text-anchor="middle" font-size="10" fill="white">USB-C</text>')
    out.append(f'<text x="{sx+75*scale:.1f}" y="{sy+2.5*scale:.1f}" text-anchor="middle" '
               'font-size="14" fill="white">150 x 120 mm / 19 mm pitch</text>')
    out.append("</svg>")
    (ROOT / f"{OUT}_placement_preview.svg").write_text("\n".join(out), encoding="utf-8")


def write_readme():
    text = """# ATmega32U4 USB-C 27ボタン基板（統合版）

作業日: 2026-11-06
基板: 150 mm × 120 mm、2層、ボタン中心ピッチ19 mm、上段3個＋下段4段各6個

## 今回の変更

AmazonのPro Microモジュールを載せる方式から、JLCPCBで実装しやすい
ATmega32U4-AU（LQFP-44）とUSB-Cコネクタを基板上に直接実装する方式へ変更した。
USB-CはTYPE-C-31-M-12を右向きに配置している。

## 主要部品候補

- U1: ATmega32U4-AU / JLCPCB C44854
- J1: TYPE-C-31-M-12 / JLCPCB C165948
- X1: 16 MHz 2端子水晶 / JLCPCB C122519
- D01-D27: 1N4148WS SOD-323 / JLCPCB C493187
- SW01-SW27: DTS-24N候補 / JLCPCB C483776（DTS-24N-V表記のため、キャップ適合は発注前に実物・仕様書で最終確認）

## MCUの接続

- ROW1..ROW5 = PF0, PF1, PF4, PF5, PF6（U1 pin 36,37,38,39,40）
- COL1..COL6 = PB7, PD0, PD1, PD2, PD3, PD5（U1 pin 12,18,19,20,21,22）
- USB D- / D+ = U1 pin 3 / 4
- RESET = U1 pin 13、HWB = U1 pin 33
- USB-C CC1/CC2には各5.1 kΩのGNDプルダウン
- UCAP=1 µF、RESET/HWB=各10 kΩプルアップ、16 MHz水晶＋33 pF×2

## プログラミング

J2にAVR ICSP 2×3を設けた。ATmega32U4-AU単体は、購入時にArduino
ブートローダーが書き込まれているとは限らない。初回はICSPでブートローダーと
ファームウェアを書き込む前提。

## JLCPCB入稿

ATmega32U4_27Button_JLCPCB_BOM.csv と ATmega32U4_27Button_JLCPCB_CPL.csv、
Gerber/ドリルZIPを使用する。CPLはSMD部品のみ。DTS-24NとICSPヘッダはTHTで、
JLCの波はんだ実装を使う場合は、C483776の現行パッケージと工程を別途選択する。

## 発注前に残る確認

1. DTS-24N本体と12 mmキャップの型番・高さ・押し方向がC483776の部品と一致すること。
2. J1のJLC/EasyEDAフットプリントが、KiCad標準のHRO TYPE-C-31-M-12と一致すること。
3. R/C部品のLCSC番号は候補値であり、JLCの現行Basic部品・定格・サイズを注文画面で再確認すること。
4. ATmega32U4に必要なArduino系ブートローダーを書き込む手段を準備すること。
"""
    (ROOT / f"{OUT}_README.md").write_text(text, encoding="utf-8")


def main():
    d = build_pcb()
    (ROOT / f"{OUT}.kicad_pcb").write_text("\n".join(d.lines) + "\n", encoding="utf-8")
    (ROOT / f"{OUT}.sch").write_text(build_legacy_schematic(), encoding="utf-8")
    (ROOT / f"{OUT}.kicad_pro").write_text("{}\n", encoding="utf-8")
    write_csvs(d)
    write_preview()
    write_readme()
    print(f"Wrote {OUT} design to {ROOT}")


if __name__ == "__main__":
    main()
