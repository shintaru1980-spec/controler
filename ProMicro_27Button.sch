EESchema Schematic File Version 4
LIBS:ProMicro_27Button-cache
EELAYER 29 0
EELAYER END
$Descr A3 16535 11693
Sheet 1 1
Title "Pro Micro 27-button matrix controller"
Date "2026-11-05"
Rev "1.0-DRAFT"
Comp "Source-verified Pro Micro 5V/16MHz reference design"
Comment1 "Rows: D2,D3,D4,D5,D6; columns: A2,A1,A0,D15,D14,D16"
Comment2 "DTS-24N pins 1-2 = row; pins 3-4 = diode anode"
Comment3 "D_SOD-323 pad 2 = anode, pad 1 = cathode; cathode -> column"
Comment4 "Amazon listing has no mechanical drawing; confirm actual clone before ordering"
$EndDescr
Text Notes 700 600 0    120  ~ 24
PROMICRO 27-BUTTON MATRIX
Text Notes 700 820 0    60   ~ 12
Each button is ROW -> DTS-24N -> diode anode -> diode cathode -> COL.
Text Notes 700 980 0    60   ~ 12
All 27 diodes are SMD 1N4148WS / SOD-323 and are intended for JLCPCB SMT assembly.
Text Notes 700 1140 0    60   ~ 12
The first row is left-aligned and has three buttons; rows 2-5 have six buttons.
Text Notes 10800 650 0    65   ~ 13
PRO MICRO PIN MAP
Text Notes 10800 820 0    55   ~ 11
ROW1 = D2
Text Notes 10800 940 0    55   ~ 11
ROW2 = D3
Text Notes 10800 1060 0    55   ~ 11
ROW3 = D4
Text Notes 10800 1180 0    55   ~ 11
ROW4 = D5
Text Notes 10800 1300 0    55   ~ 11
ROW5 = D6
Text Notes 10800 1460 0    55   ~ 11
COL1 = A2
Text Notes 10800 1580 0    55   ~ 11
COL2 = A1
Text Notes 10800 1700 0    55   ~ 11
COL3 = A0
Text Notes 10800 1820 0    55   ~ 11
COL4 = D15
Text Notes 10800 1940 0    55   ~ 11
COL5 = D14
Text Notes 10800 2060 0    55   ~ 11
COL6 = D16
$Comp
L Switch:SW_Push SW01
U 1 1 10000001
P 3000 1800
F 0 "SW01" H 3000 2050 50  0000 C CNN
F 1 "DTS-24N" H 3000 1550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    3000 1800
	1    0    0    -1
$EndComp
$Comp
L Device:D D01
U 1 1 20000001
P 3350 1800
F 0 "D01" H 3350 2000 50  0000 C CNN
F 1 "1N4148WS" H 3350 1600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    3350 1800
	-1    0    0    1
$EndComp
Wire Wire Line
	2700 1800 2900 1800
Wire Wire Line
	3100 1800 3250 1800
Wire Wire Line
	3450 1800 3700 1800
Text Label 2720 1800 2    50   ~ 0
ROW1
Text Label 3680 1800 0    50   ~ 0
COL1
$Comp
L Switch:SW_Push SW02
U 1 1 10000002
P 4200 1800
F 0 "SW02" H 4200 2050 50  0000 C CNN
F 1 "DTS-24N" H 4200 1550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    4200 1800
	1    0    0    -1
$EndComp
$Comp
L Device:D D02
U 1 1 20000002
P 4550 1800
F 0 "D02" H 4550 2000 50  0000 C CNN
F 1 "1N4148WS" H 4550 1600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    4550 1800
	-1    0    0    1
$EndComp
Wire Wire Line
	3900 1800 4100 1800
Wire Wire Line
	4300 1800 4450 1800
Wire Wire Line
	4650 1800 4900 1800
Text Label 3920 1800 2    50   ~ 0
ROW1
Text Label 4880 1800 0    50   ~ 0
COL2
$Comp
L Switch:SW_Push SW03
U 1 1 10000003
P 5400 1800
F 0 "SW03" H 5400 2050 50  0000 C CNN
F 1 "DTS-24N" H 5400 1550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    5400 1800
	1    0    0    -1
