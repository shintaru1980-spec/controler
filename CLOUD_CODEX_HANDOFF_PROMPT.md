# クラウドCodex引継ぎプロンプト

以下の設計作業を、添付フォルダ内の資料と既存ファイルを確認したうえで引き継いでください。

## 最終目的

JLCPCBで製造・実装できる、27ボタンUSBコントローラーのKiCadプロジェクトを完成させる。

基板上にATmega32U4を直接実装し、USB Type-Cコネクタ、マトリクス用ダイオード、27個のDTS-24N用スイッチ穴と銅配線を設ける。ダイオード、ATmega32U4、USB Type-Cなど、JLCPCBで実装可能な部品はJLCPCB実装を想定する。スイッチ本体は、正確な部品適合が確認できる場合のみ実装候補とし、未確認なら手はんだまたは別途実装とする。

## 重要な前提

現在のフォルダには試作中の統合版がありますが、完成品ではありません。現行のATmega32U4_27Button.kicad_pcbは、DRCで484件の違反、未接続15件が残っているため、発注可能な完成データとして扱わないでください。必要なら回路図・フットプリント・配線を再構成してください。

既存ファイルを再利用する場合も、資料とデータシートに照合し、ネット名、ピン番号、フットプリント、極性、実装面、寸法を検証してください。

## ユーザーが決定した仕様

- 用途: 27ボタンのUSBコントローラー
- MCU: ATmega32U4-AU、5 V、16 MHz
- USB: USB Type-C
- USBコネクタの向き: 上面視で右側、ケーブル出口は右上
- 基板: 2層、外形150 mm × 120 mm以内を基本案とする
- ボタンピッチ: 横19 mm、縦19 mm
- 配置: 上面視で5段
  - 1段目: 左から3個、左合わせ
  - 2段目: 左から6個
  - 3段目: 左から6個
  - 4段目: 左から6個
  - 5段目: 左から6個
- DTS-24Nの押下部に取り付けキャップを使う想定。キャップ適合、干渉、高さ、向きは必ず確認する
- 上段3個は左合わせ
- 基板内でスイッチ、ダイオード、MCUを接続し、外付け配線を最小化する
- JLCPCBのSMT実装を使用する計画

## スイッチ仕様

DTS-2シリーズ仕様書を正とする。

- 部品: DTS-24N
- 本体外形: 約12 mm角
- 取付穴: 4穴、仕上がり穴径は仕様書に従う
- 穴中心間隔: 横12.5 mm、縦5.0 mm
- 内部接続: 4本脚のうち、1番と2番が同一接点、3番と4番が同一接点
- 回路上は、同一接点側の2端子を同じネットへ接続する
- 穴径やパッド径は、仕様書の公差、JLCPCBの製造能力、手はんだ・実装方法を考慮して確定する

4本脚の内部接続を推測で変更しないこと。DTS-24N用キャップの機械的適合が確認できない場合は、未確定事項として報告すること。

## マトリクスの基本方針

27個のスイッチを5行6列のマトリクスに配置する。ただし1段目は3個のみ。

- SW1からSW27まで、配置順を図面・回路図・BOM・配線表で一致させる
- スイッチごとに行ネット、ダイオード、列ネットを一意に割り当てる
- ダイオードの向きと行列の読み取り方向を回路図に明記する
- ゴースト対策のため、各スイッチに1個のダイオードを配置する
- 共通化できる配線は、ATmega32U4の実際の回路・データシート・ファームウェアの前提を確認したうえでのみ行う
- 根拠のない端子共通化、端子省略、未接続のままのパッドを残さない

現在の試作で使っている仮割り当ては次のとおり。必ずデータシートと実際の回路図で再確認すること。

- ROW1 = PF0、U1 pin36
- ROW2 = PF1、U1 pin37
- ROW3 = PF4、U1 pin38
- ROW4 = PF5、U1 pin39
- ROW5 = PF6、U1 pin40
- COL1 = PB7、U1 pin12
- COL2 = PD0、U1 pin18
- COL3 = PD1、U1 pin19
- COL4 = PD2、U1 pin20
- COL5 = PD3、U1 pin21
- COL6 = PD5、U1 pin22

## ATmega32U4とUSBの確認事項

ATmega32U4-AUの電源、USB、クロック、リセット、HWB、デカップリング、ICSPを、Microchip公式データシートに従って設計する。

確認対象:

- VCC、AVCC、UVCCの接続
- GND全ピンの接続
- UCAPのコンデンサ
- AREF
- RESET
- HWB
- XTAL1、XTAL2と16 MHz水晶
- USB D+、D−
- USB Type-CのCC1、CC2抵抗
- USB VBUS、GND、シールド
- ICSP端子
- USBコネクタの向きとケーブル干渉

