# クラウドCodex引継ぎ資料

作成日: 2026-11-06
作業フォルダ: 20261106/ProMicro_27Button_150x120_19mm
状態: 中断。現行PCBは未完成で、発注不可。

## 1. このプロジェクトの経緯

当初はREVIVE USB MICROのADRVBRBを別基板として取り付ける案だったが、ユーザーの決定により、現在はATmega32U4を基板上に直接実装する統合設計へ変更された。

旧ADRVBRB案の資料とファイルは参考用に残っているが、現行の最終要求はADRVBRBを使わないATmega32U4版である。

## 2. 確定している設計条件

- 27ボタン
- DTS-24Nタクトスイッチ
- 5段配置
- 1段目3個、2から5段目は各6個
- 1段目は左合わせ
- ボタンピッチは横19 mm、縦19 mm
- 基板外形は150 mm × 120 mm以内
- 2層基板
- ATmega32U4-AU、5 V、16 MHz
- USB Type-C
- USBコネクタは上面視で右側、右上からケーブルを出す
- JLCPCB実装を利用する
- ダイオードはJLCPCBで実装する方向
- USB-CとMCUも実装候補だが、部品の実装可否とフットプリントを注文前に確認する
- DTS-24N用キャップを使う想定

## 3. DTS-24Nの機械・電気条件

DTS-2シリーズ仕様書を正とする。

- 本体は約12 mm角
- 4本脚
- 取付穴4個
- 穴中心間隔は横12.5 mm、縦5.0 mm
- 4本脚の内部接続は、1番と2番が同一接点、3番と4番が同一接点
- この内部接続を利用し、同一接点側の2端子は同じ行または同じダイオード側ネットにする
- 穴径、パッド径、メッキ、クリアランスは仕様書とJLCPCB能力を照合して決める

DTS-24N用キャップについて、キャップの型番・外形・取付高さ・押下ストローク・隣接19 mmピッチでの干渉は未確定。注文前に確認が必要。

## 4. マトリクス仮割り当て

試作版での仮割り当て。最終版ではATmega32U4公式データシートとファームウェアに照合する。

行:

- ROW1 = PF0、U1 pin36
- ROW2 = PF1、U1 pin37
- ROW3 = PF4、U1 pin38
- ROW4 = PF5、U1 pin39
- ROW5 = PF6、U1 pin40

列:

- COL1 = PB7、U1 pin12
- COL2 = PD0、U1 pin18
- COL3 = PD1、U1 pin19
- COL4 = PD2、U1 pin20
- COL5 = PD3、U1 pin21
- COL6 = PD5、U1 pin22

スイッチ接続の仮方針:

- DTS-24N pin1とpin2を行ネット
- DTS-24N pin3とpin4をダイオードのアノード側ネット
- ダイオードpad2をスイッチ側アノード
- ダイオードpad1を列ネット側カソード

この向きは仮設計であり、ファームウェアのスキャン方向と合わせて最終確認する。

## 5. ATmega32U4の確認対象

現行試作で使用した主な候補部品:

- U1: ATmega32U4-AU、QFP-44、JLC候補 C44854
- J1: TYPE-C-31-M-12系、JLC候補 C165948
- X1: 16 MHz 2端子水晶、候補 C122519
- R1、R2: USB CC用5.1 kΩ
- R3、R4: RESET/HWB用10 kΩ
- C1、C2、C4: 100 nF
- C3、C7: 1 uF
- C5、C6: 33 pF
- J2: AVR ICSP 2×3
- D1からD27: 1N4148WS、SOD-323、JLC候補 C493187

必ず再確認するピン:

- USB D− = U1 pin3
- USB D+ = U1 pin4
- RESET = U1 pin13
- XTAL2 = U1 pin16
- XTAL1 = U1 pin17
- UVCC = U1 pin2
- VBUS = U1 pin7
- UCAP = U1 pin6
- AVCC = U1 pin24、pin44
- VCC = U1 pin14、pin34
- GND = U1 pin5、pin15、pin23、pin35、pin43
- HWB/PE2 = U1 pin33
- AREF = U1 pin42
- ICSP MISO = PB3 pin11
- ICSP MOSI = PB2 pin10
- ICSP SCK = PB1 pin9

USB Type-CのCC抵抗、VBUS、シールド、D+、D−、USBコネクタの上下向きは、部品データと実物図で確認すること。

## 6. フォルダ内の現行ファイル

旧試作:

- generate_promicro_design.py
- ProMicro_27Button.kicad_pcb
- ProMicro_27Button.sch
- ProMicro_27Button.kicad_pro
- BOM.csv
- CPL.csv
- JLCPCB_BOM.csv
- JLCPCB_CPL.csv
- wiring_map.csv
- placement_preview.svg
- README.md
- drc_preliminary.rpt
- DESIGN_UPDATE_20261106.md

現行ATmega32U4統合版:

