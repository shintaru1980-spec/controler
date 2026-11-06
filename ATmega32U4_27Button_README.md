# ATmega32U4 USB-C 27ボタン基板（統合版）

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
