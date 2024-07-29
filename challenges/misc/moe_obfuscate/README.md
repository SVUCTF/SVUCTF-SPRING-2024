# 签到

- 作者：13m0n4de
- 参考：[IOCCC](https://www.ioccc.org/)
- 难度：-
- 分类：Misc
- 镜像：-
- 端口：-

## 题目描述

## 题目解析

附件 [saya.c](./attachments/saya.c)：

```c
                          L[29]={18414916,16301615                          
                       ,31491134,16303663,32570431                          
                    ,1113151,32039998,18415153,14815374                     
                  ,15254040,18128177,32539681,18405233,                     
                18667121,33080895,1097263,17258030, 18136623                
               ,33061951,4329631,33080881,4539953,18732593,18157905         
             ,4329809,32575775,31523934,16007439,32505856 ,};F              
            [27] ={ 5,11,0,    6,26,12,14,4,28,14,1,5  ,20,18,2,            
          0,19,  4, 3,28,2,     28,2 ,14,3,4,27};row,i ,column,length       
        ,idx;main(int argc,      char* argv[]){char*text={ 0};if(argc       
      ==1){for( row=0;row          <5;   row++){for(i= 0;i <27;i++){for     
    (column=0;  column<               5;    column++){ putchar((            
               L[F [i]]                        &( 1<<( row *                
               5+column                           )))? '#'                  
               :' ');}putchar                     (' ');}putchar            
                ('\n');                           }printf(                  
                "Usage: %s <text>\n"              ,argv[0                   
                ]) ;}else                         if(argc                   
                ==2){text                        =argv [1                   
                ];length =                       strlen(text                
                );for(row=0;                   row<5; row                   
                ++) {for(i=0;i               <length; i++                   
                ){if (text[i]>=           'A' && text [i]                   
               <='Z'){idx =text[         i]-'A';}else if(text               
               [i]>= 'a'   &&text         [i]<='z'){ idx=text               
               [i]-'a';}else if(           text [i]=='{'){                  
               idx=26  ;}else                if (text[i]==                  
              '}')     {idx                     =27   ;}else                
              if        (text                  [i]       ==                 
             '_')        {idx                  =28        ;}                
             else         {continue           ;}for       (column           
            =0;column      <5;                column      ++)               
            {putchar         ((              L[           idx]              
           &(1<<(              row                        *5+column         
           )))?'#'                                       :' ');}            
           putchar                                       (' ');}            
       putchar('\n');}}else{printf("Usage: %s <text>\n",argv[0]);}}
```

好吧，只是一个被混淆的 C 语言代码，编译后就能得到 Flag。

为了使代码更简洁，更容易被格式化/混淆，编写的时候省略了很多东西，比如引入头文件、声明变量类型，所以你可能感觉这个代码怪怪的。

在 C89 的标准下这些都是允许的，`printf` 等函数可以隐式声明，不需要 `#include` 语句，并且变量不指定类型时默认其为 `int`。

如果使用新一点的编译器的话，也许需要手动指定 C89 标准，比如 GCC 需要指定 `-std=c89`。

（但貌似选手们很多都是「老旧 IDE 享受者」、「在线编译器爱好者」，可能根本不需要在意这个。）

```bash
$ gcc saya.c -std=c89 -o flag && ./flag
##### #       #    ####  #### #   # ##### #####       ##### ####  ##### #   # #####  ####   #   ##### ##### ####
#     #      # #  #      #    ## ## #   # #           #   # #   # #     #   # #     #      # #    #   #     #   #
##### #     ##### #  ## #     # # # #   # #####       #   # ####  ##### #   # ##### #     #####   #   ##### #   #
#     #     #   # #   #  #    #   # #   # #           #   # #   # #     #   #     # #     #   #   #   #     #   #
#     ##### #   #  ####  #### #   # ##### ##### ##### ##### ####  #     ##### #####  #### #   #   #   ##### ####  #####
Usage: ./flag <text>
```

然后就出现了 ASCII Art 形式的 Flag 文本：

```
flag{moe_obfuscated_c_code}
```

全大写或全小写都是可以提交的。

## 后话

### 这个程序还有什么用

细心的你可能注意到输出： `Usage: ./flag <text>`，这个程序其实是一个文本转 ASCII Art 的小工具，只是在没任何参数的情况下会输出 Flag 。

```bash
$ ./flag "HELLOSVUCTF"
#   # ##### #     #     ##### ##### #   # #   #  #### ##### #####
#   # #     #     #     #   # #     #   # #   # #       #   #
##### ##### #     #     #   # ##### #   # #   # #       #   #####
#   # #     #     #     #   #     #  # #  #   # #       #   #
#   # ##### ##### ##### ##### #####   #   #####  ####   #   #
```

只支持 26 个英文字母。

最原始版本的代码在 [flag.c](./build/flag.c)，代码逻辑不复杂，可能令人困惑的只有如何打印对应字母的 ASCII 艺术字。

```c
int letters[29] = {
    18414916, 16301615, 31491134, 16303663, 32570431, 1113151,
    32039998, 18415153, 14815374, 15254040, 18128177, 32539681,
    18405233, 18667121, 33080895, 1097263,  17258030, 18136623,
    33061951, 4329631,  33080881, 4539953,  18732593, 18157905,
    4329809,  32575775, 31523934, 16007439, 32505856,
};

void print_text(const char* text) {
    int length = strlen(text);
    for (int row = 0; row < 5; row++) {
        for (int i = 0; i < length; i++) {
            int letter_index = 0;
            if (text[i] >= 'A' && text[i] <= 'Z') {
                letter_index = text[i] - 'A';
            } else if (text[i] >= 'a' && text[i] <= 'z') {
                letter_index = text[i] - 'a';
            } else if (text[i] == '{') {
                letter_index = 26;
            } else if (text[i] == '}') {
                letter_index = 27;
            } else if (text[i] == '_') {
                letter_index = 28;
            } else {
                continue;
            }

            for (int column = 0; column < 5; column++) {
                putchar((letters[letter_index] & (1 << (row * 5 + column)))
                            ? '#'
                            : ' ');
            }
            putchar(' ');
        }
        putchar('\n');
    }
}
```

我把每个字母都设计为了 5 x 5 的大小，由 `#` 和 ` ` 组成，表示为 5 x 5 的 [Bitmap](https://en.wikipedia.org/wiki/Bitmap)，`0` 表示 ` `，`1` 表示 `#`。

比如 `A`：

```
00100
01010
11111
10001
10001
```

把这五行从右到左排列，可以得到一个二进制数：

```
1000110001111110101000100
```

这个数转化为十进制数，就是 `18414916`。

只要按照这个步骤，将所有字母对应的整数存在 `letters` 数组里，打印时取出对应的整数，按照二进制位输出 ` ` 或 `#` 就可以了。

生成数组的脚本在 [ascii_art.py](./build/ascii_art.py)，可以直接生成 C 语言数组代码。

### 代码怎么混淆成对应图案的

基本思路为：从图像文件生成掩码（只有正负，按照像素亮度划分），对 C 语言代码进行分词，如果掩码为正，打印并消耗当前 Token，否则打印空格。

写了个命令行工具，地址在：https://github.com/13m0n4de/c-code-to-ascii-art

这样就能得到一个大致轮廓与图片一致的 C 语言代码文件。（C 语言格式真的很宽松）

不过在那之前还进行了人工的初步混淆，得到 [flag.obfus.c](./build/flag.obfus.c)。

使用图片生成掩码，使用掩码生成混淆后的代码，得到：[flag.saya.c](./build/flag.saya.c)，也就是附件。

### 出题灵感

灵感来自于 [IOCCC](https://www.ioccc.org/) 和 [Why do C Programmers Always Obfuscate Their Code? ](https://www.youtube.com/watch?v=fJbAiXIum0k)。

IOCCC 是国际 C 代码混淆大赛，旨在使用各种技巧混淆 C 语言代码。

以下是几个代表性的作品：

#### 甜甜圈

https://www.a1k0n.net/2006/09/15/obfuscated-c-donut.html

甜甜圈形状的代码，可以打印出 3D 旋转的甜甜圈。

```c
             k;double sin()
         ,cos();main(){float A=
       0,B=0,i,j,z[1760];char b[
     1760];printf("\x1b[2J");for(;;
  ){memset(b,32,1760);memset(z,0,7040)
  ;for(j=0;6.28>j;j+=0.07)for(i=0;6.28
 >i;i+=0.02){float c=sin(i),d=cos(j),e=
 sin(A),f=sin(j),g=cos(A),h=d+2,D=1/(c*
 h*e+f*g+5),l=cos      (i),m=cos(B),n=s\
in(B),t=c*h*g-f*        e;int x=40+30*D*
(l*h*m-t*n),y=            12+15*D*(l*h*n
+t*m),o=x+80*y,          N=8*((f*e-c*d*g
 )*m-c*d*e-f*g-l        *d*n);if(22>y&&
 y>0&&x>0&&80>x&&D>z[o]){z[o]=D;;;b[o]=
 ".,-~:;=!*#$@"[N>0?N:0];}}/*#****!!-*/
  printf("\x1b[H");for(k=0;1761>k;k++)
   putchar(k%80?b[k]:10);A+=0.04;B+=
     0.02;}}/*****####*******!!=;:~
       ~::==!!!**********!!!==::-
         .,~~;;;========;;;:~-.
             ..,--------,*/
```

<video autoplay loop muted>
  <source src="writeups/donut.webm" type="video/webm">
Your browser does not support the video tag.
</video>

#### AKARI

http://uguu.org/src_akari_c.html

`akari` 是一个图像采样工具，可以接受 PGM、PPM、ASCII art 的输入输出格式。

```
                                       /*
                                      +
                                     +
                                    +
                                    +
                                    [         >i>n[t
                                     */   #include<stdio.h>
                        /*2w0,1m2,]_<n+a m+o>r>i>=>(['0n1'0)1;
                     */int/**/main(int/**/n,char**m){FILE*p,*q;int        A,k,a,r,i/*
                   #uinndcelfu_dset<rsitcdti_oa.nhs>i/_*/;char*d="P%"   "d\n%d\40%d"/**/
                 "\n%d\n\00wb+",b[1024],y[]="yuriyurarararayuruyuri*daijiken**akkari~n**"
          "/y*u*k/riin<ty(uyr)g,aur,arr[a1r2a82*y2*/u*r{uyu}riOcyurhiyua**rrar+*arayra*="
       "yuruyurwiyuriyurara'rariayuruyuriyuriyu>rarararayuruy9uriyu3riyurar_aBrMaPrOaWy^?"
      "*]/f]`;hvroai<dp/f*i*s/<ii(f)a{tpguat<cahfaurh(+uf)a;f}vivn+tf/g*`*w/jmaa+i`ni("/**
     */"i+k[>+b+i>++b++>l[rb";int/**/u;for(i=0;i<101;i++)y[i*2]^="~hktrvg~dmG*eoa+%squ#l2"
     ":(wn\"1l))v?wM353{/Y;lgcGp`vedllwudvOK`cct~[|ju {stkjalor(stwvne\"gt\"yogYURUYURI"[
     i]^y[i*2+1]^4;/*!*/p=(n>1&&(m[1][0]-'-'||m[1][1]  !='\0'))?fopen(m[1],y+298):stdin;
      /*y/riynrt~(^w^)],]c+h+a+r+*+*[n>)+{>f+o<r<(-m]    =<2<5<64;}-]-(m+;yry[rm*])/[*
       */q=(n<3||!(m[2][0]-'-'||m[2][1]))?stdout /*]{     }[*/:fopen(m[2],d+14);if(!p||/*
       "]<<*-]>y++>u>>+r >+u+++y>--u---r>++i+++"  <)<      ;[>-m-.>a-.-i.++n.>[(w)*/!q/**/)
    return+printf("Can "  "not\x20open\40%s\40"    ""       "for\40%sing\n",m[!p?1:2],!p?/*
  o=82]5<<+(+3+1+&.(+  m  +-+1.)<)<|<|.6>4>-+(>    m-        &-1.9-2-)-|-|.28>-w-?-m.:>([28+
 */"read":"writ");for  (   a=k=u= 0;y[u];  u=2    +u){y[k++   ]=y[u];}if((a=fread(b,1,1024/*
,mY/R*Y"R*/,p/*U*/)/*          R*/ )>/*U{  */   2&& b/*Y*/[0]/*U*/=='P' &&4==/*"y*r/y)r\}
*/sscanf(b,d,&k,& A,&           i,  &r)&&        !   (k-6&&k -5)&&r==255){u=A;if(n>3){/*
]&<1<6<?<m.-+1>3> +:+ .1>3+++     .   -m-)      -;.u+=++.1<0< <; f<o<r<(.;<([m(=)/8*/
u++;i++;}fprintf   (q,    d,k,           u      >>1,i>>1,r);u  = k-5?8:4;k=3;}else
  /*]>*/{(u)=/*{   p> >u  >t>-]s                >++(.yryr*/+(    n+14>17)?8/4:8*5/
     4;}for(r=i=0  ;  ;){u*=6;u+=                (n>3?1:0);if    (y[u]&01)fputc(/*
      <g-e<t.c>h.a r  -(-).)8+<1.                 >;+i.(<)<     <)+{+i.f>([180*/1*
      (r),q);if(y[u   ]&16)k=A;if                               (y[u]&2)k--;if(i/*
      ("^w^NAMORI; {   I*/==a/*"                               )*/){/**/i=a=(u)*11
       &255;if(1&&0>=     (a=                                 fread(b,1,1024,p))&&
        ")]i>(w)-;} {                                         /i-f-(-m--M1-0.)<{"
         [ 8]==59/* */                                       )break;i=0;}r=b[i++]
            ;u+=(/**>>                                     *..</<<<)<[[;]**/+8&*
            (y+u))?(10-              r?4:2):(y[u]         &4)?(k?2:4):2;u=y[u/*
             49;7i\(w)/;}             y}ru\=*ri[        ,mc]o;n}trientuu ren (
             */]-(int)'`';}             fclose(          p);k= +fclose( q);
              /*] <*.na/m*o{ri{                       d;^w^;}  }^_^}}
               "   */   return  k-                -1+   /*\'   '-`*/
                     (   -/*}/   */0x01        );       {;{    }}
                            ;           /*^w^*/        ;}`
```

`akari.c` 可以被它自己采样成 `akari2.c`：

```


                       int
            *w,m,_namori=('n');
         #include<stdio.h>/*;hrd"%  dnd4%"*/
     /**/int(y),u,r[128*2/*{y}icuhya*rr*rya=
   */];void/**/i(){putchar(u);}int/**/main(/*
  "(n"l)?M5{YlcpvdluvKct[j skao(tve"t"oYRYR"
   */int(w),char**n){for(m  =256;--m;r[m]/*
   "<*]y+u>r>u+y-u-r+i+" )   ;>m.a.i+n>()/q*/
 =25<(31&( m -1))||64-(  m    &192)||2>w?m:(2+
m/*"*,/U//     R/)/U *  & /Y/0/U/=P &=/"*/)\
&16?m-13 : 13+     m)   ;u=+10 ;for(;(m=/*
 *>/()/{ p u t-s        +(yy*+  n1>7?/:*/
   getchar ())+1         ;i()   ){if(10/*
   "wNMR;{ I/=/"               )/{*/==u*1
    )i();                      if(m-10){
      u=/*>                  *./<)[;*/8*
      4;i();       }u=r[    m];}return(
       * *n/*{i            ;w; }_}
          ( -*/ *00    )    ;  }
```

`akari2.c` 也是一个有效的 C 程序，可以用来生成“扩展”后的文本。

如果对 `akari2.c` 进行采样，可以得到 `akari3.c`：

```
      wm_aoi(n)
  /*ity,,[2*/{}char*y=
 (")M{lpduKtjsa(v""YY"
 "*yuruyuri") ;main(/*
/",U/  R)U*  Y0U= ="/\
*/){puts    (y+ 17/*
 "NR{I="       ){/=*
   =*         */);/*
   **/{      ;;}}
```

同样地，对 `akari3.c` 进行采样可以得到 `akari4.c`：

```
   main
(){puts("Y"
"U RU YU "\
"RI"   )/*
 */   ;}
```

`akari3.c` 和 `akari4.c` 也都是有效的 C 程序。

```
$ ./akari3
yuruyuri
$ ./akari4
YU RU YU RI
```