$EndComp
$Comp
L Device:D D03
U 1 1 20000003
P 5750 1800
F 0 "D03" H 5750 2000 50  0000 C CNN
F 1 "1N4148WS" H 5750 1600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    5750 1800
	-1    0    0    1
$EndComp
Wire Wire Line
	5100 1800 5300 1800
Wire Wire Line
	5500 1800 5650 1800
Wire Wire Line
	5850 1800 6100 1800
Text Label 5120 1800 2    50   ~ 0
ROW1
Text Label 6080 1800 0    50   ~ 0
COL3
$Comp
L Switch:SW_Push SW04
U 1 1 10000004
P 1800 2800
F 0 "SW04" H 1800 3050 50  0000 C CNN
F 1 "DTS-24N" H 1800 2550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    1800 2800
	1    0    0    -1
$EndComp
$Comp
L Device:D D04
U 1 1 20000004
P 2150 2800
F 0 "D04" H 2150 3000 50  0000 C CNN
F 1 "1N4148WS" H 2150 2600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    2150 2800
	-1    0    0    1
$EndComp
Wire Wire Line
	1500 2800 1700 2800
Wire Wire Line
	1900 2800 2050 2800
Wire Wire Line
	2250 2800 2500 2800
Text Label 1520 2800 2    50   ~ 0
ROW2
Text Label 2480 2800 0    50   ~ 0
COL1
$Comp
L Switch:SW_Push SW05
U 1 1 10000005
P 3000 2800
F 0 "SW05" H 3000 3050 50  0000 C CNN
F 1 "DTS-24N" H 3000 2550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    3000 2800
	1    0    0    -1
$EndComp
$Comp
L Device:D D05
U 1 1 20000005
P 3350 2800
F 0 "D05" H 3350 3000 50  0000 C CNN
F 1 "1N4148WS" H 3350 2600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    3350 2800
	-1    0    0    1
$EndComp
Wire Wire Line
	2700 2800 2900 2800
Wire Wire Line
	3100 2800 3250 2800
Wire Wire Line
	3450 2800 3700 2800
Text Label 2720 2800 2    50   ~ 0
ROW2
Text Label 3680 2800 0    50   ~ 0
COL2
$Comp
L Switch:SW_Push SW06
U 1 1 10000006
P 4200 2800
F 0 "SW06" H 4200 3050 50  0000 C CNN
F 1 "DTS-24N" H 4200 2550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    4200 2800
	1    0    0    -1
$EndComp
$Comp
L Device:D D06
U 1 1 20000006
P 4550 2800
F 0 "D06" H 4550 3000 50  0000 C CNN
F 1 "1N4148WS" H 4550 2600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    4550 2800
	-1    0    0    1
$EndComp
Wire Wire Line
	3900 2800 4100 2800
Wire Wire Line
	4300 2800 4450 2800
Wire Wire Line
	4650 2800 4900 2800
Text Label 3920 2800 2    50   ~ 0
ROW2
Text Label 4880 2800 0    50   ~ 0
COL3
$Comp
L Switch:SW_Push SW07
U 1 1 10000007
P 5400 2800
F 0 "SW07" H 5400 3050 50  0000 C CNN
F 1 "DTS-24N" H 5400 2550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    5400 2800
	1    0    0    -1
$EndComp
$Comp
L Device:D D07
U 1 1 20000007
P 5750 2800
F 0 "D07" H 5750 3000 50  0000 C CNN
F 1 "1N4148WS" H 5750 2600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    5750 2800
	-1    0    0    1
$EndComp
Wire Wire Line
	5100 2800 5300 2800
Wire Wire Line
	5500 2800 5650 2800
Wire Wire Line
	5850 2800 6100 2800
Text Label 5120 2800 2    50   ~ 0
ROW2
Text Label 6080 2800 0    50   ~ 0
COL4
$Comp
L Switch:SW_Push SW08
U 1 1 10000008
P 6600 2800
F 0 "SW08" H 6600 3050 50  0000 C CNN
F 1 "DTS-24N" H 6600 2550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    6600 2800
	1    0    0    -1
