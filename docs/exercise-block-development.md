# 题目与题解块开发记录

本文以 `problem` / `solution` 题目与题解块的开发为例，说明如何在当前 Fuwari 博客中新增一组 Markdown 扩展模块。目标是让文章可以使用类似提示块的语法，同时拥有独立语义与统一视觉风格。

## 目标

原始需求是把例题和题解从普通标题、引用或 `note` 提示块中拆出来，形成专门的语义模块：

```md
:::problem[例1]
这里写题目内容。
:::

:::solution[题解]
这里写题解内容，默认折叠。
:::
```

设计目标：

- `problem` 表示题目，不占用 `note` 的语义。
- `solution` 表示题解，默认折叠，点击标题后展开。
- 两者视觉上继承 Fuwari 现有 admonition 风格，包括左侧色条、标题图标、主题色与排版节奏。
- 题目块和题解块左侧色条必须严格对齐。
- Markdown 内仍然支持数学公式、列表、段落、代码块等常规内容。

## 相关机制

本项目已经接入了 Markdown directive 与 rehype 组件渲染链路，核心配置在 `astro.config.mjs`：

```js
remarkPlugins: [
  remarkMath,
  remarkReadingTime,
  remarkExcerpt,
  remarkGithubAdmonitionsToDirectives,
  remarkDirective,
  remarkSectionize,
  parseDirectiveNode,
],
rehypePlugins: [
  rehypeKatex,
  rehypeSlug,
  [
    rehypeComponents,
    {
      components: {
        note: (x, y) => AdmonitionComponent(x, y, "note"),
        // ...
      },
    },
  ],
],
```

其中：

- `remark-directive` 负责识别 `:::name[title] ... :::` 这类语法。
- `parseDirectiveNode` 会把 directive label 标记到节点属性里。
- `rehype-components` 会根据 directive 名称调用对应组件函数。
- 现有 `AdmonitionComponent` 已经提供了 `note`、`tip`、`warning` 等提示块的实现参考。

因此新增模块时，不需要重新写 Markdown 解析器，只要：

1. 新增组件函数。
2. 在 `astro.config.mjs` 注册组件名。
3. 在样式文件中补齐对应 class。
4. 在文章中使用新 directive。

## 组件实现

新增文件：`src/plugins/rehype-component-exercise.mjs`

该文件导出两个组件：

- `ProblemComponent`：渲染为 `blockquote.admonition.exercise-block.bdm-problem`。
- `SolutionComponent`：渲染为 `details.admonition.exercise-block.bdm-solution`。

实现要点：

- 通过 `properties["has-directive-label"]` 判断是否存在 `[标题]`。
- 如果存在标题，取 `children[0]` 作为标题内容，并把它从正文中移除。
- `problem` 使用 `blockquote`，保持与现有提示块接近的语义和样式基础。
- `solution` 使用原生 `details` / `summary`，获得无 JavaScript 的折叠能力。
- 正文包在 `.bdm-content` 中，方便处理展开后的间距。

示意结构：

```html
<blockquote class="admonition exercise-block bdm-problem">
  <span class="bdm-title">例1</span>
  <p>题目内容</p>
</blockquote>

<details class="admonition exercise-block bdm-solution">
  <summary class="bdm-title">题解</summary>
  <div class="bdm-content">
    <p>题解内容</p>
  </div>
</details>
```

## 配置注册

修改 `astro.config.mjs`，引入组件：

```js
import { ProblemComponent, SolutionComponent } from "./src/plugins/rehype-component-exercise.mjs";
```

然后在 `rehypeComponents` 的 `components` 中注册：

```js
components: {
  github: GithubCardComponent,
  note: (x, y) => AdmonitionComponent(x, y, "note"),
  tip: (x, y) => AdmonitionComponent(x, y, "tip"),
  important: (x, y) => AdmonitionComponent(x, y, "important"),
  caution: (x, y) => AdmonitionComponent(x, y, "caution"),
  warning: (x, y) => AdmonitionComponent(x, y, "warning"),
  problem: ProblemComponent,
  solution: SolutionComponent,
},
```

注册完成后，Markdown 中的 `:::problem` 和 `:::solution` 就会进入对应组件。

## 样式设计

样式主要写在 `src/styles/markdown-extend.styl`。

最初题目块和题解块分别继承了 `blockquote` 与 `details` 的不同默认布局，导致左侧蓝色条和绿色条没有完全对齐。最终做法是给两者增加统一的基础 class：`exercise-block`。

关键原则：

- `blockquote.exercise-block` 和 `details.exercise-block` 使用同一套 `position`、`margin`、`padding-left`。
- 左侧色条统一由 `&:before` 绘制，且 `left: 0`。
- 不再让 `details` 自己模拟一个近似布局，而是和 `blockquote` 共享布局基线。

核心结构：

```stylus
.custom-md
  blockquote.exercise-block,
  details.exercise-block
    position: relative
    margin: 1.6em 0
    padding-left: 1.25rem
    border: 0
    font-weight: inherit

    &:before
      content: ''
      position: absolute
      left: 0
      top: 0
      display: block
      width: .25rem
      height: 100%
      border-radius: 999px
      background: var(--btn-regular-bg)
```

然后分别定义题目与题解的颜色、图标、展开箭头：

