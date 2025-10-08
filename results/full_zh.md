# 入选题目

含解答

![](images/887553d1131f80d9bb9f062f009381d2eedbb3f6f9d9df11fbfef3957b1824c5.jpg)

# 含解答的入选题目

在下一届国际数学奥林匹克竞赛结束之前，入选题目必须严格保密。IMO总规章第6.6条

# 贡献国家

IMO 2024 组织委员会和题目遴选委员会感谢以下63个国家提交的229道题目提案：

阿尔及利亚，澳大利亚，阿塞拜疆，孟加拉国，白俄罗斯，巴西，保加利亚，加拿大，中国，哥伦比亚，克罗地亚，塞浦路斯，捷克共和国，丹麦，多米尼加共和国，厄瓜多尔，爱沙尼亚，法国，格鲁吉亚，德国，加纳，希腊，香港，印度，印度尼西亚，爱尔兰，伊朗，以色列，日本，哈萨克斯坦，科索沃，拉脱维亚，立陶宛，卢森堡，马来西亚，墨西哥，摩尔多瓦，荷兰，新西兰，挪威，秘鲁，波兰，葡萄牙，罗马尼亚，塞内加尔，塞尔维亚，新加坡，斯洛伐克，斯洛文尼亚，南非，韩国，西班牙，瑞典，瑞士，叙利亚，台湾，泰国，突尼斯，土耳其，乌干达，乌克兰，美国，乌兹别克斯坦。

# 题目遴选委员会

![](images/4a25c17d8e5d644bc1fc27cad1ac18895c2d2a125e774ac92c0bd73f8adc551c.jpg)

Aron Thomas，艾颖华，Andrew Ng，Géza Kos，郭胤，Alice Carlotti，James Aaronson，Sam Bealing，Adrian Agisilaou，James Cranch，Joseph Myers（主席），姚浩然，Maria-Romina Ivan，Michael Ren，Elisa Lorenzo Garcia

# Problems
# 代数
## A1.
确定所有实数 $\alpha$，使得对于每个正整数 $n$，数

$$
\lfloor \alpha \rfloor + \lfloor 2 \alpha \rfloor + \cdot \cdot \cdot + \lfloor n \alpha \rfloor
$$

是 $n$ 的倍数。（这里 $\lfloor z \rfloor$ 表示不超过 $z$ 的最大整数）

（哥伦比亚）


# Solutions
# 代数
## A1.
确定所有实数 $\alpha$，使得对于每个正整数 $n$，数

$$
\lfloor \alpha \rfloor + \lfloor 2 \alpha \rfloor + \cdot \cdot \cdot + \lfloor n \alpha \rfloor
$$

是 $n$ 的倍数。（这里 $\lfloor z \rfloor$ 表示不超过 $z$ 的最大整数）

（哥伦比亚）
**解法 1**. 首先我们证明所有偶整数满足条件。若 $\alpha = 2 m$，其中 $m$ 是整数，则

$$
\lfloor \alpha \rfloor + \lfloor 2 \alpha \rfloor + \cdot \cdot \cdot + \lfloor n \alpha \rfloor = 2 m + 4 m + \cdot \cdot \cdot + 2 m n = m n ( n + 1 )
$$

这是 $n$ 的倍数：

现在我们证明只有这些实数满足题设条件。设 $\alpha = k + \epsilon$，其中 $k$ 是整数且 $0 \leqslant \epsilon < 1$。则数

$$
\begin{array} { r } { \lfloor \alpha \rfloor + \lfloor 2 \alpha \rfloor + \dots + \lfloor n \alpha \rfloor = k + \lfloor \epsilon \rfloor + 2 k + \lfloor 2 \epsilon \rfloor + \dots + n k + \lfloor n \epsilon \rfloor } \\ { = \displaystyle \frac { k n ( n + 1 ) } { 2 } + \lfloor \epsilon \rfloor + \lfloor 2 \epsilon \rfloor + \dots + \lfloor n \epsilon \rfloor } \end{array}
$$

必须是 $n$ 的倍数。我们根据 $k$ 的奇偶性分两种情况讨论：

情况1：$k$ 为偶数。

此时 kn(n+1) 总是 n 的倍数。因此

$$
\lfloor \epsilon \rfloor + \lfloor 2 \epsilon \rfloor + \cdot \cdot \cdot + \lfloor n \epsilon \rfloor
$$

也必须是 $n$ 的倍数：

我们将用强归纳法证明对所有正整数 $n$ 有 $\lfloor n \epsilon \rfloor = 0$。基础情形 $n = 1$ 成立是因为 $0 \leqslant \epsilon < 1$。假设对所有 $1 \leqslant m < n$ 都有 $\lfloor m \epsilon \rfloor = 0$。则数

