# Paper Zh Layout Reader

[English](README.md) | 中文说明

`paper-zh-layout-reader` 是一个 Codex skill，用于把英文论文 PDF 转换成中文阅读产物。

它面向一个很实际的论文阅读流程：读一篇英文论文，保留来源可追溯性，提取图表，重建重要公式，并同时生成中英文对照 Markdown 阅读版和中文同版式 HTML/PDF 版本。

## 产出内容

对每篇论文，这个 skill 目标生成：

- `paper.md`：全文中英文段落对照阅读版
- `paper_zh_layout.html`：中文翻译同版式 HTML
- `paper_zh_layout.pdf`：由同版式 HTML 打印得到的 PDF
- `source_map.json`：稳定来源 ID、页码、图表、公式和置信度记录
- `translation_notes.md`：OCR、图表裁剪、公式重建和低置信内容说明
- `coverage_audit.md`：最终“原论文 vs 翻译论文”的文字覆盖和排版复查
- `assets/`：提取或裁剪出来的图表资源
- `assets/equations/*.mml`：可被 MathType 兼容工具打开或复用的 MathML 公式文件

如果中文同版式 PDF 无法同时承载完整中英文对照而不溢出，skill 应保留 `paper_zh_layout.html/pdf` 作为中文同版式版本，并额外生成 `paper_full_bilingual.html/pdf` 用于完整原文/译文对照。

## 适用场景

当你希望 Codex 处理类似下面的任务时，可以使用这个 skill：

```text
Use $paper-zh-layout-reader to translate this English paper PDF into Chinese.
Generate the Chinese same-layout HTML/PDF, keep figures, captions, page numbers,
source IDs, source_map.json, translation_notes.md, and MathType-compatible formulas.
```

它特别适合：

- IEEE / ACM / Nature 风格的英文学术 PDF
- 中英文对照论文阅读笔记
- 按原论文页序组织的中文翻译 HTML/PDF
- 需要保留图表和图注位置的论文翻译
- 需要通过 MathML / MathType 兼容源文件保持公式可编辑的论文

## 安装方式

把这个仓库克隆到 Codex skills 目录：

```powershell
git clone https://github.com/1635032352-lgtm/paper-zh-layout-reader.git "$env:USERPROFILE\.codex\skills\paper-zh-layout-reader"
```

然后重启 Codex，让 skill 元数据重新加载。

如果你的 Codex 配置支持项目级 skills，也可以把它放在项目本地 skills 目录中。

## 仓库结构

```text
paper-zh-layout-reader/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── layout.css
├── references/
│   ├── mathml_mathtype.md
│   └── output_contract.md
├── scripts/
│   ├── probe_pdf.py
│   └── validate_reader.py
├── .gitignore
└── license.txt
```

## 辅助脚本

翻译前探测 PDF：

```powershell
python scripts\probe_pdf.py --pdf "C:\path\paper.pdf" --out "D:\论文\paper-probe" --render-pages --extract-images
```

验证已生成的 reader 文件夹：

```powershell
python scripts\validate_reader.py --root "D:\论文\paper-reader" --render-previews
```

验证步骤会检查资源链接、JSON、MathML 数量、PDF 预览，以及是否存在 `coverage_audit.md` 复查记录。这些脚本需要 Python 包，例如 `pypdf`；如果要渲染页面或验证 PDF 预览，还可安装 `pypdfium2`。

## 最终覆盖复查

在声明完成前，需要把原 PDF 与生成的中文产物逐项对照：

- 确认每个可抽取页面或段落都在 `paper.md` 中有可见的 `Original` / `中文` 对，并在 `source_map.json` 中有稳定来源记录；
- 渲染原 PDF 和翻译后的 PDF/HTML，检查题名页、方法/公式页、图表页、结果页、参考文献页和末页是否有漏字、截断、重叠、空白页、公式显示异常或图表错位；
- 把覆盖结论、数量统计、排版问题和低置信内容写入 `coverage_audit.md`；
- 如果中文同版式 PDF 为了保持版式压缩了文字，应额外生成 `paper_full_bilingual.html/pdf` 作为完整对照版本。

## 关于公式

HTML/PDF 不能直接包含原生 MathType OLE 对象。这个 skill 使用 MathML 作为可互操作的公式源格式：

- MathML 会内嵌在 `paper_zh_layout.html` 中。
- 对应的 `.mml` 文件会保存到 `assets/equations/`。
- 条件允许时，会在 MathML 中附带 TeX annotation。

详细约定见 `references/mathml_mathtype.md`。

## 合法性边界

请将这个 skill 用于用户自己提供的 PDF 或合法开放获取来源。它不是用来绕过付费墙或访问控制的工具。

## 许可证

MIT License。见 `license.txt`。