- generate_atmega32u4_design.py
- ATmega32U4_27Button.kicad_pcb
- ATmega32U4_27Button.sch
- ATmega32U4_27Button.kicad_pro
- ATmega32U4_27Button_BOM.csv
- ATmega32U4_27Button_JLCPCB_BOM.csv
- ATmega32U4_27Button_JLCPCB_CPL.csv
- ATmega32U4_27Button_placement.csv
- ATmega32U4_27Button_wiring_map.csv
- ATmega32U4_27Button_placement_preview.svg
- ATmega32U4_27Button_README.md

DRC履歴:

- drc_integrated_first.rpt
- drc_integrated_second.rpt
- drc_integrated_third.rpt
- drc_integrated_fourth.rpt
- drc_integrated_fifth.rpt

## 7. 現行試作の検証状態

最後に生成した現行統合版は、DRCレポート drc_integrated_fifth.rpt の状態で止まっている。

- 違反総数: 484
- 未接続: 15
- シルクと銅箔: 199
- ソルダーマスクブリッジ: 69
- ショート: 37
- クリアランス: 34
- フットプリント不一致: 32
- 文字高さ: 23
- ドリル範囲: 21
- トラック未接続端: 13
- フットプリント問題: 12
- シルク重なり: 12
- 穴クリアランス: 12
- 基板外形と銅のクリアランス: 4
- 配線交差: 4
- サーマル問題: 4
- ビア未接続端: 3
- トラック幅: 2
- 穴の同位置: 2
- 穴同士の距離: 1

結論: 現行ファイルは設計の叩き台であり、JLCPCBへの発注には使用しない。

## 8. 検証に使う環境

- KiCad CLI: C:\Program Files\KiCad\10.0\bin\kicad-cli.exe
- Python: C:\Users\kr0653\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
- USB標準フットプリント: C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_USB.pretty\USB_C_Receptacle_HRO_TYPE-C-31-M-12.kicad_mod

DRC実行例:

C:\Program Files\KiCad\10.0\bin\kicad-cli.exe pcb drc --severity-all --refill-zones --save-board --output .\drc_final.rpt .\ATmega32U4_27Button.kicad_pcb

## 9. 最終成果物の受け入れ条件

- 回路図とPCBのネットが一致
- DRC未接続0
- ショート0
- 配線交差0
- フットプリント不一致0
- 穴・パッド・基板外形のクリアランス違反0
- 27個のDTS-24Nが機械的に取り付け可能
- DTS-24Nの内部接続が正しい
- ダイオード27個の向きとネットが正しい
- ATmega32U4の電源、USB、クロック、RESET、HWB、ICSPが正しい
- USB Type-Cが右側向きで、ケーブルが右上から出せる
- 基板外形が150 mm × 120 mm以内
- JLCPCB実装対象の部品番号、向き、座標、面、BOMが一致
- Gerberとドリルデータを生成し、内容を検査
- 注文前に未確認事項を一覧で報告

## 10. 参照URL

- DTS-24N商品ページ: https://www.sengoku.co.jp/mod/sgk_cart/detail.php?code=8DK4-U6J5
- DTS-2シリーズ仕様書: https://tokiwa-image.sakura.ne.jp/html/upload/pdf/product/0000032007DTS-2_Spec_02.pdf
- ADRVBRB商品ページ: https://bit-trade-one.co.jp/adrvbrb/
- ADRVBRB回路図: https://github.com/bit-trade-one/ADRVMICR2-REVIVE-USB-Micro-Rev2/blob/master/Schematics/ADRVBRB/ADRVBRB_V1_sch.pdf
- ADRVBRB基板図: https://github.com/bit-trade-one/ADRVMICR2-REVIVE-USB-Micro-Rev2/blob/master/Dimensions/ADRVBRB/ADRVBRB_V1_brd.pdf
- REVIVE USB MICROサポート: https://bit-trade-one.github.io/ADRVMICR2-REVIVE-USB-Micro-Rev2/
- マトリクス設定: https://bit-trade-one.github.io/ADRVMIC-REVIVE-USB-Micro/Matrix.html
- JLCPCB: https://jlcpcb.com/jp
- JLC ATmega32U4-AU C44854: https://jlcpcb.com/partdetail/MicrochipTech-ATMEGA32U4AU/C44854
- JLC USB Type-C C165948: https://jlcpcb.com/partdetail/C165948
- JLCPCB実装能力: https://jlcpcb.com/capabilities/pcb-assembly-capabilities
- Microchip公式ATmega32U4データシート: https://ww1.microchip.com/downloads/en/devicedoc/atmel-7766-8-bit-avr-atmega16u4-32u4_datasheet.pdf
- USB-C Pro Micro参考回路図: https://cdn.sparkfun.com/assets/4/4/f/2/a/Qwiic_Pro_Micro_V2_0_USB_C_Schematic.pdf

## 11. 中断地点

この資料の作成時点で、ローカル側のPCB設計作業は中断する。クラウドCodexはこの資料を読み、現行試作を完成品と見なさず、必要な再設計・配線・検証・入稿データ生成を行うこと。