$EndComp
$Comp
L Device:D D08
U 1 1 20000008
P 6950 2800
F 0 "D08" H 6950 3000 50  0000 C CNN
F 1 "1N4148WS" H 6950 2600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    6950 2800
	-1    0    0    1
$EndComp
Wire Wire Line
	6300 2800 6500 2800
Wire Wire Line
	6700 2800 6850 2800
Wire Wire Line
	7050 2800 7300 2800
Text Label 6320 2800 2    50   ~ 0
ROW2
Text Label 7280 2800 0    50   ~ 0
COL5
$Comp
L Switch:SW_Push SW09
U 1 1 10000009
P 7800 2800
F 0 "SW09" H 7800 3050 50  0000 C CNN
F 1 "DTS-24N" H 7800 2550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    7800 2800
	1    0    0    -1
$EndComp
$Comp
L Device:D D09
U 1 1 20000009
P 8150 2800
F 0 "D09" H 8150 3000 50  0000 C CNN
F 1 "1N4148WS" H 8150 2600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    8150 2800
	-1    0    0    1
$EndComp
Wire Wire Line
	7500 2800 7700 2800
Wire Wire Line
	7900 2800 8050 2800
Wire Wire Line
	8250 2800 8500 2800
Text Label 7520 2800 2    50   ~ 0
ROW2
Text Label 8480 2800 0    50   ~ 0
COL6
$Comp
L Switch:SW_Push SW10
U 1 1 1000000A
P 1800 3800
F 0 "SW10" H 1800 4050 50  0000 C CNN
F 1 "DTS-24N" H 1800 3550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    1800 3800
	1    0    0    -1
$EndComp
$Comp
L Device:D D10
U 1 1 2000000A
P 2150 3800
F 0 "D10" H 2150 4000 50  0000 C CNN
F 1 "1N4148WS" H 2150 3600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    2150 3800
	-1    0    0    1
$EndComp
Wire Wire Line
	1500 3800 1700 3800
Wire Wire Line
	1900 3800 2050 3800
Wire Wire Line
	2250 3800 2500 3800
Text Label 1520 3800 2    50   ~ 0
ROW3
Text Label 2480 3800 0    50   ~ 0
COL1
$Comp
L Switch:SW_Push SW11
U 1 1 1000000B
P 3000 3800
F 0 "SW11" H 3000 4050 50  0000 C CNN
F 1 "DTS-24N" H 3000 3550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    3000 3800
	1    0    0    -1
$EndComp
$Comp
L Device:D D11
U 1 1 2000000B
P 3350 3800
F 0 "D11" H 3350 4000 50  0000 C CNN
F 1 "1N4148WS" H 3350 3600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    3350 3800
	-1    0    0    1
$EndComp
Wire Wire Line
	2700 3800 2900 3800
Wire Wire Line
	3100 3800 3250 3800
Wire Wire Line
	3450 3800 3700 3800
Text Label 2720 3800 2    50   ~ 0
ROW3
Text Label 3680 3800 0    50   ~ 0
COL2
$Comp
L Switch:SW_Push SW12
U 1 1 1000000C
P 4200 3800
F 0 "SW12" H 4200 4050 50  0000 C CNN
F 1 "DTS-24N" H 4200 3550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    4200 3800
	1    0    0    -1
$EndComp
$Comp
L Device:D D12
U 1 1 2000000C
P 4550 3800
F 0 "D12" H 4550 4000 50  0000 C CNN
F 1 "1N4148WS" H 4550 3600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    4550 3800
	-1    0    0    1
$EndComp
Wire Wire Line
	3900 3800 4100 3800
Wire Wire Line
	4300 3800 4450 3800
Wire Wire Line
	4650 3800 4900 3800
Text Label 3920 3800 2    50   ~ 0
ROW3
Text Label 4880 3800 0    50   ~ 0
COL3
$Comp
L Switch:SW_Push SW13
U 1 1 1000000D
P 5400 3800
F 0 "SW13" H 5400 4050 50  0000 C CNN
F 1 "DTS-24N" H 5400 3550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    5400 3800
	1    0    0    -1
$EndComp
$Comp
L Device:D D13
U 1 1 2000000D
P 5750 3800
F 0 "D13" H 5750 4000 50  0000 C CNN
F 1 "1N4148WS" H 5750 3600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    5750 3800
	-1    0    0    1
