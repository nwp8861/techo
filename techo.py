#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# techo  ---  Teto's echo
#
# usage: $ techo [-0~5] [-q] [-f text-file] [message ... ]
#
# example1: $ techo hello world
# example2: $ cat sample.txt | techo
# example3: $ techo -q
#
# copyright of the source code:
#   2024, nwp8861, released under the MIT No Attribution license (MIT-0)
#                              or the MIT license
#   MIT-0: https://opensource.org/license/MIT-0
#   MIT:   https://opensource.org/license/mit
# copyright of Teto:
#   PCL (applied mutatis mutandisapp)
#   https://kasaneteto.jp/guideline/ctu.html
#
# 補足:
#   PowerShellでパイプラインで日本語を送り込む場合は
#   コマンドラインであらかじめ以下のように実行する必要がある。
#   PS C:\ > $OutputEncoding = [Text.Encoding]::Default
#   PS C:\ > echo あいうえお | python techo.py
#

import signal
import sys
import sys
import re
import shutil
import os
import unicodedata

version = '31.0'

#---------------------------------------------
# usage
#---------------------------------------------
def usage(argv0, ver):
  print(f"""{argv0} --- TETO's echo Version {ver}

usage: {argv0} [-0~5|-q|-b|-d|-l|-r|-f text-file] [--] [message ... ]

  -0 ~ -5      ... change face (default: -0)
  -q           ... output no message (show face only)
  -b           ... color brightness change
  -d           ... reduce Teto's vertical width
  -l           ... position face to the left
  -r           ... position face to the right (default)
  -f text-file ... read message from text-file
  --           ... end of command line options
""", file=sys.stderr)
  exit()

#---------------------------------------------
# Ctrl+cが来たら画面設定をリセットして終了
#
def ctrlC(signal, frame):
  print ('\e[0m', end='')
  sys.exit(0)
signal.signal(signal.SIGINT, ctrlC)   # SIGINTにctrlC()を紐づける

#---------------------------------------------
# Windowsの端末の場合はエスケープシーケンスを有効にする
#
if os.name == 'nt':
  import ctypes
  import io
  ENABLE_PROCESSED_OUTPUT = 0x0001
  ENABLE_WRAP_AT_EOL_OUTPUT = 0x0002
  ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
  MODE = ENABLE_PROCESSED_OUTPUT + ENABLE_WRAP_AT_EOL_OUTPUT + ENABLE_VIRTUAL_TERMINAL_PROCESSING
 
  handle = ctypes.windll.kernel32.GetStdHandle(-11)
  ctypes.windll.kernel32.SetConsoleMode(handle, MODE)

  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
  sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

