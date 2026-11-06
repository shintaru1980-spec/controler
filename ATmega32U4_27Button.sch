EESchema Schematic File Version 4
LIBS:power
LIBS:device
LIBS:Connector_Generic
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
Sheet 1 1
Title "ATmega32U4 USB-C 27-button matrix controller"
Comment1 "Integrated MCU design for JLCPCB SMT assembly"
Comment2 "150 x 120 mm / 19 mm pitch / 2-layer"
Comment3 "PCB netlist and routing are authoritative"
Comment4 "2026-11-06"
$EndDescr
Text Notes 800 700 0    120  ~ 24
ATmega32U4-AU (JLC C44854) + USB-C TYPE-C-31-M-12 (JLC C165948)
Text Notes 800 950 0    80   ~ 16
Power: USB VBUS -> +5V; CC1/CC2 each have 5.1k pull-down to GND
Text Notes 800 1150 0    80   ~ 16
Clock: 16MHz crystal X1, 33pF each side; UCAP=1uF; RESET/HWB=10k pull-up
Text Notes 800 1350 0    80   ~ 16
ICSP J2: 1=MISO 2=+5V 3=SCK 4=MOSI 5=RESET 6=GND
Text Notes 800 1550 0    80   ~ 16
Matrix rows: PF0/PF1/PF4/PF5/PF6 = ROW1..ROW5
Text Notes 800 1750 0    80   ~ 16
Matrix columns: PB7/PD0/PD1/PD2/PD3/PD5 = COL1..COL6
Text Notes 800 2050 0    90   ~ 18
DTS-24N internal contact: pins 1-2 are one side; pins 3-4 are the other.
Text Notes 800 2250 0    90   ~ 18
Each key uses one 1N4148WS SOD-323: switch side -> diode anode, cathode -> column.
Text Notes 800 2550 0    80   ~ 16
27 keys: row1 has 3 keys; rows2-5 have 6 keys each.
Text Notes 800 2850 0    75   ~ 15
Do not order until DTS-24N cap and the JLC USB-C footprint are checked against physical parts.
$EndSCHEMATC