$EndComp
Wire Wire Line
	5100 3800 5300 3800
Wire Wire Line
	5500 3800 5650 3800
Wire Wire Line
	5850 3800 6100 3800
Text Label 5120 3800 2    50   ~ 0
ROW3
Text Label 6080 3800 0    50   ~ 0
COL4
$Comp
L Switch:SW_Push SW14
U 1 1 1000000E
P 6600 3800
F 0 "SW14" H 6600 4050 50  0000 C CNN
F 1 "DTS-24N" H 6600 3550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    6600 3800
	1    0    0    -1
$EndComp
$Comp
L Device:D D14
U 1 1 2000000E
P 6950 3800
F 0 "D14" H 6950 4000 50  0000 C CNN
F 1 "1N4148WS" H 6950 3600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    6950 3800
	-1    0    0    1
$EndComp
Wire Wire Line
	6300 3800 6500 3800
Wire Wire Line
	6700 3800 6850 3800
Wire Wire Line
	7050 3800 7300 3800
Text Label 6320 3800 2    50   ~ 0
ROW3
Text Label 7280 3800 0    50   ~ 0
COL5
$Comp
L Switch:SW_Push SW15
U 1 1 1000000F
P 7800 3800
F 0 "SW15" H 7800 4050 50  0000 C CNN
F 1 "DTS-24N" H 7800 3550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    7800 3800
	1    0    0    -1
$EndComp
$Comp
L Device:D D15
U 1 1 2000000F
P 8150 3800
F 0 "D15" H 8150 4000 50  0000 C CNN
F 1 "1N4148WS" H 8150 3600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    8150 3800
	-1    0    0    1
$EndComp
Wire Wire Line
	7500 3800 7700 3800
Wire Wire Line
	7900 3800 8050 3800
Wire Wire Line
	8250 3800 8500 3800
Text Label 7520 3800 2    50   ~ 0
ROW3
Text Label 8480 3800 0    50   ~ 0
COL6
$Comp
L Switch:SW_Push SW16
U 1 1 10000010
P 1800 4800
F 0 "SW16" H 1800 5050 50  0000 C CNN
F 1 "DTS-24N" H 1800 4550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    1800 4800
	1    0    0    -1
$EndComp
$Comp
L Device:D D16
U 1 1 20000010
P 2150 4800
F 0 "D16" H 2150 5000 50  0000 C CNN
F 1 "1N4148WS" H 2150 4600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    2150 4800
	-1    0    0    1
$EndComp
Wire Wire Line
	1500 4800 1700 4800
Wire Wire Line
	1900 4800 2050 4800
Wire Wire Line
	2250 4800 2500 4800
Text Label 1520 4800 2    50   ~ 0
ROW4
Text Label 2480 4800 0    50   ~ 0
COL1
$Comp
L Switch:SW_Push SW17
U 1 1 10000011
P 3000 4800
F 0 "SW17" H 3000 5050 50  0000 C CNN
F 1 "DTS-24N" H 3000 4550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    3000 4800
	1    0    0    -1
$EndComp
$Comp
L Device:D D17
U 1 1 20000011
P 3350 4800
F 0 "D17" H 3350 5000 50  0000 C CNN
F 1 "1N4148WS" H 3350 4600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    3350 4800
	-1    0    0    1
$EndComp
Wire Wire Line
	2700 4800 2900 4800
Wire Wire Line
	3100 4800 3250 4800
Wire Wire Line
	3450 4800 3700 4800
Text Label 2720 4800 2    50   ~ 0
ROW4
Text Label 3680 4800 0    50   ~ 0
COL2
$Comp
L Switch:SW_Push SW18
U 1 1 10000012
P 4200 4800
F 0 "SW18" H 4200 5050 50  0000 C CNN
F 1 "DTS-24N" H 4200 4550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    4200 4800
	1    0    0    -1
$EndComp
$Comp
L Device:D D18
U 1 1 20000012
P 4550 4800
F 0 "D18" H 4550 5000 50  0000 C CNN
F 1 "1N4148WS" H 4550 4600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    4550 4800
	-1    0    0    1