#---------------------------------------------
# 顔データ
img = [
  #----------おすまし
  [
  '...........111...........',
  '..........13.............',
  '..........1..............',
  '...........1.............',
  '..........11011216...11..',
  '.....16..1125731516.41113',
  '...1135..1051110115401155',
  '..11101014111101311511111',
  '..11010115237333111061611',
  '...0165151111115511041332',
  '...1012110111101511131011',
  '...1050110051500151500106',
  '...1101110405130011501055',
  '....101105340573345510101',
  '....110100013110001134041',
  '.....10147107731030150506',
  '.....141677777777315.011.',
  '......1057375377331..102.',
  '......1..6777777730..113.',
  '.......1..07013730....1..',
  '...........0777300....1..',
  '.006000000..000050.......',
  '.030470700000001104......',
  '.0407460407001100006000..',
  '000042004400001101760000.',
  '1150203330060000421076600',
  '0150003377706020120207060',
  '0350030737330605002020500',
  ],

  #----------にっこり
  [
  '...........111...........',
  '..........13.............',
  '..........1..............',
  '...........1.............',
  '..........11011216...11..',
  '.....16..1125731516.41113',
  '...1135.11051110115401155',
  '..11101014111101311511111',
  '..11010115237333111061611',
  '...0165151111115511041332',
  '...1012110111101511131011',
  '...1050110051520151500106',
  '...1101110305173011501055',
  '....101107730577305510101',
  '....110107073170770134041',
  '.....10160707707070150506',
  '.....141677777777315.011.',
  '......1057375377331..102.',
  '......1..6704407330..113.',
  '.......1..07017730....1..',
  '...........0777300....1..',
  '.006000000..000050.......',
  '.030470700000001104......',
  '.0407460407001100006000..',
  '000042004400001101760000.',
  '1150203330060000421076600',
  '0150003377706020120207060',
  '0350030737330605002020500',
  ],

  #----------きりっ+笑い？
  [
  '...........111...........',
  '..........13.............',
  '..........1..............',
  '...........1.............',
  '..........11011216...11..',
  '.....16..1125731516.41113',
  '...1135.11051110115401155',
  '..11101014111101311511111',
  '..11010115237333111061611',
  '...0165151111115511041332',
  '...1012110111101511131011',
  '...1050110051500151500106',
  '...1101110405134011501055',
  '....101107340543045510101',
  '....110100073170001134041',
  '.....10147107701030150506',
  '.....141677777777315.011.',
  '......1057375377331..102.',
  '......1..6704407730..113.',
  '.......1..07013730....1..',
  '...........0777300....1..',
  '.006000000..000050.......',
  '.030470700000001104......',
  '.0407460407001100006000..',
  '000042004400001101760000.',
  '1150203330060000421076600',
  '0150003377706020120207060',
  '0350030737330605002020500',
  ],

  #----------ぱっちり
  [
  '...........111...........',
  '..........13.............',
  '..........1..............',
  '...........1.............',
  '..........11011216...11..',
  '.....16..1125731516.41113',
  '...1135.11051110115401155',
  '..11101014111101311511111',
  '..11010115237333111061611',
  '...0165151111115511041332',
  '...1012110111101511131011',
  '...1050110051500151500106',
  '...1101110405130011501055',
  '....101105340573345510101',
  '....110100000110001134041',
  '.....10147017710130150506',
  '.....141670077700315.011.',
  '......1057375377331..102.',
  '......1..6777777730..113.',
  '.......1..07010730....1..',
  '...........0777300....1..',
  '.006000000..000050.......',
  '.030470700000001104......',
  '.0407460407001100006000..',
  '000042004400001101760000.',
  '1150203330060000421076600',
  '0150003377706020120207060',
  '0350030737330605002020500',
  ],

  #----------びっくり
  [
  '...........111...........',
  '..........13.............',
  '..........1..............',
  '...........1.............',
  '..........11011216...11..',
  '.....16..1125731516.41113',
  '...1135.11051110115401155',
  '..11101014111101311511111',
  '..11010115237333111061611',
  '...0165151111115511041332',
  '...1012110111101511131011',
  '...1050110051500151500106',
  '...1101110405140011501055',
  '....101105040540445510101',
  '....110100703107001134041',
  '.....10140707707030150506',
  '.....141670777707315.011.',
  '......1057375377331..102.',
  '......1..6770007730..113.',
  '.......1..07010730....1..',
  '...........0777300....1..',
  '.006000000..000050.......',
  '.030470700000001104......',
  '.0407460407001100006000..',
  '000042004400001101760000.',
  '1150203330060000421076600',
  '0150003377706020120207060',
  '0350030737330605002020500',
  ],

  #----------困った
  [
  '...........111...........',
  '..........13.............',
  '..........1..............',
  '...........1.............',
  '..........11011216...11..',
  '.....16..1125731516.41113',
  '...1135.11051110115401155',
  '..11101014111101311511111',
  '..11010115237333111061611',
  '...0165151111115511041332',
  '...1012110111101511131011',
  '...1050110051500151500106',
  '...1101110405140011501055',
  '....101105440574345510101',
  '....110100003100031134041',
  '.....10147177771730150506',
  '.....141600077000315.011.',
  '......1057375377331..102.',
  '......1..6777777730..113.',
  '.......1..07010730....1..',
  '...........0777300....1..',
  '.006000000..000050.......',
  '.030470700000001104......',
  '.0407460407001100006000..',
  '000042004400001101760000.',
  '1150203330060000421076600',
  '0150003377706020120207060',
  '0350030737330605002020500',
  ],
]