$$
\lfloor \epsilon \rfloor + \lfloor 2 \epsilon \rfloor + \cdot \cdot \cdot + \lfloor n \epsilon \rfloor = \lfloor n \epsilon \rfloor
$$

必须是 $n$ 的倍数。由于 $0 \leqslant \epsilon < 1$，那么 $0 \leqslant n \epsilon < n$，这意味着数 $\lfloor n \epsilon \rfloor$ 必须等于 $0$：

等式 $\lfloor n \epsilon \rfloor = 0$ 推出 $0 \leqslant \epsilon < 1 / n$。由于这对所有 $n$ 都必须成立，我们得出 $\epsilon = 0$，从而 $\alpha$ 是一个偶整数。

情况2：$k$ 为奇数。

我们将用强归纳法证明对所有自然数 $n$ 有 $\lfloor n \epsilon \rfloor = n - 1$。基础情形 $n = 1$ 再次由 $0 \leqslant \epsilon < 1$ 得出。假设对所有 $1 \leqslant m < n$ 有 $\lfloor m \epsilon \rfloor = m - 1$。我们需要数

$$
{ \begin{array} { r l } & { { \frac { k n ( n + 1 ) } { 2 } } + \left\lfloor \epsilon \right\rfloor + \left\lfloor 2 \epsilon \right\rfloor + \cdot \cdot \cdot + \left\lfloor n \epsilon \right\rfloor = { \frac { k n ( n + 1 ) } { 2 } } + 0 + 1 + \cdot \cdot \cdot + ( n - 2 ) + \left\lfloor n \epsilon \right\rfloor } \\ & { \qquad = { \frac { k n ( n + 1 ) } { 2 } } + { \frac { ( n - 2 ) ( n - 1 ) } { 2 } } + \left\lfloor n \epsilon \right\rfloor } \\ & { \qquad = { \frac { k + 1 } { 2 } } n ^ { 2 } + { \frac { k - 3 } { 2 } } n + 1 + \left\lfloor n \epsilon \right\rfloor } \end{array} }
$$

是 $n$ 的倍数。由于 $k$ 是奇数，我们需要 $1 + \lfloor n \epsilon \rfloor$ 是 $n$ 的倍数。又因为 $0 \leqslant \epsilon < 1$，所以 $0 \leqslant n \epsilon < n$，因此 $\lfloor n \epsilon \rfloor = n - 1$，正如我们所要证的。

这意味着对所有 $n$ 有 $\textstyle 1 - { \frac { 1 } { n } } \leqslant \epsilon < 1$，这是荒谬的。因此这种情况无解。
**解法 2**. 如解法1，我们验证所有偶整数满足条件。然后不失一般性可假设 $0 \leqslant \alpha < 2$。令 $S _ { n } = \lfloor \alpha \rfloor + \lfloor 2 \alpha \rfloor + \cdot \cdot \cdot + \lfloor n \alpha \rfloor$：注意到

$$
\begin{array} { l l } { { S _ { n } \equiv 0 } } & { { ( \mathrm { m o d } n ) } } \\ { { S _ { n } \equiv S _ { n } - S _ { n - 1 } = \lfloor n \alpha \rfloor } } & { { ( \mathrm { m o d } n - 1 ) } } \end{array}
$$

由于 $\operatorname* { g c d } ( n , n - 1 ) = 1$，(1) 和 (2) 推出

$$
S _ { n } \equiv n { \bigl \lfloor } n \alpha { \bigr \rfloor } { \pmod { n ( n - 1 ) } } .
$$

此外，

$$
0 \leqslant n \lfloor n \alpha \rfloor - S _ { n } = \sum _ { k = 1 } ^ { n } \left( \lfloor n \alpha \rfloor - \lfloor k \alpha \rfloor \right) < \sum _ { k = 1 } ^ { n } \left( n \alpha - k \alpha + 1 \right) = { \frac { n ( n - 1 ) } { 2 } } \alpha + n .
$$

当 $n$ 足够大时，(4) 的右边小于 $n ( n - 1 )$。于是 (3) 强制

$$
0 = S _ { n } - n { \big \lfloor } n \alpha { \big \rfloor } = \sum _ { k = 1 } ^ { n } { \Big ( } { \big \lfloor } n \alpha { \big \rfloor } - { \big \lfloor } k \alpha { \big \rfloor } { \Big ) }
$$

对足够大的 $n$ 成立。

