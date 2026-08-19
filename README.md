# RenWork 品牌视觉系统与视频生成服务

心同共生（心同书院 × 心同共生）品牌视觉系统与视频生产的统一服务：以 **skills（剧本）+ plugin（工具）+ MCP（品牌 Token）+ pipeline（渲染管线）** 四层打包，覆盖「品牌建档 → 产品事实库 → 战役策划 → 渠道内容 → 视频生成 → 封面/配音/配色」全链路。

> 版本 v1.0.0 · 面向 RenWork / OpenCode 生态

---

## 架构分层

| 层 | 目录 | 职责 |
| :--- | :--- | :--- |
| **Skills（剧本）** | `skills/` | 22 个技能包，定义品牌建档、内容生产、视频导演等可复用工作流 |
| **Plugin（工具）** | `plugin.ts` | OpenCode 插件，暴露 4 个工具：TTS 合成、品牌配色提取、视频生成、加封面 |
| **MCP（品牌 Token）** | `mcp/` | 本地品牌 Token 解析服务 + 云端网关规格 |
| **Pipeline（渲染管线）** | `pipeline/` | Node + Python + FFmpeg 视频生成脚本 |
| **Schemas / Templates** | `schemas/` `templates/` | 6 大 JSON Schema + 5 大类内容模板 |
| **品牌数据** | `brands/` | 心同共生品牌档案、产品事实库、战役规划 |
| **素材** | `pipeline/assets/` | 真实场景图 |

---

## 目录结构

```
renwork-brand-video-service/
├── plugin.ts                     # OpenCode 插件（4 个视频/品牌工具）
├── opencode.json                 # 注册 plugin + MCP
├── package.json
├── README.md
├── skills/
│   ├── brand-content-orchestrator/  # 主控调度
│   ├── brand-onboarding/            # 品牌建档
│   ├── product-truth-builder/       # 产品事实库
│   ├── campaign-planner/            # 战役策划
│   ├── channel-content-creator/     # 8 渠道文案
│   ├── brand-visual-director/       # 视觉总监
│   ├── short-video-director/        # 短视频导演
│   ├── locale-market-adapter/       # 多国本地化
│   ├── content-brand-auditor/       # 四道合规审计
│   ├── xintong-brand-video/         # ★ 统一视频生成（本服务入口）
│   └── ...（brand-voice / brandkit / svg-logo-designer 等）
├── mcp/
│   ├── brandkit-token-server/       # 品牌 Token MCP（多租户 + WCAG 对比度）
│   └── renwork-cloud-spec.json      # 云端网关规格
├── pipeline/
│   ├── package.json
│   └── src/
│       ├── config.js                # 全局配置（含 TTS 默认云扬配音）
│       ├── lib/                     # 渲染器 / TTS / 爬虫
│       └── agents/                  # 10 个生成器脚本
├── schemas/                          # 6 大 JSON Schema
├── templates/                        # 5 大类内容模板
├── brands/xintong_gongsheng/        # 品牌档案数据
└── pipeline/assets/xintong-scenes/  # 12 张真实场景图
```

---

## 安装

### 环境依赖

| 依赖 | 用途 | 安装 |
| :--- | :--- | :--- |
| Node.js ≥ 22.5 | 管线运行（内置 `node:sqlite`、`fetch`） | https://nodejs.org |
| Python 3 | 帧渲染 / TTS | 系统自带 |
| Pillow | 文字帧、配色提取 | `pip install pillow` |
| edge-tts | 云扬中文配音 | `pip install edge-tts` |
| FFmpeg | 视频编码/转场/混音 | `brew install ffmpeg` |
| Remotion（可选） | 进阶逐帧动效 | 按需 |

### 安装依赖

```bash
git clone <repo-url>
cd renwork-brand-video-service
npm install            # 插件依赖（zod）
cd pipeline && npm install   # 管线依赖（cheerio、nodemailer）
```

### 注册技能到 agent

```bash
# Claude Code
ln -sfn "$PWD/skills" ~/.claude/skills
# 或逐个 symlink 到 ~/.claude/skills/<name>

# OpenCode / RenWork：在 opencode.json 的 plugin 数组加入 "./plugin.ts"
```

---

## 使用

### 快速生成品牌介绍片

```bash
npm run generate
# 输出：out/videos/xintong-intro/心同共生-真实场景介绍片-横版.mp4
```

### 换配音

默认已全局使用云扬男声 `zh-CN-YunyangNeural`（语速 +4%，音调 +0Hz）。可通过环境变量覆盖：

```bash
RENWORK_TTS_VOICE=zh-CN-XiaoxiaoNeural RENWORK_TTS_RATE=+0% node pipeline/src/agents/09-xintong-intro.js
```

回退本地 macOS 配音：

```bash
RENWORK_TTS_PROVIDER=say node pipeline/src/agents/09-xintong-intro.js
```

### 加封面（防黑场）

```bash
node pipeline/src/agents/10-add-cover.js
```

### 通过插件工具调用（在 RenWork/OpenCode 会话中）

- `synthesize_tts` —— 合成中文语音
- `extract_brand_palette` —— 从图片提取品牌配色 + WCAG 对比度
- `generate_brand_video` —— 生成品牌介绍片
- `add_video_cover` —— 给视频加封面

---

## 品牌规范（心同共生）

- **主色**：朱红 `#A0261C`；**辅助**：赭金 `#E0B060`；**深底**：墨 `#1A0C09`；**浅底**：米白 `#FFFBF5`
- **字体**：宋体（标题）/ 黑体（正文）
- **配音**：云扬男声 `zh-CN-YunyangNeural`，语速 `+4%`，音调 `+0Hz`
- **红线**：见 `brands/xintong_gongsheng/product-truth.json` 的 `prohibited_claims`（收费晋级、卖导师身份、借公益强制成交、虚假反哺承诺等）

---

## 隐私与安全

- 私密信息（API Key、SMTP 凭据）一律走环境变量或 `.env`（已 gitignore），绝不入库
- 生成的视频产物在 `out/`（已 gitignore），仓库只保留代码、技能、素材与品牌数据
- MCP 品牌 Token 服务支持多租户隔离、HEX 正则过滤、路径白名单与操作审计

---

## 许可

商业 / 专有。作者：人人易 AI（Renrenyi AI）。
