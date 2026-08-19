---
name: xintong-brand-video
description: 心同共生品牌视频生成服务。基于真实场景图 + 连贯旁白 + 字幕 + 背景音乐，生成横版/竖版品牌介绍片、文化节预热短片、多语言产品视频，并支持封面、配音（默认云扬男声 zh-CN-YunyangNeural）与品牌配色提取。当用户需要生成/修改品牌视频、加封面、换配音、提取品牌色时使用。
---

# 心同共生品牌视频生成服务

统一的心同共生品牌视觉与视频生产引擎，整合品牌建档、产品事实库、战役策划与视频渲染全链路。

## 能力总览

| 能力 | 工具/脚本 | 说明 |
| :--- | :--- | :--- |
| 品牌建档 | `brand-onboarding` skill | 生成 BrandProfile（含 WCAG 色彩校验） |
| 产品事实库 | `product-truth-builder` skill | 锁定事实锚点与宣传红线 |
| 战役策划 | `campaign-planner` skill | 生成 CampaignPlan |
| 语音合成 | `synthesize_tts` 工具 | 默认 zh-CN-YunyangNeural，语速 +4% |
| 品牌配色提取 | `extract_brand_palette` 工具 | 主色/辅助色 + WCAG 对比度 |
| 品牌介绍片 | `generate_brand_video` 工具 / `09-xintong-intro.js` | 1920×1080 真实场景 + 旁白 + 字幕 + BGM |
| 加封面 | `add_video_cover` 工具 / `10-add-cover.js` | 4 秒可见封面，防黑场 |
| 品牌影片（动画） | `07-brand-film.js` | 逐帧关键帧动画品牌片 |
| 多语言短视频 | `05-video.js` | 多语言产品/品牌短视频 |

## 默认品牌规范（心同共生）

- 主色朱红 `#A0261C`、辅助赭金 `#E0B060`、墨底 `#1A0C09`、米白 `#FFFBF5`
- 字体：宋体（标题）/ 黑体（正文）
- 配音：`zh-CN-YunyangNeural`（云扬男声），语速 `+4%`，音调 `+0Hz`
- 旁白红线：严禁收费晋级、卖导师身份、借公益强制成交、虚假反哺承诺等（见 `brands/xintong_gongsheng/product-truth.json` 的 `prohibited_claims`）

## 环境依赖

- Node.js ≥ 22（内置 `node:sqlite`、`fetch`）
- Python 3（Pillow、edge-tts）
- FFmpeg / ffprobe
- 可选：Remotion（进阶动效）、macOS `say`（本地回退配音）

## 快速开始

```bash
# 生成真实场景介绍片（默认云扬配音）
node pipeline/src/agents/09-xintong-intro.js

# 换配音引擎（回退本地 say）
RENWORK_TTS_PROVIDER=say node pipeline/src/agents/09-xintong-intro.js

# 给成片加封面
node pipeline/src/agents/10-add-cover.js
```

产出默认在 `out/videos/` 下。素材放 `assets/xintong-scenes/`，品牌档案放 `brands/xintong_gongsheng/`。