USB-Cコネクタは、JLCPCB/EasyEDAで公開されている実部品のフットプリント・ピン配置と、KiCad標準フットプリントが一致するか照合する。部品番号だけで一致と判断しない。

候補部品は以下だが、在庫・実装可否・フットプリントを注文前に再確認する。

- ATmega32U4-AU: JLC候補 C44854
- USB Type-C: JLC候補 C165948、TYPE-C-31-M-12系
- ダイオード: 1N4148WS、SOD-323、JLC候補 C493187
- 水晶: 16 MHz 2端子品の候補を、負荷容量・寸法・実装可否と合わせて確定する

## 設計・検証の必須成果物

次の成果物を、最終版と試作版が混ざらない名前で作成する。

1. KiCad回路図
2. KiCad PCB
3. 27個のSWとダイオードの対応表
4. MCUピン割り当て表
5. 実装部品BOM
6. JLCPCB用BOM
7. JLCPCB用CPL/Posファイル
8. 基板外形・穴位置・部品高さ・USB方向の配置図
9. Gerber一式
10. ドリルデータ
11. DRCレポート
12. 組立・手はんだ用の接続説明
13. 未確認事項と注文前チェックリスト

## 合格条件

発注前の最終版について、少なくとも次を満たすこと。

- DRCで未接続0
- ショート0
- 配線交差0
- パッド間クリアランス違反0
- 穴同士、穴と銅、穴と基板外形の違反0
- フットプリント不一致0
- シルクの銅箔・パッド・基板外形への重大な重なり0
- すべての電源ピン、USBピン、クロックピン、リセット、HWB、ICSPが意図どおり接続済み
- 27個すべてのスイッチが行・ダイオード・列に接続済み
- DTS-24Nの4穴が仕様書と一致
- USB Type-Cが上面視で右側を向き、ケーブルが右上から出せる
- 基板外形が150 mm × 120 mm以内
- 2層配線として製造可能な線幅・クリアランス・ビア・穴径
- JLCPCBのSMT実装面、部品向き、極性、CPL座標が一致

## 最初に読むファイル

同じフォルダにある次の資料を最初に確認する。

- CLOUD_CODEX_HANDOFF_STATUS.md
- ATmega32U4_27Button_README.md
- ATmega32U4_27Button_wiring_map.csv
- ATmega32U4_27Button_placement.csv
- ATmega32U4_27Button_BOM.csv
- ATmega32U4_27Button_JLCPCB_BOM.csv
- ATmega32U4_27Button_JLCPCB_CPL.csv
- generate_atmega32u4_design.py
- drc_integrated_fifth.rpt

## 公式資料

- DTS-24N商品ページ: https://www.sengoku.co.jp/mod/sgk_cart/detail.php?code=8DK4-U6J5
- DTS-2シリーズ仕様書: https://tokiwa-image.sakura.ne.jp/html/upload/pdf/product/0000032007DTS-2_Spec_02.pdf
- ADRVBRB商品ページ: https://bit-trade-one.co.jp/adrvbrb/
- ADRVBRB回路図: https://github.com/bit-trade-one/ADRVMICR2-REVIVE-USB-Micro-Rev2/blob/master/Schematics/ADRVBRB/ADRVBRB_V1_sch.pdf
- ADRVBRB基板図: https://github.com/bit-trade-one/ADRVMICR2-REVIVE-USB-Micro-Rev2/blob/master/Dimensions/ADRVBRB/ADRVBRB_V1_brd.pdf
- REVIVE USB MICROサポート: https://bit-trade-one.github.io/ADRVMICR2-REVIVE-USB-Micro-Rev2/
- マトリクス設定: https://bit-trade-one.github.io/ADRVMIC-REVIVE-USB-Micro/Matrix.html
- JLCPCB: https://jlcpcb.com/jp
- JLCPCB部品 ATmega32U4-AU C44854: https://jlcpcb.com/partdetail/MicrochipTech-ATMEGA32U4AU/C44854
- JLCPCB部品 USB Type-C C165948: https://jlcpcb.com/partdetail/C165948
- JLCPCB実装能力: https://jlcpcb.com/capabilities/pcb-assembly-capabilities
- Microchip公式ATmega32U4データシート: https://ww1.microchip.com/downloads/en/devicedoc/atmel-7766-8-bit-avr-atmega16u4-32u4_datasheet.pdf
- USB-C Pro Micro参考回路図: https://cdn.sparkfun.com/assets/4/4/f/2/a/Qwiic_Pro_Micro_V2_0_USB_C_Schematic.pdf

作業完了時は、検証済みの最終ファイル名、DRC件数、Gerber/ドリルZIPの場所、未解決事項を日本語で報告してください。未確認の寸法や部品適合を、推測で確定しないでください。

