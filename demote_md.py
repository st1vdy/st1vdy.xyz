#!/usr/bin/env python3
"""
demote_headings.py — 将 Markdown 文件中所有标题下调一级，删除原一级标题。
注意：会跳过 LaTeX 公式区域（$...$ / $$...$$  / ```...```）内的 # 符号。
"""

import argparse
import re
from pathlib import Path

# ── 在这里修改默认路径，便于在 IDE 中直接运行 ──────────────────────
DEFAULT_INPUT  = "/home/st1vdy/dy/astro/st1vdy/src/content/posts/segment_tree_tutorial/index.md"   # 输入文件路径
DEFAULT_OUTPUT = ""           # 输出文件路径，留空则原地修改输入文件
# ──────────────────────────────────────────────────────────────────


def parse_segments(text: str):
    """
    将文本切分为「受保护区段」和「普通区段」。
    受保护区段：
      - 行级代码块  ```...```
      - 行内代码    `...`
      - 块级公式    $$...$$
      - 行内公式    $...$
    返回 list of (is_protected: bool, content: str)
    """
    # 匹配顺序很重要：长的/多行的优先
    pattern = re.compile(
        r'(```[\s\S]*?```'      # 代码块 (``` ... ```)
        r'|`[^`\n]*?`'          # 行内代码
        r'|\$\$[\s\S]*?\$\$'    # 块级 LaTeX $$ ... $$
        r'|\$[^\$\n]*?\$'       # 行内 LaTeX $ ... $
        r')',
        re.MULTILINE
    )

    segments = []
    last = 0
    for m in pattern.finditer(text):
        start, end = m.start(), m.end()
        if start > last:
            segments.append((False, text[last:start]))
        segments.append((True, text[start:end]))
        last = end
    if last < len(text):
        segments.append((False, text[last:]))
    return segments


# 匹配行首的 ATX 标题（# 到 ######）
HEADING_RE = re.compile(r'^(#{1,6})(\s+.*)$', re.MULTILINE)


def process_text(text: str):
    """
    处理整段文本，返回 (new_text, changes)。
    changes: list of dict，记录每处修改。
    """
    segments = parse_segments(text)
    changes = []
    result_parts = []

    for is_protected, chunk in segments:
        if is_protected:
            result_parts.append(chunk)
            continue

        # 在普通区段内处理标题
        new_chunk = []
        for line in chunk.split('\n'):
            m = HEADING_RE.match(line)
            if m:
                hashes = m.group(1)
                rest = m.group(2)
                level = len(hashes)
                if level == 1:
                    # 删除一级标题（整行替换为空字符串，但保留换行结构）
                    changes.append({
                        'action': 'deleted',
                        'original': line,
                        'new': '(已删除)',
                        'level': 1,
                    })
                    new_chunk.append('')   # 保留空行，避免段落合并
                else:
                    new_hashes = '#' * (level - 1)
                    new_line = f'{new_hashes}{rest}'
                    changes.append({
                        'action': 'demoted',
                        'original': line,
                        'new': new_line,
                        'level': level,
                    })
                    new_chunk.append(new_line)
            else:
                new_chunk.append(line)
        result_parts.append('\n'.join(new_chunk))

    return ''.join(result_parts), changes


def main():
    parser = argparse.ArgumentParser(
        description="将 Markdown 文件中所有标题下调一级，并删除原一级标题。"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=DEFAULT_INPUT,
        help=f"输入 .md 文件路径（默认：{DEFAULT_INPUT!r}）",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=DEFAULT_OUTPUT,
        help="输出 .md 文件路径（默认：原地修改输入文件）",
    )
    args = parser.parse_args()

    input_path  = Path(args.input)
    output_path = Path(args.output) if args.output else input_path

    if not input_path.exists():
        parser.error(f"文件不存在：{input_path}")

    original_text = input_path.read_text(encoding='utf-8')
    new_text, changes = process_text(original_text)
    output_path.write_text(new_text, encoding='utf-8')

    # ── 输出修改报告 ──────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  修改报告 | {input_path} → {output_path}")
    print(f"{'='*60}")

    if not changes:
        print("  未发现任何 Markdown 标题，文件未作修改。")
    else:
        deleted = [c for c in changes if c['action'] == 'deleted']
        demoted = [c for c in changes if c['action'] == 'demoted']

        print(f"\n▸ 共修改 {len(changes)} 处标题：{len(deleted)} 处已删除（原一级标题），{len(demoted)} 处已下调。\n")

        if deleted:
            print("【已删除的一级标题】")
            for c in deleted:
                print(f"  - {c['original']!r}")

        if demoted:
            print("\n【已下调的标题】")
            for c in demoted:
                arrow = f"H{c['level']} → H{c['level']-1}"
                print(f"  {arrow}  {c['original']!r}  →  {c['new']!r}")

    print(f"\n{'='*60}\n")


if __name__ == '__main__':
    main()