- `bdm-problem` 使用 `var(--admonitions-color-note)`，视觉上接近“题目/信息”。
- `bdm-solution` 使用 `var(--admonitions-color-tip)`，视觉上接近“提示/解法”。
- `summary.bdm-title` 去掉浏览器默认 marker，自定义右侧箭头。
- `details[open]` 时旋转箭头。

## 内容迁移

以 `src/content/posts/formal_power_series1/fps1.md` 为验收文章：

- 原先的 `:::note[例n]` 改为 `:::problem[例n]`。
- 每个题解段落包入 `:::solution[题解]`。
- 题解之外的解释性正文保持在外面，例如例 1 后续的概念讲解、例 12 的 bonus 引用。

迁移后的典型片段：

```md
:::problem[例1]
给定集合 $A=\{2,3\}$，$B=\{2,4\}$，$C=\{3,5,7\}$。从每个集合中各选 $1$ 个元素 $a,b,c$。有多少种选法能使得 $a+b+c=n$？
:::

:::solution[题解]
解：$[x^{n}](x^{2}+x^{3})(x^{2}+x^{4})(x^{3}+x^{5}+x^{7})$。
:::
```

同时在 `src/content/posts/fuwari_guide/index.md` 中补充了新语法说明，方便后续写作时查阅。

## 构建问题与修复

开发过程中，`astro build` 暴露了一个既有样式问题：

```css
@apply btn-regular-dark ...
```

该写法位于 `src/styles/markdown.css`，它跨文件 `@apply` 了一个在 `main.css` 中定义的自定义 class。在当前构建链路中，Tailwind 无法保证这个自定义 class 对 `markdown.css` 可见，因此报错：

```txt
The `btn-regular-dark` class does not exist.
```

修复方式是把 `btn-regular-dark` 展开为它原本代表的原子类，不改变视觉效果：

```css
@apply flex items-center justify-center
  bg-[oklch(0.45_0.01_var(--hue))]
  hover:bg-[oklch(0.50_0.01_var(--hue))]
  active:bg-[oklch(0.55_0.01_var(--hue))]
  dark:bg-[oklch(0.30_0.02_var(--hue))]
  dark:hover:bg-[oklch(0.35_0.03_var(--hue))]
  dark:active:bg-[oklch(0.40_0.03_var(--hue))]
  ...;
```

这类修复属于构建链路稳定性修复，与题目/题解组件本身无关，但会影响新模块能否通过完整构建。

## 验证流程

本次使用了三类验证。

### 1. 静态搜索

确认目标文章中有 13 个题目块和 13 个题解块：

```sh
rg -n "^:::(problem|solution)\[" src/content/posts/formal_power_series1/fps1.md
```

### 2. 构建验证

运行：

```sh
pnpm astro build
```

在本地环境中如果没有 `pnpm`，也可以使用项目本地 Astro 可执行文件：

```sh
./node_modules/.bin/astro build
```

实际验证结果：`astro build` 通过。

`astro check` 仍然存在仓库既有类型错误，位置包括：

- `src/components/Navbar.astro`
- `src/pages/archive.astro`

这些类型错误与本次新增的题目/题解模块无关。

### 3. 浏览器验证

在预览页中确认：

- 页面中存在 13 个 `blockquote.admonition.bdm-problem`。
- 页面中存在 13 个 `details.admonition.bdm-solution`。
- `solution` 默认没有 `open` 属性，即默认折叠。
- 点击 `summary` 后 `details` 获得 `open` 属性，即可以展开。
- 题目块与题解块左侧色条严格对齐。

对齐验证可在浏览器控制台中执行：

```js
const problem = document.querySelector("blockquote.exercise-block.bdm-problem");
const solution = document.querySelector("details.exercise-block.bdm-solution");
const pb = problem.getBoundingClientRect();
const sb = solution.getBoundingClientRect();

console.log({
  problemLeft: pb.left,
  solutionLeft: sb.left,
  delta: Math.abs(pb.left - sb.left),
});
```

本次最终结果：

```txt
problemLeft: 21
solutionLeft: 21
delta: 0
```

## 后续新增类似模块的建议

如果以后还要新增类似 Markdown 模块，可以按以下流程走：

1. 先确认模块是否应该拥有独立语义，还是可以复用 `note`、`tip`、`warning`。
2. 如果需要独立语义，新建一个 rehype component 文件。
3. 组件里统一处理 directive label，避免每个组件重复解析 `[标题]`。
4. 在 `astro.config.mjs` 的 `rehypeComponents.components` 中注册新 directive 名称。
5. 在 `markdown-extend.styl` 中尽量复用现有 `.admonition`、`.bdm-title`、颜色变量和图标规则。
6. 如果多个块在视觉上属于同一组，提取共享 class，例如这次的 `exercise-block`。
7. 用真实文章迁移一组内容作为验收样例。
8. 至少运行一次 `astro build`，再用浏览器确认 DOM、交互和视觉对齐。

## 本次涉及文件

- `astro.config.mjs`
- `src/plugins/rehype-component-exercise.mjs`
- `src/styles/markdown-extend.styl`
- `src/styles/markdown.css`
- `src/content/posts/formal_power_series1/fps1.md`
- `src/content/posts/fuwari_guide/index.md`
