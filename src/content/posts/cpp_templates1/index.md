---
title: 模板元编程1：全特化与偏特化
published: 2026-03-25
description: '从一个通用的打印类出发，理解模板全特化与偏特化的语法、匹配规则与使用场景'
image: ''
tags: ['C++', '模板元编程']
category: 'C++'
draft: false
lang: ''
---

本文编译环境：clang-21，C++23标准。

模板的核心价值在于"通用性"——一份代码适配多种类型。但通用性不是万能的，某些特定类型需要完全不同的实现。**模板特化**就是为这些特例"开后门"的机制。

## 全特化

假设我们有这样一个 `my_printer`：

```cpp
template<typename T>
class my_printer {
public:
    void print(const T& obj) {
        std::println("Default print: {}", obj);
    }
};
```

对大部分基础类型，这个模板能直接工作：

```cpp
my_printer<float> p1;
p1.print(114.514f);       // Default print: 114.514

my_printer<int> p2;
p2.print(1919810);        // Default print: 1919810

my_printer<std::string> p3;
p3.print("hello");        // Default print: hello
```

但如果 `T` 是 `std::vector<int>` 呢？C++23之前，`vector` 没有直接支持 `{}` 格式化，通用模板无法打印它的内容，需要我们单独处理。

> C++23中完全支持以下写法：
>
> ```cpp
> #include <format>
> #include <vector>
> #include <print>
> 
> int main() {
>     std::vector v = {1, 2, 3};
>     std::println("{}", v);  // C++23 输出：[1, 2, 3]
> }
> ```

针对 `vector<int>` 的**全特化**写法：

```cpp
template<>
class my_printer<std::vector<int>> {
public:
    void print(const std::vector<int>& v) {
        std::print("Vector<int> print:");
        for (const auto& i : v) {
            std::print(" {}", i);
        }
        std::println();
    }
};
```

语法要点：

- `template<>` 表示全特化，尖括号内**没有**任何模板参数
- `my_printer<std::vector<int>>` 中的 `<std::vector<int>>` 精确指定了这套实现生效的类型

调用效果：

```cpp
std::vector vec{114, 514, 1919, 810};
my_printer<std::vector<int>> p4;
p4.print(vec);  // Vector<int> print: 114 514 1919 810
```

编译器遇到 `my_printer<std::vector<int>>` 时，会优先匹配全特化版本，而不是通用模板。

## 偏特化

全特化解决了 `vector<int>` 的问题，但如果我们想打印 `vector<float>`、`vector<std::string>`……难道要为每种元素类型都写一份全特化吗？

更合理的做法是**偏特化**——对 `vector<ElemType>` 这一整类类型统一处理，其中 `ElemType` 仍然是未确定的模板参数：

```cpp
template<typename ElemType>
class my_printer<std::vector<ElemType>> {
public:
    void print(const std::vector<ElemType>& v) {
        std::print("Vector print:");
        for (const auto& i : v) {
            std::print(" {}", i);
        }
        std::println();
    }
};
```

与全特化的语法区别：

- `template<typename ElemType>` 保留了未确定的参数（全特化是 `template<>`）
- `my_printer<std::vector<ElemType>>` 中的 `<std::vector<ElemType>>` 描述的是一个**模式**，而不是一个精确类型

现在 `my_printer<std::vector<ElemType>>` 对任意 `ElemType` 都能工作：

```cpp
std::vector<float> vf{1.1f, 2.2f, 3.3f};
my_printer<std::vector<float>> p5;
p5.print(vf);   // Vector print: 1.1 2.2 3.3

std::vector<std::string> vs{"hello", "world"};
my_printer<std::vector<std::string>> p6;
p6.print(vs);   // Vector print: hello world
```

### 偏特化的另一种用途：指针模式

偏特化不仅能匹配容器类型，还能匹配类型的结构特征（如"是否是指针"）。以下面的 `my_pair` 为例：

```cpp
template<typename T, typename U>
class my_pair {
public:
    T first;
    U second;
    my_pair(T f, U s) : first(f), second(s) {}
    void show() const {
        std::println("Default show: ({}, {})", first, second);
    }
};
```

默认情况下：

```cpp
my_pair pr1(114, 514);
pr1.show();   // Default show: (114, 514)

int x = 810;
my_pair pr2(1919, &x);
pr2.show();   // Default show: (1919, 0x...)  ← 输出的是指针地址，不是值
```

`pr2` 的第二个参数是指针，通用模板直接打印地址。如果我们希望当第二个参数是指针时自动解引用输出值，可以对 `<T, U*>` 做偏特化：

```cpp
template<typename T, typename U>
class my_pair<T, U*> {
public:
    T first;
    U* second;
    my_pair(T f, U* s) : first(f), second(s) {}
    void show() const {
        std::println("<T, U*> show: ({}, {})", first, *second);  // 解引用
    }
};

int main() {
    my_pair pr2(1919, &x);
    pr2.show();   // <T, U*> show: (1919, 810)
}
```

这里偏特化的匹配条件是"第二个参数是某种类型的指针"，`T` 和 `U` 仍然是自由的模板参数——这就是偏特化"只对部分参数施加约束"的含义。

## 全特化 vs 偏特化

|          | 全特化                     | 偏特化                                |
| -------- | -------------------------- | ------------------------------------- |
| 语法     | `template<>`               | `template<typename ...>` 保留部分参数 |
| 匹配方式 | 精确匹配特定类型           | 匹配符合某种模式的一类类型            |
| 典型用途 | 针对单一特殊类型的定制实现 | 针对指针、容器、模板类等整类类型      |

当同时存在多个候选时，编译器的优先级是：

> **全特化** > **最匹配的偏特化** > **通用模板**

全特化的匹配最精确，因此优先级最高；多个偏特化之间选择"最具体"的那个（最窄的模式）；通用模板是兜底选项。