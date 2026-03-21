---
title: Fuwari使用教程
published: 2026-03-18
description: 汇总 Fuwari 主题的完整使用说明，涵盖文章配置、Markdown 语法、代码块增强、扩展功能及视频嵌入。
image: ''
tags: [Fuwari, 教程]
category: '系统'
draft: false
lang: ''
---

## 一、文章 Front-matter 字段

每篇文章的开头需要包含 YAML front-matter，用于配置文章的元信息：

```yaml
---
title: 我的第一篇博客
published: 2024-01-01
description: 这是文章的简短描述，会显示在首页卡片上。
image: ./cover.jpg
tags: [标签1, 标签2]
category: 分类名
draft: false
---
```

| 字段          | 说明                                                                                                                         |
|---------------|------------------------------------------------------------------------------------------------------------------------------|
| `title`       | 文章标题                                                                                                                     |
| `published`   | 发布日期                                                                                                                     |
| `description` | 文章简介，显示在首页卡片                                                                                                     |
| `image`       | 封面图路径。以 `http://` 或 `https://` 开头则使用网络图片；以 `/` 开头则相对于 `public/` 目录；否则相对于当前 Markdown 文件 |
| `tags`        | 标签列表                                                                                                                     |
| `category`    | 分类                                                                                                                         |
| `draft`       | 是否为草稿。设为 `true` 时文章不会对外展示                                                                                   |

---

## 二、文章文件组织

所有文章放在 `src/content/posts/` 目录下，支持两种形式：

```
src/content/posts/
├── single-file-post.md       # 单文件形式
└── post-with-assets/         # 目录形式（推荐，方便管理图片等资源）
    ├── cover.png
    └── index.md
```

---

## 三、草稿

将 front-matter 中的 `draft` 设为 `true`，文章就不会公开显示：

```yaml
---
title: 还没写完的文章
draft: true
---
```

写完后改为 `draft: false` 即可发布。

---

## 四、标准 Markdown 语法

### 基础格式

```markdown
_斜体_、**粗体**、`行内代码`

> 引用块

---  （水平分割线）
```

### 列表

```markdown
- 无序列表项1
- 无序列表项2

1. 有序列表项1
2. 有序列表项2
```

### 链接与图片

```markdown
[链接文字](https://example.com)

![图片描述](./image.png)
```

### 表格

```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| A   | B   | C   |
```

### 数学公式

行内公式用单个 `$`，块级公式用 `$$`：

```markdown
行内公式：$\omega = d\phi / dt$

块级公式：
$$
I = \int \rho R^{2} dV
$$
```

### 脚注

```markdown
这里有一个脚注[^1]。

[^1]: 脚注内容写在这里。
```

---

## 五、扩展 Markdown 功能

### GitHub 仓库卡片

自动从 GitHub API 拉取仓库信息并显示为卡片：

```markdown
::github{repo="owner/repo-name"}
```

### 提示块（Admonitions）

支持五种类型：`note`、`tip`、`important`、`warning`、`caution`

```markdown
:::note
这是一条注意事项。
:::

:::tip
这是一条小技巧。
:::

:::important
这是重要信息。
:::

:::warning
这是警告信息。
:::

:::caution
这是危险提示。
:::
```

效果预览：

:::note
这是一条注意事项。
:::

:::tip
这是一条小技巧。
:::

:::warning
这是警告信息。
:::

#### 自定义标题

```markdown
:::note[自定义标题]
内容...
:::
```

#### GitHub 风格语法

```markdown
> [!NOTE]
> 也支持 GitHub 风格的提示块语法。

> [!TIP]
> 同样支持。
```

### 剧透遮罩

```markdown
内容 :spoiler[被隐藏的文字] 继续。
```

效果：内容 :spoiler[被隐藏的文字] 继续。

---

## 六、代码块增强（Expressive Code）

### 语法高亮

直接在代码块后加语言名即可：

```js
console.log('Hello World')
```

### 显示文件名

通过 `title` 属性显示文件名：

```js title="my-file.js"
console.log('带文件名的代码块')
```

### 终端样式

`bash`、`sh`、`powershell` 等语言会自动渲染为终端样式：

```bash
echo "这是终端样式的代码块"
```

```powershell title="PowerShell 示例"
Write-Output "这是带标题的 PowerShell 终端"
```

### 行高亮标记

用 `{行号}` 语法高亮指定行：

```js {1, 4}
// 第1行高亮
// 第2行普通
// 第3行普通
// 第4行高亮
```

### 新增/删除标记

用 `ins` 和 `del` 标记新增/删除行：

```js title="line-markers.js" del={2} ins={3-4}
function demo() {
  console.log('这行被标记为删除')
  // 这行被标记为新增
  console.log('这也是新增行')
  return true
}
```

### diff 语法

````markdown
```diff lang="js"
  function demo() {
-   console.log('旧代码')
+   console.log('新代码')
  }
```
````

效果预览：

```diff lang="js"
  function demo() {
-   console.log('旧代码')
+   console.log('新代码')
  }
```

### 行内文字高亮

用 `"文字"` 语法高亮行内指定内容：

```js "指定文字"
// 高亮行内某段指定文字
return '这里的 指定文字 会被高亮，所有匹配都会高亮';
```

也可以组合 `ins` / `del` 做行内标记：

```js "return true;" ins="inserted" del="deleted"
function demo() {
  console.log('inserted 和 deleted 是行内标记');
  return true;
}
```

### 折叠代码段

用 `collapse={行范围}` 折叠不重要的部分：

```js collapse={1-4, 11-13}
// 这些 import 会被折叠
import { someBoilerplateEngine } from '@example/some-boilerplate'
import { evenMoreBoilerplate } from '@example/even-more-boilerplate'
const engine = someBoilerplateEngine(evenMoreBoilerplate())

// 这部分默认展开
engine.doSomething(1, 2, 3)

function calcFn() {
  const a = 1, b = 2
  // 这部分也会被折叠
  console.log(`结果: ${a} + ${b} = ${a + b}`)
  return a + b
}
```

### 显示行号

```js showLineNumbers
// 显示行号
console.log('第2行')
console.log('第3行')
```

指定起始行号：

```js showLineNumbers startLineNumber=10
console.log('从第10行开始编号')
console.log('第11行')
```

### 自动换行

加 `wrap` 参数后超长行会自动换行：

```js wrap
// 开启换行后，下面这行超长内容不会产生横向滚动条，而是自动折到下一行显示
function getLongString() {
  return 'This is a very long string that will most probably not fit into the available space unless the container is extremely wide'
}
```

---

## 七、嵌入视频

直接在 Markdown 中粘贴 iframe 嵌入代码即可。

### YouTube

```html
<iframe width="100%" height="468"
  src="https://www.youtube.com/embed/VIDEO_ID"
  title="YouTube video player"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  allowfullscreen>
</iframe>
```

### Bilibili

```html
<iframe width="100%" height="468"
  src="//player.bilibili.com/player.html?bvid=BV_ID&p=1"
  scrolling="no" border="0" frameborder="no"
  framespacing="0" allowfullscreen="true">
</iframe>
```

将 `VIDEO_ID` / `BV_ID` 替换为对应视频的 ID 即可。
