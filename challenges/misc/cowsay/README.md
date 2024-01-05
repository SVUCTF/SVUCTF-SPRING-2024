# cowsay

- 作者：13m0n4de
- 参考：-
- 难度：-
- 分类：Misc
- 镜像：-
- 端口：-

## 题目描述

网页结果中的命令行仅供参考和测试，后端执行命令代码如下：

```python
cowfile = request.form["cowfile"]
input = request.form["input"]
arg = request.form["arg"]

p = subprocess.Popen(
    ["/usr/bin/cowsay", "-f", cowfile, arg],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
stdout, _ = p.communicate(input=input.encode())

command_line = '$ echo -n -e "{input}" | cowsay -f {cowfile} "{arg}"'.format(
    input=codecs.escape_encode(input.encode())[0].decode(),
    cowfile=cowfile,
    arg=arg,
)
result = f"{command_line}\n{stdout.decode()}"
```

## 题目解析

<analysis>
