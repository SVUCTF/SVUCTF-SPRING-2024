# 帕鲁问答

- 作者：13m0n4de
- 参考：-
- 难度：-
- 分类：Web
- 镜像：[svuctf-spring-2024/pal_quiz](https://ghcr.io/svuctf/svuctf-spring-2024/pal_quiz:latest)
- 端口：80

## 题目描述

过年睡得太多，例行的问答题完全没了出题思路

求助同学，却得到了这样的回复：

「帕鲁知识小问答嘛？」

说罢，我的电脑竟然自己动了起来 ~~（自动下载幻兽帕鲁~~）。

「帮你出好了，顺带还去掉了后端，这样就再也不用担心后端漏洞了。」

## 题目解析

考点：JavaScript 代码分析

这题出在过年，真的求助了同学，也真的得到了「帕鲁知识小问答嘛？」的回复，只是间隔时间太长，开赛的时候帕鲁都已经不火了，蹭热度都蹭不上。

这题模仿了[猫咪问答](../../misc/neko_quiz/README.md)的页面，问题内容是杜撰的，甚至有些离谱。

> 4\. RFC 81024 定义了一种通过思维直接交流的网络协议。这种协议允许传输的最大思维复杂度是多少比特 （10 分）
>
> 提示：使用数字表示，如 1024

这是为了暗示此题是 Web 题，而不是问答题。如果尝试提交，会发现根本没有网络请求发出，就和题目描述说的一样，没有后端。

查看网页源码，发现引入了 `index.js`，内容如下：

```javascript
const questionMap = {
    "q1": -6565984,
    "q2": -7942262,
    "q3": -6238514,
    "q4": -7025504,
    "q5": -6960247,
    "q6": -3421540,
    "q7": -7483761,
    "q8": -929000826,
    "q9": -1600549426,
    "q10": -862872640,
};


function checkAnswers() {
    const resultAlert = document.getElementById("resultAlert");
    resultAlert.hidden = false;

    let totalScore = 0;
    let answers = [];

    document.querySelectorAll("input").forEach(input => {
        const answer = input.value.trim();
        answers.push(answer);
        if (check(answer, input.id)) {
            totalScore += 10;
        }
    });

    if (totalScore == 100) {
        resultAlert.className = 'alert alert-success';
        resultAlert.innerHTML = `恭喜你，本次测验总得分为 ${totalScore}。<br>flag{pal_pal_pal_${getFlag(answers)}}`;
    } else {
        resultAlert.className = 'alert alert-secondary';
        resultAlert.innerHTML = `本次测验总得分为 ${totalScore}。<br>没有全部答对，不能给你 flag 哦。`;
    }

    return false;
}

function check(answer, questionId) {
    return questionMap[questionId] == ~parseInt(answer, 2);
}

function getFlag(answers) {
    return answers.map(answer => {
        return answer.match(/.{1,8}/g).map(b => {
            return String.fromCharCode(parseInt(b, 2));
        }).join("");
    }).join("");
}
```

点击提交按钮执行 `checkAnswers` 函数，获得所有答案输入框的内容，依次调用 `check` 函数检查答案是否正确：

```javascript
document.querySelectorAll("input").forEach(input => {
    const answer = input.value.trim();
    answers.push(answer);
    if (check(answer, input.id)) {
        totalScore += 10;
    }
});
```

`check` 函数将用户输入的答案按照二进制转换为整数，对其进行按位取反操作，然后与预设的答案比较：

```javascript
const questionMap = {
    "q1": -6565984,
    "q2": -7942262,
    "q3": -6238514,
    "q4": -7025504,
    "q5": -6960247,
    "q6": -3421540,
    "q7": -7483761,
    "q8": -929000826,
    "q9": -1600549426,
    "q10": -862872640,
};

function check(answer, questionId) {
    return questionMap[questionId] == ~parseInt(answer, 2);
}
```

确认所有答案都正确后，使用 `getFlag` 函数把答案字符串转换为 Flag 字符串的后半段。

```javascript
function getFlag(answers) {
    return answers.map(answer => {
        return answer.match(/.{1,8}/g).map(b => {
            return String.fromCharCode(parseInt(b, 2));
        }).join("");
    }).join("");
}
```

- 使用 `map` 方法遍历 `answers` 数组中的每个答案；
- 对每个答案，使用正则表达式 `/.{1,8}/g` 将其分割成 8 位一组的二进制字符串；
- 对每组 8 位二进制字符串使用 `parseInt(b, 2)` 将其转换为十进制数；
- 使用 `String.fromCharCode()` 将十进制数转换为对应的 ASCII 字符；
- 将转换后的字符连接成字符串。

于是可以写出解密脚本 [solve.py](./writeup/solve.py)：

```python
question_map = {
    "q1": -6565984,
    "q2": -7942262,
    "q3": -6238514,
    "q4": -7025504,
    "q5": -6960247,
    "q6": -3421540,
    "q7": -7483761,
    "q8": -929000826,
    "q9": -1600549426,
    "q10": -862872640,
}

flag = "flag{pal_pal_pal_"

for number in question_map.values():
    binary = bin(~number)[2:]
    padding_length = ((len(binary) + 7) // 8) * 8
    binary = binary.rjust(padding_length, "0")
    print(binary)

    for i in range(0, padding_length, 8):
        char_code = int(binary[i : i + 8], 2)
        flag += chr(char_code)

flag += "}"

print(flag)
```

得到 Flag：`flag{pal_pal_pal_d0_y0u_11k3_j4v45cr1p7_my_fr13nd?}`

注意二进制数首部填充 `0` 至 8 的倍数。