#---------------------------------------------
# コマンドライン引数処理
#
inFile = ''              # ファイルからメッセージを読む場合にファイル名を入れる
quiet = False            # True=メッセージを読まず顔出力のみ
showWhole = True         # True=出力文が短くても顔全体を表示する
imgSeq = 0               # 出力する顔の番号
align = 'R'              # R=右揃え、L=左揃え
cBase = 40               # 背景色のベースの数値
argv0 = sys.argv.pop(0)
while (len(sys.argv) > 0 and re.match('^-', sys.argv[0])):
  arg = sys.argv.pop(0)
  if   arg == '--': break
  elif arg == '-l': align = 'L'
  elif arg == '-r': align = 'R'
  elif arg == '-q': quiet = True
  elif arg == '-b': cBase = 100
  elif arg == '-d': showWhole = False
  elif arg == '-f' and len(sys.argv) > 0: inFile = sys.argv.pop(0)
  elif re.match('^-[0-' + str(len(img)-1) + ']$', arg): imgSeq = abs(int(arg))
  else: usage(argv0, version)

#---------------------------------------------
# 出力文字列を得る
#
msg = '';
if quiet:
  msg = ''                   # 顔画像だけ出力させる場合はなにもしない
elif inFile != '':
  f = open(inFile, 'r')      # -f で指定したファイルを読み込むとき
  msg = f.read()             # 改行が\nでないファイルだと問題があるかも。
  f.close()
elif len(sys.argv) > 0:
  msg = ' '.join(sys.argv)   # コマンドライン引数から文字列を得るとき
else:
  while True:                # 標準入力から文字列を得るとき
    try:
      msg += input() + "\n"
    except EOFError:
      break

#---------------------------------------------
# 出力文字列をいったん行毎に配列化し、制御文字を整形したうえで1つの文字列に戻す。
# 改行文字以外の制御文字を処理したいので。
#
msg = msg.replace('\t', ' ').rstrip('\n')         # TABを空白にする。末尾の改行を削除する
msgTmp = ''
for s in msg.splitlines():
  msgTmp += re.sub(r'[\x00-\x1F\x7F]', '', s) + '\n'
msg = msgTmp

#---------------------------------------------
# 出力行数を得る。ただし文字数が多すぎた場合はずれる。
#
lineNum = msg.count('\n')
if lineNum <= 0: lineNum = 1

#---------------------------------------------
# 顔を表示する範囲を決め、配列から出力する要素のみを残す
#
if showWhole == False:
  yStart = 0
  yEnd = len(img[imgSeq])
  if lineNum < 6:                          # 顔は最小でも6行表示させる
    yStart = int(len(img[imgSeq]) / 2) - int(6 / 2) + 2
    yEnd = yStart + 6
  elif lineNum + 2 < len(img[imgSeq]):     # 顔サイズよりメッセージ文が短そうなとき
    yStart = int(len(img[imgSeq]) / 2) - int(lineNum / 2) + 1
    yEnd = yStart + lineNum + 1
  img[imgSeq] = img[imgSeq][yStart : yEnd] # 配列から出力する要素のみ残す

#---------------------------------------------
# 端末の横幅を求め、顔が右端に来るよう左側に余白(.)を挿入する
#
width = shutil.get_terminal_size().columns
if align == 'R':
  mWidth = width - len(img[imgSeq][0]) * 2;
  if mWidth > 0:
    for i in range(len(img[imgSeq])):
      img[imgSeq][i] = '.' * int(mWidth / 2) + img[imgSeq][i];
  else:
    # 画面が狭すぎるときは、文字列のみ出力して終了する
    print('warning: too narrow screen', file=sys.stderr)
    exit()

#---------------------------------------------
# メッセージの出力開始行msgStartを決める
#
if align == 'R':
  msgStart = 0
  outN = len(msg)
  N = 0
  for l in reversed(range(len(img[imgSeq]))):
    for color in list(img[imgSeq][l]):
      if color == '.': N += 1
      else: break
    if outN < N:
      msgStart = l
      break
  msgStart2 = int(len(img[imgSeq]) / 2 - lineNum / 2 + 0.5)  # 上下中央ぞろえの場合
  if msgStart2 < 0: msgStart2 = 0
  if msgStart > msgStart2: msgStart = msgStart2   # より小さい方の行番号を開始位置にする