$EndComp
Wire Wire Line
	3900 4800 4100 4800
Wire Wire Line
	4300 4800 4450 4800
Wire Wire Line
	4650 4800 4900 4800
Text Label 3920 4800 2    50   ~ 0
ROW4
Text Label 4880 4800 0    50   ~ 0
COL3
$Comp
L Switch:SW_Push SW19
U 1 1 10000013
P 5400 4800
F 0 "SW19" H 5400 5050 50  0000 C CNN
F 1 "DTS-24N" H 5400 4550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    5400 4800
	1    0    0    -1
$EndComp
$Comp
L Device:D D19
U 1 1 20000013
P 5750 4800
F 0 "D19" H 5750 5000 50  0000 C CNN
F 1 "1N4148WS" H 5750 4600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    5750 4800
	-1    0    0    1
$EndComp
Wire Wire Line
	5100 4800 5300 4800
Wire Wire Line
	5500 4800 5650 4800
Wire Wire Line
	5850 4800 6100 4800
Text Label 5120 4800 2    50   ~ 0
ROW4
Text Label 6080 4800 0    50   ~ 0
COL4
$Comp
L Switch:SW_Push SW20
U 1 1 10000014
P 6600 4800
F 0 "SW20" H 6600 5050 50  0000 C CNN
F 1 "DTS-24N" H 6600 4550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    6600 4800
	1    0    0    -1
$EndComp
$Comp
L Device:D D20
U 1 1 20000014
P 6950 4800
F 0 "D20" H 6950 5000 50  0000 C CNN
F 1 "1N4148WS" H 6950 4600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    6950 4800
	-1    0    0    1
$EndComp
Wire Wire Line
	6300 4800 6500 4800
Wire Wire Line
	6700 4800 6850 4800
Wire Wire Line
	7050 4800 7300 4800
Text Label 6320 4800 2    50   ~ 0
ROW4
Text Label 7280 4800 0    50   ~ 0
COL5
$Comp
L Switch:SW_Push SW21
U 1 1 10000015
P 7800 4800
F 0 "SW21" H 7800 5050 50  0000 C CNN
F 1 "DTS-24N" H 7800 4550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    7800 4800
	1    0    0    -1
$EndComp
$Comp
L Device:D D21
U 1 1 20000015
P 8150 4800
F 0 "D21" H 8150 5000 50  0000 C CNN
F 1 "1N4148WS" H 8150 4600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    8150 4800
	-1    0    0    1
$EndComp
Wire Wire Line
	7500 4800 7700 4800
Wire Wire Line
	7900 4800 8050 4800
Wire Wire Line
	8250 4800 8500 4800
Text Label 7520 4800 2    50   ~ 0
ROW4
Text Label 8480 4800 0    50   ~ 0
COL6
$Comp
L Switch:SW_Push SW22
U 1 1 10000016
P 1800 5800
F 0 "SW22" H 1800 6050 50  0000 C CNN
F 1 "DTS-24N" H 1800 5550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    1800 5800
	1    0    0    -1
$EndComp
$Comp
L Device:D D22
U 1 1 20000016
P 2150 5800
F 0 "D22" H 2150 6000 50  0000 C CNN
F 1 "1N4148WS" H 2150 5600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    2150 5800
	-1    0    0    1
$EndComp
Wire Wire Line
	1500 5800 1700 5800
Wire Wire Line
	1900 5800 2050 5800
Wire Wire Line
	2250 5800 2500 5800
Text Label 1520 5800 2    50   ~ 0
ROW5
Text Label 2480 5800 0    50   ~ 0
COL1
$Comp
L Switch:SW_Push SW23
U 1 1 10000017
P 3000 5800
F 0 "SW23" H 3000 6050 50  0000 C CNN
F 1 "DTS-24N" H 3000 5550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    3000 5800
	1    0    0    -1
$EndComp
$Comp
L Device:D D23
U 1 1 20000017
P 3350 5800
F 0 "D23" H 3350 6000 50  0000 C CNN
F 1 "1N4148WS" H 3350 5600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    3350 5800
	-1    0    0    1
$EndComp
Wire Wire Line
	2700 5800 2900 5800
