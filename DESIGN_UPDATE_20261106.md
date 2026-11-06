# 2026-11-06 設計変更メモ

## ユーザーからの変更

以前は基板外形を100×100mm、ボタンピッチを15.5mmとしていた。

今回、次のように変更された。

- 基板外形は150×120mmでもよい。
- ボタン中心間ピッチは19mmにする。

この変更により、狭い100×100mmへの押し込みをやめ、スイッチ周辺のはんだ付けスペースとPro Micro配置の自由度を増やす方向で検討する。

## 暫定レイアウト

150×120mmの基板を仮定し、原点を左上、座標単位をmmとする。

### ボタン中心

- X座標：15, 34, 53, 72, 91, 110
- Y座標：22, 41, 60, 79, 98
- X方向の隣接差：19mm
- Y方向の隣接差：19mm
- 6列の中心間スパン：95mm
- 5段の中心間スパン：76mm

1段目はX=15, 34, 53の3個だけにし、2〜5段目は6列すべて使う。

### ボタン番号

左から右、上から下に連番する。

| 番号 | X | Y | 行 | 列 |
|---:|---:|---:|---|---|
| SW01 | 15 | 22 | ROW1 | COL1 |
| SW02 | 34 | 22 | ROW1 | COL2 |
| SW03 | 53 | 22 | ROW1 | COL3 |
| SW04 | 15 | 41 | ROW2 | COL1 |
| SW05 | 34 | 41 | ROW2 | COL2 |
| SW06 | 53 | 41 | ROW2 | COL3 |
| SW07 | 72 | 41 | ROW2 | COL4 |
| SW08 | 91 | 41 | ROW2 | COL5 |
| SW09 | 110 | 41 | ROW2 | COL6 |
| SW10 | 15 | 60 | ROW3 | COL1 |
| SW11 | 34 | 60 | ROW3 | COL2 |
| SW12 | 53 | 60 | ROW3 | COL3 |
| SW13 | 72 | 60 | ROW3 | COL4 |
| SW14 | 91 | 60 | ROW3 | COL5 |
| SW15 | 110 | 60 | ROW3 | COL6 |
| SW16 | 15 | 79 | ROW4 | COL1 |
| SW17 | 34 | 79 | ROW4 | COL2 |
| SW18 | 53 | 79 | ROW4 | COL3 |
| SW19 | 72 | 79 | ROW4 | COL4 |
| SW20 | 91 | 79 | ROW4 | COL5 |
| SW21 | 110 | 79 | ROW4 | COL6 |
| SW22 | 15 | 98 | ROW5 | COL1 |
| SW23 | 34 | 98 | ROW5 | COL2 |
| SW24 | 53 | 98 | ROW5 | COL3 |
| SW25 | 72 | 98 | ROW5 | COL4 |
| SW26 | 91 | 98 | ROW5 | COL5 |
| SW27 | 110 | 98 | ROW5 | COL6 |

### 余白の意味

- 左端のボタン穴中心はX=15mm。
- 右端のボタン穴中心はX=110mm。
- 右端ボタンのDTS-24N穴はおおよそX=116.25mmまで広がる。
- 右端ボタンのダイオード中心はX=120mmになる暫定配置。
- 基板右端150mmまで約30mmの領域があり、Pro MicroやUSB-Cの置き場所に使える。
- 上端から1段目中心まで22mm、5段目中心から下端まで22mm。

## 重要：これはまだ発注版ではない

今回のファイルは「150×120mm・19mmピッチに変更した暫定配置と配線のたたき台」である。

次の未解決事項がある。

1. 使用するPro Micro USB-Cモジュールの正式な穴位置・外形・USB-C突出量が未確定。
2. v2の配線生成ロジックを新しいボタン位置へ移植しただけで、配線経路は最適化途中。
3. preliminary DRCでは未配線0だが、トラック交差2件とシルク・文字違反が残っている。
4. DRCは159件の違反を検出している。発注してはいけない。
5. 最終的には実部品図面・現物測定値をもとにPro Micro位置を決める。

## 暫定Pro Micro位置

現在の生成スクリプトは、v2と同じく一般的なPro Micro互換寸法を仮定している。

- 仮定外形：17.78×33.02mm。
- 仮定穴パターン：24ピン、2.54mmピッチ。
- ホスト側穴径：1.1mm。
- USB-Cを右向きにするため、フットプリントを+90度回転。
- 暫定的に基板右側へ置く。

この位置は、ユーザーの実モジュール寸法が確認できるまで最終確定しない。

## 電気接続はv2を暫定継承

```text
ROW1 = D2
ROW2 = D3
ROW3 = D4
ROW4 = D5
ROW5 = D6

COL1 = A2
COL2 = A1
COL3 = A0
COL4 = D15
COL5 = D14
COL6 = D16
```

各ボタンは次の順。

```text
ROW -> DTS-24N pad 1/2（内部共通）
    -> DTS-24N pad 3/4（内部共通）
    -> diode pad 2 = A
    -> diode pad 1 = K
    -> COL
```

DTS-24Nの端子番号・内部接続は、`source_materials\DTS-2_Spec_02.pdf`を正とする。

## 生成ファイル

- `ProMicro_27Button.kicad_pcb`
- `ProMicro_27Button.sch`
- `generate_promicro_design.py`
- `wiring_map.csv`
- `BOM.csv`
- `JLCPCB_BOM.csv`
- `CPL.csv`
- `JLCPCB_CPL.csv`
- `placement_preview.svg`
- `README.md`
- `drc_preliminary.rpt`

## 再生成

このフォルダで以下を実行すると、現在の暫定パラメータからファイルを再生成できる。

```powershell
& 'C:\Users\kr0653\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\generate_promicro_design.py
```

再生成後は、必ずKiCad DRCを実行する。

```powershell
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' pcb drc --exit-code-violations -o .\drc_preliminary.rpt .\ProMicro_27Button.kicad_pcb
```

