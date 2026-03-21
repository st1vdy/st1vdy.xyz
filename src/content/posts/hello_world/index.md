---
title: Hello World
published: 2026-03-18
description: ''
image: ''
tags: []
category: ''
draft: false 
lang: ''
---

# Hello World

## TL;DR

自从我2020年开始构建博客以来已经过了六年，我尝试了博客园、云服务器+wordpress、hexo等方案，现在我计划重新将博客迁移至astro框架+fuwari主题的方案。

## Hello New World

我的上一代自建博客基于 [wordpress](https://github.com/WordPress/WordPress) + [argon theme](https://github.com/solstice23/argon-theme)，我初次接触argon是在洛谷的主题商店，翻了作者的github发现有wordpress版本的主题就直接决定用这套方案了。wordpress的创作体验类似于博客园，都可以通过一个后台的管理系统进行发文和管理，但是wordpress毕竟是自行搭建的，可定制化程度远高于博客园，适合我这样愿意折腾的人。

但是过去几年来，我愈发感觉wordpress的发文流相对落后了，这主要是以下几个原因：

1. wordpress原生的Gutenberg编辑器和我常用的markdown（Typora）格式并不完美兼容，这就导致我很难直接将我的markdown笔记复制到服务端；
2. 在现在ai辅助开发的生产流水线中，ai辅助是至关重要的一环，就算我写好笔记、文章后也会让ai进行校对，但是wordpress的发文流让我不得不多进行一层“人工转译”（Typora to Gutenberg），而不是直接写好markdown就完工；
3. wordpress的后台管理界面虽然适合非编程环境下使用，但是对于需要氪金的云服务器运行成本较高；
4. argon已不再更新，而我在发文过程中遇到了非常多的bug，包括latex渲染、代码高亮等；

综上所述，我决定迁移到[astro](https://github.com/withastro/astro)框架，astro是现代前端框架下的静态站点，不需要像wordpress那种动态网站占用大量资源，完全可以做到在本地开发+上传静态资源到云服务器的发文流。

迁移以后的发文流将会是：
 - 本地编写markdown文章
 - github作为云端备份
 - 导出静态页面上传云服务器

因此，今后的文章原稿将会在github上完全开源（`src/content/posts`）。

::github{repo="st1vdy/st1vdy.xyz"}

由于时间问题，暂时不支持评论系统，如果遇到typo可以直接[QQ](https://qm.qq.com/q/VcpLevlI0c)联系，以后有空可能会加上……有生之年……