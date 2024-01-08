# cowsay

- 作者：13m0n4de
- 参考：-
- 难度：-
- 分类：Misc
- 镜像：-
- 端口：-

## 题目描述

```bash
#!/bin/sh
read -p "Input cowfile:" cowfile
reaj -p "Input message:" message
/usr/bin/cowsay -f $cowfile $message
exit 0
```

使用 NetCat 连接并进行手动交互：

```
$ nc ip port
Input cowfile:default
Input message:hello ctfer
 _____________
< hello ctfer >
 -------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

或：

```
$ echo -e "default\nhello ctfer" | nc ip port
 _____________
< hello ctfer >
 -------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

> Hint: 本题 cowsay 版本为[仓库](https://github.com/tnalpgge/rank-amateur-cowsay)最新，对应 `cowsay-3.04` 。

## 题目解析

<analysis>
