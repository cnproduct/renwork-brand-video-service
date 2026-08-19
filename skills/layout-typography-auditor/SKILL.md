---
name: Layout & Typography Auditor
description: 排版与中英文字体防错全域审计技能。专门用于检查并优化所有生成的 HTML/CSS 界面、讲义表格、Word 文档及矢量 UI，防止单行文字换行错位、内容超出容器边界、中英文字体乱码及打印截断等问题。
---

# Layout & Typography Auditor Skill

`layout-typography-auditor` 是全域布局与字体防错审计技能。它确保 AI 在生成任何 UI 界面、讲义表格、印刷文档或 CSS 样式时，自动完成排版零缺陷校验。

---

## 🛠️ 5 大排版防错原则 (5 Golden Layout Rules)

1. **单行文字防换行错位 (Line-Wrap Protection)**:
   - 标签 Key（如 `姓名:`、`日期:`、`得分:`、`导师:`）强制配置 `white-space: nowrap !important; flex-shrink: 0;`。
   - 杜绝将“姓名:”切割为“姓”与“名:”。

2. **容器边界与溢出保护 (Overflow Boundary Protection)**:
   - 父容器统一设置 `box-sizing: border-box; width: 100%; overflow: hidden;`。
   - Grid / Flex 子元素配置 `min-width: 0` 防止超出右侧边界。

3. **中英文混排与防乱码 (Font & Encoding Guard)**:
   - `<meta charset="UTF-8">`
   - 包含跨平台备用字体栈（`PingFang SC`, `Noto Sans SC`, `Microsoft YaHei`）。

4. **表格固定布局 (Table Column Control)**:
   - 配置 `table-layout: fixed; width: 100%;` 与 `word-break: break-word;`。

5. **打印防截断与跨页分割 (Print Page-Break Avoidance)**:
   - 为 `.module-section`, `.brand-table`, `.pattern-card`, `.model-box`, `.ex-card`, `tr` 配置 `break-inside: avoid !important; page-break-inside: avoid !important;`。
   - 防止同一卡片或表格在第一页底和第二页顶被截断断开。