由于当 $1 \leqslant k \leqslant n$ 时 $\lfloor n \alpha \rfloor - \lfloor k \alpha \rfloor \geqslant 0$，由 (5) 可得：对所有足够大的 $n$，上述不等式均为等式。特别地，对所有足够大的 $n$ 有 $\lfloor \alpha \rfloor = \lfloor n \alpha \rfloor$，除非 $\alpha = 0$，否则这是荒谬的。
**解法 3**. 如其他解法一样，不失一般性可假设 $0 \leqslant \alpha < 2$。偶整数满足条件，因此我们假设 $0 < \alpha < 2$，并导出矛盾。

对 $n$ 进行归纳，我们将同时证明

$$
\lfloor \alpha \rfloor + \lfloor 2 \alpha \rfloor + \cdot \cdot \cdot + \lfloor n \alpha \rfloor = n ^ { 2 } ,
$$

$$
\mathrm { a n d } \qquad { \frac { 2 n - 1 } { n } } \leqslant \alpha < 2 .
$$

基础情形为 $n = 1$：若 $\alpha < 1$，考虑 $\begin{array} { r } { m = \left| \frac { 1 } { \alpha } \right| > 1 } \end{array}$，则

$$
\lfloor \alpha \rfloor + \lfloor 2 \alpha \rfloor + \cdot \cdot \cdot + \lfloor m \alpha \rfloor = 1
$$

不是 $m$ 的倍数，因此我们得到 (7)。于是 $\lfloor \alpha \rfloor = 1$，从而 (6) 成立。

归纳步骤：假设对 $n$ 归纳假设成立，则由 (7)

$$
2 n + 1 - \frac { 1 } { n } \leqslant ( n + 1 ) \alpha < 2 n + 2 .
$$

因此，

$$
n ^ { 2 } + 2 n \leqslant \lfloor \alpha \rfloor + \lfloor 2 \alpha \rfloor + \cdot \cdot + \lfloor n \alpha \rfloor + \lfloor ( n + 1 ) \alpha \rfloor = n ^ { 2 } + \lfloor ( n + 1 ) \alpha \rfloor < n ^ { 2 } + 2 n + 2 .
$$

为了得到 $n + 1$ 的倍数，必须有 $\lfloor ( n + 1 ) \alpha \rfloor = 2 n + 1$ 且

$$
\lfloor \alpha \rfloor + \lfloor 2 \alpha \rfloor + \cdot \cdot \cdot + \lfloor n \alpha \rfloor + \lfloor ( n + 1 ) \alpha \rfloor = ( n + 1 ) ^ { 2 }
$$

这两个等式分别给出 (6) 和 (7)。最后，我们注意到对所有 $n$ 成立的条件 (7) 导致矛盾。
**解法 4**. 如其他解法，不失一般性我们假设 $0 < \alpha < 2$ 并导出矛盾。对每个 $n$，定义

$$
b _ { n } = { \frac { \lfloor \alpha \rfloor + \lfloor 2 \alpha \rfloor + \cdot \cdot \cdot + \lfloor n \alpha \rfloor } { n } } ,
$$

根据题设条件和我们的假设，这是一个非负整数。注意

$$
\lfloor ( n + 1 ) \alpha \rfloor \geqslant \left\lfloor \alpha \right\rfloor , \left\lfloor 2 \alpha \right\rfloor , \ldots , \left\lfloor n \alpha \right\rfloor \quad { \mathrm { a n d } } \quad \left\lfloor ( n + 1 ) \alpha \right\rfloor > \left\lfloor \alpha \right\rfloor
$$

对所有 $\textstyle n > { \frac { 1 } { \alpha } }$ 成立。由此可得当 $\textstyle n > { \frac { 1 } { \alpha } }$ 时 $b _ { n + 1 } > b _ { n } \implies b _ { n + 1 } \geqslant b _ { n } + 1$。因此，对所有这样的 $n$，

$$
b _ { n } \geqslant n + C
$$

其中 $C$ 是一个固定整数。另一方面，$b _ { n }$ 的定义给出

$$
b _ { n } = { \frac { \lfloor \alpha \rfloor + \lfloor 2 \alpha \rfloor + \cdot \cdot \cdot + \lfloor n \alpha \rfloor } { n } } \leqslant { \frac { \alpha + 2 \alpha + \cdot \cdot \cdot + n \alpha } { n } } = { \frac { \alpha } { 2 } } ( n + 1 ) ,
$$

这对足够大的 $n$ 是矛盾的。
**评论**. 上述解法的一个替代结尾如下。

由定义有 $S _ { n } \leqslant \alpha \frac { n ( n + 1 ) } { 2 }$，另一方面 (5) 意味着对所有足够大的 $n$ 有 $S _ { n } \geqslant \alpha n ^ { 2 } - n$，因此 $\alpha = 0$：