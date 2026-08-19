---
name: Workspace Asset Persistence
description: 项目工作区资产自动同步与持久化技能。确保 AI 生成的所有图片（JPG/PNG/SVG）、文档（Word .docx / PPT .pptx / Excel .xlsx / HTML .html）均自动复制并保存至当前项目工作区目录，并采用项目相对路径进行引用。
---

# Workspace Asset Persistence Skill

`workspace-asset-persistence` 是全域资产同步与项目落地技能。它确保所有生成的视觉图片与文档资产能够第一时间保存在用户选定的项目工作区根目录下。

---

## 🛠️ 核心操作与处理流程 (Asset Sync Protocol)

1. **图片生成自动同步 (Auto Image Sync)**:
   - 调用 `generate_image` 生成图片后，自动将导出的 JPG/PNG 复制到当前项目工作区目录（`Cwd`）。
   - 在 HTML / Markdown 中使用 `./filename.jpg` 相对路径引用。

2. **文档即时落地 (Direct Document Saving)**:
   - 生成 Word `.docx`、PPT `.pptx`、Excel `.xlsx` 或 HTML `.html` 时，直接将目标路径指定在项目工作区目录下。

3. **相对路径引用修正 (Relative Path Alignment)**:
   - 检查所有 HTML, SVG, Markdown 引用，确保路径在跨平台迁移时依然生效。
