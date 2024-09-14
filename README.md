# techo - TETO's echo

![help screen](https://github.com/nwp8861/techo/blob/main/techo-help.png)

## Overview

This Python script is simply print text message to stdout like echo or cat command on Linux, but it can decorate your terminal with dotted Teto's face at that time. 

It must offers not only making severe system administration jobs relax, but also practicality that prevents important notice overlooked. 

## Requirement

- Python3
- CLI terminal supporting ANSI escape sequence. 

## Usage
```
techo [-0~5|-q|-b|-d|-l|-r|-f text-file] [--] [message ... ]

  -0 ~ -5      ... change face (default: -0)
  -q           ... output no message (show face only)
  -b           ... color brightness change
  -d           ... reduce Teto's vertical width
  -l           ... position face to the left
  -r           ... position face to the right (default)
  -f text-file ... read message from text-file
  --           ... end of command line options
```

(simple example)
```
$ techo hello world
```

(reading message from pipeline)
```
$ date | techo
```

(just see Teto's face)
```
$ techo -q
```

(change face depending on command execution result)
```
$ gcc sample.c && techo -1 -q -d || techo -5 -q -d
```

(instant ramen timer)
```
$ sleep 180; techo -1 'READY!'
```

## License

the source code:
  2024, nwp8861, released under the MIT No Attribution license (MIT-0)
  MIT-0: https://opensource.org/license/MIT-0

Teto:
  PCL (applied mutatis mutandis)
  [https://kasaneteto.jp/guideline/ctu.html](https://kasaneteto.jp/guideline/ctu.html)
