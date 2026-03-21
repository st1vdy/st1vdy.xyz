---
title: 傅里叶变换
published: 2026-03-19
description: '从傅里叶级数的复数形式推导傅里叶变换，并介绍离散傅里叶变换（DFT）与FFT的基本思想。'
image: ''
tags: [高等数学, 傅里叶变换]
category: '数学'
draft: false 
lang: ''
---

## 傅里叶级数的复数形式

### 推导

在傅里叶级数章节中，我们已知一个周期为 $2l$ 的周期函数可以展开为
$$
f(x) = a_0 + \sum_{i=1}^{\infty}a_i \cos \frac{i\pi x}{l} + \sum_{i=1}^{\infty} b_i\sin \frac{i\pi x}{l}
$$
为了方便起见，我们作如下定义：常数项 $a_0$ 记作 $\frac{a_0}{2}$，设周期 $T=2l$，记 $\omega = \frac{2\pi}{T}$，则有
$$
f(t) = \frac{a_0}{2} + \sum_{n=1}^{\infty}a_n\cos n\omega t + \sum_{n=1}^{\infty}b_n\sin n\omega t
$$
根据欧拉公式 $e^{i\theta} = \cos\theta + i\sin\theta$ 的推论 $\begin{cases}\cos\theta = \frac{1}{2}(e^{i\theta} + e^{-i\theta})\\ \sin\theta = -\frac{1}{2}i(e^{i\theta}-e^{-i\theta})\end{cases}$，代入傅里叶级数的表达式中就有
$$
\begin{aligned}
f(t) &= \frac{a_0}{2} + \sum_{n=1}^{\infty} \bigg[\frac{a_n}{2}(e^{in\omega t}+e^{-in\omega t}) - \frac{ib_n}{2}(e^{in\omega t}-e^{-in\omega t})\bigg]\\
&= \frac{a_0}{2} + \sum_{n=1}^{\infty} \bigg[\frac{a_n-ib_n}{2}e^{in\omega t} + \frac{a_n+ib_n}{2}e^{-in\omega t}\bigg]\\
&= \frac{a_0}{2} + \sum_{n=1}^{\infty}\frac{a_n-ib_n}{2}e^{in\omega t} + \sum_{n=1}^{\infty}\frac{a_n+ib_n}{2}e^{-in\omega t}\\
&= \sum_{n=0}^0\frac{a_0}{2}e^{in\omega t} + \sum_{n=1}^{\infty}\frac{a_n-ib_n}{2}e^{in\omega t} + \sum_{n=-\infty}^{-1}\frac{a_{-n}+ib_{-n}}{2}e^{in\omega t}\quad(令n为-n)\\
&= \sum_{n=-\infty}^{\infty} c_ne^{in\omega t}
\end{aligned}
$$
这里，$c_n = \begin{cases}\frac{a_0}{2} & n=0\\ \frac{a_n-ib_n}{2} & n\gt 0\\ \frac{a_{-n}+ib_{-n}}{2} & n\lt 0\end{cases}$，根据常数项 $a_n,b_n$ 在傅里叶级数中的公式可知 $\begin{cases}a_0 = \frac{2}{T}\int_0^T f(t)\mathrm dt\\ a_n = \frac{2}{T}\int_0^Tf(t)\cos n\omega t\mathrm dt\\ b_n=\frac{2}{T}\int_0^T f(t)\sin n\omega t\mathrm dt\end{cases}$，代入 $c_n$ 的表达式就有
$$
c_n = \begin{cases}
\begin{aligned}
\frac{a_0}{2} &= \frac{1}{2}\cdot \frac{2}{T}\int_0^Tf(t)\mathrm dt\\
&= \frac{1}{T}\int_0^Tf(t)\mathrm dt
\end{aligned}& n=0\\
\\
\begin{aligned}
\frac{a_n-ib_n}{2} &= \frac{1}{2}\cdot\bigg(\frac{2}{T}\int_0^T f(t)\cos n\omega t\mathrm dt - i\frac{2}{T}\int_0^Tf(t)\sin n\omega t \mathrm dt\bigg)\\
&= \frac{1}{T}\int_0^Tf(t)(\cos n\omega t - i\sin n\omega t)\mathrm dt\\
&= \frac{1}{T}\int_0^Tf(t)(\cos (-n\omega t) + i\sin (-n\omega t))\mathrm dt\quad(奇偶性)\\
&= \frac{1}{T}\int_0^Tf(t)e^{-in\omega t}\mathrm dt \quad(欧拉公式)\\
\end{aligned} & n\gt 0\\
\\
\begin{aligned}
\frac{a_{-n}+ib_{-n}}{2} &= \frac 12\cdot\bigg(\frac 2 T \int_0^T f(t)\cos(-n\omega t)\mathrm dt + i\frac 2T \int_0^T f(t)\sin(-n\omega t)\mathrm dt\bigg)\\
&= \frac 1T \int_0^T f(t)e^{-in\omega t}\mathrm dt\\
\end{aligned} & n\lt 0
\end{cases}
$$
注意到 $n\gt 0,n\lt 0$ 两种情况的积分是完全一致的，所以
$$
c_n=\begin{cases}
\frac{1}{T}\int_0^Tf(t)\mathrm dt & n=0\\
\frac{1}{T}\int_0^Tf(t)e^{-in\omega t}\mathrm dt & n\neq0\\
\end{cases} = \frac{1}{T}\int_0^Tf(t)e^{-in\omega t}\mathrm dt
$$

### 结论

