---
name: short-video-director
description: 外贸短视频导演技能。负责 6秒黄金Hook、15秒产品速递、30秒深度演示短视频的脚本分镜、口播文案、B-roll设计、字幕安全区与Remotion视频渲染配置。
---

# 短视频导演技能 (Short Video Director)

`short-video-director` 专为外贸企业打造快节奏、高转化、高完播率的短视频分镜脚本体系。兼容 TikTok、Instagram Reels、YouTube Shorts 及微信视频号。

---

## 3 大标准化视频时长与结构模板

### 1. 6 秒黄金 Hook 极速卡点片 (The 6-Second Scroll Stopper)
- **0.0s - 1.5s (The Visual Shock)**：极端破坏性测试或极具视觉张力的微距特写（如：用铁锤猛击石材表面、防暴拉链测试）；
- **1.5s - 4.5s (The Proof)**：展现毫发无损的硬核结果与权威检测数字；
- **4.5s - 6.0s (The Brand Stamp & CTA)**：品牌 Logo 闪现 + “Factory Direct Worldwide / DM for Samples”。

### 2. 15 秒产品速递与实景种草片 (The 15-Second Value Pitch)
- **0s - 3s (Hook)**：买家日常最头疼的质量/损耗问题；
- **3s - 8s (Feature & Tech)**：工厂自动化切割/数控精雕真实镜头 + 核心参数字幕；
- **8s - 12s (Application)**：海外实景工程上墙或模特穿戴全景展示；
- **12s - 15s (CTA)**：限时集装箱订货优惠 + WhatsApp/询盘联系方式。

### 3. 30 秒 B2B 决策人信任深度演示片 (The 30-Second B2B Trust Builder)
- **0s - 4s (Industry Problem)**：行业痛点分析（如破损率高达15%的传统包装）；
- **4s - 12s (Engineering Solution)**：加厚防震木箱包装结构与全自动打带流程；
- **12s - 20s (Capacity & Factory Scale)**：俯瞰现代化大厂房、ISO9001质检台与集装箱装柜现场；
- **20s - 26s (Client Proof)**：累计出口 40+ 国家，30,000 ㎡ 稳定月产能；
- **26s - 30s (Call to Action)**：点击主页链接免费申领 2026 最新样品盒。

---

## 结构化分镜脚本生成规范

分镜脚本保存于 `content_item.video_storyboard` 中，示例：

```json
{
  "duration_seconds": 15,
  "aspect_ratio": "9:16",
  "background_music_mood": "Upbeat Modern Industrial Electronic (120 BPM)",
  "scenes": [
    {
      "scene_number": 1,
      "duration_sec": 3.0,
      "visual_prompt": "Extreme macro close-up, diamond saw blade cutting through genuine quartzite stone, water mist splashing with dramatic high-speed lighting",
      "b_roll_description": "Factory CNC automated cutting machine",
      "narration_text": "How do you achieve zero installation gap on stone veneer?",
      "subtitle_overlay": "ZERO-GAP INTERLOCKING DESIGN",
      "camera_motion": "Fast push-in to macro texture"
    },
    {
      "scene_number": 2,
      "duration_sec": 5.0,
      "visual_prompt": "Worker snapping two stacked stone panels together effortlessly without mortar showing, seamless joint perfection",
      "b_roll_description": "Dry installation demonstration on wall mockup",
      "narration_text": "With our Z-shaped precision interlocking panels, installation is 40% faster.",
      "subtitle_overlay": "40% FASTER INSTALLATION",
      "camera_motion": "Smooth pan along the interlocking seam"
    },
    {
      "scene_number": 3,
      "duration_sec": 4.0,
      "visual_prompt": "Forklift loading heavy wooden crates into a clean shipping container at modern port warehouse",
      "b_roll_description": "Export container loading dock",
      "narration_text": "Supplied directly from our Fujian quarry to 40+ countries.",
      "subtitle_overlay": "GLOBAL EXPORT TO 40+ COUNTRIES",
      "camera_motion": "Drone pull-back reveal of factory"
    },
    {
      "scene_number": 4,
      "duration_sec": 3.0,
      "visual_prompt": "Elegant sample box opening on architect desk, showcasing 5 stone color finishes, RenWork / Brand Logo on top lid",
      "b_roll_description": "Studio architectural desktop",
      "narration_text": "Request your free sample box today. Link in bio!",
      "subtitle_overlay": "GET FREE SAMPLE BOX TODAY",
      "camera_motion": "Static hero lock-off with soft zoom"
    }
  ]
}
```
