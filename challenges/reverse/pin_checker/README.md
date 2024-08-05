# PIN Checker

- 作者：13m0n4de
- 参考：-
- 难度：-
- 分类：Misc
- 镜像：[svuctf-spring-2024/pin_checker](https://ghcr.io/svuctf/svuctf-spring-2024/pin_checker:latest)
- 端口：70

## 题目描述

## 题目解析

考点：侧信道（指令数）

### 分析程序

执行程序，提示输入 N 位数字作为 PIN 码：

```
$ ./pin_checker 
Please enter your PIN code (N digits):
123123123123
Checking PIN...
Access denied.
```

反编译结果有些奇怪，全部都是 `mov` 指令：

```asm
 805576c:       mov    DWORD PTR [eax],edx
 805576e:       mov    edx,DWORD PTR ds:0x80570d4
 8055774:       mov    DWORD PTR [eax+0x4],edx
 8055777:       mov    edx,DWORD PTR ds:0x80570d8
 805577d:       mov    DWORD PTR [eax+0x8],edx
 8055780:       mov    DWORD PTR ds:0x84001f4,0x860022c
 805578a:       mov    eax,DWORD PTR [ecx*4+0x84001f0]
 8055791:       mov    edx,DWORD PTR ds:0x80570e0
 8055797:       mov    DWORD PTR [eax],edx
 8055799:       mov    edx,DWORD PTR ds:0x80570e4
 805579f:       mov    DWORD PTR [eax+0x4],edx
 80557a2:       mov    edx,DWORD PTR ds:0x80570e8
 80557a8:       mov    DWORD PTR [eax+0x8],edx
 80557ab:       mov    edx,DWORD PTR ds:0x80570ec
 80557b1:       mov    DWORD PTR [eax+0xc],edx
 80557b4:       mov    edx,DWORD PTR ds:0x80570f0
 80557ba:       mov    DWORD PTR [eax+0x10],edx
 80557bd:       mov    edx,DWORD PTR ds:0x80570f4
 80557c3:       mov    DWORD PTR [eax+0x14],edx
 80557c6:       mov    eax,ds:0x84001d8
 80557cb:       mov    eax,DWORD PTR [eax*4+0x84001d0]
 80557d2:       mov    DWORD PTR [eax],0x0
 80557d8:       mov    esp,DWORD PTR ds:0x84001b0
 80557de:       mov    cs,eax
```

这是因为程序是由 [movfuscator](https://github.com/xoreaxeaxeax/movfuscator) 混淆得出的，反编译难度很大。（有些方式可以还原程序的部分逻辑结构，但分析依旧比较困难）

试猜想某种特殊情况，程序源码中判断 PIN 码的逻辑可能会是这样（以 Python 为例）：

```python
if len(user_pin) != PIN_LENGTH:
    print("Access denied.")
    exit(-1)

for i in range(PIN_LENGTH):
    if user_pin[i] != corrent_pin[i]:
        print("Access denied.")
        exit(-1)

print("Success.")
```

- 先比较输入 PIN 码长度与正确 PIN 码长度，如果不一致会直接退出；
- 如果长度一样，会**逐个**判断 PIN 码，遇到不对的数字就退出。

当输入的 PIN 码长度正确时，程序会继续执行到字符比较的步骤，这比长度不正确时多执行几行代码。因此，理论上，对于长度正确的输入，程序的执行时间会稍长一些。

并且由于程序是逐个字符比较的，当猜对了前面的字符时，程序会执行更多的比较操作才退出。这意味着，猜对越多位，程序的执行时间就越长。

利用这种执行时间的微小差异，可以先推断出正确 PIN 码的长度，再逐位猜解出正确的 PIN 码。

一个标准的**侧信道攻击**。

### 验证猜想

在实际情况中，执行时间受不定因素影响很大，**统计 CPU 执行的指令数量**比测量实际执行时间更加可靠。

统计 CPU 指令数可以使用 `perf stat` 工具。

下面的例子中能够观察到，输入 8 位数字时，指令数为 `324400`（这个指令数会在一个小范围内浮动）：

```bash
$ perf stat -x , -e instructions:u ./pin_checker
Please enter your PIN code (N digits):
00000000
Checking PIN...
Access denied.
320440,,instructions:u,904675,100.00,,
```

不同 PIN 码长度下指令的数量：

```bash
$ printf "%01d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
317251,,instructions:u,1037319,100.00,,
$ printf "%02d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
317715,,instructions:u,736632,100.00,,
$ printf "%03d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
318182,,instructions:u,809423,100.00,,
$ printf "%04d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
318644,,instructions:u,767913,100.00,,
$ printf "%05d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
319113,,instructions:u,786749,100.00,,
$ printf "%06d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
319574,,instructions:u,693680,100.00,,
$ printf "%07d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
320039,,instructions:u,764286,100.00,,
$ printf "%08d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
320502,,instructions:u,693730,100.00,,
$ printf "%09d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
320962,,instructions:u,739498,100.00,,
$ printf "%010d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
321429,,instructions:u,792379,100.00,,
$ printf "%011d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
321895,,instructions:u,791488,100.00,,
$ printf "%012d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
331498,,instructions:u,666769,100.00,,
$ printf "%013d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
322824,,instructions:u,751541,100.00,,
$ printf "%014d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
323285,,instructions:u,786138,100.00,,
```

可以发现，每多一位，指令数就少量增加，这有可能是长度判断函数中执行了更多指令。

唯独当输入 12 位 PIN 码时，指令数增加更加剧烈，达到了 33 万以上。

当固定 12 位 PIN 码，只变动首位数字时的情况：

````bash
$ printf "0%011d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
331435,,instructions:u,672199,100.00,,
$ printf "1%011d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
331435,,instructions:u,782300,100.00,,
$ printf "2%011d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
331437,,instructions:u,847526,100.00,,
$ printf "3%011d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
331436,,instructions:u,711815,100.00,,
$ printf "4%011d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
331438,,instructions:u,984908,100.00,,
$ printf "5%011d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
331437,,instructions:u,788923,100.00,,
$ printf "6%011d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
331437,,instructions:u,707867,100.00,,
$ printf "7%011d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
331438,,instructions:u,841043,100.00,,
$ printf "8%011d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
340576,,instructions:u,773043,100.00,,
$ printf "9%011d\n" | perf stat -x , -e instructions:u ./pin_checker 1>/dev/null
331437,,instructions:u,814612,100.00,,```
````

首位为 `8` 时，指令数急剧增加。

这说明之前针对判断逻辑的猜想很可能是正确的，我们可以通过类似于“撬锁”的方式猜解 PIN 码：不断尝试移动销钉，当销钉的断点与剪切线对齐时会听到轻微的咔嗒声。

对应到程序中，咔嗒声就相当于指令数激增，当指令数激增，说明此次猜解的 PIN 码正确。

### 自动化猜解

自动化猜解脚本 [solve.py](./writeup/solve.py)：

```python
#!/usr/bin/env python3

import subprocess


def check(pin: str) -> int:
    result = subprocess.run(
        [
            "perf",
            "stat",
            "-x",
            ",",
            "-e",
            "instructions:u",
            "../attachments/pin_checker",
        ],
        input=pin,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    output = result.stderr.split(",")[0]
    return int(output)


def find_len() -> int:
    pin = ""
    max_count = 0
    length = 0

    for i in range(30):
        pin += "0"
        count = check(pin)

        if count > max_count:
            max_count = count
            length = i + 1

    return length


def find_pin(length: int) -> str:
    pin = ""

    for _ in range(length):
        char = ""
        max_count = 0

        for code in "0123456789":
            paded_pin = (pin + code).ljust(length, "0")
            count = check(paded_pin)
            print(f"{paded_pin}: {count}")

            if count > max_count:
                max_count = count
                char = code
        pin += char

    return pin


if __name__ == "__main__":
    length = find_len()
    pin = find_pin(length)
    print("PIN:", pin)
```

程序有点长但不复杂，只是将之前验证猜想时人工完成的事情写成程序了。

这里还有个 Fish 版本：[solve.fish](./writeup/solve.fish)。

运行得到 PIN：`863978754614`

```
...
863978754617: 432036
863978754618: 432034
863978754619: 432034
PIN: 863978754614
```

连接靶机，输入 PIN 码获得 Flag。

```
Please enter your PIN code (N digits):
863978754614
Checking PIN...
Flag: flag{GZCTF_dynamic_flag_test}
```
