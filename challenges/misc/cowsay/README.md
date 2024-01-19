# cowsay

- 作者：13m0n4de
- 参考：-
- 难度：-
- 分类：Misc
- 镜像：-
- 端口：-

## 题目描述

```
$ ssh ctf@{IP} -p {PORT} -oStrictHostKeyChecking=no -oCheckHostIP=no -oUserKnownHostsFile=/dev/null
```

```sh
#!/bin/sh

read -p "Enter the name of the cowfile (e.g., default, sheep, dragon):" cowfile
read -p "Enter the message:" message

/usr/bin/cowsay -f $cowfile $message
```

> Hint: 本题 cowsay 版本为[仓库](https://github.com/tnalpgge/rank-amateur-cowsay)最新，对应 `cowsay-3.04` 。

## 题目解析

<analysis>