Wire Wire Line
	3100 5800 3250 5800
Wire Wire Line
	3450 5800 3700 5800
Text Label 2720 5800 2    50   ~ 0
ROW5
Text Label 3680 5800 0    50   ~ 0
COL2
$Comp
L Switch:SW_Push SW24
U 1 1 10000018
P 4200 5800
F 0 "SW24" H 4200 6050 50  0000 C CNN
F 1 "DTS-24N" H 4200 5550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    4200 5800
	1    0    0    -1
$EndComp
$Comp
L Device:D D24
U 1 1 20000018
P 4550 5800
F 0 "D24" H 4550 6000 50  0000 C CNN
F 1 "1N4148WS" H 4550 5600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    4550 5800
	-1    0    0    1
$EndComp
Wire Wire Line
	3900 5800 4100 5800
Wire Wire Line
	4300 5800 4450 5800
Wire Wire Line
	4650 5800 4900 5800
Text Label 3920 5800 2    50   ~ 0
ROW5
Text Label 4880 5800 0    50   ~ 0
COL3
$Comp
L Switch:SW_Push SW25
U 1 1 10000019
P 5400 5800
F 0 "SW25" H 5400 6050 50  0000 C CNN
F 1 "DTS-24N" H 5400 5550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    5400 5800
	1    0    0    -1
$EndComp
$Comp
L Device:D D25
U 1 1 20000019
P 5750 5800
F 0 "D25" H 5750 6000 50  0000 C CNN
F 1 "1N4148WS" H 5750 5600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    5750 5800
	-1    0    0    1
$EndComp
Wire Wire Line
	5100 5800 5300 5800
Wire Wire Line
	5500 5800 5650 5800
Wire Wire Line
	5850 5800 6100 5800
Text Label 5120 5800 2    50   ~ 0
ROW5
Text Label 6080 5800 0    50   ~ 0
COL4
$Comp
L Switch:SW_Push SW26
U 1 1 1000001A
P 6600 5800
F 0 "SW26" H 6600 6050 50  0000 C CNN
F 1 "DTS-24N" H 6600 5550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    6600 5800
	1    0    0    -1
$EndComp
$Comp
L Device:D D26
U 1 1 2000001A
P 6950 5800
F 0 "D26" H 6950 6000 50  0000 C CNN
F 1 "1N4148WS" H 6950 5600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    6950 5800
	-1    0    0    1
$EndComp
Wire Wire Line
	6300 5800 6500 5800
Wire Wire Line
	6700 5800 6850 5800
Wire Wire Line
	7050 5800 7300 5800
Text Label 6320 5800 2    50   ~ 0
ROW5
Text Label 7280 5800 0    50   ~ 0
COL5
$Comp
L Switch:SW_Push SW27
U 1 1 1000001B
P 7800 5800
F 0 "SW27" H 7800 6050 50  0000 C CNN
F 1 "DTS-24N" H 7800 5550 50  0000 C CNN
F 2 "DTS-24N" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    7800 5800
	1    0    0    -1
$EndComp
$Comp
L Device:D D27
U 1 1 2000001B
P 8150 5800
F 0 "D27" H 8150 6000 50  0000 C CNN
F 1 "1N4148WS" H 8150 5600 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-323" H 0 0 50  0001 C CNN
F 3 "" H 0 0 50  0001 C CNN
	1    8150 5800
	-1    0    0    1
$EndComp
Wire Wire Line
	7500 5800 7700 5800
Wire Wire Line
	7900 5800 8050 5800
Wire Wire Line
	8250 5800 8500 5800
Text Label 7520 5800 2    50   ~ 0
ROW5
Text Label 8480 5800 0    50   ~ 0
COL6
Text Notes 700 7200 0    60   ~ 12
PCB mechanical reference: provisional 17.78 x 33.02 mm; host holes use 1.1 mm drill.
Text Notes 700 7400 0    60   ~ 12
DTS-24N hole pattern: four holes, 1.2 mm drill, 12.5 mm horizontal x 5.0 mm vertical.
Text Notes 700 7600 0    60   ~ 12
USB-C module is Amazon B0DMNBJHT7; confirm its 24-hole pattern and body before ordering.
$EndSCHEMATC
