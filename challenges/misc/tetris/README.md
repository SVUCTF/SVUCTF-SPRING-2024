# 俄罗斯方块

- 作者：13m0n4de
- 参考：-
- 难度：-
- 分类：Misc
- 镜像：-
- 端口：-

## 题目描述

玩到 100000 分就可以获得 Flag 哦。

## 题目解析

俄罗斯方块游戏，消一行得 1 分，得到 100000 分即可获得 Flag。

这道题考察内存搜索和修改。使用内存搜索工具定位游戏分数在内存中的位置，然后直接修改内存中的分数值改到 100000 或以上。

Windows 下可以用 Cheat Engine，Linux 下可以用 [scanmem](https://github.com/scanmem/scanmem)，下面以 scanmem 为例。

启动游戏，在 scanmem 中填入 PID：

```
> pid 29383
info: maps file located at /proc/29383/maps opened.
info: 114 suitable regions found.
Scan the current process for variables with given value.
```

消除骨牌刷新得分，扫描内存中对应值的地址，不断重复这个步骤，最终可以锁定得分的内存地址：

```
> = 0
info: we currently have 233213324 matches.
233213324> = 1
..........ok
info: we currently have 17341 matches.
17341> = 2
..........ok
info: we currently have 169 matches.
169> = 3
...........ok
info: we currently have 42 matches.
42> = 4
.................ok
info: we currently have 30 matches.
30> = 6
...........ok
info: we currently have 29 matches.
29> = 7
...........ok
info: we currently have 26 matches.
26> = 8
..........ok
info: we currently have 26 matches.
26> = 9
..........ok
info: we currently have 26 matches.
26> = 11
..........ok
info: we currently have 1 matches.
info: match identified, use "set" to modify value.
info: enter "help" for other commands.
```

修改为大于 100000 的值，获得 Flag：

```
1> set 999999
info: setting *0x57be6396d4c0 to 0xf423f...
```

![flag](./writeup/flag.png)

## 其他

游戏代码修改自 https://github.com/NightsWatchGames/tetris

虽然编译的时候制作了 Windows 版本，但由于种种原因，没在 Windows 上测试，如果题目在 Windows 上没法复现，非常抱歉。