else:
  for i in range(len(img[imgSeq])):
    img[imgSeq][i] = img[imgSeq][i][::-1]
  msgStart = int(len(img[imgSeq]) - lineNum)
  msgStart2 = int(len(img[imgSeq]) / 2 - lineNum / 2 + 0.5)  # 上下中央ぞろえの場合
  if msgStart2 < 0: msgStart2 = 0
  if msgStart > msgStart2: msgStart = msgStart2   # より小さい方の行番号を開始位置にする

#---------------------------------------------
# 画面出力（顔が左、メッセージが右の場合）
#---------------------------------------------
def outLeft(img, imgSeq, width, msg, msgStart):
  msgChars = list(msg)
  print("\033[0m", end='')                                     # 文字設定のリセット
  for l in range(len(img[imgSeq])):
    # 顔データを1行分出力
    for color in list(img[imgSeq][l]):
      if color == '.': print("\033[0m  ", end='')              # 背景を描画する
      else: print("\033[%dm  " % (int(color) + cBase), end='') # 顔を描画する
    print("\033[0m", end='')                                   # 文字設定をリセットする

    # 出力するメッセージが無いなら次の行へ
    if l < msgStart or len(msgChars) <= 0:
      print('')
      continue

    # メッセージを出力する
    x = len(img[imgSeq][l]) * 2                         # x...カーソル位置
    while x < width:
      w = unicodedata.east_asian_width(msgChars[0])     # 出力文字の文字幅を求める
      if w in 'FWA' and x + 1 >= width:                 # 全角文字で行をまたがる場合
        print(' ' * (width - x))
        break
      outc = msgChars.pop(0)                            # メッセージを1文字取り出す
      if outc == '\n':                                  # メッセージが改行だった場合
        print(' ' * (width - x))
        break
      print(outc, end='')                               # メッセージを1文字出力する
      if w in 'FWA': x += 2                             # xの更新。全角なら+2
      else: x += 1
  if len(msgChars) > 0: print(''.join(msgChars) + "\n") # 未出力の文字列があれば出力する

#---------------------------------------------
# 画面出力（顔が右、メッセージが左の場合）
#---------------------------------------------
def outRight(img, imgSeq, width, msg, msgStart):
  msgChars = list(msg)
  print("\033[0m", end='')              # 文字設定のリセット
  for l in range(len(img[imgSeq])):
    # フラグを初期化
    msgok = True
    if l < msgStart: msgok = False      # True=メッセージ出力OK

    # 顔やメッセージを一文字ずつ出力
    for color in list(img[imgSeq][l]):
      if color != '.': msgok = False    # 顔の右側に文字を表示させない

      # 色設定
      if color == '.': print("\033[0m", end='')               # 背景
      else: print("\033[%dm" % (int(color) + cBase), end='')  # 顔

      # メッセージを出力しない場所の場合
      if msgok == False or len(msgChars) <= 0:
        print('  ', end='')          # 空白を出力して次の文字へ
        continue

      # 出力文字を1つ取り出す
      outc = msgChars.pop(0)

      # 出力文字が改行コードだった場合
      if outc == '\n':
        print('  ', end='')
        msgok = False
        continue

      # 出力文字が普通の文字だった場合
      w = unicodedata.east_asian_width(outc)  # 文字幅を求める
      if not(w in 'FWA'):                     # 1文字目が半角だったら後続文字との連結を試みる
        if len(msgChars) <= 0: outc += ' '    # 後続文字が無い場合
        else:                                 # 後続文字がある場合
          w = unicodedata.east_asian_width(msgChars[0])
          if not(w in 'FWA'):                 # 後続文字が半角なら取り出して連結
            outc2 = msgChars.pop(0)
            if outc2 == '\n':                 # 後続文字が改行コードだった場合
              outc2 = ' '
              msgok = False
            outc += outc2
          else:
            outc += ' '
      print(outc, end='')                     # 1文字出力
    print("\033[0m")                          # 行末の改行出力
  if len(msgChars) > 0: print(''.join(msgChars) + "\n")  # 未出力の文字列があれば出力する


#---------------------------------------------
# 画面出力
#
if align == 'L': outLeft (img, imgSeq, width, msg, msgStart)
else:            outRight(img, imgSeq, width, msg, msgStart)

# 文字設定をリセットする
print("\033[0m", end='')

