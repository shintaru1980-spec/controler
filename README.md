# ProMicro_27Button

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