根据上方推导，我们可以得出结论：对于一个周期为 $T$ 的复变函数 $f(t)$，可以展开为傅里叶级数
$$
f(t) = \sum_{n=-\infty}^{\infty} c_ne^{in\omega t}
$$
其中
$$
c_n=\frac{1}{T}\int_0^Tf(t)e^{-in\omega t}\mathrm dt
$$

## 傅里叶变换

### 傅里叶变换

上文已经得出了傅里叶级数的复数形式，即一个周期为 $T$ 的函数 $f_T(t)$可以展开为
$$
\begin{aligned}
f(t) &= \sum_{n=-\infty}^{\infty} c_n e^{in\omega t}\\
&= \sum_{n=-\infty}^{\infty} (\frac{1}{T}\int_{-\frac T 2}^{\frac T 2}f(t)e^{-in\omega t}\mathrm dt) e^{in\omega t}\\
\end{aligned}
$$
对于这个式子，我们可以将 $n\omega$ 视作一个整体，也就是说傅里叶级数实际上是在枚举不同频率 $\cdots,1\omega,2\omega,\cdots,n \omega,\cdots$。可以想象一个数轴，该数轴上的点均为 $n\omega$，每个点的值对应一个复数 $c_n$。根据该思想，记 $\omega_0 = \frac{2\pi}{T}$（这个参数也被称为是基频率），那么傅里叶级数就是在枚举基频率 $\cdots,1\omega_0,2\omega_0,\cdots,n \omega_0,\cdots$，于是傅里叶级数就可以用基频率表示为
$$
\begin{aligned}
f(t) &= \sum_{n=-\infty}^{\infty} c_n e^{in\omega_0 t}\\
&= \sum_{n=-\infty}^{\infty} (\frac{1}{T}\int_{-\frac T 2}^{\frac T 2}f(t)e^{-in\omega_0 t}\mathrm dt) e^{in\omega_0 t}\\
\end{aligned}
$$
对于一个非周期函数 $f(t)$，我们能否也将其展开为傅里叶级数呢？答案就是傅里叶变换，我们可以将这个非周期函数 $f(t)$ 视作一个周期为 $\infty$ 的“周期函数”。当 $T\rightarrow\infty$ 时，$\omega_0\rightarrow 0$，此时对于基频率 $\omega_0$ 的枚举就从一个离散函数变成了一个连续函数。

记 $\Delta\omega = (n+1)\omega_0 - n\omega_0 = \omega_0 = \frac{2\pi}{T}$，$\omega = n\omega_0$ 则
$$
\begin{aligned}
f(t) &= \sum_{n=-\infty}^{\infty} (\frac{1}{T}\int_{-\frac T 2}^{\frac T 2}f(t)e^{-in\omega_0 t}\mathrm dt) e^{in\omega_0 t}\\
&= \sum_{n=-\infty}^{\infty}\frac{\Delta\omega}{2\pi}\int_{-\frac T 2}^{\frac T 2}f(t)e^{-i\omega t}\mathrm dt\cdot e^{i\omega t}\\
&= \frac{1}{2\pi}\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}f(t)e^{-i\omega t}\mathrm dt\mathrm\cdot e^{i\omega t} d\omega\quad(T\rightarrow \infty,\omega_0\rightarrow 0)
\end{aligned}
$$
这里可以类比定积分的几何意义（在区间 $[a,b]$ 内取 $n-1$ 个分点 $a=x_0\lt x_1\lt \cdots\lt x_{n}=b$，记 $\Delta x_i = x_i-x_{i-1}$，$\xi_i\in(x_{i-1},x_i)$，则 $\int_a^b f(x)\mathrm dx = \lim_{n\rightarrow\infty}\sum_{i=1}^n f(\xi_i)\Delta x_i$），只不过上下限都变成了无穷（不定积分）。

记 $F(\omega)=\int_{-\infty}^{\infty}f(t)e^{-i\omega t}\mathrm dt$，该式就是**傅里叶变换**，而 $f(t) = \frac{1}{2\pi}\int_{-\infty}^{\infty}F(\omega)e^{i\omega t}\mathrm d\omega$ 就是**逆傅里叶变换**。

### 离散傅里叶变换（DFT）

在实际应用中，我们很难做到对连续函数做傅里叶变换，但是可以对函数进行采样，然后做离散傅里叶变换，公式为
$$
X_k = \sum_{n=0}^{N-1}x_ne^{-i \frac{2\pi }{N}nk}
$$
假设我们已知序列 $x_0,x_1,\cdots,x_{N-1}$ 的值，那我们根据离散傅里叶变换公式就能求出对应的 $X_0,X_1,\cdots,X_{N-1}$ 了。这里 $N$ 是所分析函数/信号的长度（采样区间），$x_0,x_1,\cdots,x_{N-1}$ 可以视作是我们对连续信号的离散采样。

同理存在离散傅里叶逆变换
$$
x_k = \frac 1N \sum_{n=0}^{N-1}X_ne^{i \frac{2\pi}{N}nk}
$$

> 对于离散傅里叶变换，如果用 $N$ 阶单位根（$W_{N,k}=e^{-i\frac{2\pi}{N}k}$）代入，则
> $$
> X_k=\sum_{n=0}^{N-1}x_n W_{N,k}^{n}
> $$
> 实际上，这就是在求一个多项式 $f(t)=x_0+x_1t+x_2t^2+\cdots+x_{N-1}t^{N-1}$ 在 $N$ 阶单位根构成的群上的点值表示，这个问题可以用Cooley–Tukey算法等优化至 $O(N\log N)$ 的复杂度，也就是快速傅里叶变换（FFT）。